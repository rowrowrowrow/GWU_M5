#!/usr/bin/env python
# coding: utf-8

# # Financial Planning with APIs and Simulations
# 
# In this Challenge, you’ll create two financial analysis tools by using a single Jupyter notebook:
# 
# Part 1: A financial planner for emergencies. The members will be able to use this tool to visualize their current savings. The members can then determine if they have enough reserves for an emergency fund.
# 
# Part 2: A financial planner for retirement. This tool will forecast the performance of their retirement portfolio in 30 years. To do this, the tool will make an Alpaca API call via the Alpaca SDK to get historical price data for use in Monte Carlo simulations.
# 
# You’ll use the information from the Monte Carlo simulation to answer questions about the portfolio in your Jupyter notebook.
# 
# 

# In[1]:


# Import the required libraries and dependencies
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
from datetime import date, timedelta

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Load the environment variables from the .env file
#by calling the load_dotenv function
load_dotenv()


# ## Part 1: Create a Financial Planner for Emergencies

# ### Evaluate the Cryptocurrency Wallet by Using the Requests Library
# 
# In this section, you’ll determine the current value of a member’s cryptocurrency wallet. You’ll collect the current prices for the Bitcoin and Ethereum cryptocurrencies by using the Python Requests library. For the prototype, you’ll assume that the member holds the 1.2 Bitcoins (BTC) and 5.3 Ethereum coins (ETH). To do all this, complete the following steps:
# 
# 1. Create a variable named `monthly_income`, and set its value to `12000`.
# 
# 2. Use the Requests library to get the current price (in US dollars) of Bitcoin (BTC) and Ethereum (ETH) by using the API endpoints that the starter code supplies.
# 
# 3. Navigate the JSON response object to access the current price of each coin, and store each in a variable.
# 
#     > **Hint** Note the specific identifier for each cryptocurrency in the API JSON response. The Bitcoin identifier is `1`, and the Ethereum identifier is `1027`.
# 
# 4. Calculate the value, in US dollars, of the current amount of each cryptocurrency and of the entire cryptocurrency wallet.
# 
# 

# In[3]:


# The current number of coins for each cryptocurrency asset held in the portfolio.
btc_coins = 1.2
eth_coins = 5.3


# #### Step 1: Create a variable named `monthly_income`, and set its value to `12000`.

# In[4]:


# The monthly amount for the member's household income
# YOUR CODE HERE
monthly_income = 12000


# #### Review the endpoint URLs for the API calls to Free Crypto API in order to get the current pricing information for both BTC and ETH.

# In[5]:


# The Free Crypto API Call endpoint URLs for the held cryptocurrency assets
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=USD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=USD"


# #### Step 2. Use the Requests library to get the current price (in US dollars) of Bitcoin (BTC) and Ethereum (ETH) by using the API endpoints that the starter code supplied.

# In[6]:


# Using the Python requests library, make an API call to access the current price of BTC
btc_response = requests.get(btc_url).json()

# Use the json.dumps function to review the response data from the API call
# Use the indent and sort_keys parameters to make the response object readable
# YOUR CODE HERE
print(json.dumps(btc_response, indent=4, sort_keys=True))


# In[7]:


# Using the Python requests library, make an API call to access the current price ETH
eth_response = requests.get(eth_url).json()

# Use the json.dumps function to review the response data from the API call
# Use the indent and sort_keys parameters to make the response object readable
# YOUR CODE HERE
print(json.dumps(eth_response, indent=4, sort_keys=True))


# #### Step 3: Navigate the JSON response object to access the current price of each coin, and store each in a variable.

# In[8]:


# Navigate the BTC response object to access the current price of BTC
btc_price = btc_response['data']['1']['quotes']['USD']['price']

# Print the current price of BTC
# YOUR CODE HERE
print(f"The current price of BTC in USD: {btc_price}")


# In[9]:


# Navigate the BTC response object to access the current price of ETH
eth_price = eth_response['data']['1027']['quotes']['USD']['price']

# Print the current price of ETH
# YOUR CODE HERE
print(f"The current price of ETH in USD: {eth_price}")


# ### Step 4: Calculate the value, in US dollars, of the current amount of each cryptocurrency and of the entire cryptocurrency wallet.

# In[10]:


# Compute the current value of the BTC holding 
btc_value = btc_price * btc_coins

# Print current value of your holding in BTC
# YOUR CODE HERE
print(f"The current value of BTC holding in USD: {btc_value}")


