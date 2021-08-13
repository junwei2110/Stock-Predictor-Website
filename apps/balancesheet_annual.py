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
import pathlib
from app import app
from .functions import BS_datatable



# # Getting the path
# PATH = pathlib.Path(__file__).parent # Gets the path url of this file (i.e. the parent url)
# DATA_PATH = PATH.joinpath("../datasets").resolve() # Adds the datasets path link to the parent url
# balance_df = pd.read_csv(DATA_PATH.joinpath('Book2.csv')) # Adds the file name to the overall url


################################################################ Begin the app layout #############################################################################

annual_balance_layout = dbc.Container(children=[
    # html.H1(children='Balance Sheet'),

    # # Choose your stock
    # html.Div([
    #     html.Div([
    #     dcc.Dropdown(
    #     id='stock-dropdown-balance',
    #     options=[
    #         {"label": label, "value": label} for label in balance_df['symbol'].unique()
    #     ],
    #     value = balance_df['symbol'][0]
    #     )],
    #     className = "two columns"),
        
        
    #     html.Button('Annual', id='annual_btn', n_clicks=0),
    #     html.Button('Quarter', id='quarter_btn', n_clicks=0)
                
    
    # ]),

    # html.Br(),



    html.Br(),

# This is the data table for the balance sheet, the assets and liabilities graphs 
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
            id='balance-table-annual',
            columns=[],
            data = [],
            fixed_columns={'headers': True, 'data': 1},
            style_cell={'textAlign': 'left',
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
            },
            style_data_conditional=[ # Make the odd rows a shade darker
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header= { # Make the row header a shade darker and the font bold
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
                },
            style_table={'minWidth': '100%'},
            ), 
            width = 12),
    ]),

    dbc.Row([
        
        dbc.Col(
            dcc.Graph(id = "AssetsBarPlot-annual",
            figure = {},
            style={'height': 450}),
            width = 6),
        
        dbc.Col(
            dcc.Graph(id = "LiabilitiesBarPlot-annual",
            figure = {},
            style={'height': 450})
            ,
            width = 6)
    ]),

# This is the equity graphs  
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "EquityBarPlot-annual",
            figure = {}),
            width = 12)
    ]),

# This is the liquidity ratios and the solvency ratios graphs  
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "liquidityRatios-annual",
            figure = {})
            ,
            width = 6),

        dbc.Col(
            dcc.Graph(id = "solvencyRatios-annual",
            figure = {})
            ,
            width = 6),

        
    ]),


# This is the current assets breakdown and the long term assets breakdown graphs  
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "currentAssetsBreakdownPlot-annual",
            figure = {})
            ,
            width = 6),

        dbc.Col(
            dcc.Graph(id = "longtermAssetsBreakdownPlot-annual",
            figure = {})
            ,
            width = 6),

        
    ]),

# This is the current liabilities breakdown and the long term liabilities breakdown graph

    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "currentLiabilitiesBreakdownPlot-annual",
            figure = {})
            ,
            width = 6),

        dbc.Col(
            dcc.Graph(id = "longtermLiabilitiesBreakdownPlot-annual",
            figure = {})
            ,
            width = 6)

    
    ])


], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################


@app.callback(
     [Output(component_id = 'balance-table-annual', component_property = 'columns'),
     Output(component_id = 'balance-table-annual', component_property = 'data'),
     Output(component_id='AssetsBarPlot-annual', component_property='figure'),
     Output(component_id='LiabilitiesBarPlot-annual', component_property='figure'),
     Output(component_id='EquityBarPlot-annual', component_property='figure'),
     Output(component_id='liquidityRatios-annual', component_property='figure'),
     Output(component_id='solvencyRatios-annual', component_property='figure'),
     Output(component_id='currentAssetsBreakdownPlot-annual', component_property='figure'),
     Output(component_id='longtermAssetsBreakdownPlot-annual', component_property='figure'),
     Output(component_id='currentLiabilitiesBreakdownPlot-annual', component_property='figure'),
     Output(component_id='longtermLiabilitiesBreakdownPlot-annual', component_property='figure')],
    [Input(component_id='period-slider-annual', component_property='value'),
    Input(component_id = "annual-balance-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value")]
)

