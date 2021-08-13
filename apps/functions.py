import datetime
from dateutil import parser
import requests
import pandas as pd


# Input your API key
api_polygon = 'f3Ap4fklGb6p5IphyTGaJJRvLRJtQ2y1'
api_FMPC = 'f5fc1f8bd64c0288e56bb21b10840d1f'
api_FMP = '9986f4c3a10c45418d13105f50ee7f94'

##################################################################### Functions for API pulling of stock info #################################################################

def total_stock_tickers():
    list_of_tickers = []
    stock_list = requests.get(
        f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_FMP}').json()
    for tick in stock_list:
        list_of_tickers.append(tick["symbol"])
    
    return list_of_tickers



def time_period_annual(date):
    return parser.parse(date).year

def time_period_quarter(date):
    quarter_date = str(parser.parse(date).year) + " Q" + \
            str(pd.Timestamp(datetime.date(parser.parse(date).year, parser.parse(date).month, parser.parse(date).day)).quarter)
    return quarter_date 

def company_profile(stock, profile_table = {}):
    
    profile = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={api_FMP}').json()

    if len(profile) == 0:
        return pd.DataFrame()

    # You need to put ur elements into a list form so as to be able to convert it into a dataframe. Remember that for Series columns and indexes are the same
    profile_table["Ticker"] = [profile[0]["symbol"]]
    profile_table["Price"] = [profile[0]["price"]]
    profile_table["Beta"] = [profile[0]["beta"]]
    profile_table["Market Cap"] = [profile[0]["mktCap"]]
    profile_table["Exchange"] = [profile[0]["exchange"]]
    profile_table["Sector"] = [profile[0]["sector"]]
    profile_table["Industry"] = [profile[0]["industry"]]
    profile_table["Country of Origin"] = [profile[0]["country"]]
    profile_table["CEO"] = [profile[0]["ceo"]]
    profile_table["Description"] = [profile[0]["description"]]
    profile_table["Company Name"] = [profile[0]["companyName"]]
    profile_table["image URL"] = [profile[0]["image"]]

    profile_table = pd.DataFrame.from_dict(profile_table)
    profile_table.rename(index = {0: "Info"}, inplace = True)


    return profile_table


def stock_price(stock):
    
    stock_prices = requests.get(
        f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_FMP}').json()

    if len(stock_prices["historical"]) == 0:
        return pd.DataFrame()

    stock_prices_df = pd.DataFrame(stock_prices["historical"], index = list(range(len(stock_prices["historical"]))))

    return stock_prices_df