# In[11]:


# Compute the current value of the ETH holding 
eth_value = eth_price * eth_coins

# Print current value of your holding in ETH
# YOUR CODE HERE
print(f"The current value of ETH holding in USD: {eth_value}")


# In[12]:


# Compute the total value of the cryptocurrency wallet
# Add the value of the BTC holding to the value of the ETH holding
total_crypto_wallet = btc_value + eth_value

# Print current cryptocurrency wallet balance
# YOUR CODE HERE
print(f"The current value of all cryptocurrency holdings in USD: {total_crypto_wallet}")


# ### Evaluate the Stock and Bond Holdings by Using the Alpaca SDK
# 
# In this section, you’ll determine the current value of a member’s stock and bond holdings. You’ll make an API call to Alpaca via the Alpaca SDK to get the current closing prices of the SPDR S&P 500 ETF Trust (ticker: SPY) and of the iShares Core US Aggregate Bond ETF (ticker: AGG). For the prototype, assume that the member holds 110 shares of SPY, which represents the stock portion of their portfolio, and 200 shares of AGG, which represents the bond portion. To do all this, complete the following steps:
# 
# 1. In the `Starter_Code` folder, create an environment file (`.env`) to store the values of your Alpaca API key and Alpaca secret key.
# 
# 2. Set the variables for the Alpaca API and secret keys. Using the Alpaca SDK, create the Alpaca `tradeapi.REST` object. In this object, include the parameters for the Alpaca API key, the secret key, and the version number.
# 
# 3. Set the following parameters for the Alpaca API call:
# 
#     - `tickers`: Use the tickers for the member’s stock and bond holdings.
# 
#     - `timeframe`: Use a time frame of one day.
# 
#     - `start_date` and `end_date`: Use the same date for these parameters, and format them with the date of the previous weekday (or `2020-08-07`). This is because you want the one closing price for the most-recent trading day.
# 
# 4. Get the current closing prices for `SPY` and `AGG` by using the Alpaca `get_bars` function. Format the response as a Pandas DataFrame by including the `df` property at the end of the `get_bars` function.
# 
# 5. Navigating the Alpaca response DataFrame, select the `SPY` and `AGG` closing prices, and store them as variables.
# 
# 6. Calculate the value, in US dollars, of the current amount of shares in each of the stock and bond portions of the portfolio, and print the results.
# 

# #### Review the total number of shares held in both (SPY) and (AGG).

# In[13]:


# Current amount of shares held in both the stock (SPY) and bond (AGG) portion of the portfolio.
spy_shares = 110
agg_shares = 200


# #### Step 1: In the `Starter_Code` folder, create an environment file (`.env`) to store the values of your Alpaca API key and Alpaca secret key.

# #### Step 2: Set the variables for the Alpaca API and secret keys. Using the Alpaca SDK, create the Alpaca `tradeapi.REST` object. In this object, include the parameters for the Alpaca API key, the secret key, and the version number.

# In[14]:


# Set the variables for the Alpaca API and secret keys
alpaca_api_key = os.getenv('ALPACA_API_KEY')
alpaca_secret_key = os.getenv('ALPACA_SECRET_KEY')

# Create the Alpaca tradeapi.REST object
alpaca = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version="v2" 
)


# #### Step 3: Set the following parameters for the Alpaca API call:
# 
# - `tickers`: Use the tickers for the member’s stock and bond holdings.
# 
# - `timeframe`: Use a time frame of one day.
# 
# - `start_date` and `end_date`: Use the same date for these parameters, and format them with the date of the previous weekday (or `2020-08-07`). This is because you want the one closing price for the most-recent trading day.
# 

# In[15]:


# Set the tickers for both the bond and stock portion of the portfolio
tickers = [
    'SPY',
    'AGG'
]

# Set timeframe to 1Day
timeframe = '1Day'

# Format current date as ISO format
# Set both the start and end date at the date of your prior weekday 
# This will give you the closing price of the previous trading day
# Alternatively you can use a start and end date of 2020-08-07

# Add a function so we don't need to recalculate the previous weekday each time this is run
# https://stackoverflow.com/questions/12053633/previous-weekday-in-python
def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() > 4: # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate

prior_weekday = prev_weekday(date.today())

start_date = pd.Timestamp(prior_weekday.isoformat(), tz="America/New_York").isoformat()
end_date = pd.Timestamp(prior_weekday.isoformat(), tz="America/New_York").isoformat()


