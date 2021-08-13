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
import json
import pathlib
from app import app
from .functions import profile_datatable, liquidity_solvency_summary_table, growth_ratios_summary_table, profit_ratios_summary_table, investment_ratios_summary_table


################################################################ Begin the app layout #############################################################################

summary_layout = dbc.Container([

    #Create a message when there is no input yet
    dbc.Row([
        dbc.Col(
            dbc.Jumbotron([
            html.H1(id = "financial-statements-message", children = ["Single Ticker Analysis"], className = "text-white"),
            html.P(
                "Understanding the financials of the company",
                className="lead text-white",
                ),
        
            html.Hr(),
        
            html.P("Step 1: Input the stock ticker that you wish to analyze into the search bar above"
            , className = "text-white"), 
            html.P("Step 2: Use the summary page to get the high level understanding of the business and its relevant metrics"
            , className = "text-white"),
            html.P("Step 3: Dive into the annual and quarter figures of the income statement, balance sheet and cash flow statements for more details"
            , className = "text-white"),    
        ], style ={"background": "rgba(80, 80, 80, 0.8)", "margin": 0})

        ,className = "pt-5"
        )
    
    ], id = "starting-message"),

    
    dbc.Row([
        dbc.Col(
        html.Img(src=app.get_asset_url('cool-background.png'), style = {"width": "100%", "height": "80%" }),
        className = "text-center")
    ], id = "temp-background"),

    dbc.Row([
        dbc.Col(
            html.H1(id = "company-name", children = []),
            width = 2),

        dbc.Col(
            html.Img(id = "company-logo", src = ""),
            width = 1),

    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(
            html.P(id = "company-desc", children = []),
            width = 12)
    
    ]),

    dbc.Row([

            dbc.Col(

            dash_table.DataTable(
            id='company-summary-table',
            columns= [],
            data = [],
            fixed_columns={'headers': True},
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
            width = 4, className = "pt-5"),    

            dbc.Col(
                dbc.Row([], id = "price-figure"),

            width = 8)
    ]),




    dbc.Row([

    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(

            dash_table.DataTable(
            id='liq-sol-summary-table',
            columns= [],
            data = [],
            fixed_columns={'headers': True},
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

    html.Br(),

    dbc.Row([
        dbc.Col(

            dash_table.DataTable(
            id='growth-ratios-summary-table',
            columns= [],
            data = [],
            fixed_columns={'headers': True},
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

    html.Br(),

    dbc.Row([
        dbc.Col(

            dash_table.DataTable(
            id='profit-ratios-summary-table',
            columns= [],
            data = [],
            fixed_columns={'headers': True},
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

    html.Br(),

    dbc.Row([
        dbc.Col(

            dash_table.DataTable(
            id='investment-ratios-summary-table',
            columns= [],
            data = [],
            fixed_columns={'headers': True},
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



], id = "summary-page", fluid = True, style = {"background-image": 'url("/assets/cool-background.png")', "width": "100%", "height": "100%" })


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

# First callback to get all the necessary data for the graphs 
@app.callback(
     [Output(component_id = 'starting-message', component_property = 'children'),
     Output(component_id = 'temp-background', component_property = 'children'),
     Output(component_id = 'summary-page', component_property = 'style'),
     Output(component_id = 'company-name', component_property = 'children'),
     Output(component_id = 'company-logo', component_property = 'src'),
     Output(component_id = 'company-desc', component_property = 'children'),
     Output(component_id = 'price-figure', component_property = 'children'),
     Output(component_id = 'company-summary-table', component_property = 'columns'),
     Output(component_id = 'company-summary-table', component_property = 'data'),
     Output(component_id = 'liq-sol-summary-table', component_property = 'columns'),
     Output(component_id = 'liq-sol-summary-table', component_property = 'data'),
     Output(component_id = 'growth-ratios-summary-table', component_property = 'columns'),
     Output(component_id = 'growth-ratios-summary-table', component_property = 'data'),
     Output(component_id = 'profit-ratios-summary-table', component_property = 'columns'),
     Output(component_id = 'profit-ratios-summary-table', component_property = 'data'),
     Output(component_id = 'investment-ratios-summary-table', component_property = 'columns'),
     Output(component_id = 'investment-ratios-summary-table', component_property = 'data')],
    [Input(component_id = "company-profile", component_property = "data"),
    Input(component_id = "annual-ratios-memory", component_property = "data"),
    Input(component_id = "quarter-ratios-memory", component_property = "data"),
    Input(component_id = "TTM-ratios-memory", component_property = "data"),
    Input(component_id = "annual-income-memory", component_property = "data"),
    Input(component_id = "annual-cash-memory", component_property = "data"),
    Input(component_id = "quarter-income-memory", component_property = "data"),
    Input(component_id = "quarter-cash-memory", component_property = "data"),
    Input(component_id = "quarter-balance-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value")]
)

def figure_callback(data_summary, ratios_data_A, ratios_data_Q, ratios_data_TTM, income_A, cash_A, income_Q, cash_Q, balance_Q, state):

    # If there is no stock in the bar, do not trigger any callbacks
    if len(state) == 0:
        raise PreventUpdate

    #When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if (len(pd.read_json(data_summary)) == 0):
        raise PreventUpdate    


    # Message and Image
    message = []
    temp_background = []
    style = {}

    profile_dff = pd.read_json(data_summary)
    ratios_A_dff = pd.read_json(ratios_data_A)
    ratios_Q_dff = pd.read_json(ratios_data_Q)
    ratios_TTM_dff = pd.read_json(ratios_data_TTM)
    income_A_dff = pd.read_json(income_A)
    cash_A_dff = pd.read_json(cash_A)
    income_Q_dff = pd.read_json(income_Q)
    cash_Q_dff = pd.read_json(cash_Q)
    balance_Q_dff = pd.read_json(balance_Q)

    # Get the company name
    company_name = profile_dff["Company Name"][0]
    

    # Get the link to the logo
    company_logo = profile_dff["image URL"][0]
    
    # Get the company description
    company_desc = profile_dff["Description"][0]
    

    # Get the graph figure
    children = [dbc.Col(    
                    dcc.Graph(id = "price-for-last-3-years",
                    figure = {}
                    ),
                    width = 12),
                    ]
                


    # Summary Table
    columns_profile, data_profile = profile_datatable(profile_dff)
    
    # Liquidity and Solvency Summary Table
    columns_liq, data_liq = liquidity_solvency_summary_table(ratios_Q_dff)
    
    # Growth Ratios Summary Table
    columns_growth, data_growth = growth_ratios_summary_table(income_Q_dff, cash_Q_dff, income_A_dff, cash_A_dff)
    
    # Profit Ratios Summary Table
    columns_profit, data_profit = profit_ratios_summary_table(income_Q_dff, balance_Q_dff)
    
    # Investment Ratios Summary Table
    columns_investment, data_investment = investment_ratios_summary_table(ratios_TTM_dff, ratios_A_dff)
    




    return message, temp_background, style, company_name, company_logo, company_desc, children, columns_profile, data_profile, columns_liq, data_liq, columns_growth, data_growth, columns_profit, data_profit, columns_investment, data_investment


@app.callback(
     Output(component_id = 'price-for-last-3-years', component_property = 'figure'),
     Input(component_id = 'price-figure', component_property = 'children'),
     State(component_id = "company-stock-price", component_property = "data"),
)

def price_graph_update(children, data_prices):

    #When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if (len(pd.read_json(data_prices)) == 0):
        raise PreventUpdate    


    prices_dff = pd.read_json(data_prices)

    prices_dff = prices_dff.sort_values(by = ["date"])
    
    fig_prices = go.Figure(data=[go.Candlestick(x=prices_dff['date'],
                open=prices_dff['open'],
                high=prices_dff['high'],
                low=prices_dff['low'],
                close=prices_dff['close'])])

    fig_prices.update_layout(
        title_text="Stock Daily Closing Price",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
            ))

    return fig_prices








######################################################################## Create the server ####################################################################################
