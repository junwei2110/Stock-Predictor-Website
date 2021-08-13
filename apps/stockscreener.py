import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import requests
import json
from app import app
from .functions import *



################################################################ Begin the app layout #############################################################################
# Get the list of stocks for the dropdown
list_of_tickers = total_stock_tickers()

card_similarstocks = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Find Similar Stocks", className="card-header text-center"),
            html.P("Let's say you LOVE this particular stock but find it too expensive. One way is to find stocks that are in the same sector and with similar market cap and check if they fit your valuation.", className="card-text"),
            html.Br(),
            dcc.Dropdown(
                id='single-ticker-stock-search-bar',
                options=
                        [{"label": label, "value": label} for label in list_of_tickers],
                value = "",
                multi = False
                ),

        ]),
    ],
)

card_input_parameters = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Use Simple Parameters", className="card-header text-center"),
            html.P("Choose the Market Cap Category: ", className ="font-weight-bolder"),
            dcc.RadioItems(id = "mktcap-search",
                options=[
                {'label': 'Mega Cap (>200 bn) ', 'value': "200000000000"},
                {'label': 'Large Cap (10 - 200 bn) ', 'value': "10000000000, 200000000000"},
                {'label': 'Mid Cap (2 - 10 bn) ', 'value': "2000000000, 10000000000"},
                {'label': 'Small Cap (300 mil - 2 bn) ', 'value': "300000000, 2000000000"},
                {'label': 'Micro Cap (50 mil - 300 mil) ', 'value': "50000000, 300000000"},
                {'label': 'Penny Cap (<50 mil) ', 'value': "50000000"}
                    ],
                value= "200000000000",
                labelStyle= {'display': 'inline-block', "margin-right": "20px"},
                inputStyle={"margin-right": "10px"}
                ),
            html.P("Select the sectors: ", className ="font-weight-bolder"),
            dcc.RadioItems( id = "sector-search",
                options=[
                {'label': 'Consumer Cyclical', 'value': 'Consumer Cyclical'},
                {'label': 'Energy', 'value': 'Energy'},
                {'label': 'Technology', 'value': 'Technology'},
                {'label': 'Industrials', 'value': 'Industrials'},
                {'label': 'Financial Services', 'value': 'Financial Services'},
                {'label': 'Basic Materials', 'value': 'Basic Materials'},
                {'label': 'Communication Services', 'value': 'Communication Services'},
                {'label': 'Consumer Defensive', 'value': 'Consumer Defensive'},
                {'label': 'Healthcare', 'value': 'Healthcare'},
                {'label': 'Real Estate', 'value': 'Real Estate'},
                {'label': 'Utilities', 'value': 'Utilities'},
                {'label': 'Industrial Goods', 'value': 'Industrial Goods'},
                {'label': 'Financial', 'value': 'Financial'},
                {'label': 'Services', 'value': 'Services'},
                {'label': 'Conglomerates', 'value': 'Conglomerates'},
                    ],
                value= 'Consumer Cyclical',
                labelStyle= {'display': 'inline-block', "margin-right": "20px"},
                inputStyle={"margin-right": "10px"}
                ),  

            dbc.Row([
                dbc.Col(
                    html.Button('Generate', id='generate-stock-list', n_clicks=0, className = 'btn-primary'),
                    className = "text-center pt-3")
            ])
        ]),
    ],
)

# card_saved_screeners = dbc.Card(
#     [
#         dbc.CardBody([
#             html.H4("Use Popular Screeners", className="card-header text-center"),
#             html.P("Coming Soon =D", className="card-text text-center"),
#             html.Br(),

#         ]),
#     ],
# )