# #### Step 4: Get the current closing prices for `SPY` and `AGG` by using the Alpaca `get_bars` function. Format the response as a Pandas DataFrame by including the `df` property at the end of the `get_bars` function.

# In[16]:


# Use the Alpaca get_bars function to get current closing prices the portfolio
# Be sure to set the `df` property after the function to format the response object as a DataFrame
prices_df = alpaca.get_bars(
    tickers,
    timeframe,
    start = start_date,
    end = end_date
).df

# Reorganize the DataFrame
# Separate ticker data
individual_dataframes = map(lambda symbol: prices_df[prices_df['symbol']==symbol].drop('symbol', axis=1), tickers)

# Concatenate the ticker DataFrames
prices_df = pd.concat(individual_dataframes, axis=1, keys=tickers)

# Review the first 5 rows of the Alpaca DataFrame
prices_df.head()


# #### Step 5: Navigating the Alpaca response DataFrame, select the `SPY` and `AGG` closing prices, and store them as variables.

# In[17]:


# Access the closing price for AGG from the Alpaca DataFrame
# Converting the value to a floating point number
agg_close_price = float(prices_df['AGG']['close'])

# Print the AGG closing price
# YOUR CODE HERE
agg_close_price


# In[18]:


# Access the closing price for SPY from the Alpaca DataFrame
# Converting the value to a floating point number
spy_close_price = float(prices_df['SPY']['close'])

# Print the SPY closing price
spy_close_price


# #### Step 6: Calculate the value, in US dollars, of the current amount of shares in each of the stock and bond portions of the portfolio, and print the results.

# In[19]:


# Calculate the current value of the bond portion of the portfolio
agg_value = agg_close_price * agg_shares

# Print the current value of the bond portfolio
agg_value


# In[20]:


# Calculate the current value of the stock portion of the portfolio
spy_value = spy_close_price * spy_shares

# Print the current value of the stock portfolio
spy_value


# In[21]:


# Calculate the total value of the stock and bond portion of the portfolio
total_stocks_bonds = agg_value + spy_value

# Print the current balance of the stock and bond portion of the portfolio
total_stocks_bonds


# In[22]:


# Calculate the total value of the member's entire savings portfolio
# Add the value of the cryptocurrency walled to the value of the total stocks and bonds
total_portfolio = total_crypto_wallet + total_stocks_bonds

# Print current cryptocurrency wallet balance
total_portfolio


# ### Evaluate the Emergency Fund
# 
# In this section, you’ll use the valuations for the cryptocurrency wallet and for the stock and bond portions of the portfolio to determine if the credit union member has enough savings to build an emergency fund into their financial plan. To do this, complete the following steps:
# 
# 1. Create a Python list named `savings_data` that has two elements. The first element contains the total value of the cryptocurrency wallet. The second element contains the total value of the stock and bond portions of the portfolio.
# 
# 2. Use the `savings_data` list to create a Pandas DataFrame named `savings_df`, and then display this DataFrame. The function to create the DataFrame should take the following three parameters:
# 
#     - `savings_data`: Use the list that you just created.
# 
#     - `columns`: Set this parameter equal to a Python list with a single value called `amount`.
# 
#     - `index`: Set this parameter equal to a Python list with the values of `crypto` and `stock/bond`.
# 
# 3. Use the `savings_df` DataFrame to plot a pie chart that visualizes the composition of the member’s portfolio. The y-axis of the pie chart uses `amount`. Be sure to add a title.
# 
# 4. Using Python, determine if the current portfolio has enough to create an emergency fund as part of the member’s financial plan. Ideally, an emergency fund should equal to three times the member’s monthly income. To do this, implement the following steps:
# 
#     1. Create a variable named `emergency_fund_value`, and set it equal to three times the value of the member’s `monthly_income` of $12000. (You set this earlier in Part 1).
# 
#     2. Create a series of three if statements to determine if the member’s total portfolio is large enough to fund the emergency portfolio:
# 
#         1. If the total portfolio value is greater than the emergency fund value, display a message congratulating the member for having enough money in this fund.
# 
#         2. Else if the total portfolio value is equal to the emergency fund value, display a message congratulating the member on reaching this important financial goal.
# 
#         3. Else the total portfolio is less than the emergency fund value, so display a message showing how many dollars away the member is from reaching the goal. (Subtract the total portfolio value from the emergency fund value.)
# 

