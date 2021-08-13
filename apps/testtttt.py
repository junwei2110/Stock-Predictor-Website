
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from functions import time_period_annual, investment_ratios_comparison_data



api_FMP = '9986f4c3a10c45418d13105f50ee7f94'

stock = "CRSR"

# profile = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={api_FMP}').json()

# #profile_hello = pd.DataFrame(profile, index = list(range(len(profile))))
# profile_table = {}  

# profile_table["Ticker"] = [profile[0]["symbol"]]
# profile_table["Price"] = [profile[0]["price"]]
# profile_table["Beta"] = [profile[0]["beta"]]
# profile_table["Market Cap"] = [profile[0]["mktCap"]]
# profile_table["Exchange"] = [profile[0]["exchange"]]
# profile_table["Sector"] = [profile[0]["sector"]]
# profile_table["Industry"] = [profile[0]["industry"]]
# profile_table["Country of Origin"] = [profile[0]["country"]]
# profile_table["CEO"] = [profile[0]["ceo"]]
# profile_table["Description"] = [profile[0]["description"]]
# profile_table["Company Name"] = [profile[0]["companyName"]]
# profile_table["image URL"] = [profile[0]["image"]]

# profile_table = pd.DataFrame.from_dict(profile_table)
# profile_table.rename(index = {0: "Info"}, inplace = True)

# profile_table = profile_table.drop(columns = ["Company Name", "image URL", "Description"])
# profile_table = profile_table.transpose().reset_index()
# columns = [{"name": str(i), "id": str(i)} for i in profile_table.columns]
# data = profile_table.to_dict('records')


# print(len(profile_hello))
# print(len(profile_table))

# stock_prices = requests.get(
#         f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_FMP}').json()


# stock_prices_df = pd.DataFrame(stock_prices["historical"], index = list(range(len(stock_prices["historical"]))))

# print(stock_prices_df)

#print("TTM" > "20 Q1")

# print(profile_table)

# profile_table.drop(labels = ["Description", "Company Name", "image URL"], inplace = True)

# x = profile_table.to_json()
# y = json.loads(x)
# print(x)

# data = [profile_table.to_dict()]

#print(data)
# profile_table = profile_table.drop(columns = ["Description","Company Name","image URL"])
# profile_table = profile_table.set_index("date").transpose().reset_index()


x = investment_ratios_comparison_data(stock)

print(x)