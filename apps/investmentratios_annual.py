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

annual_invratio_layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.P("Investment valuation ratios highlight the relationship of a company or its equity's market value with some fundamental financial metrics, such as earnings. Valuation ratios show the price you pay for some financial metrics such as earning streams, cash flow, and revenues."
        , className = 'text-center text-primary mb-4'), 
        width = 12)
    ]),

# This is the graph for the PE Ratio  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Price-to-Earnings Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


        dbc.Row([

        dbc.Col(
            dcc.Graph(id = "PERatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "PERatioDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The financial reporting of both companies and investment research services use a basic earnings per share (EPS) figure divided into the current stock price to calculate the P/E multiple (i.e. how many times a stock is trading (its price) per each dollar of EPS)."),
            ], width = 3)   
        
        ])
    ], fluid = True),

# This is the graph for the PS Ratio  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Price-to-Sales Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "PSRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "PSRatioDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The P/E ratio and P/S reflects how many times investors are paying for every dollar of a company's sales. Since earnings are subject, to one degree or another, to accounting estimates and management manipulation, many investors consider a company's sales (revenue) figure a more reliable ratio component in calculating a stock's price multiple than the earnings figure."),
            ], width = 3)   

        ])        
    ], fluid = True),



# This is the graph for the PBV Ratio  

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Price-to-BookValue Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "PBVRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "PBVRatioDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The price-to-book value ratio, expressed as a multiple (i.e. how many times a company's stock is trading per share compared to the company's book value per share), is an indication of how much shareholders are paying for the net assets of a company."),
            html.P("Book Value of a company is the Shareholders' Equity, or Total Assets minus Total Liabilities")
            ], width = 3)   
        ]) 
    ], fluid = True),


# This is the graph for the PFCF Ratio
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Price-to-FreeCashFlow Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "PFCFRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "PFCFRatioDescrip-annual",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Price to free cash flow is an equity valuation metric that indicates a company's ability to generate additional revenues. It is calculated by dividing its market capitalization by free cash flow values."),
            html.P("This metric is very similar to the valuation metric of price to cash flow but is considered a more exact measure, owing to the fact that it uses free cash flow, which subtracts capital expenditures (CAPEX) from a company's total operating cash flow, thereby reflecting the actual cash flow available to fund non-asset-related growth. Companies use this metric when they need to expand their asset bases either in order to grow their businesses or simply to maintain acceptable levels of free cash flow.") 
            ], width = 3)   

    ])    
    ], fluid = True),

# This is the graph for the PEG Ratio

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Price/Earnings-to-Growth Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "PEGRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "PEGRatioDescrip-annual",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The price/earnings to growth ratio (PEG ratio) is a stock's price-to-earnings (P/E) ratio divided by the growth rate of its earnings for a specified time period. The PEG ratio enhances the P/E ratio by adding in expected earnings growth into the calculation."),
            html.P("The PEG ratio is used to determine a stock's value while also factoring in the company's expected earnings growth, and it is thought to provide a more complete picture than the more standard P/E ratio.") 
            ], width = 3)   
        ])
    ], fluid = True),


    html.Hr(),



], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'PERatio-annual', component_property = 'figure'),
    Output(component_id = 'PSRatio-annual', component_property = 'figure'),
    Output(component_id = 'PBVRatio-annual', component_property = 'figure'),
    Output(component_id = 'PFCFRatio-annual', component_property = 'figure'),
    Output(component_id = 'PEGRatio-annual', component_property = 'figure'),
    Input(component_id='period-slider-annual', component_property='value'),
    Input(component_id = "annual-ratios-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value")
)

def figure_callback(period_range, data_annual, state):

    # If there is no stock in the bar, do not trigger any callbacks
    if len(state) == 0:
        raise PreventUpdate

    # When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if len(pd.read_json(data_annual)) == 0:
         raise PreventUpdate    

    # Create a copy since you don't want to mess up the original
    ratios_dff = pd.read_json(data_annual)


    # Filter based on date range
    ratios_dff = ratios_dff.iloc[period_range[0]:period_range[1]+1]

    # PE Ratio figure
    fig_PEratio = px.line(ratios_dff, x = "date", y = "priceEarningsRatio")

    # PS Ratio figure
    fig_PSratio = px.line(ratios_dff, x = "date", y = "priceToSalesRatio")

    # PBV Ratio figure
    fig_BVratio = px.line(ratios_dff, x = "date", y = "priceToBookRatio")

    # PFCF Ratio figure
    fig_PFCFratio = px.line(ratios_dff, x = "date", y = "priceToFreeCashFlowsRatio")

    # PEG Ratio figure
    fig_PEGratio = px.line(ratios_dff, x = "date", y = "priceEarningsToGrowthRatio")


    return fig_PEratio, fig_PSratio, fig_BVratio, fig_PFCFratio, fig_PEGratio




######################################################################## Create the server ####################################################################################