# #### Step 1: Create a Python list named `savings_data` that has two elements. The first element contains the total value of the cryptocurrency wallet. The second element contains the total value of the stock and bond portions of the portfolio.

# In[23]:


# Consolidate financial assets data into a Python list
savings_data = [
    total_crypto_wallet,
    total_stocks_bonds
]

# Review the Python list savings_data
# YOUR CODE HERE
savings_data


# #### Step 2: Use the `savings_data` list to create a Pandas DataFrame named `savings_df`, and then display this DataFrame. The function to create the DataFrame should take the following three parameters:
# 
# - `savings_data`: Use the list that you just created.
# 
# - `columns`: Set this parameter equal to a Python list with a single value called `amount`.
# 
# - `index`: Set this parameter equal to a Python list with the values of `crypto` and `stock/bond`.
# 

# In[24]:


# Create a Pandas DataFrame called savings_df 
savings_df = pd.DataFrame(data=savings_data, columns=['amount'], index=['crypto','stock/bond'])

# Display the savings_df DataFrame
savings_df


# #### Step 3: Use the `savings_df` DataFrame to plot a pie chart that visualizes the composition of the member’s portfolio. The y-axis of the pie chart uses `amount`. Be sure to add a title.

# In[25]:


# Plot the total value of the member's portfolio (crypto and stock/bond) in a pie chart
savings_df.plot(
    y='amount',
    kind='pie',
    title='Pie chart of portfolio value',
    autopct='%1.1f%%'
)


# #### Step 4: Using Python, determine if the current portfolio has enough to create an emergency fund as part of the member’s financial plan. Ideally, an emergency fund should equal to three times the member’s monthly income. To do this, implement the following steps:
# 
# Step 1. Create a variable named `emergency_fund_value`, and set it equal to three times the value of the member’s `monthly_income` of 12000. (You set this earlier in Part 1).
# 
# Step 2. Create a series of three if statements to determine if the member’s total portfolio is large enough to fund the emergency portfolio:
# 
# * If the total portfolio value is greater than the emergency fund value, display a message congratulating the member for having enough money in this fund.
# 
# * Else if the total portfolio value is equal to the emergency fund value, display a message congratulating the member on reaching this important financial goal.
# 
# * Else the total portfolio is less than the emergency fund value, so display a message showing how many dollars away the member is from reaching the goal. (Subtract the total portfolio value from the emergency fund value.)
# 

# ##### Step 4-1: Create a variable named `emergency_fund_value`, and set it equal to three times the value of the member’s `monthly_income` of 12000. (You set this earlier in Part 1).

# In[26]:


# Create a variable named emergency_fund_value
emergency_fund_value = 3 * monthly_income


# ##### Step 4-2: Create a series of three if statements to determine if the member’s total portfolio is large enough to fund the emergency portfolio:
# 
# * If the total portfolio value is greater than the emergency fund value, display a message congratulating the member for having enough money in this fund.
# 
# * Else if the total portfolio value is equal to the emergency fund value, display a message congratulating the member on reaching this important financial goal.
# 
# * Else the total portfolio is less than the emergency fund value, so display a message showing how many dollars away the member is from reaching the goal. (Subtract the total portfolio value from the emergency fund value.)

# In[27]:


# Evaluate the possibility of creating an emergency fund with 3 conditions:
if total_portfolio > emergency_fund_value:
    print("Congrats, you have enough money in your fund to cover emergencies!")
elif total_portfolio == emergency_fund_value:
    print("Congrats, you have enough money to match your emergency needs!")
else:
    emergency_fund_gap = emergency_fund_value - total_portfolio
    print(f"You are {emergency_fund_gap} away from your emergency fund goal")


# ## Part 2: Create a Financial Planner for Retirement

# ### Create the Monte Carlo Simulation
# 
# In this section, you’ll use the MCForecastTools library to create a Monte Carlo simulation for the member’s savings portfolio. To do this, complete the following steps:
# 
# 1. Make an API call via the Alpaca SDK to get 3 years of historical closing prices for a traditional 60/40 portfolio split: 60% stocks (SPY) and 40% bonds (AGG).
# 
# 2. Run a Monte Carlo simulation of 500 samples and 30 years for the 60/40 portfolio, and then plot the results.The following image shows the overlay line plot resulting from a simulation with these characteristics. However, because a random number generator is used to run each live Monte Carlo simulation, your image will differ slightly from this exact image:
# 
# ![A screenshot depicts the resulting plot.](Images/5-4-monte-carlo-line-plot.png)
# 
# 3. Plot the probability distribution of the Monte Carlo simulation. Plot the probability distribution of the Monte Carlo simulation. The following image shows the histogram plot resulting from a simulation with these characteristics. However, because a random number generator is used to run each live Monte Carlo simulation, your image will differ slightly from this exact image:
# 
# ![A screenshot depicts the histogram plot.](Images/5-4-monte-carlo-histogram.png)
# 
# 4. Generate the summary statistics for the Monte Carlo simulation.
# 
# 

