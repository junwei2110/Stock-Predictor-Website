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

comparison_invratio_layout = dbc.Container([

# This is the graph for the PE Ratio  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Price-to-Earnings Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


        dbc.Row([

        dbc.Col(
            dcc.Graph(id = "PERatio-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
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
            dcc.Graph(id = "PSRatio-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
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
            dcc.Graph(id = "PBVRatio-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
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
            dcc.Graph(id = "PFCFRatio-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Price to free cash flow is an equity valuation metric that indicates a company's ability to generate additional revenues. It is calculated by dividing its market capitalization by free cash flow values."),
            html.P("This metric is very similar to the valuation metric of price to cash flow but is considered a more exact measure, owing to the fact that it uses free cash flow, which subtracts capital expenditures (CAPEX) from a company's total operating cash flow, thereby reflecting the actual cash flow available to fund non-asset-related growth. Companies use this metric when they need to expand their asset bases either in order to grow their businesses or simply to maintain acceptable levels of free cash flow.") 
            ], width = 3)   

    ])    
    ], fluid = True),



], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'PERatio-comparison', component_property = 'figure'),
    Output(component_id = 'PSRatio-comparison', component_property = 'figure'),
    Output(component_id = 'PBVRatio-comparison', component_property = 'figure'),
    Output(component_id = 'PFCFRatio-comparison', component_property = 'figure'),
    Input(component_id = "tabs-fin-ratios-comparison", component_property = "value"),
     Input(component_id = "comparison-investment", component_property = "data"),
    State(component_id = "multiple-tickers-input-bar", component_property = "value")
)

def figure_callback(tab, data_comparison, stock_list):

    # When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if len(stock_list) == 0:
         raise PreventUpdate    

    # When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if len(pd.read_json(data_comparison)) == 0:
         raise PreventUpdate    

    # When you are not in the right tab, do not update     
    if tab != "tab-4":
         raise PreventUpdate

    # Create a copy since you don't want to mess up the original
    ratios_dff = pd.read_json(data_comparison)

    # PE Ratio figure
    fig_PEratio = px.scatter(ratios_dff, x = "Last Reported", y = "Price-to-Earnings", color = "symbol")
    fig_PEratio.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # PS Ratio figure
    fig_PSratio = px.scatter(ratios_dff, x = "Last Reported", y = "Price-to-Sales", color = "symbol")
    fig_PSratio.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # PBV Ratio figure
    fig_BVratio = px.scatter(ratios_dff, x = "Last Reported", y = "Price-to-Bookvalue",color = "symbol")
    fig_BVratio.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # PFCF Ratio figure
    fig_PFCFratio = px.scatter(ratios_dff, x = "Last Reported", y = "Price-to-FreeCashFlow", color = "symbol")
    fig_PFCFratio.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))


    return fig_PEratio, fig_PSratio, fig_BVratio, fig_PFCFratio




######################################################################## Create the server ####################################################################################