screener_layout = dbc.Container([

    dbc.Row([
        dbc.Col(
            dbc.Row([
                dbc.Col(
                    card_similarstocks, width = 12),

                dbc.Col(
                    html.Br()
                ),

                dbc.Col(
                    card_input_parameters, width = 12),
            ]), 
         width = 4),


    
dbc.Col(
    dbc.Row([
        dbc.Col(
            dbc.Jumbotron([
            html.H1(id = "comparison-message", children = ["Screen and Compare"]),
            html.P(
                "Find stocks of similar nature and compare their metrics",
                className="lead",
                ),
        
            html.Hr(),
        
            html.P("Option 1: Skip the screening step and input all your interested stock tickers into the main bar right at the top"
            ), 
            html.P("Option 2: Screen stocks that you are interested in using the 2 screen options to your left. From the table generated, choose the stocks you wish to compare OR conduct fundamental analysis on"
            ),    
        ], style ={"background": "rgba(240, 240, 240, 0.8)"}),

        id = "screener-intro"),
    
    
    dbc.Col(

    dash_table.DataTable(
        columns=[],
        data= [],
        editable=False,
        id='table_of_stocks_after_screener',
        style_as_list_view= True,
        style_header={'backgroundColor': 'white', "font-size" : "14px", 'fontWeight': 'bold', 'textAlign': 'center'},
        is_focused=True,

        column_selectable= 'single',
        style_data_conditional=[
            {'if': {'state': 'active'},'backgroundColor': 'green', 'border': '12px solid white'},
            {'if': {'column_id': 'Ticker'}, 'text_align':'center', 'backgroundColor': 'green', 'color': 'white', 
             'border': '12px solid white', 'letter-spacing': '3px'},
                               ],
        style_data={"font-size" : "14px", 'height': 15, "background":"white", 'border': '1px solid white'},
        style_cell = {'minWidth': '180px', 'width': '180px', 'maxWidth': '180px', "textAlign": "center"},
        style_table = {'overflowY': 'auto', 'minWidth': '100%'},
        fixed_rows={'headers': True}),

            
       ),
    ]),

    width = 8)  
    
    ])

], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

@app.callback(    ########## This callback is for the first card - to search for stocks that are similar to a specific company ###########
    Output(component_id = "table_of_stocks_after_screener", component_property = "columns"), 
    Output(component_id = 'table_of_stocks_after_screener', component_property = "data"),
    Output(component_id = 'screener-intro', component_property = "children"), 
    Input(component_id = 'single-ticker-stock-search-bar', component_property = 'value'), 
    Input(component_id = 'generate-stock-list', component_property = "n_clicks"),
    State(component_id = "mktcap-search", component_property = 'value'),
    State(component_id = "sector-search", component_property = 'value') 

)
  
def update_table(stock, n, capvalue, sector):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'single-ticker-stock-search-bar' in changed_id:
        peer_dataframe = stock_peers(stock)
        columns = [{"name": i, "id": i} for i in peer_dataframe.columns]
        data = peer_dataframe.to_dict('records')
        children = []
        return columns, data, children
    elif 'generate-stock-list' in changed_id:
        peer_dataframe = input_parameters_peers(capvalue, sector)
        columns = [{"name": i, "id": i} for i in peer_dataframe.columns]
        data = peer_dataframe.to_dict('records')
        children = []
        return columns, data, children
    else:
        raise PreventUpdate




@app.callback(    ########## This callback is for either directing to fundamental analysis page ###########
    Output(component_id = "url", component_property = "pathname"), # By clicking the button, you trigger the pathname change which should redirect you to the other page
    Output(component_id = 'single-ticker', component_property = "data"), # Store it in the store to be used in the single ticker
    Input('table_of_stocks_after_screener', 'active_cell'), #active_cell - A dictionary: The row and column indices and IDs of the currently active cell.
    Input('table_of_stocks_after_screener', 'derived_viewport_data') # This is a list of dictionaries - This property represents the current state of data on the current page. This property will be updated on paging, sorting, and filtering.

)
  
def interactive_table(cell, data):
    if not cell:
        raise PreventUpdate    
    
    if cell["column_id"] == 'Analysis':
        if cell:
            selected = data[cell["row"]]["Ticker"]
            pathname = "/apps/finanalysis"
            return pathname, json.dumps(selected)
    
    else:
        raise PreventUpdate


@app.callback(    ########## This callback is for adding ticker to the multi-stock search bar ###########
    Output(component_id = "multiple-tickers-input-bar", component_property = "value"),
    Input('table_of_stocks_after_screener', 'active_cell'), #active_cell - A dictionary: The row and column indices and IDs of the currently active cell.
    Input('table_of_stocks_after_screener', 'derived_viewport_data'), # This is a list of dictionaries - This property represents the current state of data on the current page. This property will be updated on paging, sorting, and filtering.
    State(component_id = "multiple-tickers-input-bar", component_property = "value")
)
  
def interactive_table(cell, data, stock_list):
    if not cell:
        raise PreventUpdate    
    
    if cell["column_id"] == 'Add for Comparison':
        if cell:
            selected = data[cell["row"]]["Ticker"]

            for stock in stock_list:
                if selected == stock:
                    return stock_list

            stock_list.append(selected)
            return stock_list
    
    else:
        raise PreventUpdate





######################################################################## Create the server ####################################################################################