# #### Step 1: Make an API call via the Alpaca SDK to get 3 years of historical closing prices for a traditional 60/40 portfolio split: 60% stocks (SPY) and 40% bonds (AGG).

# In[28]:


# Set start and end dates of 3 years back from your current date
# Alternatively, you can use an end date of 2020-08-07 and work 3 years back from that date 
three_years_ago = date.today() - timedelta(days=(3*365))

start_date = pd.Timestamp(three_years_ago.isoformat(), tz="America/New_York").isoformat()
end_date = pd.Timestamp(date.today().isoformat(), tz="America/New_York").isoformat()


# In[29]:


# Use the Alpaca get_bars function to make the API call to get the 3 years worth of pricing data
# The tickers and timeframe parameters should have been set in Part 1 of this activity 
# The start and end dates should be updated with the information set above
# Remember to add the df property to the end of the call so the response is returned as a DataFrame
past_three_years_prices_df = alpaca.get_bars(
    tickers,
    timeframe,
    start = start_date,
    end = end_date
).df

# Reorganize the DataFrame
# Separate ticker data
three_years_individual_dataframes = map(lambda symbol: past_three_years_prices_df[past_three_years_prices_df['symbol']==symbol].drop('symbol', axis=1), tickers)

# Concatenate the ticker DataFrames
past_three_years_prices_df = pd.concat(three_years_individual_dataframes, axis=1, keys=tickers)

# Display both the first and last five rows of the DataFrame
display(past_three_years_prices_df.head())
display(past_three_years_prices_df.tail())


# #### Step 2: Run a Monte Carlo simulation of 500 samples and 30 years for the 60/40 portfolio, and then plot the results.

# In[30]:


# Configure the Monte Carlo simulation to forecast 30 years cumulative returns
# The weights should be split 40% to AGG and 60% to SPY.
# Run 500 samples.
MC_60_40 = MCSimulation(
    portfolio_data=past_three_years_prices_df,
    weights=[.6,.4],
    num_simulation=500,
    num_trading_days=252*30
)

# Review the simulation input data
MC_60_40.portfolio_data.head()


# In[31]:


# Run the Monte Carlo simulation to forecast 30 years cumulative returns
MC_60_40.calc_cumulative_return()


# In[32]:


# Visualize the 30-year Monte Carlo simulation by creating an
# overlay line plot
MC_60_40.plot_simulation()


# #### Step 3: Plot the probability distribution of the Monte Carlo simulation.

# In[33]:


# Visualize the probability distribution of the 30-year Monte Carlo simulation 
# by plotting a histogram
MC_60_40.plot_distribution()


# #### Step 4: Generate the summary statistics for the Monte Carlo simulation.

# In[34]:


# Generate summary statistics from the 30-year Monte Carlo simulation results
# Save the results as a variable
thirty_year_summary_stats = MC_60_40.summarize_cumulative_return()


# Review the 30-year Monte Carlo summary statistics
thirty_year_summary_stats


# ### Analyze the Retirement Portfolio Forecasts
# 
# Using the current value of only the stock and bond portion of the member's portfolio and the summary statistics that you generated from the Monte Carlo simulation, answer the following question in your Jupyter notebook:
# 
# -  What are the lower and upper bounds for the expected value of the portfolio with a 95% confidence interval?
# 

# In[35]:


# Print the current balance of the stock and bond portion of the members portfolio
print(f"The current balance of the stock and bond portion of the members portfolio is USD {total_stocks_bonds}")


# In[36]:


# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes for the current stock/bond portfolio
ci_lower_thirty_cumulative_return = thirty_year_summary_stats[8] * total_stocks_bonds
ci_upper_thirty_cumulative_return = thirty_year_summary_stats[9] * total_stocks_bonds

