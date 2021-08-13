import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import json
from app import app
from .functions import *
from .financial_statements_Summary import summary_layout
from .financial_statements_A import annual_layout
from .financial_statements_Q import quarter_layout



################################################################ Begin the app layout #############################################################################

# Get the list of stocks for the dropdown
list_of_tickers = total_stock_tickers()

layout = dbc.Container([
    
    
    dbc.Row([
        dbc.Col(
        html.H1(children='Financial Analysis'),
        width = 4),

    
        dbc.Col(
            dcc.Dropdown(
                id='single-ticker-input-bar',
                options=
                        [{"label": label, "value": label} for label in list_of_tickers],
                value = "",
                multi = False,
                persistence_type = "memory",
                persistence = True
                ),
                width = 3),

    ]),

    html.Br(),        
        
    dcc.Tabs(id='tabs-financial-statement', value='tab-1', children=[
    dcc.Tab(label='Summary', value='tab-1'),
    dcc.Tab(label='Annual', value='tab-2'),
    dcc.Tab(label='Quarter', value='tab-3'),
    dcc.Tab(label='Price & News', value='tab-4'),
    ]),
    
    html.Br(),

    html.Div(id='financial-analysis-content')

], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

# First callback to render the various apps
@app.callback(
     Output(component_id='financial-analysis-content', component_property='children'),
    Input(component_id = "tabs-financial-statement", component_property = "value")
)

def render_content(tab):
    
    if (tab == "tab-1"):
        return summary_layout
    elif (tab == "tab-2"):
        return annual_layout
    elif (tab == "tab-3"):
        return quarter_layout
    elif (tab == "tab-4"):
        return "Work in Progress"

# Data store is used to store a ticker from the screener page, and is used to trigger a direct api pull 
@app.callback(
    Output(component_id = "single-ticker-input-bar", component_property = "value"),
    Input(component_id = "single-ticker", component_property = "data") # This data store is found in the index page and is used to store the stock ticker from the screener 
)

def input_content(stock):
    if stock is None:
        raise PreventUpdate    
    else:
        return json.loads(stock)




# callback to pull the financial data from the API
@app.callback(
    Output(component_id = "company-profile", component_property = "data"),
    Output(component_id = "company-stock-price", component_property = "data"),
    Output(component_id = "annual-income-memory", component_property = "data"),
    Output(component_id = "annual-balance-memory", component_property = "data"),
    Output(component_id = "annual-cash-memory", component_property = "data"),
    Output(component_id = "annual-ratios-memory", component_property = "data"),
    Output(component_id = "annual-growthratios-memory", component_property = "data"),
    Output(component_id = "quarter-income-memory", component_property = "data"),
    Output(component_id = "quarter-balance-memory", component_property = "data"),
    Output(component_id = "quarter-cash-memory", component_property = "data"),
    Output(component_id = "quarter-ratios-memory", component_property = "data"),
    Output(component_id = "quarter-growthratios-memory", component_property = "data"),
    Output(component_id = "TTM-ratios-memory", component_property = "data"),
    Output(component_id = "single-ticker", component_property = "clear_data"), 
    # This specific data clear is for the data store found in index page. Data store is used to store a ticker from the screener page, and is used to trigger a direct api pull 
    # Data is to be cleared right after the api pull so that the ticker does not trigger the api pull whenever we enter this financial statements page
    Input(component_id = "single-ticker-input-bar", component_property = "value")
)

def api_call_financialstatements(stock_ticker):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "single-ticker-input-bar" not in changed_id:
        raise PreventUpdate
    else:
        company_profile_info = company_profile(stock_ticker)
        company_stock_prices = stock_price_candle(stock_ticker)
        annual_income_sheet = annual_income_statement(stock_ticker)
        annual_balance_sheet = annual_balance_statement(stock_ticker)
        annual_cash_sheet = annual_CF_statement(stock_ticker)
        annual_ratios_sheet = single_ticker_fin_ratio_annual(stock_ticker)
        annual_growthratios_sheet = single_ticker_growth_ratio_annual(stock_ticker)
        quarter_income_sheet = quarter_income_statement(stock_ticker)
        quarter_balance_sheet = quarter_balance_statement(stock_ticker)
        quarter_cash_sheet = quarter_CF_statement(stock_ticker)
        quarter_ratios_sheet = single_ticker_fin_ratio_quarter(stock_ticker)
        quarter_growthratios_sheet = single_ticker_growth_ratio_quarter(stock_ticker)
        TTM_ratios_sheet = single_ticker_ratio_TTM(stock_ticker)


    return company_profile_info.to_json(), company_stock_prices.to_json(), annual_income_sheet.to_json(), annual_balance_sheet.to_json(), annual_cash_sheet.to_json(), annual_ratios_sheet.to_json(), annual_growthratios_sheet.to_json(), quarter_income_sheet.to_json(), quarter_balance_sheet.to_json(), quarter_cash_sheet.to_json(), quarter_ratios_sheet.to_json(), quarter_growthratios_sheet.to_json(), TTM_ratios_sheet.to_json(), True




######################################################################## Create the server ####################################################################################
