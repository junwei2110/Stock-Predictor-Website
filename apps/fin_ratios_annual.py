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
from .liquidityratios_annual import annual_liqratio_layout
from .profitabilityratios_annual import annual_profratio_layout
from .investmentratios_annual import annual_invratio_layout
from .growthratios_annual import annual_growratio_layout

################################################################ Begin the app layout #############################################################################

annual_fin_ratio_layout = dbc.Container([

        
    dcc.Tabs(id='tabs-fin-ratios-annual', value='tab-1', children=[
    dcc.Tab(label='Liquidity & Solvency Ratios', value='tab-1'),
    dcc.Tab(label='Growth Ratios', value='tab-2'),
    dcc.Tab(label='Profitability Ratios', value='tab-3'),
    dcc.Tab(label='Investment Valuation Ratios', value='tab-4'),
    ]),
    
    html.Br(),

    html.Div(id='fin-ratios-content-annual')

], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

# First callback to change the tabs
@app.callback(
     Output(component_id='fin-ratios-content-annual', component_property='children'),
    Input(component_id = "tabs-fin-ratios-annual", component_property = "value")
)

def render_content(tab):
    
    if tab == "tab-1":
        return annual_liqratio_layout
    elif tab == "tab-2":
        return annual_growratio_layout
    elif tab == "tab-3":
        return annual_profratio_layout
    elif tab == "tab-4":
        return annual_invratio_layout






######################################################################## Create the server ####################################################################################
