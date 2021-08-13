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
from .functions import IS_datatable


################################################################ Begin the app layout #############################################################################

quarter_income_layout = dbc.Container([

# This is the data table, revenue and gross profit graphs 
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
            id='income-table-quarter',
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
            dcc.Graph(id = "RevenueBarPlot-quarter",
            figure = {},
            ),
            width = 6),
        
        dbc.Col(
            dcc.Graph(id = "GrossProfitBarPlot-quarter",
            figure = {},
            ),
            width = 6)
    ]),

# This is the opex and Depreciation graphs
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "OperatingExpBarPlot-quarter",
            figure = {}
            ),
            width = 6),

        dbc.Col(
            dcc.Graph(id = "Deprec-AmortBarPlot-quarter",
            figure = {}
            ),
            width = 6),

    ]),

# This is the EBITDA & net income graphs

    dbc.Row([
        
        dbc.Col(
            dcc.Graph(id = "EBITDA-OpIncomeBarPlot-quarter",
            figure = {}
            ),
            width = 6),   

        dbc.Col(
            dcc.Graph(id = "NetIncome-quarter",
            figure = {}
            ),
            width = 6),


    
    ]),

# This is the earnings vs expectations graphs

    dbc.Row([
        dbc.Col(
            dcc.Graph(id = "EPS-quarter",
            figure = {}
            ),
            )
        
    ])



], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################

# First callback to get all the necessary data for the graphs 
@app.callback(
     [Output(component_id = 'income-table-quarter', component_property = 'columns'),
     Output(component_id = 'income-table-quarter', component_property = 'data'),
     Output(component_id='RevenueBarPlot-quarter', component_property='figure'),
     Output(component_id='GrossProfitBarPlot-quarter', component_property='figure'),
     Output(component_id='OperatingExpBarPlot-quarter', component_property='figure'),
     Output(component_id='Deprec-AmortBarPlot-quarter', component_property='figure'),
     Output(component_id='EBITDA-OpIncomeBarPlot-quarter', component_property='figure'),
     Output(component_id='NetIncome-quarter', component_property='figure'),
     Output(component_id='EPS-quarter', component_property='figure')],
    [Input(component_id='period-slider-quarter', component_property='value'),
    Input(component_id = "quarter-income-memory", component_property = "data"),
    State(component_id = "single-ticker-input-bar", component_property = "value")]
)

