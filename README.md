# Stock-Predictor-Website

The project objective is to create a website that provides fundamental and stock price predictor for companies specified by the user. We will not be providing a search function for the stock, this will be provided by the user. Such functionality may be provided in future improvements. 

Website front end will just be basic html and CSS/bootstrap. Backend will be using Python's module Flask.

The website will be segmented into several categories:
1) Fundamental Analysis
2) Stock Price Predictor 
3) DCF calculator

For the fundamental analysis, we will look at the company's income statement, balance sheet and cash flow statements and showcase specific parameters of that company. We will also provide the PE, PS, EV, EV/EBITDA, P/BV, P/FCF, PEG and CAGR ratios to provide a well rounded fundamental view of the company.
1) A dashboard showcasing the important financial properties (income statement, balance sheet and cash flow statements) 
2) Provide a valuation grading of several metrics of the company, i.e. Revenue Growth - A; Balance Sheet - B; and label the company into the following categories: GROWTH AND SUSTAINING, GROWTH BUT PLATEAUING, OVER-VALUED, UNDER-VALUED

For the stock price predictor, we will look at the company's stock price movement for a specified number of years, and deploy specific machine learning algorithms to help predict the upcoming stock prices
1) Time-Series Analysis using simple algo of SMA, exponential-smoothing and more complex algo such as LSTM
2) Explore webscraping of news articles during large growth and decline periods (>10%) to try and figure out the rationale for the movement

For the DCF Calculator
1) Provide a step by step guide to help user calculate the estimated stock value using the discounted cash flow method

Future ideas
1) A search engine to allow the user to find stocks based on the parameters specified
