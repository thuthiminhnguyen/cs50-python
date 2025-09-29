import yfinance as yf
import re
import datetime

from datetime import datetime, timedelta
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

def main():
  budget = check_budget_input(input("Please input your budget amount ($): "))
  stocks = check_number_of_stocks(input("Specify the number of stocks you'll be entering symbols for: "))
  start_date = is_valid_date_format(input("Enter the start date for your calculations (YYYY-MM-DD): "))
  end_date = is_valid_date_format(input("Enter the deadline for your purchases (YYYY-MM-DD): "))
  start_date, end_date = check_valid_start_end_date(start_date, end_date)
  validation_date = is_valid_date_format(input("Enter the date you want to validate data against (YYYY-MM-DD): "))
  end_date, validation_date = check_valid_start_end_date(end_date, validation_date)

  symbols = input_each_stock_symbol(stocks, start_date, end_date)
  df = extract_stock_price(symbols, start_date, end_date)
  allocation, leftover, latest_prices = optimal_portfolio(df, budget)

  profit, invest_amt, validation_df = validation(symbols, budget, allocation, leftover, validation_date)

  print(f"Allocation: {allocation}")
  print(f"Investment amount ($): {round(invest_amt, 1)}")
  print(f"Leftover amount ($): {round(leftover, 1)}")

  if profit >= 0:
    print(f"Profit ($): {round(profit, 1)}")
    print(f"Profit (%): {round(profit*100/invest_amt, 1)}")
  else:
    print(f"Loss ($): {-round(profit, 1)}")
    print(f"Loss (%): {round(-profit*100/invest_amt, 1)}")

  eq_profit, eq_invest_amt = equally_distributed(stocks, budget, latest_prices, validation_df)
  print("\nEqually distributed investment amount:")
  print(f"Investment amount ($): {round(eq_invest_amt, 1)}")
  if eq_profit >= 0:
    print(f"Profit ($): {round(eq_profit, 1)}")
    print(f"Profit (%): {round(eq_profit*100/eq_invest_amt, 1)}")
  else:
    print(f"Loss ($): {-round(eq_profit, 1)}")
    print(f"Loss (%): {round(-eq_profit*100/eq_invest_amt, 1)}")

# Check if bugdet is a number or not
def check_budget_input(budget):
  try:
    return float(budget)
  except:
    raise TypeError("Please input a number.")

# Check if stocks is an integer number or not
def check_number_of_stocks(stocks):
  try:
    return int(stocks)
  except:
    raise TypeError("Please input an integer number")

# Check if date input is in format YYYY-MM-DD or not
def is_valid_date_format(date_string):
  date_regex = r"^\d{4}-\d{2}-\d{2}$"  # Regular expression for YYYY-MM-DD

  # Check format using regular expression
  if not re.match(date_regex, date_string):
    raise ValueError("Please input date in format YYYY-mm-dd.")

  # Attempt parsing with datetime.strptime (raises exception for invalid dates)
  try:
    datetime.strptime(date_string, "%Y-%m-%d")
    return date_string
  except:
    raise ValueError("The input date does not exist.")

def check_valid_start_end_date(start_date, end_date):
  if datetime.strptime(start_date, "%Y-%m-%d") < datetime.strptime(end_date, "%Y-%m-%d"):
    return start_date, end_date
  else:
    raise ValueError("Start date must before end date.")

# Check if stock symbol is available over the input period or not
def check_symbol_existence(symbol, start_date, end_date):
  try:
    # Download historical data for the specified period
    data = yf.download(symbol, start=start_date, end=end_date)
    # Check if data is empty (might indicate delisted)
    if data.empty:
      raise ValueError(f"{symbol} doesn't exist")
    else:
      return symbol
  except (yf.DownloadError, ValueError):
    # Download error or invalid symbol, symbol likely doesn't exist
    raise ValueError(f"{symbol} might not exist or data not available for the period")

def input_each_stock_symbol(stocks, start_date, end_date):
  symbols = []
  for i in (range(int(stocks))):
    symbols.append(check_symbol_existence(input(f"Enter stock symbol #{i+1}: "), start_date, end_date))
  return symbols

# Check if all stock symbols have the same length of data and then extract stock price
def extract_stock_price(symbols, start_date, end_date):
  len_arr = []
  print("\nLoading ...")
  for symbol in symbols:
    # Download historical data for the specified period
    df = yf.download(symbol, start=start_date, end=end_date)
    len_arr.append(len(df))

  print("\nLoading ...")
  if all(i == len_arr[0] for i in len_arr):
    df = yf.download(symbols, start=start_date, end=end_date)
    df = df["Adj Close"]
    df = df.dropna(axis='rows')
    return df
  else:
    raise ValueError("The length of history data are not equal.")

def optimal_portfolio(df, budget):
  # Calculate expected returns and sample covariance
  mu = expected_returns.mean_historical_return(df)
  S = risk_models.sample_cov(df)

  # Optimize for maximal Sharpe ratio
  ef = EfficientFrontier(mu, S)
  raw_weights = ef.max_sharpe()
  cleaned_weights = ef.clean_weights()
  ef.portfolio_performance(verbose=True)

  latest_prices = get_latest_prices(df)
  da = DiscreteAllocation(raw_weights, latest_prices, total_portfolio_value=float(budget))
  allocation, leftover = da.greedy_portfolio()

  return allocation, leftover, latest_prices

def validation(symbols, budget, allocation, leftover, validation_date):
  print("\nLoading ...")
  print("\nOptimal Portfolio:")
  validation_df = yf.download(symbols, start = validation_date, end = datetime.strptime(validation_date, "%Y-%m-%d") + timedelta(days=1))
  if len(validation_df) == 0:
    raise ValueError("No available data for validation. Please choose another date.")
  else:
    validation_df = validation_df["Adj Close"].to_dict('records')[0]
    # Use for loop to create the product dictionary
    product_dict = {}
    for key in allocation:
      product_dict[key] = allocation[key] * validation_df[key]

    revenue = sum(product_dict.values())
    profit = revenue - (float(budget) - leftover)
    invest_amt = (float(budget) - leftover)
    return profit, invest_amt, validation_df

def equally_distributed(stocks, budget, latest_prices, validation_df):
  latest_prices = latest_prices.to_dict()
  each_stock_budget = float(budget)/float(stocks)
  # return number of stocks for each symbol
  allocation = {}
  for key in latest_prices:
    allocation[key] = round(each_stock_budget/latest_prices[key], 0)

  invest_amount = 0
  for key in latest_prices:
    invest_amount = invest_amount + allocation[key] * latest_prices[key]

  product_dict = {}
  for key in allocation:
      product_dict[key] = allocation[key] * validation_df[key]

  revenue = sum(product_dict.values())
  profit = revenue - invest_amount
  return profit, invest_amount

if __name__ == "__main__":
    main()