def figure_callback(period_range, data_quarter, state):

    # If there is no stock in the bar, do not trigger any callbacks
    if len(state) == 0:
        raise PreventUpdate

    # When you enter a ticker, the callback is triggered. This time, if the data store comes up empty, stop the callback again     
    if len(pd.read_json(data_quarter)) == 0:
         raise PreventUpdate    


    income_dff = pd.read_json(data_quarter)

    # Filter based on date range
    income_dff = income_dff.iloc[period_range[0]:period_range[1]+1]

    # Income Statement Table
    income_data = income_dff.copy()
    columns, data = IS_datatable(income_data)

    # Reverse the order of the date to make the graphs' x-axis in ascending order
    income_dff = income_dff.sort_values(by = ["date"])
    
    # Revenue graph
    fig_revenue = px.bar(income_dff, x="date", y="revenue", barmode = "group")

    # Gross profit graph
    fig_grossprofit = make_subplots(specs=[[{"secondary_y": True}]]) # Create figure with secondary y-axis
    fig_grossprofit.add_trace(   # For multicharts, you need to add each plot individually - first one barplot for grossProfit
        go.Bar(x=income_dff["date"], y=income_dff["grossProfit"], name = "Gross Profit"),
        secondary_y = False
    )
    fig_grossprofit.add_trace(   # For multicharts, you need to add each plot individually - second one barplot for cost of revenue
        go.Bar(x=income_dff["date"], y=income_dff["costOfRevenue"], name = "Cost of Revenue"),
        secondary_y = False
    )
    fig_grossprofit.add_trace( # Add the line plots
        go.Scatter(x=income_dff["date"], y=income_dff["grossProfitRatio"], name = "Gross Profit Ratio"),
        secondary_y = True
    )
    fig_grossprofit.update_layout(
        title_text="Gross Profit & Costs of Revenue",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
            ),
    )



    # OPEX graph
    fig_opex = make_subplots(specs=[[{"secondary_y": True}]]) # Create figure with secondary y-axis
    fig_opex.add_trace(   # For multicharts, you need to add each plot individually - first one barplot for operating expenses
        go.Bar(x=income_dff["date"], y=income_dff["operatingExpenses"], name = "Operating Expenses"),
        secondary_y = False
    )
    fig_opex.add_trace(   # For multicharts, you need to add each plot individually - second one line chart for the research expenses ratio
        go.Scatter(x=income_dff["date"], y=income_dff["researchExpRatio"], name = "Research Exp Ratio"),
        secondary_y = True
    )
    fig_opex.add_trace( # Add the line plots
        go.Scatter(x=income_dff["date"], y=income_dff["sellingMktExpRatio"], name = "Sell & Market Exp Ratio"),
        secondary_y = True
    )
    fig_opex.update_layout(
        title_text="Operating Expenses",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
            ),
    )



    # Depreciation & Amortization graph
    fig_deprec = px.bar(income_dff, x="date", y="depreciationAndAmortization", title="Depreciation & Amortization",
        labels=dict(date="", depreciationAndAmortization="USD"))



    # EBITDA, Operating Income graph
    fig_ebitOp = make_subplots(specs=[[{"secondary_y": True}]]) # Create figure with secondary y-axis
    fig_ebitOp.add_trace(   # For multicharts, you need to add each plot individually - first one barplot for ebitda
        go.Bar(x=income_dff["date"], y=income_dff["ebitda"], name = "EBITDA"),
        secondary_y = False
    )
    fig_ebitOp.add_trace(   # For multicharts, you need to add each plot individually - second one barplot for operating income
        go.Bar(x=income_dff["date"], y=income_dff["operatingIncome"], name = "Op Income"),
        secondary_y = False
    )
    fig_ebitOp.add_trace(   # For multicharts, you need to add each plot individually - third one line chart for the ebitda ratio
        go.Scatter(x=income_dff["date"], y=income_dff["ebitdaratio"], name = "EBITDA Ratio"),
        secondary_y = True
    )
    fig_ebitOp.add_trace( # Add the line plots
        go.Scatter(x=income_dff["date"], y=income_dff["operatingIncomeRatio"], name = "Op Income Ratio"),
        secondary_y = True
    )
    fig_ebitOp.update_layout(
        title_text="EBITDA & Operating Income",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
            ),
        legend=dict(
            x=1.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
    ),
    )

    # Net Income graph
    fig_Netincome = make_subplots(specs=[[{"secondary_y": True}]]) # Create figure with secondary y-axis
    fig_Netincome.add_trace(   # For multicharts, you need to add each plot individually - first one barplot for Net Income
        go.Bar(x=income_dff["date"], y=income_dff["netIncome"], name = "Net Income"),
        secondary_y = False
    )    
    fig_Netincome.add_trace(   # For multicharts, you need to add each plot individually - third one line chart for the ebitda ratio
        go.Scatter(x=income_dff["date"], y=income_dff["netIncomeRatio"], name = "Net Income Ratio"),
        secondary_y = True
    )
    fig_Netincome.update_layout(
        title_text="Net Income",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
            ),
        legend=dict(
            x=1.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
    )
    )

    # EPS graph
    fig_EPS = px.scatter(income_dff, x="date", y="eps", title="Earnings per Share",
        labels=dict(date="", eps="USD"))
    fig_EPS.update_traces(
        marker=dict(size=12,
                    line=dict(width=2,
                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))


    return columns, data, fig_revenue, fig_grossprofit, fig_opex, fig_deprec, fig_ebitOp, fig_Netincome, fig_EPS




######################################################################## Create the server ####################################################################################
