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
import pathlib
from app import app
from .functions import *
from .stockscreener import screener_layout
from .fin_ratios_comparison import comparison_fin_ratio_layout
from .historical_prices_comparison import comparison_prices_layout




################################################################ Begin the app layout #############################################################################

# Get the list of stocks for the dropdown
list_of_tickers = total_stock_tickers()

layout = dbc.Container([
    
    
    dbc.Row([

        dbc.Col(
            dcc.Dropdown(
                id='multiple-tickers-input-bar',
                options=
                        [{"label": label, "value": label} for label in list_of_tickers],
                value = [],
                multi = True
                ),
                width = 11),
            
            dbc.Col(
                    html.Button('Analyze', id='generate-comparison-charts', n_clicks=0, className = 'btn-primary'),
                width = 1)

    ]),

    html.Br(),

    dcc.Tabs(id='technical-analysis-tabs', value='tab-1', children=[
    dcc.Tab(label='Stocks Finder', value='tab-1'),
    dcc.Tab(label='Ratios Comparison', value='tab-2'),
    dcc.Tab(label='Price Action Comparison', value='tab-3'),
    ]),

    html.Br(),

    html.Div(id='multiple-tickers-content')

], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

@app.callback(    ########## This callback is for directing to other pages ###########
    Output(component_id = "multiple-tickers-content", component_property = "children"),
    Input(component_id = "technical-analysis-tabs", component_property = "value"),

)

def render_content(tab):
    
    if tab == "tab-1":
        return screener_layout
    
    elif tab == "tab-2":
        return comparison_fin_ratio_layout
    
    elif tab == "tab-3":
        return comparison_prices_layout



# callback to pull the financial data from the API
@app.callback(
    Output(component_id = "comparison-liq", component_property = "data"),
    Output(component_id = "comparison-growth", component_property = "data"),
    Output(component_id = "comparison-profit", component_property = "data"),
    Output(component_id = "comparison-investment", component_property = "data"),
    Output(component_id = "historical-prices-comparison-data", component_property = "data"),
    Input(component_id = "generate-comparison-charts", component_property = "n_clicks"),
    State(component_id = "multiple-tickers-input-bar", component_property = "value")
)

def api_call_financialstatements(n, stock_list):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "generate-comparison-charts" not in changed_id:
        raise PreventUpdate
    
    elif len(stock_list) == 0:
        raise PreventUpdate

    else:
        overall_liq_sol_data = pd.DataFrame()
        overall_growth_data = pd.DataFrame()
        overall_profit_data = pd.DataFrame()
        overall_investment_data = pd.DataFrame()
        overall_prices_data = pd.DataFrame()
        
        for stock_ticker in stock_list:
            single_liq_sol_data = liquidity_solvency_comparison_data(stock_ticker)
            single_growth_data = growth_ratios_comparison_data(stock_ticker)
            single_profit_data = profit_ratios_comparison_data(stock_ticker)
            single_investment_data = investment_ratios_comparison_data(stock_ticker)
            single_stock_price = historical_prices_comparison(stock_ticker)

            overall_liq_sol_data = pd.concat([overall_liq_sol_data, single_liq_sol_data], ignore_index = True)
            overall_growth_data = pd.concat([overall_growth_data, single_growth_data], ignore_index = True)
            overall_profit_data = pd.concat([overall_profit_data, single_profit_data], ignore_index = True)
            overall_investment_data = pd.concat([overall_investment_data, single_investment_data], ignore_index = True)
            overall_prices_data = pd.concat([overall_prices_data, single_stock_price], ignore_index = True)



    return overall_liq_sol_data.to_json(), overall_growth_data.to_json(), overall_profit_data.to_json(), overall_investment_data.to_json(), overall_prices_data.to_json()


######################################################################## Create the server ####################################################################################