def figure_callback(period_range, data_annual, state):

    # If there is no stock in the bar, do not trigger any callbacks
    if len(state) == 0:
        raise PreventUpdate

    # When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if len(pd.read_json(data_annual)) == 0:
         raise PreventUpdate    
    
    balance_dff = pd.read_json(data_annual)
    
    # Filter based on date range
    balance_dff = balance_dff.iloc[period_range[0]:period_range[1]+1]

    # Balance Sheet Table
    balance_data = balance_dff.copy()
    columns, data = BS_datatable(balance_data)

    # Creating another copy of the data
    balance_ratios = balance_dff.copy()
    
    # Assets barplot
    fig_assetsbar = make_subplots(specs=[[{"secondary_y": True}]]) # Create figure with secondary y-axis
    fig_assetsbar.add_trace(   # For multicharts, you need to add each plot individually
        go.Bar(x=balance_ratios["date"], y=balance_ratios["totalCurrentAssets"], name = "Current Assets"),
        secondary_y = False
    )
    fig_assetsbar.add_trace(   
        go.Bar(x=balance_ratios["date"], y=balance_ratios["totalNonCurrentAssets"], name = "Non-Current Assets"),
        secondary_y = False
    )
    fig_assetsbar.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["totalCurrentAssetsRatio"], name = "Current Assets Ratio"),
        secondary_y = True
    )
    fig_assetsbar.update_layout(
        title_text="Assets",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
    ))

    # Liabilities barplot
    fig_liabilitiesbar = make_subplots(specs=[[{"secondary_y": True}]]) # Create figure with secondary y-axis
    fig_liabilitiesbar.add_trace(   # For multicharts, you need to add each plot individually 
        go.Bar(x=balance_ratios["date"], y=balance_ratios["totalCurrentLiabilities"], name = "Current Liabilities"),
        secondary_y = False
    )
    fig_liabilitiesbar.add_trace(   
        go.Bar(x=balance_ratios["date"], y=balance_ratios["totalNonCurrentLiabilities"], name = "Non-Current Liabilities"),
        secondary_y = False
    )
    fig_liabilitiesbar.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["totalCurrentLiabilitiesRatio"], name = "Current Liabilities Ratio"),
        secondary_y = True
    )
    fig_liabilitiesbar.update_layout(
        title_text="Liabilities",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
    ))

    # Equities barplot
    fig_equitiesbar = make_subplots(specs=[[{"secondary_y": True}]]) # Create figure with secondary y-axis
    fig_equitiesbar.add_trace(   # For multicharts, you need to add each plot individually 
        go.Bar(x=balance_ratios["date"], y=balance_ratios["totalStockholdersEquity"], name = "StockHolder Equity"),
        secondary_y = False
    )
    fig_equitiesbar.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["retainedEarningsRatio"], name = "Retained Earnings Ratio"),
        secondary_y = True
    )
    fig_equitiesbar.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["commonStockRatio"], name = "Common Stock Ratio"),
        secondary_y = True
    )
    fig_equitiesbar.update_layout(
        title_text="Equity",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
    ))

    # Liquidity Ratios
    fig_liquidity = go.Figure()
    fig_liquidity.add_trace(   # For multicharts, you need to add each plot individually
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["currentRatio"], name = "Current Ratio"),
    )    
    fig_liquidity.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["quickRatio"], name = "Quick Ratio"),
    )        
    fig_liquidity.update_layout(
        title_text="Liquidity Ratio",
        yaxis=dict(
            title=''
            )
    )

    # Solvency Ratios
    fig_solvency = go.Figure()
    fig_solvency.add_trace(   # For multicharts, you need to add each plot individually 
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["debtToEquityRatio"], name = "Debt to Equity Ratio"),
    )    
    fig_solvency.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["debtToAssetsRatio"], name = "Debt to Assets Ratio"),
    )        
    fig_solvency.update_layout(
        title_text="Solvency Ratio",
        yaxis=dict(
            title=''
            )
    )

    # Current Assets Breakdown Graph
    fig_assetsBreakdown = go.Figure()
    fig_assetsBreakdown.add_trace(   # For multicharts, you need to add each plot individually
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["cashAndCashEquivalentsRatio"], name = "Cash and Cash Equivalent"),
    )    
    fig_assetsBreakdown.add_trace(  
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["shortTermInvestmentsRatio"], name = "Short Term Investments"),
    )        
    fig_assetsBreakdown.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["netReceivablesRatio"], name = "Net Receivables"),
    )   
    fig_assetsBreakdown.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["inventoryRatio"], name = "Inventory"),
    )          
    fig_assetsBreakdown.update_layout(
        title_text="Current Assets Breakdown",
        yaxis=dict(
            title=''
            )
    )

    # Non-current Assets Breakdown Graph
    fig_noncurrentassetsBreakdown = go.Figure()
    fig_noncurrentassetsBreakdown.add_trace(   # For multicharts, you need to add each plot individually 
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["propertyPlantEquipmentNetRatio"], name = "Property, Plant & Equipment"),
    )    
    fig_noncurrentassetsBreakdown.add_trace( 
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["goodwillAndIntangibleAssetsRatio"], name = "Good Will & Intangibles"),
    )        
    fig_noncurrentassetsBreakdown.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["longTermInvestmentsRatio"], name = "Long Term Investments"),
    )   
    fig_noncurrentassetsBreakdown.update_layout(
        title_text="Non-current Assets Breakdown",
        yaxis=dict(
            title=''
            )
    )

    # Current Liabilities Breakdown Graph
    fig_liabilitiesBreakdown = go.Figure()
    fig_liabilitiesBreakdown.add_trace(   # For multicharts, you need to add each plot individually 
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["accountPayablesRatio"], name = "Account Payables"),
    )    
    fig_liabilitiesBreakdown.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["shortTermDebtRatio"], name = "Short Term Debt"),
    )        
    fig_liabilitiesBreakdown.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["deferredRevenueRatio"], name = "Deferred Revenue"),
    )   
    fig_liabilitiesBreakdown.update_layout(
        title_text="Current Liabilities Breakdown",
        yaxis=dict(
            title=''
            )
    )

    # Non-current Liabilities Breakdown Graph
    fig_noncurrentliabilitiesBreakdown = go.Figure()
    fig_noncurrentliabilitiesBreakdown.add_trace(   # For multicharts, you need to add each plot individually 
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["longTermDebtRatio"], name = "Long Term Debt"),
    )    
    fig_noncurrentliabilitiesBreakdown.add_trace(  
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["deferredRevenueNonCurrentRatio"], name = "Deferred Non-Current Revenue"),
    )        
    fig_noncurrentliabilitiesBreakdown.add_trace(   
        go.Scatter(x=balance_ratios["date"], y=balance_ratios["deferredTaxLiabilitiesNonCurrentRatio"], name = "Deferred Tax Liabilities"),
    )   
    fig_noncurrentliabilitiesBreakdown.update_layout(
        title_text="Non-current Liabilities Breakdown",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
            )
    )


    return columns, data, fig_assetsbar, fig_liabilitiesbar, fig_equitiesbar, fig_liquidity, fig_solvency, fig_assetsBreakdown, fig_noncurrentassetsBreakdown, fig_liabilitiesBreakdown, fig_noncurrentliabilitiesBreakdown




######################################################################## Create the server ####################################################################################