def stock_price_candle(stock):
    
    stock_prices = requests.get(
        f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?apikey={api_FMP}').json()

    if len(stock_prices["historical"]) == 0:
        return pd.DataFrame()

    stock_prices_df = pd.DataFrame(stock_prices["historical"], index = list(range(len(stock_prices["historical"]))))

    return stock_prices_df



def get_market_cap(stock):
    mktcap = requests.get(f'https://financialmodelingprep.com/api/v3/historical-market-capitalization/{stock}?apikey={api_FMP}').json()    

    return mktcap



def annual_income_statement(stock, income_sheet = pd.DataFrame()):
    
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?apikey={api_FMP}').json()

    if len(IS) == 0:
        return pd.DataFrame()

    income_sheet = pd.DataFrame(IS, index = list(range(len(IS))))
    income_sheet.drop(columns = ["reportedCurrency","fillingDate","acceptedDate","period","link", "finalLink"], inplace = True)
    income_sheet["researchExpRatio"] = income_sheet["researchAndDevelopmentExpenses"]/income_sheet["operatingExpenses"]
    income_sheet["sellingMktExpRatio"] = income_sheet["sellingAndMarketingExpenses"]/income_sheet["operatingExpenses"]
    income_sheet.date = income_sheet.date.apply(time_period_annual)
    income_sheet.reset_index(drop = True, inplace = True)

    return income_sheet

def quarter_income_statement(stock, income_sheet = pd.DataFrame()):

    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&apikey={api_FMP}').json()         
    
    if len(IS) == 0:
        return pd.DataFrame()
    
    income_sheet = pd.DataFrame(IS, index = list(range(len(IS))))
    income_sheet.drop(columns = ["reportedCurrency","fillingDate","acceptedDate","period","link", "finalLink"], inplace = True)
    income_sheet["researchExpRatio"] = income_sheet["researchAndDevelopmentExpenses"]/income_sheet["operatingExpenses"]
    income_sheet["sellingMktExpRatio"] = income_sheet["sellingAndMarketingExpenses"]/income_sheet["operatingExpenses"]
    
    income_sheet.date = income_sheet.date.apply(time_period_quarter)
    income_sheet.reset_index(drop = True, inplace = True)

    return income_sheet



def annual_balance_statement(stock, balance_ratios = pd.DataFrame()):        
    
    BS = requests.get(
            f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?apikey={api_FMP}').json()
    
    if len(BS) == 0:
        return pd.DataFrame()

    balance_ratios = pd.DataFrame(BS, index = list(range(len(BS))))
    balance_ratios.drop(columns = ["reportedCurrency","fillingDate","acceptedDate","period","link", "finalLink"], inplace = True)
    # Assets Ratios
    balance_ratios["totalCurrentAssetsRatio"] = balance_ratios["totalCurrentAssets"]/balance_ratios["totalAssets"]
    balance_ratios["cashAndCashEquivalentsRatio"] = balance_ratios["cashAndCashEquivalents"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["shortTermInvestmentsRatio"] = balance_ratios["shortTermInvestments"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["netReceivablesRatio"] = balance_ratios["netReceivables"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["inventoryRatio"] = balance_ratios["inventory"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["propertyPlantEquipmentNetRatio"] = balance_ratios["propertyPlantEquipmentNet"]/balance_ratios["totalNonCurrentAssets"]
    balance_ratios["goodwillAndIntangibleAssetsRatio"] = balance_ratios["goodwillAndIntangibleAssets"]/balance_ratios["totalNonCurrentAssets"]
    balance_ratios["longTermInvestmentsRatio"] = balance_ratios["longTermInvestments"]/balance_ratios["totalNonCurrentAssets"]
    # Liabilities Ratios
    balance_ratios["totalCurrentLiabilitiesRatio"] = balance_ratios["totalCurrentLiabilities"]/balance_ratios["totalLiabilities"]
    balance_ratios["accountPayablesRatio"] = balance_ratios["accountPayables"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["shortTermDebtRatio"] = balance_ratios["shortTermDebt"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["deferredRevenueRatio"] = balance_ratios["deferredRevenue"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["longTermDebtRatio"] = balance_ratios["longTermDebt"]/balance_ratios["totalNonCurrentLiabilities"]
    balance_ratios["deferredRevenueNonCurrentRatio"] = balance_ratios["deferredRevenueNonCurrent"]/balance_ratios["totalNonCurrentLiabilities"]
    balance_ratios["deferredTaxLiabilitiesNonCurrentRatio"] = balance_ratios["deferredTaxLiabilitiesNonCurrent"]/balance_ratios["totalNonCurrentLiabilities"]
    # Equities Ratios
    balance_ratios["commonStockRatio"] = balance_ratios["commonStock"]/balance_ratios["totalStockholdersEquity"]
    balance_ratios["retainedEarningsRatio"] = balance_ratios["retainedEarnings"]/balance_ratios["totalStockholdersEquity"]
    # Liquidity Ratios
    balance_ratios["currentRatio"] = balance_ratios["totalCurrentAssets"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["quickRatio"] = (balance_ratios["cashAndShortTermInvestments"]+balance_ratios["netReceivables"])/balance_ratios["totalCurrentLiabilities"]
    # Solvency Ratios
    balance_ratios["debtToEquityRatio"] = balance_ratios["totalLiabilities"]/balance_ratios["totalStockholdersEquity"]
    balance_ratios["debtToAssetsRatio"] = balance_ratios["totalLiabilities"]/balance_ratios["totalAssets"]    
    
    balance_ratios.date = balance_ratios.date.apply(time_period_annual)
    balance_ratios.reset_index(drop = True, inplace = True)

    return balance_ratios


def quarter_balance_statement(stock, balance_ratios = pd.DataFrame()):        
    
    BS = requests.get(
            f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=quarter&apikey={api_FMP}').json()
    
    if len(BS) == 0:
        return pd.DataFrame()

    # for order in range(len(BS)):
    #     balance_ratios = pd.concat([balance_ratios, pd.DataFrame(BS[order], index = [order])])
    balance_ratios = pd.DataFrame(BS, index = list(range(len(BS))))
    balance_ratios.drop(columns = ["reportedCurrency","fillingDate","acceptedDate","period","link", "finalLink"], inplace = True)
    # Assets Ratios
    balance_ratios["totalCurrentAssetsRatio"] = balance_ratios["totalCurrentAssets"]/balance_ratios["totalAssets"]
    balance_ratios["cashAndCashEquivalentsRatio"] = balance_ratios["cashAndCashEquivalents"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["shortTermInvestmentsRatio"] = balance_ratios["shortTermInvestments"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["netReceivablesRatio"] = balance_ratios["netReceivables"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["inventoryRatio"] = balance_ratios["inventory"]/balance_ratios["totalCurrentAssets"]
    balance_ratios["propertyPlantEquipmentNetRatio"] = balance_ratios["propertyPlantEquipmentNet"]/balance_ratios["totalNonCurrentAssets"]
    balance_ratios["goodwillAndIntangibleAssetsRatio"] = balance_ratios["goodwillAndIntangibleAssets"]/balance_ratios["totalNonCurrentAssets"]
    balance_ratios["longTermInvestmentsRatio"] = balance_ratios["longTermInvestments"]/balance_ratios["totalNonCurrentAssets"]
    # Liabilities Ratios
    balance_ratios["totalCurrentLiabilitiesRatio"] = balance_ratios["totalCurrentLiabilities"]/balance_ratios["totalLiabilities"]
    balance_ratios["accountPayablesRatio"] = balance_ratios["accountPayables"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["shortTermDebtRatio"] = balance_ratios["shortTermDebt"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["deferredRevenueRatio"] = balance_ratios["deferredRevenue"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["longTermDebtRatio"] = balance_ratios["longTermDebt"]/balance_ratios["totalNonCurrentLiabilities"]
    balance_ratios["deferredRevenueNonCurrentRatio"] = balance_ratios["deferredRevenueNonCurrent"]/balance_ratios["totalNonCurrentLiabilities"]
    balance_ratios["deferredTaxLiabilitiesNonCurrentRatio"] = balance_ratios["deferredTaxLiabilitiesNonCurrent"]/balance_ratios["totalNonCurrentLiabilities"]
    # Equities Ratios
    balance_ratios["commonStockRatio"] = balance_ratios["commonStock"]/balance_ratios["totalStockholdersEquity"]
    balance_ratios["retainedEarningsRatio"] = balance_ratios["retainedEarnings"]/balance_ratios["totalStockholdersEquity"]
    # Liquidity Ratios
    balance_ratios["currentRatio"] = balance_ratios["totalCurrentAssets"]/balance_ratios["totalCurrentLiabilities"]
    balance_ratios["quickRatio"] = (balance_ratios["cashAndShortTermInvestments"]+balance_ratios["netReceivables"])/balance_ratios["totalCurrentLiabilities"]
    # Solvency Ratios
    balance_ratios["debtToEquityRatio"] = balance_ratios["totalLiabilities"]/balance_ratios["totalStockholdersEquity"]
    balance_ratios["debtToAssetsRatio"] = balance_ratios["totalLiabilities"]/balance_ratios["totalAssets"]    
    
    balance_ratios.date = balance_ratios.date.apply(time_period_quarter)
    balance_ratios.reset_index(drop = True, inplace = True)

    return balance_ratios



def annual_CF_statement(stock, cashflow_ratios = pd.DataFrame()):        

    CF = requests.get(
            f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?apikey={api_FMP}').json()
    
    if len(CF) == 0:
        return pd.DataFrame()

    cashflow_ratios = pd.DataFrame(CF, index = list(range(len(CF))))
    cashflow_ratios.drop(columns = ["reportedCurrency","fillingDate","acceptedDate","period","link", "finalLink"], inplace = True)
    # Operating Cash Flow Ratio
    cashflow_ratios["netIncometoCashflowRatio"] = cashflow_ratios["netIncome"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["deprectoCashflowRatio"] = cashflow_ratios["depreciationAndAmortization"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["deferIncomeTaxRatio"] = cashflow_ratios["deferredIncomeTax"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["stockCompenseRatio"] = cashflow_ratios["stockBasedCompensation"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["accountsReceivableRatio"] = cashflow_ratios["accountsReceivables"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["inventoryRatio"] = cashflow_ratios["inventory"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["accountsPayablesRatio"] = cashflow_ratios["accountsPayables"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    # Investing Cash Flow Ratio
    cashflow_ratios["PPERatio"] = cashflow_ratios["investmentsInPropertyPlantAndEquipment"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    cashflow_ratios["acquisitionRatio"] = cashflow_ratios["acquisitionsNet"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    cashflow_ratios["investmentPurchaseRatio"] = cashflow_ratios["purchasesOfInvestments"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    cashflow_ratios["salesMaturityInvestmentRatio"] = cashflow_ratios["salesMaturitiesOfInvestments"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    # Financial Cash Flow Ratio
    cashflow_ratios["debtRepaymentRatio"] = cashflow_ratios["debtRepayment"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]
    cashflow_ratios["stockIssueRatio"] = cashflow_ratios["commonStockIssued"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]
    cashflow_ratios["stockRepurchaseRatio"] = cashflow_ratios["commonStockRepurchased"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]
    cashflow_ratios["dividendsPaidRatio"] = cashflow_ratios["dividendsPaid"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]

    cashflow_ratios.date = cashflow_ratios.date.apply(time_period_annual)
    cashflow_ratios.reset_index(drop = True, inplace = True)

    return cashflow_ratios

def quarter_CF_statement(stock, cashflow_ratios = pd.DataFrame()):        

    CF = requests.get(
            f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?period=quarter&apikey={api_FMP}').json()
    
    if len(CF) == 0:
        return pd.DataFrame()

    cashflow_ratios = pd.DataFrame(CF, index = list(range(len(CF))))
    cashflow_ratios.drop(columns = ["reportedCurrency","fillingDate","acceptedDate","period","link", "finalLink"], inplace = True)
    # Operating Cash Flow Ratio
    cashflow_ratios["netIncometoCashflowRatio"] = cashflow_ratios["netIncome"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["deprectoCashflowRatio"] = cashflow_ratios["depreciationAndAmortization"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["deferIncomeTaxRatio"] = cashflow_ratios["deferredIncomeTax"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["stockCompenseRatio"] = cashflow_ratios["stockBasedCompensation"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["accountsReceivableRatio"] = cashflow_ratios["accountsReceivables"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["inventoryRatio"] = cashflow_ratios["inventory"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    cashflow_ratios["accountsPayablesRatio"] = cashflow_ratios["accountsPayables"]/cashflow_ratios["netCashProvidedByOperatingActivities"]
    # Investing Cash Flow Ratio
    cashflow_ratios["PPERatio"] = cashflow_ratios["investmentsInPropertyPlantAndEquipment"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    cashflow_ratios["acquisitionRatio"] = cashflow_ratios["acquisitionsNet"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    cashflow_ratios["investmentPurchaseRatio"] = cashflow_ratios["purchasesOfInvestments"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    cashflow_ratios["salesMaturityInvestmentRatio"] = cashflow_ratios["salesMaturitiesOfInvestments"]/cashflow_ratios["netCashUsedForInvestingActivites"]
    # Financial Cash Flow Ratio
    cashflow_ratios["debtRepaymentRatio"] = cashflow_ratios["debtRepayment"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]
    cashflow_ratios["stockIssueRatio"] = cashflow_ratios["commonStockIssued"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]
    cashflow_ratios["stockRepurchaseRatio"] = cashflow_ratios["commonStockRepurchased"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]
    cashflow_ratios["dividendsPaidRatio"] = cashflow_ratios["dividendsPaid"]/cashflow_ratios["netCashUsedProvidedByFinancingActivities"]

    cashflow_ratios.date = cashflow_ratios.date.apply(time_period_quarter)
    cashflow_ratios.reset_index(drop = True, inplace = True)

    return cashflow_ratios


def single_ticker_fin_ratio_annual(stock, fin_ratios = pd.DataFrame()):        

    FR = requests.get(
            f'https://financialmodelingprep.com/api/v3/ratios/{stock}?apikey={api_FMP}').json()
    
    if len(FR) == 0:
        return pd.DataFrame()


    fin_ratios = pd.DataFrame(FR, index = list(range(len(FR))))
    
    fin_ratios.date = fin_ratios.date.apply(time_period_annual)

    return fin_ratios


def single_ticker_growth_ratio_annual(stock, growth_ratios = pd.DataFrame()):        

    FG = requests.get(
            f'https://financialmodelingprep.com/api/v3/financial-growth/{stock}?apikey={api_FMP}').json()
    
    if len(FG) == 0:
        return pd.DataFrame()

    
    growth_ratios = pd.DataFrame(FG, index = list(range(len(FG))))
    growth_ratios.date = growth_ratios.date.apply(time_period_annual)
    
    return growth_ratios


def single_ticker_fin_ratio_quarter(stock, fin_ratios = pd.DataFrame()):        

    FR = requests.get(
            f'https://financialmodelingprep.com/api/v3/ratios/{stock}?period=quarter&apikey={api_FMP}').json()
    
    if len(FR) == 0:
        return pd.DataFrame()

    fin_ratios = pd.DataFrame(FR, index = list(range(len(FR))))
    
    fin_ratios.date = fin_ratios.date.apply(time_period_quarter)

    return fin_ratios


def single_ticker_growth_ratio_quarter(stock, growth_ratios = pd.DataFrame()):        

    FG = requests.get(
            f'https://financialmodelingprep.com/api/v3/financial-growth/{stock}?period=quarter&apikey={api_FMP}').json()

    if len(FG) == 0:
        return pd.DataFrame()

    growth_ratios = pd.DataFrame(FG, index = list(range(len(FG))))
    growth_ratios.date = growth_ratios.date.apply(time_period_quarter)

    return growth_ratios

def single_ticker_ratio_TTM(stock, TTM_ratios = pd.DataFrame()):        

    TTM = requests.get(
            f'https://financialmodelingprep.com/api/v3/ratios-ttm/{stock}?apikey={api_FMP}').json()

    if len(TTM) == 0:
        return pd.DataFrame()

    TTM_ratios = pd.DataFrame(TTM, index = list(range(len(TTM))))

    return TTM_ratios



##################################################################### Functions for Financial Statements #################################################################
def profile_datatable(profile_table):
    if len(profile_table) == 0:
        return [], []

    profile_table = profile_table.drop(columns = ["Company Name", "image URL", "Description"])
    profile_table = profile_table.transpose().reset_index()
    columns = [{"name": str(i), "id": str(i)} for i in profile_table.columns]
    data = profile_table.to_dict('records')

    return columns, data    


def liquidity_solvency_summary_table(ratios_sheet):
    if len(ratios_sheet) == 0:
        return [], []

    if len(ratios_sheet["date"]) > 5:
        current_ratio_col = [ratios_sheet["currentRatio"][0], ratios_sheet["currentRatio"][4], ratios_sheet["currentRatio"][1]]
        debt_ratio_col = [ratios_sheet["debtRatio"][0], ratios_sheet["debtRatio"][4], ratios_sheet["debtRatio"][1]]
        debt_equity_ratio_col = [ratios_sheet["debtEquityRatio"][0], ratios_sheet["debtEquityRatio"][4], ratios_sheet["debtEquityRatio"][1]]
    elif len(ratios_sheet["date"]) > 1:
        current_ratio_col = [ratios_sheet["currentRatio"][0], "NA", ratios_sheet["currentRatio"][1]]
        debt_ratio_col = [ratios_sheet["debtRatio"][0], "NA", ratios_sheet["debtRatio"][1]]
        debt_equity_ratio_col = [ratios_sheet["debtEquityRatio"][0], "NA", ratios_sheet["debtEquityRatio"][1]]
    elif len(ratios_sheet["date"]) == 1:
        current_ratio_col = [ratios_sheet["currentRatio"][0], "NA", "NA"]
        debt_ratio_col = [ratios_sheet["debtRatio"][0], "NA", "NA"]
        debt_equity_ratio_col = [ratios_sheet["debtEquityRatio"][0], "NA", "NA"]
    elif len(ratios_sheet["date"]) == 0:
        current_ratio_col = ["NA", "NA", "NA"]
        debt_ratio_col = ["NA", "NA", "NA"]
        debt_equity_ratio_col = ["NA", "NA", "NA"]
    
    column_index = ["Current Quarter", "Same Qtr Last Year", "Last Quarter"]
    liq_sol_table = pd.DataFrame({"Last Reported": column_index, "Current Ratio": current_ratio_col,"Debt Ratio": debt_ratio_col, "Debt-to-Equity Ratio": debt_equity_ratio_col })
    columns = [{"name": str(i), "id": str(i)} for i in liq_sol_table.columns]
    data = liq_sol_table.to_dict('records')
    
    return columns, data

def growth_ratios_summary_table(income_sheet_Q, CF_sheet_Q, income_sheet_A, CF_sheet_A):
    if (len(income_sheet_Q) == 0) | (len(CF_sheet_Q) == 0) | (len(income_sheet_A) == 0) | (len(CF_sheet_A) == 0):
        return [], []

    RG = ["NA", "NA", "NA"]
    FCFG = ["NA", "NA", "NA"]
    OpInG = ["NA", "NA", "NA"]

    if len(income_sheet_Q["date"]) > 7:
        revenue_current_TTM = sum(income_sheet_Q["revenue"][0:4])
        revenue_lastyr_TTM = sum(income_sheet_Q["revenue"][4:8])
        revenue_growth_TTM = ((revenue_current_TTM - revenue_lastyr_TTM)/revenue_lastyr_TTM) * 100
        Opincome_current_TTM = sum(income_sheet_Q["operatingIncome"][0:4])
        Opincome_lastyr_TTM = sum(income_sheet_Q["operatingIncome"][4:8])
        Opincome_growth_TTM = ((Opincome_current_TTM - Opincome_lastyr_TTM)/Opincome_lastyr_TTM) * 100
        RG[0] = revenue_growth_TTM
        OpInG[0] = Opincome_growth_TTM

    if len(CF_sheet_Q["date"]) > 7:
        CF_current_TTM = sum(CF_sheet_Q["freeCashFlow"][0:4])
        CF_lastyr_TTM = sum(CF_sheet_Q["freeCashFlow"][4:8])
        CF_growth_TTM = ((CF_current_TTM - CF_lastyr_TTM)/CF_lastyr_TTM) * 100
        FCFG[0] = CF_growth_TTM
    
    if len(income_sheet_A["date"]) > 1:
        revenue_growth_last_annual = ((income_sheet_A["revenue"][0] - income_sheet_A["revenue"][1])/income_sheet_A["revenue"][1]) * 100
        OpIn_growth_last_annual = ((income_sheet_A["operatingIncome"][0] - income_sheet_A["operatingIncome"][1])/income_sheet_A["operatingIncome"][1]) * 100
        RG[1] = revenue_growth_last_annual
        OpInG[1] = OpIn_growth_last_annual

    if len(CF_sheet_A["date"]) > 1:
        CF_growth_last_annual = ((CF_sheet_A["freeCashFlow"][0] - CF_sheet_A["freeCashFlow"][1])/CF_sheet_A["freeCashFlow"][1]) * 100
        FCFG[1] = CF_growth_last_annual
    
    if len(income_sheet_A["date"]) > 3:
        if (income_sheet_A["revenue"][0] > 0) & (income_sheet_A["revenue"][3] > 0):
            revenue_growth_CAGR = ((((income_sheet_A["revenue"][0]/income_sheet_A["revenue"][3]))**(1/3)) -1) * 100
            RG[2] = revenue_growth_CAGR
        else:
            RG[2] = "NA"

        if (income_sheet_A["operatingIncome"][0] > 0) & (income_sheet_A["operatingIncome"][3] > 0):
            OpIn_growth_CAGR = ((((income_sheet_A["operatingIncome"][0]/income_sheet_A["operatingIncome"][3]))**(1/3)) -1) * 100
            OpInG[2] = OpIn_growth_CAGR
        else:
            OpInG[2] = "NA"
    
    if len(CF_sheet_A["date"]) > 3:
        if (CF_sheet_A["freeCashFlow"][0] > 0) & (CF_sheet_A["freeCashFlow"][3] > 0):
            CF_growth_CAGR = ((((CF_sheet_A["freeCashFlow"][0]/CF_sheet_A["freeCashFlow"][3]))**(1/3)) -1) * 100
            FCFG[2] = CF_growth_CAGR
        else:
            FCFG[2] = "NA"

    column_index = ["Current Quarter-TTM", "Current Annual Report", "CAGR-3 years"]
    growth_ratios_summary_table = pd.DataFrame({"Last Reported": column_index, "Revenue Growth": RG,"FCF Growth": FCFG, "Operating Income Growth": OpInG })
    columns = [{"name": str(i), "id": str(i)} for i in growth_ratios_summary_table.columns]
    data = growth_ratios_summary_table.to_dict('records')
    
    return columns, data


def profit_ratios_summary_table(income_sheet_Q, balance_sheet_Q):
    if (len(income_sheet_Q) == 0) | (len(balance_sheet_Q) == 0):
        return [], []

    ROE = ["NA", "NA", "NA"]
    ROA = ["NA", "NA", "NA"]
    ROCE = ["NA", "NA", "NA"]

    if len(income_sheet_Q["date"]) > 8:
        netIncome_current_TTM = sum(income_sheet_Q["netIncome"][0:4])
        netIncome_lastqtr_TTM = sum(income_sheet_Q["netIncome"][1:5])
        netIncome_lastyr_TTM = sum(income_sheet_Q["netIncome"][4:8])

        ROE_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalStockholdersEquity"][0]) * 100
        ROE_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalStockholdersEquity"][1]) * 100
        ROE_lastyr_TTM = (netIncome_lastyr_TTM/balance_sheet_Q["totalStockholdersEquity"][4]) * 100
        ROE[0] = ROE_current_TTM
        ROE[1] = ROE_lastqtr_TTM
        ROE[2] = ROE_lastyr_TTM

        ROA_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalAssets"][0]) * 100
        ROA_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalAssets"][1]) * 100
        ROA_lastyr_TTM = (netIncome_lastyr_TTM/balance_sheet_Q["totalAssets"][4]) * 100
        ROA[0] = ROA_current_TTM
        ROA[1] = ROA_lastqtr_TTM
        ROA[2] = ROA_lastyr_TTM

        ROCE_current_TTM = (netIncome_current_TTM/(balance_sheet_Q["totalAssets"][0] - balance_sheet_Q["totalCurrentLiabilities"][0])) * 100
        ROCE_lastqtr_TTM = (netIncome_lastqtr_TTM/(balance_sheet_Q["totalAssets"][1] - balance_sheet_Q["totalCurrentLiabilities"][1])) * 100
        ROCE_lastyr_TTM = (netIncome_lastyr_TTM/(balance_sheet_Q["totalAssets"][4] - balance_sheet_Q["totalCurrentLiabilities"][4])) * 100
        ROCE[0] = ROCE_current_TTM
        ROCE[1] = ROCE_lastqtr_TTM
        ROCE[2] = ROCE_lastyr_TTM

    
    if len(income_sheet_Q["date"]) > 4:
        netIncome_current_TTM = sum(income_sheet_Q["netIncome"][0:4])
        netIncome_lastqtr_TTM = sum(income_sheet_Q["netIncome"][1:5])

        ROE_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalStockholdersEquity"][0]) * 100
        ROE_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalStockholdersEquity"][1]) * 100
        ROE[0] = ROE_current_TTM
        ROE[1] = ROE_lastqtr_TTM


        ROA_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalAssets"][0]) * 100
        ROA_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalAssets"][1]) * 100
        ROA[0] = ROA_current_TTM
        ROA[1] = ROA_lastqtr_TTM

        ROCE_current_TTM = (netIncome_current_TTM/(balance_sheet_Q["totalAssets"][0] - balance_sheet_Q["totalCurrentLiabilities"][0])) * 100
        ROCE_lastqtr_TTM = (netIncome_lastqtr_TTM/(balance_sheet_Q["totalAssets"][1] - balance_sheet_Q["totalCurrentLiabilities"][1])) * 100
        ROCE[0] = ROCE_current_TTM
        ROCE[1] = ROCE_lastqtr_TTM


    column_index = ["Current Quarter-TTM", "Last Quarter-TTM", "Last Year-TTM"]
    profit_ratios_summary_table = pd.DataFrame({"Last Reported": column_index, "ROE": ROE,"ROA": ROA, "ROCE": ROCE })
    columns = [{"name": str(i), "id": str(i)} for i in profit_ratios_summary_table.columns]
    data = profit_ratios_summary_table.to_dict('records')
    
    return columns, data


def investment_ratios_summary_table(TTM_ratios, ratios_A):
    if (len(TTM_ratios) == 0) | (len(ratios_A) == 0):
        return [], []

    PE = ["NA", "NA", "NA"]
    PS = ["NA", "NA", "NA"]
    PBV = ["NA", "NA", "NA"]
    PFCF = ["NA", "NA", "NA"]

    if len(ratios_A["date"]) > 1:
        PE[0] = TTM_ratios["priceEarningsRatioTTM"][0]
        PE[1] = ratios_A["priceEarningsRatio"][0]
        PE[2] = ratios_A["priceEarningsRatio"][1]

        PS[0] = TTM_ratios["priceToSalesRatioTTM"][0]
        PS[1] = ratios_A["priceToSalesRatio"][0]
        PS[2] = ratios_A["priceToSalesRatio"][1]

        PBV[0] = TTM_ratios["priceToBookRatioTTM"][0]
        PBV[1] = ratios_A["priceToBookRatio"][0]
        PBV[2] = ratios_A["priceToBookRatio"][1]

        PFCF[0] = TTM_ratios["priceToFreeCashFlowsRatioTTM"][0]
        PFCF[1] = ratios_A["priceToFreeCashFlowsRatio"][0]
        PFCF[2] = ratios_A["priceToFreeCashFlowsRatio"][1]

    else:
        PE[0] = TTM_ratios["priceEarningsRatioTTM"][0]
        PE[1] = ratios_A["priceEarningsRatio"][0]

        PS[0] = TTM_ratios["priceToSalesRatioTTM"][0]
        PS[1] = ratios_A["priceToSalesRatio"][0]

        PBV[0] = TTM_ratios["priceToBookRatioTTM"][0]
        PBV[1] = ratios_A["priceToBookRatio"][0]

        PFCF[0] = TTM_ratios["priceToFreeCashFlowsRatioTTM"][0]
        PFCF[1] = ratios_A["priceToFreeCashFlowsRatio"][0]


    column_index = ["Current Quarter-TTM", "Current Annual Report", "Last Year Annual Report"]
    investment_ratios_summary_table = pd.DataFrame({"Last Reported": column_index, "Price-to-Earnings": PE,"Price-to-Sales": PS, "Price-to-Bookvalue": PBV, "Price-to-FreeCashFlow": PFCF })
    columns = [{"name": str(i), "id": str(i)} for i in investment_ratios_summary_table.columns]
    data = investment_ratios_summary_table.to_dict('records')
    
    return columns, data




def IS_datatable(income_table):
    income_table = income_table.drop(columns = ["symbol","generalAndAdministrativeExpenses","sellingAndMarketingExpenses","costAndExpenses","totalOtherIncomeExpensesNet", 
    "incomeBeforeTaxRatio", "weightedAverageShsOut", "weightedAverageShsOutDil", "researchExpRatio", "sellingMktExpRatio"]) # These columns are deemed unnecessary
    income_table = income_table.set_index("date").transpose().reset_index() # Set index to date so that when you transpose, date is at the top. You reset index to get the headings back as a column
    income_columns = [{"name": str(i), "id": str(i)} for i in income_table.columns]
    data = income_table.to_dict('records')

    return income_columns, data

def BS_datatable(balance_table):
    balance_table = balance_table.drop(columns = ["symbol","cashAndShortTermInvestments","otherCurrentAssets", "goodwillAndIntangibleAssets",
    "taxAssets","otherNonCurrentAssets", "otherAssets", "taxPayables", "otherCurrentLiabilities","otherNonCurrentLiabilities", "otherLiabilities", 
    "accumulatedOtherComprehensiveIncomeLoss", "othertotalStockholdersEquity", "netDebt",
    "totalCurrentAssetsRatio", "cashAndCashEquivalentsRatio", "shortTermInvestmentsRatio",
    "netReceivablesRatio", "inventoryRatio", "propertyPlantEquipmentNetRatio", "goodwillAndIntangibleAssetsRatio",
    "longTermInvestmentsRatio", "totalCurrentLiabilitiesRatio", "accountPayablesRatio",
    "shortTermDebtRatio", "deferredRevenueRatio", "longTermDebtRatio", "deferredRevenueNonCurrentRatio",
    "deferredTaxLiabilitiesNonCurrentRatio", "commonStockRatio", "retainedEarningsRatio", "currentRatio",
     "quickRatio", "debtToEquityRatio", "debtToAssetsRatio"]) # These columns are deemed unnecessary
    balance_table = balance_table.set_index("date").transpose().reset_index() # Set index to date so that when you transpose, date is at the top. You reset index to get the headings back as a column
    balance_columns = [{"name": str(i), "id": str(i)} for i in balance_table.columns]
    data = balance_table.to_dict('records')

    return balance_columns, data


def CF_datatable(cashflow_table):
    #cashflow_table = cashflow_table.drop(cashflow_table.columns[0], axis = 1) # 1st column is your previous index (0,1,2,3...) - drop it to make date column in front
    cashflow_table = cashflow_table.drop(columns = ["symbol","changeInWorkingCapital","otherWorkingCapital",
    "netIncometoCashflowRatio", "deprectoCashflowRatio", "deferIncomeTaxRatio", "stockCompenseRatio",
    "accountsReceivableRatio", "inventoryRatio", "accountsPayablesRatio", "PPERatio",
    "acquisitionRatio", "investmentPurchaseRatio", "salesMaturityInvestmentRatio", "debtRepaymentRatio",
    "stockIssueRatio", "stockRepurchaseRatio", "dividendsPaidRatio"]) # These columns are deemed unnecessary
    cashflow_table = cashflow_table.set_index("date").transpose().reset_index() # Set index to date so that when you transpose, date is at the top. You reset index to get the headings back as a column
    cashflow_columns = [{"name": str(i), "id": str(i)} for i in cashflow_table.columns]
    data = cashflow_table.to_dict('records')

    return cashflow_columns, data

def CF_waterfall(waterfall_df, cashflow_dff):
    waterfall_df = waterfall_df.rename(columns = {"cashAtEndOfPeriod":"Final Amount", "operatingCashFlow":"Cash Operations", "netCashUsedForInvestingActivites": "Cash Investments", 
    "netCashUsedProvidedByFinancingActivities": "Cash Financials"}) # Rename them to alphabetical order to meet the waterfall chart requirements
    waterfall_df["Final Amount"] = None # All the final amounts will be auto calculated by the waterfall formula
    waterfall_df = pd.melt(waterfall_df, id_vars = ["date"], value_vars = ["Final Amount", "Cash Operations", "Cash Investments", "Cash Financials"], 
    var_name = "waterfall_parameters", value_name = "waterfall_val") # Create a dataframe with the columns date, waterfall_parameters and waterfall_val
    waterfall_df.sort_values(by = ["date", "waterfall_parameters"], ascending = True, inplace = True) # Sort the values in ascending order to meet waterfall chart requirements

    measure_list = [] # Create the measure list, where all the year ending quantities are labelled as total and all the changes are labelled as relative
    for i in range(len(waterfall_df["date"])):
        if waterfall_df["waterfall_parameters"][i] == "Final Amount":
            measure_list.append("total")
        else:
            measure_list.append("relative")
    waterfall_df["measure"] = pd.Series(measure_list)

    waterfall_df = waterfall_df.reset_index().drop(columns = ["index"]) # Reset the index after sorting to reorganise the index

    begin = int(cashflow_dff['cashAtBeginningOfPeriod'].where(cashflow_dff['date'] == waterfall_df["date"][0]).sum()) # Create a beginning quantity, that is where the waterfall starts

    beginning_cash = pd.DataFrame([[waterfall_df["date"][0], "Beginning", begin, "absolute"]], columns=["date", "waterfall_parameters", "waterfall_val", "measure"], index=['beg'])
    waterfall_df = beginning_cash.append(waterfall_df) # Final dataframe starts from the beginning, then goes into all the relative quantities (Op CF, Invest CF, Fin CF) then go to final amounts


    return waterfall_df



##################################################################### Functions for Stock Screeners #################################################################

def stock_peers(stock):
    similarstocks = requests.get(
        f'https://financialmodelingprep.com/api/v4/stock_peers?symbol={stock}&apikey={api_FMP}').json()

    # Add in the failsafe
    if len(similarstocks) == 0:
        return pd.DataFrame() 

    stock_list = requests.get(
        f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_FMP}').json()

    peer_list = []
    peer_names = []

    for i in range(len(similarstocks)):
        for stock in similarstocks[i]["peersList"]:
            peer_list.append(stock)

            for j in range(len(stock_list)):
                if stock_list[j]["symbol"] == stock:
                    peer_names.append(stock_list[j]["name"])
                    break
                elif j == len(stock_list) - 1:
                    peer_names.append("No name")

    peer_dict = {'Ticker': peer_list, 'Company Name': peer_names}
    peer_dataframe = pd.DataFrame(peer_dict)
    # Add a checkbox column
    peer_dataframe.insert(len(peer_dataframe.columns), 'Analysis', '⬜')
    peer_dataframe.insert(len(peer_dataframe.columns), 'Add for Comparison', '⬜') 
    
    return peer_dataframe




def input_parameters_peers(capvalue, sector_val):
    if capvalue == "200000000000":
        figure1 = f"marketCapMoreThan={capvalue}"
        figure2 = ""
    elif capvalue == "50000000":
        figure1 = f"marketCapLowerThan={capvalue}"
        figure2 = ""
    else:
        values = capvalue.split(", ")
        figure1 = f"marketCapMoreThan={values[0]}"
        figure2 = f"&marketCapLowerThan={values[1]}"


    figure3 = f"&sector={sector_val}"


    similarstocks = requests.get(
         f'https://financialmodelingprep.com/api/v3/stock-screener?{figure1}{figure2}{figure3}&exchange=NASDAQ,NYSE,AMEX&apikey={api_FMP}').json()

    # Add in the failsafe
    if len(similarstocks) == 0:
        return pd.DataFrame() 


    peer_list = []
    peer_names = []
    peer_mktcap = []
    peer_sector = []

    for i in range(len(similarstocks)):
        peer_list.append(similarstocks[i]["symbol"])
        peer_names.append(similarstocks[i]["companyName"])
        peer_mktcap.append(similarstocks[i]["marketCap"]/1000000)
        peer_sector.append(similarstocks[i]["sector"])


    peer_dict = {'Ticker': peer_list, 'Company Name': peer_names, "Market Cap (M)": peer_mktcap, "Sector": peer_sector}
    peer_dataframe = pd.DataFrame(peer_dict)
    # Add a checkbox column
    peer_dataframe.insert(len(peer_dataframe.columns), 'Analysis', '⬜')
    peer_dataframe.insert(len(peer_dataframe.columns), 'Add for Comparison', '⬜') 
    
    return peer_dataframe


############################################################### Functions for comparison charts ############################################################################

def liquidity_solvency_comparison_data(stock):        

    FR = requests.get(
            f'https://financialmodelingprep.com/api/v3/ratios/{stock}?period=quarter&apikey={api_FMP}').json()
    
    if len(FR) == 0:
        return pd.DataFrame()

    ratios_sheet = pd.DataFrame(FR, index = list(range(len(FR))))
    ratios_sheet.date = ratios_sheet.date.apply(time_period_quarter)

    if len(ratios_sheet["date"]) > 5:
        current_ratio_col = [ratios_sheet["currentRatio"][0], ratios_sheet["currentRatio"][4], ratios_sheet["currentRatio"][1]]
        debt_ratio_col = [ratios_sheet["debtRatio"][0], ratios_sheet["debtRatio"][4], ratios_sheet["debtRatio"][1]]
        debt_equity_ratio_col = [ratios_sheet["debtEquityRatio"][0], ratios_sheet["debtEquityRatio"][4], ratios_sheet["debtEquityRatio"][1]]
    elif len(ratios_sheet["date"]) > 1:
        current_ratio_col = [ratios_sheet["currentRatio"][0], "NA", ratios_sheet["currentRatio"][1]]
        debt_ratio_col = [ratios_sheet["debtRatio"][0], "NA", ratios_sheet["debtRatio"][1]]
        debt_equity_ratio_col = [ratios_sheet["debtEquityRatio"][0], "NA", ratios_sheet["debtEquityRatio"][1]]
    elif len(ratios_sheet["date"]) == 1:
        current_ratio_col = [ratios_sheet["currentRatio"][0], "NA", "NA"]
        debt_ratio_col = [ratios_sheet["debtRatio"][0], "NA", "NA"]
        debt_equity_ratio_col = [ratios_sheet["debtEquityRatio"][0], "NA", "NA"]
    elif len(ratios_sheet["date"]) == 0:
        current_ratio_col = ["NA", "NA", "NA"]
        debt_ratio_col = ["NA", "NA", "NA"]
        debt_equity_ratio_col = ["NA", "NA", "NA"]
     
    column_index = ["Current Quarter", "Same Qtr Last Year", "Last Quarter"]
    stock_list = [stock, stock, stock]
    liq_sol_data = pd.DataFrame({"Last Reported": column_index, "symbol": stock_list, "Current Ratio": current_ratio_col,"Debt Ratio": debt_ratio_col, "Debt-to-Equity Ratio": debt_equity_ratio_col })
    
    return liq_sol_data



def growth_ratios_comparison_data(stock):
    
    ISA = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?apikey={api_FMP}').json()


    ISQ = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&apikey={api_FMP}').json()         
        

    CFA = requests.get(
            f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?apikey={api_FMP}').json()
    
    CFQ = requests.get(
            f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?period=quarter&apikey={api_FMP}').json()


    if (len(ISA) == 0) | (len(ISQ) == 0) | (len(CFA) == 0) | (len(CFQ) == 0):
        return pd.DataFrame()


    income_sheet_A = pd.DataFrame(ISA, index = list(range(len(ISA))))
    income_sheet_A.date = income_sheet_A.date.apply(time_period_annual)
    income_sheet_Q = pd.DataFrame(ISQ, index = list(range(len(ISQ))))
    income_sheet_Q.date = income_sheet_Q.date.apply(time_period_quarter)
    CF_sheet_A = pd.DataFrame(CFA, index = list(range(len(CFA))))
    CF_sheet_A.date = CF_sheet_A.date.apply(time_period_annual)
    CF_sheet_Q = pd.DataFrame(CFQ, index = list(range(len(CFQ))))
    CF_sheet_Q.date = CF_sheet_Q.date.apply(time_period_quarter)


    RG = ["NA", "NA", "NA"]
    FCFG = ["NA", "NA", "NA"]
    OpInG = ["NA", "NA", "NA"]

    if len(income_sheet_Q["date"]) > 7:
        revenue_current_TTM = sum(income_sheet_Q["revenue"][0:4])
        revenue_lastyr_TTM = sum(income_sheet_Q["revenue"][4:8])
        revenue_growth_TTM = ((revenue_current_TTM - revenue_lastyr_TTM)/revenue_lastyr_TTM) * 100
        Opincome_current_TTM = sum(income_sheet_Q["operatingIncome"][0:4])
        Opincome_lastyr_TTM = sum(income_sheet_Q["operatingIncome"][4:8])
        Opincome_growth_TTM = ((Opincome_current_TTM - Opincome_lastyr_TTM)/Opincome_lastyr_TTM) * 100
        RG[0] = revenue_growth_TTM
        OpInG[0] = Opincome_growth_TTM

    if len(CF_sheet_Q["date"]) > 7:
        CF_current_TTM = sum(CF_sheet_Q["freeCashFlow"][0:4])
        CF_lastyr_TTM = sum(CF_sheet_Q["freeCashFlow"][4:8])
        CF_growth_TTM = ((CF_current_TTM - CF_lastyr_TTM)/CF_lastyr_TTM) * 100
        FCFG[0] = CF_growth_TTM
    
    if len(income_sheet_A["date"]) > 1:
        revenue_growth_last_annual = ((income_sheet_A["revenue"][0] - income_sheet_A["revenue"][1])/income_sheet_A["revenue"][1]) * 100
        OpIn_growth_last_annual = ((income_sheet_A["operatingIncome"][0] - income_sheet_A["operatingIncome"][1])/income_sheet_A["operatingIncome"][1]) * 100
        RG[1] = revenue_growth_last_annual
        OpInG[1] = OpIn_growth_last_annual

    if len(CF_sheet_A["date"]) > 1:
        CF_growth_last_annual = ((CF_sheet_A["freeCashFlow"][0] - CF_sheet_A["freeCashFlow"][1])/CF_sheet_A["freeCashFlow"][1]) * 100
        FCFG[1] = CF_growth_last_annual
    
    if len(income_sheet_A["date"]) > 3:
        if (income_sheet_A["revenue"][0] > 0) & (income_sheet_A["revenue"][3] > 0):
            revenue_growth_CAGR = ((((income_sheet_A["revenue"][0]/income_sheet_A["revenue"][3]))**(1/3)) -1) * 100
            RG[2] = revenue_growth_CAGR
        else:
            RG[2] = "NA"

        if (income_sheet_A["operatingIncome"][0] > 0) & (income_sheet_A["operatingIncome"][3] > 0):
            OpIn_growth_CAGR = ((((income_sheet_A["operatingIncome"][0]/income_sheet_A["operatingIncome"][3]))**(1/3)) -1) * 100
            OpInG[2] = OpIn_growth_CAGR
        else:
            OpInG[2] = "NA"
    
    if len(CF_sheet_A["date"]) > 3:
        if (CF_sheet_A["freeCashFlow"][0] > 0) & (CF_sheet_A["freeCashFlow"][3] > 0):
            CF_growth_CAGR = ((((CF_sheet_A["freeCashFlow"][0]/CF_sheet_A["freeCashFlow"][3]))**(1/3)) -1) * 100
            FCFG[2] = CF_growth_CAGR
        else:
            FCFG[2] = "NA"

    column_index = ["Current Quarter-TTM", "Current Annual Report", "CAGR-3 years"]
    stock_list = [stock, stock, stock]
    growth_ratios_data = pd.DataFrame({"Last Reported": column_index, "symbol": stock_list, "Revenue Growth": RG,"FCF Growth": FCFG, "Operating Income Growth": OpInG })
    
    return growth_ratios_data


def profit_ratios_comparison_data(stock):
    
    
    ISQ = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&apikey={api_FMP}').json()         
        
    BSQ = requests.get(
            f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=quarter&apikey={api_FMP}').json()
    

    if (len(ISQ) == 0) | (len(BSQ) == 0):
        return pd.DataFrame()

    income_sheet_Q = pd.DataFrame(ISQ, index = list(range(len(ISQ))))
    income_sheet_Q.date = income_sheet_Q.date.apply(time_period_quarter)
    balance_sheet_Q = pd.DataFrame(BSQ, index = list(range(len(BSQ))))    
    balance_sheet_Q.date = balance_sheet_Q.date.apply(time_period_quarter)

    
    ROE = ["NA", "NA", "NA"]
    ROA = ["NA", "NA", "NA"]
    ROCE = ["NA", "NA", "NA"]

    if len(income_sheet_Q["date"]) > 8:
        netIncome_current_TTM = sum(income_sheet_Q["netIncome"][0:4])
        netIncome_lastqtr_TTM = sum(income_sheet_Q["netIncome"][1:5])
        netIncome_lastyr_TTM = sum(income_sheet_Q["netIncome"][4:8])

        ROE_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalStockholdersEquity"][0]) * 100
        ROE_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalStockholdersEquity"][1]) * 100
        ROE_lastyr_TTM = (netIncome_lastyr_TTM/balance_sheet_Q["totalStockholdersEquity"][4]) * 100
        ROE[0] = ROE_current_TTM
        ROE[1] = ROE_lastqtr_TTM
        ROE[2] = ROE_lastyr_TTM

        ROA_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalAssets"][0]) * 100
        ROA_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalAssets"][1]) * 100
        ROA_lastyr_TTM = (netIncome_lastyr_TTM/balance_sheet_Q["totalAssets"][4]) * 100
        ROA[0] = ROA_current_TTM
        ROA[1] = ROA_lastqtr_TTM
        ROA[2] = ROA_lastyr_TTM

        ROCE_current_TTM = (netIncome_current_TTM/(balance_sheet_Q["totalAssets"][0] - balance_sheet_Q["totalCurrentLiabilities"][0])) * 100
        ROCE_lastqtr_TTM = (netIncome_lastqtr_TTM/(balance_sheet_Q["totalAssets"][1] - balance_sheet_Q["totalCurrentLiabilities"][1])) * 100
        ROCE_lastyr_TTM = (netIncome_lastyr_TTM/(balance_sheet_Q["totalAssets"][4] - balance_sheet_Q["totalCurrentLiabilities"][4])) * 100
        ROCE[0] = ROCE_current_TTM
        ROCE[1] = ROCE_lastqtr_TTM
        ROCE[2] = ROCE_lastyr_TTM

    
    if len(income_sheet_Q["date"]) > 4:
        netIncome_current_TTM = sum(income_sheet_Q["netIncome"][0:4])
        netIncome_lastqtr_TTM = sum(income_sheet_Q["netIncome"][1:5])

        ROE_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalStockholdersEquity"][0]) * 100
        ROE_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalStockholdersEquity"][1]) * 100
        ROE[0] = ROE_current_TTM
        ROE[1] = ROE_lastqtr_TTM


        ROA_current_TTM = (netIncome_current_TTM/balance_sheet_Q["totalAssets"][0]) * 100
        ROA_lastqtr_TTM = (netIncome_lastqtr_TTM/balance_sheet_Q["totalAssets"][1]) * 100
        ROA[0] = ROA_current_TTM
        ROA[1] = ROA_lastqtr_TTM

        ROCE_current_TTM = (netIncome_current_TTM/(balance_sheet_Q["totalAssets"][0] - balance_sheet_Q["totalCurrentLiabilities"][0])) * 100
        ROCE_lastqtr_TTM = (netIncome_lastqtr_TTM/(balance_sheet_Q["totalAssets"][1] - balance_sheet_Q["totalCurrentLiabilities"][1])) * 100
        ROCE[0] = ROCE_current_TTM
        ROCE[1] = ROCE_lastqtr_TTM


    column_index = ["Current Quarter-TTM", "Last Quarter-TTM", "Last Year-TTM"]
    stock_list = [stock, stock, stock]
    profit_ratios_data = pd.DataFrame({"Last Reported": column_index, "symbol": stock_list, "ROE": ROE,"ROA": ROA, "ROCE": ROCE })
    
    return profit_ratios_data


def investment_ratios_comparison_data(stock):


    TTM = requests.get(
            f'https://financialmodelingprep.com/api/v3/ratios-ttm/{stock}?apikey={api_FMP}').json()


    FR = requests.get(
            f'https://financialmodelingprep.com/api/v3/ratios/{stock}?apikey={api_FMP}').json()
    

    if (len(TTM) == 0) | (len(FR) == 0):
        return pd.DataFrame()

    TTM_ratios = pd.DataFrame(TTM, index = list(range(len(TTM))))    
    ratios_A = pd.DataFrame(FR, index = list(range(len(FR))))
    ratios_A.date = ratios_A.date.apply(time_period_annual)

    PE = ["NA", "NA", "NA"]
    PS = ["NA", "NA", "NA"]
    PBV = ["NA", "NA", "NA"]
    PFCF = ["NA", "NA", "NA"]

    if len(ratios_A["date"]) > 1:
        PE[0] = TTM_ratios["priceEarningsRatioTTM"][0]
        PE[1] = ratios_A["priceEarningsRatio"][0]
        PE[2] = ratios_A["priceEarningsRatio"][1]

        PS[0] = TTM_ratios["priceToSalesRatioTTM"][0]
        PS[1] = ratios_A["priceToSalesRatio"][0]
        PS[2] = ratios_A["priceToSalesRatio"][1]

        PBV[0] = TTM_ratios["priceToBookRatioTTM"][0]
        PBV[1] = ratios_A["priceToBookRatio"][0]
        PBV[2] = ratios_A["priceToBookRatio"][1]

        PFCF[0] = TTM_ratios["priceToFreeCashFlowsRatioTTM"][0]
        PFCF[1] = ratios_A["priceToFreeCashFlowsRatio"][0]
        PFCF[2] = ratios_A["priceToFreeCashFlowsRatio"][1]

    else:
        PE[0] = TTM_ratios["priceEarningsRatioTTM"][0]
        PE[1] = ratios_A["priceEarningsRatio"][0]
        
        PS[0] = TTM_ratios["priceToSalesRatioTTM"][0]
        PS[1] = ratios_A["priceToSalesRatio"][0]
    
        PBV[0] = TTM_ratios["priceToBookRatioTTM"][0]
        PBV[1] = ratios_A["priceToBookRatio"][0]
    
        PFCF[0] = TTM_ratios["priceToFreeCashFlowsRatioTTM"][0]
        PFCF[1] = ratios_A["priceToFreeCashFlowsRatio"][0]
    

    column_index = ["Current Quarter-TTM", "Current Annual Report", "Last Year Annual Report"]
    stock_list = [stock, stock, stock]
    investment_ratios_data = pd.DataFrame({"Last Reported": column_index, "symbol": stock_list, "Price-to-Earnings": PE,"Price-to-Sales": PS, "Price-to-Bookvalue": PBV, "Price-to-FreeCashFlow": PFCF })
    
    return investment_ratios_data


def historical_prices_comparison(stock):

    historical_prices = requests.get(
            f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_FMP}').json()
    
    hp_df = pd.DataFrame(historical_prices["historical"], index = list(range(len(historical_prices["historical"]))))

    if len(hp_df["date"]) > 1000:
        hp_df = hp_df.iloc[0:1000]
    
    hp_df.insert(0, "symbol", stock)

    return hp_df

# def historical_news_retrieval(stock):

#     historical_news = requests.get(
#             f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?apikey={api_FMP}').json()
    
#     hp_df = pd.DataFrame(historical_prices["historical"], index = list(range(len(historical_prices["historical"]))))

#     return hp_df