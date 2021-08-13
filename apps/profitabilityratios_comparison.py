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

comparison_profratio_layout = dbc.Container([


# This is the graph for the ROE  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Return-On-Equity (ROE)"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


        dbc.Row([

        dbc.Col(
            dcc.Graph(id = "ROE-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Return on equity (ROE) measures a corporation's profitability in relation to stockholders’ equity."),
            html.P("Whether an ROE is considered satisfactory will depend on what is normal for the industry or company peers. As a shortcut, investors can consider an ROE near the long-term average of the S&P 500 (14%) as an acceptable ratio and anything less than 10% as poor.") 
            ], width = 3)   
        
        ])
    ], fluid = True),

# This is the graph for the ROA  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Return-On-Assets (ROA)"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([



        dbc.Col(
            dcc.Graph(id = "ROA-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Return on assets (ROA) is an indicator of how well a company utilizes its assets in terms of profitability."),
            html.P("ROA is best used when comparing similar companies or by comparing a company to its own previous performance. ROA does not take into account a company’s debt, while return on equity (ROE) does—if a company carries no debt, its shareholders' equity and its total assets will be the same and ROA would equal ROE.") 
            ], width = 3)   

        ])        
    ], fluid = True),

# This is the graph for the ROCE 

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Return-On-Capital-Employed (ROCE)"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "ROCE-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Return on capital employed (ROCE) is a financial ratio that measures a company’s profitability in terms of all of its capital."),
            html.P("Unlike other fundamentals such as return on equity (ROE), which only analyzes profitability related to a company’s shareholders’ equity, ROCE considers debt and equity. This can help neutralize financial performance analysis for companies with significant debt.")
            ], width = 3)   
        ]) 
    ], fluid = True),


# # This is the graph for the Gross Profit Margin
#     dbc.Container(style = {'border': "2px black solid"}, children = [
        
#         dbc.Row([
#             dbc.Col(html.H4("Gross Profit Margin"
#             , className = 'text-center pt-3 mb-4'), 
#             width = 12)
#         ]),


#     dbc.Row([

#         dbc.Col(
#             dcc.Graph(id = "grossProfitMargin-annual",
#             figure = {}
#             ),
#             width = 9),

#         dbc.Col(
#             id = "grossProfitMarginDescrip-annual",
#             className = "py-5 d-inline-block",
#             children = [
#             html.H2("Description:\n"),
#             html.P("You can think of it as the amount of money from product sales left over after all of the direct costs associated with manufacturing the product have been paid."),
#             html.P("If a company's gross profit margin wildly fluctuates, this may signal poor management practices and/or inferior products. On the other hand, such fluctuations may be justified in cases where a company makes sweeping operational changes to its business model, in which case temporary volatility should be no cause for alarm.") 
#             ], width = 3)   

#     ])    
#     ], fluid = True),

# # This is the graph for the Operating Profit Margin

#     dbc.Container(style = {'border': "2px black solid"}, children = [
        
#         dbc.Row([
#             dbc.Col(html.H4("Operating Profit Margin"
#             , className = 'text-center pt-3 mb-4'), 
#             width = 12)
#         ]),


#     dbc.Row([

#         dbc.Col(
#             dcc.Graph(id = "OpProfitMargin-annual",
#             figure = {}
#             ),
#             width = 9),

#         dbc.Col(
#             id = "OpProfitMarginDescrip-annual",
#             className = "py-5 d-inline-block",
#             children = [
#             html.H2("Description:\n"),
#             html.P("An operating margin represents how efficiently a company is able to generate profit through its core operations. It is expressed on a per-sale basis after accounting for variable costs but before paying any interest or taxes (EBIT)."),
#             html.P("Higher margins are considered better than lower margins, and can be compared between similar competitors but not across different industries.") 
#             ], width = 3)   
#         ])
#     ], fluid = True),

# # This is the graph for the Net Profit Margin

#     dbc.Container(style = {'border': "2px black solid"}, children = [
        
#         dbc.Row([
#             dbc.Col(html.H4("Net Profit Margin"
#             , className = 'text-center pt-3 mb-4'), 
#             width = 12)
#         ]),


#     dbc.Row([

#         dbc.Col(
#             dcc.Graph(id = "netProfitMargin-annual",
#             figure = {}
#             ),
#             width = 9),

#         dbc.Col(
#             id = "netProfitMarginDescrip-annual",
#             className = "py-5 d-inline-block",
#             children = [
#             html.H2("Description:\n"),
#             html.P("Net profit margin measures how much net income is generated as a percentage of revenues received."),
#             html.P("Net profit margin helps investors assess if a company's management is generating enough profit from its sales and whether operating costs and overhead costs are being contained. Net profit margin is one of the most important indicators of a company's overall financial health.")
#             ], width = 3)   
#     ])

#     ], fluid = True),

#     html.Hr(),



], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'ROE-comparison', component_property = 'figure'),
    Output(component_id = 'ROA-comparison', component_property = 'figure'),
    Output(component_id = 'ROCE-comparison', component_property = 'figure'),
    Input(component_id = "tabs-fin-ratios-comparison", component_property = "value"),
    Input(component_id = "comparison-profit", component_property = "data"),
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
    if tab != "tab-3":
         raise PreventUpdate

    
    # Create a copy since you don't want to mess up the original
    ratios_dff = pd.read_json(data_comparison)

    # ROE figure
    fig_ROA = px.scatter(ratios_dff, x = "Last Reported", y = "ROE", color = "symbol")
    fig_ROA.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))    

    # ROA figure
    fig_ROE = px.scatter(ratios_dff, x = "Last Reported", y = "ROA", color = "symbol")
    fig_ROE.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # ROCE figure
    fig_ROCE = px.scatter(ratios_dff, x = "Last Reported", y = "ROCE", color = "symbol")
    fig_ROCE.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    return fig_ROA, fig_ROE, fig_ROCE


######################################################################## Create the server ####################################################################################
