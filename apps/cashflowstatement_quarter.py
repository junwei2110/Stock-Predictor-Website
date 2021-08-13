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
from .functions import CF_datatable, CF_waterfall

################################################################ Begin the app layout #############################################################################

quarter_cash_layout = dbc.Container(children=[

# This is the data table for the cash flow statement and the plots for the free cash flow, financial and investing cash flows  
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
            id='cashflow-table-quarter',
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
            dcc.Graph(id = "OpCashFlowPlot-quarter",
            figure = {},
            style={'height': 450}),
            width = 6),

        dbc.Col(    
            dcc.Graph(id = "Fin&InvestCashFlowPlot-quarter",
            figure = {},
            style={'height': 450}),
            width = 6)
    ]),

# This is the waterfall graph for the cash changes across the years  
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "NetCashChanges-quarter",
            figure = {},
            style={'height': 700}), 
        width = 12)
    ]),


# This is the breakdown of the 3 different types of cash flow 
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "OpCashFlowBreakdown-quarter",
            figure = {}),
            width = 4),

        dbc.Col(
            dcc.Graph(id = "FinCashFlowBreakdown-quarter",
            figure = {}),
            width = 4),

        dbc.Col(
            dcc.Graph(id = "InvestCashFlowBreakdown-quarter",
            figure = {}),
            width = 4)

        
    ])


], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

# First callback to get all the necessary data for the graphs 
@app.callback(
     [Output(component_id = 'cashflow-table-quarter', component_property = 'columns'),
     Output(component_id = 'cashflow-table-quarter', component_property = 'data'),
     Output(component_id='OpCashFlowPlot-quarter', component_property='figure'),
     Output(component_id='Fin&InvestCashFlowPlot-quarter', component_property='figure'),
     Output(component_id='NetCashChanges-quarter', component_property='figure'),
     Output(component_id='OpCashFlowBreakdown-quarter', component_property='figure'),
     Output(component_id='FinCashFlowBreakdown-quarter', component_property='figure'),
     Output(component_id='InvestCashFlowBreakdown-quarter', component_property='figure')],
    [Input(component_id='period-slider-quarter', component_property='value'),
    Input(component_id = "quarter-cash-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value")]
)

def figure_callback(period_range, data_quarter, state):
    
    # If there is no stock in the bar, do not trigger any callbacks
    if len(state) == 0:
        raise PreventUpdate

    # When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if len(pd.read_json(data_quarter)) == 0:
         raise PreventUpdate    

    # Create a copy since you don't want to mess up the original
    cashflow_dff = pd.read_json(data_quarter)
    
    # Filter based on date range
    cashflow_dff = cashflow_dff.iloc[period_range[0]:period_range[1]+1]

    # Cash Flow Statement Table
    cashflow_table = cashflow_dff.copy()
    columns, data = CF_datatable(cashflow_table)

    # Reverse the order of the date to make the graphs' x-axis in ascending order
    cashflow_dff = cashflow_dff.sort_values(by = ["date"])
    
    # Modifying the data to calculate the ratios
    cashflow_ratios = cashflow_dff.copy()

    # Data Preparation for waterfall chart
    waterfall_df = cashflow_dff.copy()
    waterfall_df = CF_waterfall(waterfall_df, cashflow_dff)

    # Operating CF barplot
    fig_opcf = go.Figure() 
    fig_opcf.add_trace(   # For multicharts, you need to add each plot individually
        go.Bar(x=cashflow_ratios["date"], y=cashflow_ratios["capitalExpenditure"], name = "Capital Expenditures")
    )
    fig_opcf.add_trace(   
        go.Bar(x=cashflow_ratios["date"], y=cashflow_ratios["freeCashFlow"], name = "Free Cash Flow"),
    )
    
    fig_opcf.update_layout(
        title_text="Operating Cash Flow",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
    ))

    # Financial and Investing CFplot
    fig_fininvcf = go.Figure()
    fig_fininvcf.add_trace(   # For multicharts, you need to add each plot individually 
        go.Bar(x=cashflow_ratios["date"], y=cashflow_ratios["netCashUsedProvidedByFinancingActivities"], name = "Financial Cash Flow"),
    )
    fig_fininvcf.add_trace(   
        go.Bar(x=cashflow_ratios["date"], y=cashflow_ratios["netCashUsedForInvestingActivites"], name = "Investing Cash Flow"),
    )
    fig_fininvcf.update_layout(
        title_text="Financial & Investing Cash Flows",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
    ))

    # Waterfall plot of Cash Changes across the years
    fig_waterfall = go.Figure()
    fig_waterfall.add_trace(go.Waterfall(
        x = [waterfall_df["date"], waterfall_df["waterfall_parameters"]],
        measure = waterfall_df["measure"],
        y = waterfall_df["waterfall_val"]
    ))

    fig_waterfall.update_layout(
        title_text="Net Cash Flow Changes",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
    ))

    # Operating Cash Flow Breakdown
    fig_opbreakdown = go.Figure()
    fig_opbreakdown.add_trace(   # For multicharts, you need to add each plot individually
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["netIncometoCashflowRatio"], name = "Net Income to CF Ratio"),
    )    
    fig_opbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["deprectoCashflowRatio"], name = "Depreciation & Amortization"),
    )        
    fig_opbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["deferIncomeTaxRatio"], name = "Deferred Income Tax Ratio"),
    )     
    fig_opbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["stockCompenseRatio"], name = "Stock Compensation Ratio"),
    )     
    fig_opbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["accountsReceivableRatio"], name = "Accounts Receivable Ratio"),
    )     
    fig_opbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["inventoryRatio"], name = "Inventory Ratio"),
    )         
    fig_opbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["accountsPayablesRatio"], name = "Accounts Payable Ratio"),
    )   
    fig_opbreakdown.update_layout(
        title_text="Operating Cash Flow Breakdown",
        yaxis=dict(
            title=''
            )
    )

    # Investing Cash Flow Ratios
    fig_invbreakdown = go.Figure()
    fig_invbreakdown.add_trace(   # For multicharts, you need to add each plot individually
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["PPERatio"], name = "PPE Ratio"),
    )    
    fig_invbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["acquisitionRatio"], name = "Acquisition Ratio"),
    )        
    fig_invbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["investmentPurchaseRatio"], name = "Investment Purchase Ratio"),
    )     
    fig_invbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["salesMaturityInvestmentRatio"], name = "Sales of Matured Investments"),
    )     

    fig_invbreakdown.update_layout(
        title_text="Investing Cash Flow Breakdown",
        yaxis=dict(
            title=''
            )
    )


    # Financial Cash Flow Ratios
    fig_finbreakdown = go.Figure()
    fig_finbreakdown.add_trace(   # For multicharts, you need to add each plot individually
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["debtRepaymentRatio"], name = "Debt Repayment Ratio"),
    )    
    fig_finbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["stockIssueRatio"], name = "Stock Issue Ratio"),
    )        
    fig_finbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["stockRepurchaseRatio"], name = "Stock Repurchase Ratio"),
    )     
    fig_finbreakdown.add_trace(   
        go.Scatter(x=cashflow_ratios["date"], y=cashflow_ratios["dividendsPaidRatio"], name = "Dividends Paid Ratio"),
    )     

    fig_finbreakdown.update_layout(
        title_text="Financial Cash Flow Breakdown",
        yaxis=dict(
            title=''
            )
    )

    
    return columns, data, fig_opcf, fig_fininvcf, fig_waterfall, fig_opbreakdown, fig_invbreakdown, fig_finbreakdown




######################################################################## Create the server ####################################################################################

