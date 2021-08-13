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
from .incomestatement_quarter import quarter_income_layout
from .balancesheet_quarter import quarter_balance_layout
from .cashflowstatement_quarter import quarter_cash_layout
from .fin_ratios_quarter import quarter_fin_ratio_layout


################################################################ Begin the app layout #############################################################################


quarter_layout = dbc.Container([
    
    dbc.Row([
        dbc.Col(
            dcc.RangeSlider(
                id='period-slider-quarter',
                min=0,
                max=1,
                step = 1,
                marks = {},
                value = [0, 5]

                ),
            )  
        ]),

    html.Br(), 

        
    dcc.Tabs(id='tabs-financial-statement-quarter', value='tab-1', children=[
    dcc.Tab(label='Income Statement', value='tab-1'),
    dcc.Tab(label='Balance Sheet', value='tab-2'),
    dcc.Tab(label='Cash Flow Statement', value='tab-3'),
    dcc.Tab(label='Financial Ratios', value='tab-4'),
    ]),
    
    html.Br(),

    html.Div(id='financial-analysis-content-quarter')

], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

# First callback to change the date Range Slider
@app.callback(
     Output(component_id='period-slider-quarter', component_property='max'),
     Output(component_id='period-slider-quarter', component_property='marks'),
    Input(component_id = "quarter-income-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value") 
)

def stock_daterange(data_quarter, state):

    if len(state) == 0:
        raise PreventUpdate

    if len(pd.read_json(data_quarter)) == 0:
        raise PreventUpdate


    overall_dff = pd.read_json(data_quarter)

    # Get the max value for the date range
    max_date = len(overall_dff.date.unique())-1

    # Get the marks for the Range Slider
    # Because of how long the quarter range slider can be, we will make the mark sliders shorter    
    if len(overall_dff["date"].unique()) > 10:
        marks_slider = {loop : str(value) for loop,value in enumerate(overall_dff['date'].unique()) if (loop == 0)|(loop%8 == 0)}
    else:
        marks_slider = {loop : str(value) for loop,value in enumerate(overall_dff['date'].unique())}

    return max_date, marks_slider


# Second callback to change the tabs
@app.callback(
     Output(component_id='financial-analysis-content-quarter', component_property='children'),
    Input(component_id = "tabs-financial-statement-quarter", component_property = "value")
)

def render_content(tab):
    
    if tab == "tab-1":
        return quarter_income_layout
    elif tab == "tab-2":
        return quarter_balance_layout
    elif tab == "tab-3":
        return quarter_cash_layout
    elif tab == "tab-4":
        return quarter_fin_ratio_layout






######################################################################## Create the server ####################################################################################
