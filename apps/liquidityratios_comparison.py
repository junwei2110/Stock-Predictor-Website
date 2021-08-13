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

comparison_liqratio_layout = dbc.Container([

# This is the graph for the Current Ratio  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Current Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


        dbc.Row([

        dbc.Col(
            dcc.Graph(id = "currentRatio-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The current ratio measures a company's ability to pay current, or short-term, liabilities (debts and payables) with its current, or short-term, assets, such as cash, inventory, and receivables."),
            html.P("A current ratio of 1.0 or greater is an indication that the company is well-positioned to cover its current or short-term liabilities.") 
            ], width = 3)   
        
        ])
    ], fluid = True),



# This is the graph for the Debt Ratio
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Debt Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "debtRatio-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The debt ratio is a financial ratio that measures the extent of a company’s leverage."),
            html.P("A ratio greater than 1 shows that a considerable portion of debt is funded by assets. In other words, the company has more liabilities than assets. A high ratio also indicates that a company may be putting itself at risk of default on its loans if interest rates were to rise suddenly. A ratio below 1 translates to the fact that a greater portion of a company's assets is funded by equity.") 
            ], width = 3)   

    ])    
    ], fluid = True),

# This is the graph for the Debt-to-Equity Ratio

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Debt-to-Equity Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "debtEquityRatio-comparison",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The D/E ratio is an important metric used in corporate finance. It is a measure of the degree to which a company is financing its operations through debt versus wholly owned funds. More specifically, it reflects the ability of shareholder equity to cover all outstanding debts in the event of a business downturn."),
            html.P("The debt-to-equity (D/E) ratio compares a company’s total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using. Higher-leverage ratios tend to indicate a company or stock with higher risk to shareholders. However, the D/E ratio is difficult to compare across industry groups where ideal amounts of debt will vary.Investors will often modify the D/E ratio to focus on long-term debt only because the risks associated with long-term liabilities are different than short-term debt and payables.") 
            ], width = 3)   
        ])
    ], fluid = True),


], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'currentRatio-comparison', component_property = 'figure'),
    Output(component_id = 'debtRatio-comparison', component_property = 'figure'),
    Output(component_id = 'debtEquityRatio-comparison', component_property = 'figure'),
    Input(component_id = "tabs-fin-ratios-comparison", component_property = "value"),
    Input(component_id = "comparison-liq", component_property = "data"),
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
    if tab != "tab-1":
         raise PreventUpdate    


    # Create a copy since you don't want to mess up the original
    ratios_dff = pd.read_json(data_comparison) 
    
    # Current Ratio figure
    fig_currentratio = px.scatter(ratios_dff, x = "Last Reported", y = "Current Ratio", color = "symbol")
    fig_currentratio.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # Debt Ratio figure
    fig_debtratio = px.scatter(ratios_dff, x = "Last Reported", y = "Debt Ratio", color = "symbol")
    fig_debtratio.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    # Debt Equity Ratio figure
    fig_debttoEratio = px.scatter(ratios_dff, x = "Last Reported", y = "Debt-to-Equity Ratio", color = "symbol")
    fig_debttoEratio.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    return fig_currentratio, fig_debtratio, fig_debttoEratio, 



######################################################################## Create the server ####################################################################################
