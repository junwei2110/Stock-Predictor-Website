# This is the landing page that the user will first see when he clicks on your web app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd

# Connect to the main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import homepage, financial_statements, multiple_tickers_input_page, functions

# Styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Creating the sidebar
sidebar = html.Div(
    [
        html.Img(src=app.get_asset_url('Logo.png'), style={'height':'13rem'}),
        html.Hr(),
        html.P(
            "Find your Stocks Today!", className="lead"
        ),

        dbc.Nav(
            [
                dbc.NavLink("Home", id="linktoHome", href="/", active="exact"),
                dbc.NavLink("Single Ticker Analysis", id="linktofinanalysis", href="/apps/finanalysis", active="exact"),
                dbc.NavLink("Screen & Compare", id="linktostockscreener", href="/apps/stockscreener", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        
    ],
    style=SIDEBAR_STYLE,
)

# Creating the top dropdown bar and submit button
list_of_tickers = functions.total_stock_tickers()
top_input_bar = dbc.Row([
    dbc.Col(        
         dcc.Dropdown(
         id='stock-input-bar',
         options=
             [{"label": label, "value": label} for label in list_of_tickers],
         value = "",
         multi=True
         ),
         width = 11),

    dbc.Col(
        html.Button('Analyze', id='submit-api-req', n_clicks=0),

    )    

     ])


# Creating the content page
content = html.Div(id="page-content", children=[], style = CONTENT_STYLE)


# Putting all the elements together
app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False), # The objective is that when the link is clicked, the href will be populated into the pathname
    sidebar,

    # Start adding your stores
    # Stores for your company profile and historical price
    dcc.Store(id='company-profile', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='company-stock-price', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    # Stores for your annual financial statements
    dcc.Store(id='annual-income-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='annual-balance-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='annual-cash-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='annual-ratios-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='annual-growthratios-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    # Stores for your quarter financial statements
    dcc.Store(id='quarter-income-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='quarter-balance-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='quarter-cash-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='quarter-ratios-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    dcc.Store(id='quarter-growthratios-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    # Store for your TTM ratios
    dcc.Store(id='TTM-ratios-memory', storage_type='memory', clear_data = True), # This is used to store the data when we call the API
    # Store for your single ticker input from the screener page
    dcc.Store(id='single-ticker', storage_type='memory', clear_data = True), 
    # Store for all the stocks to be analyzed in the comparison charts page
    dcc.Store(id='comparison-liq', storage_type='memory', clear_data = True),
    dcc.Store(id='comparison-growth', storage_type='memory', clear_data = True),
    dcc.Store(id='comparison-profit', storage_type='memory', clear_data = True),
    dcc.Store(id='comparison-investment', storage_type='memory', clear_data = True),
    # Store for all the historical stocks prices for comparison
    dcc.Store(id='historical-prices-comparison-data', storage_type='memory', clear_data = True),

    content # When we set the callback below, we will set conditions that when the pathlink matches a certain phrase, this website layout will be populated

])


@app.callback(    ########## This callback is for directing to other pages ###########
    Output(component_id = "page-content", component_property = "children"),
    Input(component_id = "url", component_property = "pathname"),

)

def display_page(pathname):
    if (pathname == "/apps/finanalysis"):
        return financial_statements.layout


    elif (pathname == "/apps/stockscreener"):
        return multiple_tickers_input_page.layout

    else:
        return homepage.layout




if __name__ == '__main__':
    app.run_server(debug=True)
