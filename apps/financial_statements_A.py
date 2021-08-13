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
from .incomestatement_annual import annual_income_layout
from .balancesheet_annual import annual_balance_layout
from .cashflowstatement_annual import annual_cash_layout
from .fin_ratios_annual import annual_fin_ratio_layout 


################################################################ Begin the app layout #############################################################################

annual_layout = dbc.Container([
    
    dbc.Row([
        dbc.Col(
            dcc.RangeSlider(
                id='period-slider-annual',
                min=0,
                max=1,
                step = 1,
                marks = {},
                value = [0, 5]

                ),
            )  
        ]),

    html.Br(), 

        
    dcc.Tabs(id='tabs-financial-statement-annual', value='tab-1', children=[
    dcc.Tab(label='Income Statement', value='tab-1'),
    dcc.Tab(label='Balance Sheet', value='tab-2'),
    dcc.Tab(label='Cash Flow Statement', value='tab-3'),
    dcc.Tab(label='Financial Ratios', value='tab-4'),
    ]),
    
    html.Br(),

    html.Div(id='financial-analysis-content-annual')

], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

# First callback to change the date Range Slider
@app.callback(
     Output(component_id='period-slider-annual', component_property='max'),
     Output(component_id='period-slider-annual', component_property='marks'),
    Input(component_id = "annual-income-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value")  
)

def stock_daterange(data_annual, state):

    if len(state) == 0:
        raise PreventUpdate

    if len(pd.read_json(data_annual)) == 0:
        raise PreventUpdate

    overall_dff = pd.read_json(data_annual)

    # Get the max value for the date range
    max_date = len(overall_dff.date.unique())-1

    # Get the marks for the Range Slider
    marks_slider = {loop : str(value) for loop,value in enumerate(overall_dff['date'].unique())}

    return max_date, marks_slider


# Second callback to change the tabs
@app.callback(
     Output(component_id='financial-analysis-content-annual', component_property='children'),
    Input(component_id = "tabs-financial-statement-annual", component_property = "value")
)

def render_content(tab):
    
    if tab == "tab-1":
        return annual_income_layout
    elif tab == "tab-2":
        return annual_balance_layout
    elif tab == "tab-3":
        return annual_cash_layout
    elif tab == "tab-4":
        return annual_fin_ratio_layout






######################################################################## Create the server ####################################################################################
