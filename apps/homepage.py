import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from app import app




################################################################ Begin the app layout #############################################################################

layout = dbc.Container(children=[

dbc.Row([
    dbc.Col(
    dbc.Jumbotron([
        html.H1("Stocks For Noobs", className = "text-white"),
        
        html.P(
            "Your One Stop shop for basic graphical solutions to financial analysis",
            className="lead text-white",
        ),
        
        html.Hr(),
        
        html.P(
            "The purpose of this site is for beginner traders who have no idea what to look out for in a financial statement. "
            "We have taken the data from Financial Modelling Prep and created a dashboard for easy viewing and understanding. "
            "This is just a passion project, and I hope you can give some feedback - both positive and negative are welcomed!"
        , className = "text-white"), 
    
    ], style ={"background": "rgba(80, 80, 80, 0.8)", "margin": 0})
    ,className = "pt-5")
]),

    dbc.Row([
        dbc.Col(
        
            html.Img(id = "cool-background", src=app.get_asset_url('cool-background.png'), style = {"width": "100%", "height": "50%" }),    
            width = 12),

    
    ]), 



], fluid = True, style = {"background-image": 'url("/assets/cool-background.png")', "width": "100%", "height": "100%" })


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################


#@app.callback()




######################################################################## Create the server ####################################################################################
