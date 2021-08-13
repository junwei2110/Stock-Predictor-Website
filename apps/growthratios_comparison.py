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

comparison_growratio_layout = dbc.Container([

    
# This is the graph for the Revenue Growth  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Revenue Growth"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


        dbc.Row([

        dbc.Col(
            dcc.Graph(id = "RG-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
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
            dcc.Graph(id = "FCFG-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
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
            dcc.Graph(id = "OpProfGrowth-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("Operating profit attempts to measure the profits of a company’s operating before they are impacted by non operational costs such as interest and tax expense. It measures the efficiency of running the company's operations."),
            html.P("Operating profit eliminates a number of extraneous and indirect factors that can obscure a company's real performance. Hence, its growth rate can help determine the future prospects of the company")
            ], width = 3)   
        ]) 
    ], fluid = True),



], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'RG-comparison', component_property = 'figure'),
    Output(component_id = 'FCFG-comparison', component_property = 'figure'),
    Output(component_id = 'OpProfGrowth-comparison', component_property = 'figure'),
    Input(component_id = "tabs-fin-ratios-comparison", component_property = "value"),
    Input(component_id = "comparison-growth", component_property = "data"),
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
    if tab != "tab-2":
         raise PreventUpdate

    # Create a copy since you don't want to mess up the original
    ratios_dff = pd.read_json(data_comparison)

    # Revenue Growth figure
    fig_RG = px.scatter(ratios_dff, x = "Last Reported", y = "Revenue Growth", color = "symbol")
    fig_RG.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # FCF Growth figure
    fig_FCFG = px.scatter(ratios_dff, x = "Last Reported", y = "FCF Growth", color = "symbol")
    fig_FCFG.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # Operating Income Growth figure
    fig_OpProfG = px.scatter(ratios_dff, x = "Last Reported", y = "Operating Income Growth", color = "symbol")
    fig_OpProfG.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))


    return fig_RG, fig_FCFG, fig_OpProfG




######################################################################## Create the server ####################################################################################
