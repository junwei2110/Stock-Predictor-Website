import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json
import pandas as pd
from app import app

################################################################ Begin the app layout #############################################################################
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


comparison_prices_layout = dbc.Container([


# This is the graph for the prices
 
    dbc.Row([

        dbc.Col(
            dcc.Graph(id = "prices-comparison-fig",
            figure = {}
            ),
            width = 12),

        ]),
    
    dbc.Row([
            dbc.Col(
            html.Pre(id='selected-data', style=styles['pre']),
            )
        ]),


], fluid = True)


################################################################ End of app layout #############################################################################


###################################################### Connect the Plotly graphs with Dash Components ###########################################################



# Callback to get all the necessary data for the graphs based on the specified date range
@app.callback(
    Output(component_id = 'prices-comparison-fig', component_property = 'figure'),
    Input(component_id = "technical-analysis-tabs", component_property = "value"),
    Input(component_id = "historical-prices-comparison-data", component_property = "data"),
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
    prices_dff = pd.read_json(data_comparison)
    
    prices_dff = prices_dff.sort_values(by = ["date"])
    fig_prices = px.scatter(prices_dff, x = "date", y = "close", color = "symbol", height = 600)
    fig_prices.update_layout(
        title_text="Stock Daily Closing Price",
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
            ),
        xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"),
        clickmode='event+select'
    ),

    
    return fig_prices


@app.callback(
    Output('selected-data', 'children'),
    Input('prices-comparison-fig', 'selectedData'),
    State(component_id = "historical-prices-comparison-data", component_property = "data")
)


def display_click_data(selectedData, data_comparison):
    
    if selectedData is None:
        raise PreventUpdate
    
    fig_info = selectedData

    # Create a copy since you don't want to mess up the original
    prices_dff = pd.read_json(data_comparison)

    if len(fig_info["points"]) < 2:
        return "Select one more data point to begin analysis"
    else:
        fig_df = pd.DataFrame(fig_info["points"], index = list(range(len(fig_info["points"]))))
        
        prices_filtered = prices_dff[prices_dff['date'].isin(fig_df["x"])]
        
        percentagechangedict = {}

        for stock in prices_filtered["symbol"].unique():
            prices_stock_filtered = prices_filtered.loc[prices_filtered["symbol"] == stock]
            prices_stock_filtered = prices_stock_filtered.sort_values(by = ["date"]).reset_index(drop = True)
            percentagechangearray = []

            for i in range(len(prices_stock_filtered["date"]) -1):
                percentagechange = ((prices_stock_filtered["close"][i+1] - prices_stock_filtered["close"][i])/prices_stock_filtered["close"][i]) * 100    
                percentagechangearray.append(percentagechange)
                
            percentagechangedict[stock] = percentagechangearray    
            
    return json.dumps(percentagechangedict)



######################################################################## Create the server ####################################################################################