# Print the result of your calculations
print(f'''There is a 95% chance that the current value of stocks and bonds, USD {total_stocks_bonds}, in the portfolio
      with a 60:40 SPY:AGG weighting portfolio over the next 30 years will end within in the range of
      ${ci_lower_thirty_cumulative_return} and ${ci_upper_thirty_cumulative_return}.''')


# ### Forecast Cumulative Returns in 10 Years
# 
# The CTO of the credit union is impressed with your work on these planning tools but wonders if 30 years is a long time to wait until retirement. So, your next task is to adjust the retirement portfolio and run a new Monte Carlo simulation to find out if the changes will allow members to retire earlier.
# 
# For this new Monte Carlo simulation, do the following: 
# 
# - Forecast the cumulative returns for 10 years from now. Because of the shortened investment horizon (30 years to 10 years), the portfolio needs to invest more heavily in the riskier asset&mdash;that is, stock&mdash;to help accumulate wealth for retirement. 
# 
# - Adjust the weights of the retirement portfolio so that the composition for the Monte Carlo simulation consists of 20% bonds and 80% stocks. 
# 
# - Run the simulation over 500 samples, and use the same data that the API call to Alpaca generated.
# 
# - Based on the new Monte Carlo simulation, answer the following questions in your Jupyter notebook:
# 
#     - Using the current value of only the stock and bond portion of the member's portfolio and the summary statistics that you generated from the new Monte Carlo simulation, what are the lower and upper bounds for the expected value of the portfolio (with the new weights) with a 95% confidence interval?
# 
#     - Will weighting the portfolio more heavily toward stocks allow the credit union members to retire after only 10 years?
# 

# In[37]:


# Configure a Monte Carlo simulation to forecast 10 years cumulative returns
# The weights should be split 20% to AGG and 80% to SPY.
# Run 500 samples.
MC_10_years = MCSimulation(
    portfolio_data=past_three_years_prices_df,
    weights=[.8,.2],
    num_simulation=500,
    num_trading_days=252*10
)

# Review the simulation input data
MC_10_years.portfolio_data.head()


# In[38]:


# Run the Monte Carlo simulation to forecast 10 years cumulative returns
MC_10_years.calc_cumulative_return()


# In[39]:


# Visualize the 10-year Monte Carlo simulation by creating an
# overlay line plot
MC_10_years.plot_simulation()


# In[40]:


# Visualize the probability distribution of the 10-year Monte Carlo simulation 
# by plotting a histogram
MC_10_years.plot_distribution()


# In[41]:


# Generate summary statistics from the 10-year Monte Carlo simulation results
# Save the results as a variable
ten_years_summary_stats = MC_10_years.summarize_cumulative_return()


# Review the 10-year Monte Carlo summary statistics
ten_years_summary_stats


# ### Answer the following questions:

# #### Question: Using the current value of only the stock and bond portion of the member's portfolio and the summary statistics that you generated from the new Monte Carlo simulation, what are the lower and upper bounds for the expected value of the portfolio (with the new weights) with a 95% confidence interval?

# In[42]:


# Print the current balance of the stock and bond portion of the members portfolio
print(f"The current balance of the stock and bond portion of the members portfolio is USD {total_stocks_bonds}")


# In[43]:


# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes for the current stock/bond portfolio
ci_lower_ten_cumulative_return = ten_years_summary_stats[8] * total_stocks_bonds
ci_upper_ten_cumulative_return = ten_years_summary_stats[9] * total_stocks_bonds

# Print the result of your calculations
print(f'''There is a 95% chance that the current value of stocks and bonds, USD {total_stocks_bonds}, in the portfolio
      with 80:20 SPY:AGG weighting portfolio over the next 10 years will end within in the range of
      ${ci_lower_ten_cumulative_return} and ${ci_upper_ten_cumulative_return}.''')


# #### Question: Will weighting the portfolio more heavily to stocks allow the credit union members to retire after only 10 years?
In short, no.

This is a subjective question, in my opinion neither of the upper bounded returns for either approaches provide enough for retirement. Especially considering that the earlier the retirement the more funds needed for the rest of your life and activities. Other factors like inflation need to be considered as well.

I think changing the weighting is not enough to significantly alter the amount saved in 10 years, although relatively speaking it does cut the time by 1/3 while still obtaining about 1/2 of the funds of the thirty year approach. It would be better to heavily weight stocks over a longer period of time, similar to target date funds.
# In[ ]:




