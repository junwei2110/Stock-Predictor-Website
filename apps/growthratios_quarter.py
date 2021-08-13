import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from app import app

################################################################ Begin the app layout #############################################################################

quarter_growratio_layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.P("Growth ratios can give an indication of how fast your business is growing. You can even argue that this metric is even more important in modern day investing since disruptive technology is on the rage right now. Such growth companies do not follow the usual investment valuations, so growth metrics are an alternative to assessing them"
        , className = 'mb-4'), 
        width = 12)
    ]),

# This is the graph for the Revenue Growth  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Revenue Growth"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


        dbc.Row([

        dbc.Col(
            dcc.Graph(id = "RG-quarter",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "RGDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Revenue Growth is the most straightforward way to see how fast the company is growing. As the saying goes, good product don't lie."),
            html.P("It is calculated by the increase, or decrease, in a company’s sales between two periods. Communicated as a percentage, revenue growth demonstrates the degree to which your company's revenue has grown (or shrunk) over time.") 
            ], width = 3)   
        
        ])
    ], fluid = True),

# This is the graph for the FCF Growth  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Free-Cash-Flow Growth"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([



        dbc.Col(
            dcc.Graph(id = "FCFG-quarter",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "FCFGDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Free cash flow is an important measurement since it shows how efficient a company is at generating cash. Investors use free cash flow to measure whether a company might have enough cash for dividends or share buybacks. In addition, the more free cash flow a company has, the better it is placed to pay down debt and pursue opportunities that can enhance its business, making it an attractive choice for investors."),
            html.P("Hence, its growth rate is important for the future of the company. Short term wise, if a company has a decreasing free cash flow, that is not necessarily bad if the company is investing in its growth.") 
            ], width = 3)   

        ])        
    ], fluid = True),

# This is the graph for the Op Profit Growth 

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Operating Profit Growth"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "OpProfGrowth-quarter",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "OpProfGrowthDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Operating profit attempts to measure the profits of a company’s operating before they are impacted by non operational costs such as interest and tax expense. It measures the efficiency of running the company's operations."),
            html.P("Operating profit eliminates a number of extraneous and indirect factors that can obscure a company's real performance. Hence, its growth rate can help determine the future prospects of the company")
            ], width = 3)   
        ]) 
    ], fluid = True),


# This is the graph for the Assets Growth
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Assets Growth"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "assetsgrowth-quarter",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "assetsgrowthDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("There are three ways a firm can raise capital to invest: equity issuance, debt issuance, and growth in retained earnings. Asset growth aggregates financing from all three methods. Equity issuance and growth in retained earnings both lead to an increase in the book equity of a firm and, as a result, to an increase in total assets. Debt issuance leads to an increase in the liabilities of a firm and consequently also to an increase in its total assets. Thus, we can focus on asset growth as a broad measure of investment to examine the relation between investment and expected returns."),
            ], width = 3)   

    ])    
    ], fluid = True),

# This is the graph for the Debt Growth

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Debt Growth"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "debtgrowth-quarter",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "debtgrowthDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Debt has its pros and cons. Pros include injection of capital to fund projects, reduces tax obligations, and increases access to new opportunities; cons include risks of solvency, compromises collateralized property, and restricts company to new debt"),
            html.P("When looking at the assets growth, we should also monitor the total debt growth. This can help paint a separate picture if the asset growth is high but still lower than the debt growth"),
            ], width = 3)   
        ])
    ], fluid = True),


], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'RG-quarter', component_property = 'figure'),
    Output(component_id = 'FCFG-quarter', component_property = 'figure'),
    Output(component_id = 'OpProfGrowth-quarter', component_property = 'figure'),
    Output(component_id = 'assetsgrowth-quarter', component_property = 'figure'),
    Output(component_id = 'debtgrowth-quarter', component_property = 'figure'),
    Input(component_id='period-slider-quarter', component_property='value'),
    Input(component_id = "quarter-growthratios-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value")
)

def figure_callback(period_range, data_quarter, state):

    # If there is no stock in the bar, do not trigger any callbacks
    if len(state) == 0:
        raise PreventUpdate

    # When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if len(pd.read_json(data_quarter)) == 0:
         raise PreventUpdate    

    # Create a copy since you don't want to mess up the original
    ratios_dff = pd.read_json(data_quarter)

    # Filter based on date range
    ratios_dff = ratios_dff.iloc[period_range[0]:period_range[1]+1]

    # Reverse the order of the date to make the graphs' x-axis in ascending order
    ratios_dff = ratios_dff.sort_values(by = ["date"])

    # Revenue Growth figure
    fig_RG = px.line(ratios_dff, x = "date", y = "revenueGrowth")

    # FCF Growth figure
    fig_FCFG = px.line(ratios_dff, x = "date", y = "freeCashFlowGrowth")

    # Operating Income Growth figure
    fig_OpProfG = px.line(ratios_dff, x = "date", y = "operatingIncomeGrowth")

    # Assets Growth figure
    fig_assetsg = px.line(ratios_dff, x = "date", y = "assetGrowth")

    # Debt Growth figure
    fig_debtg = px.line(ratios_dff, x = "date", y = "debtGrowth")

    return fig_RG, fig_FCFG, fig_OpProfG, fig_assetsg, fig_debtg




######################################################################## Create the server ####################################################################################
