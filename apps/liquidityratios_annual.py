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

annual_liqratio_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Liquidity Ratio"
        , className = 'text-center text-primary mb-4'), 
        width = 12)
    ]),


    dbc.Row([
        dbc.Col(html.P("Liquidity ratios are an important class of financial metrics used to determine a debtor's ability to pay off current debt obligations without raising external capital. Liquidity ratios measure a company's ability to pay debt obligations and its margin of safety through the calculation of metrics including the current ratio, quick ratio, and operating cash flow ratio."
        , className = 'text-center text-primary mb-4'), 
        width = 12)
    ]),

# This is the graph for the Current Ratio  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Current Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


        dbc.Row([

        dbc.Col(
            dcc.Graph(id = "currentRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "currentRatioDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The current ratio measures a company's ability to pay current, or short-term, liabilities (debts and payables) with its current, or short-term, assets, such as cash, inventory, and receivables."),
            html.P("A current ratio of 1.0 or greater is an indication that the company is well-positioned to cover its current or short-term liabilities.") 
            ], width = 3)   
        
        ])
    ], fluid = True),

# This is the graph for the Quick Ratio  
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Quick Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([



        dbc.Col(
            dcc.Graph(id = "quickRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "quickRatioDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The quick ratio measures a company's capacity to pay its current liabilities without needing to sell its inventory or obtain additional financing."),
            html.P("Since it indicates the company’s ability to instantly use its near-cash assets (assets that can be converted quickly to cash) to pay down its current liabilities, it is also called the acid test ratio.") 
            ], width = 3)   

        ])        
    ], fluid = True),

# This is the graph for the Short Term Coverage Ratio  

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Short Term Coverage Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "shortTermCoverageRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "shortTermCoverageDescrip",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The short-term debt coverage ratio compares the sum of a company's short-term borrowings and the current portion of its long-term debt to operating cash flow."),
            ], width = 3)   
        ]) 
    ], fluid = True),


# Break for the Solvency Ratios
    html.Hr(),
    html.Br(),
    
    dbc.Row([
        dbc.Col(html.H2("Solvency Ratios"
        , className = 'text-center text-primary mb-4'), 
        width = 12)
    ]),

    dbc.Row([
        dbc.Col(html.P("A solvency ratio is a key metric used to measure an enterprise's ability to meet its long-term debt obligations and is used often by prospective business lenders. A solvency ratio indicates whether a company's cash flow is sufficient to meet its long-term liabilities and thus is a measure of its financial health."
        , className = 'text-center text-primary mb-4'), 
        width = 12)
    ]),


# This is the graph for the Debt Ratio
    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Debt Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "debtRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "debtRatioDescrip-annual",
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
            dcc.Graph(id = "debtEquityRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "debtEquityRatioDescrip-annual",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The D/E ratio is an important metric used in corporate finance. It is a measure of the degree to which a company is financing its operations through debt versus wholly owned funds. More specifically, it reflects the ability of shareholder equity to cover all outstanding debts in the event of a business downturn."),
            html.P("The debt-to-equity (D/E) ratio compares a company’s total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using. Higher-leverage ratios tend to indicate a company or stock with higher risk to shareholders. However, the D/E ratio is difficult to compare across industry groups where ideal amounts of debt will vary.Investors will often modify the D/E ratio to focus on long-term debt only because the risks associated with long-term liabilities are different than short-term debt and payables.") 
            ], width = 3)   
        ])
    ], fluid = True),

# This is the graph for the Cash Flow Coverage Ratio

    dbc.Container(style = {'border': "2px black solid"}, children = [
        
        dbc.Row([
            dbc.Col(html.H4("Cash Flow Coverage Ratio"
            , className = 'text-center pt-3 mb-4'), 
            width = 12)
        ]),


    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "CFCoverageRatio-annual",
            figure = {}
            ),
            width = 9),

        dbc.Col(
            id = "CFCoverageRatioDescrip-annual",
            className = "py-5 d-inline-block",
            children = [
            html.H2("Description:\n"),
            html.P("The operating cash flow is simply the amount of cash generated by the company from its main operations, which are used to keep the business funded."),
            ], width = 3)   
    ])

    ], fluid = True),

    html.Hr(),



], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'currentRatio-annual', component_property = 'figure'),
    Output(component_id = 'quickRatio-annual', component_property = 'figure'),
    Output(component_id = 'shortTermCoverageRatio-annual', component_property = 'figure'),
    Output(component_id = 'debtRatio-annual', component_property = 'figure'),
    Output(component_id = 'debtEquityRatio-annual', component_property = 'figure'),
    Output(component_id = 'CFCoverageRatio-annual', component_property = 'figure'),
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

    # Current Ratio figure
    fig_currentratio = px.line(ratios_dff, x = "date", y = "currentRatio")

    # Quick Ratio figure
    fig_quickratio = px.line(ratios_dff, x = "date", y = "quickRatio")

    # Short Term Cash Coverage Ratio figure
    fig_STCRatio = px.line(ratios_dff, x = "date", y = "shortTermCoverageRatios")

    # Debt Ratio figure
    fig_debtratio = px.line(ratios_dff, x = "date", y = "debtRatio")

    # Debt Equity Ratio figure
    fig_debttoEratio = px.line(ratios_dff, x = "date", y = "debtEquityRatio")

    # Coverage Ratio figure
    fig_Coverageratio = px.line(ratios_dff, x = "date", y = "cashFlowCoverageRatios")

    return fig_currentratio, fig_quickratio, fig_STCRatio, fig_debtratio, fig_debttoEratio, fig_Coverageratio




######################################################################## Create the server ####################################################################################
