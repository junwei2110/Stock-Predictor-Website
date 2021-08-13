###### Testing #####
urlyahoo = 'https://finance.yahoo.com/losers'
r = requests.get(urlyahoo, headers = {'User-Agent':'Mozilla/5.0'}) # If you want to access the site's data , then it's requirement is to get your real identification that's why you have to inject user-agent as header.
tables = pd.read_html(r.text)
losers = pd.DataFrame(tables[0])

losers.drop(['Volume', 'Avg Vol (3 month)', 'PE Ratio (TTM)', '52 Week Range'], axis='columns', inplace=True)
# Raname Columns
losers.columns = ['Ticker','Company Name','Price', 'Change', '% Change', 'Mkt Cap']
# Add a checkbox column
losers.insert(0, 'Select', '⬜') 


    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in losers.columns],
        data=losers.to_dict('records'),
        editable=False,
        id='table_losers',
        style_as_list_view= True,
        style_header={'backgroundColor': 'white', "font-size" : "14px", 'fontWeight': 'bold', 'textAlign': 'center'},
        is_focused=True,

        column_selectable= 'single',
        style_data_conditional=[
            {'if': {'state': 'active'},'backgroundColor': 'green', 'border': '12px solid white'},
            {'if': {'column_id': 'Select'}, 'width': 10},
            {'if': {'column_id': 'Ticker'}, 'text_align':'center', 'backgroundColor': 'green', 'width': 30, 'color': 'white', 
             'border': '12px solid white', 'letter-spacing': '3px'},
            {'if': {'column_id': 'Company Name'}, 'textAlign': 'left', 'text-indent': '10px', 'width':100},
            {'if': {'column_id': '% Change'}, 'backgroundColor': 'yellow', 'color': 'red', 'font-weight': 'bold'},
                               ],
        style_data={"font-size" : "14px", 'height': 15, "background":"white", 'border': '1px solid white'},
        fixed_rows={'headers': True}),

