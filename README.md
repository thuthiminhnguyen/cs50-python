# Building Optimal Portfolio Using the Efficient Frontier
This is the final project for CS50 Introduction to Python.
The project implements a classical portfolio optimization methodology called Efficient Frontier using Python. It provides a simple yet effective approach to constructing optimal portfolios.

Video Demo:  [here](https://youtu.be/ggZyU5vK0io)

## Table of contents
* [General Information](#general_info)
* [Description](#description)
* [Video Demo](#video-demo)
* [Installation](#installation)
* [Usage](#usage)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## General Information:
In the world of investments, achieving the best results often involves finding the optimal portfolio. This isn't just about picking investments with the highest returns. It's about creating a balance between risk and reward that aligns with your financial goals and risk tolerance. It can either include high-potential investments with controlled risk or lower-risk options with a guaranteed minimum return.

Developed in 1952 by Harry Markowitz, the efficient frontier is a core principle of modern portfolio theory. It helps you find investment combinations that balance risk and reward. It highlights portfolios with the best return for a specific risk level, or the lowest risk for a desired return.

The visualization of Efficient Frontier is as follows:
![Efficient Frontier](/img/EF.png)

For more information, you can read in [here](https://www.investopedia.com/terms/e/efficientfrontier.asp#:~:text=The%20efficient%20frontier%20is%20the,given%20level%20of%20expected%20return.).

## Description:
This final project includes 2 main files:

### `project.py` contains all functions which are used to gernerate an optimal portfolio based on user's input.
* `check_budget_input`: check if the budget is a valid number (no text or special characters),
* `check_number_of_stocks`: verify that the user provided a valid integer for the number of stock symbols,
* `is_valid_date_format`: make sure the date is formatted correctly (YYYY-MM-DD),
* `check_valid_start_end_date`: the calculation start date should be before you buy,
* `check_symbol_existence`: ensure the provided stock symbol exists in the financial data source,
* `input_each_stock_symbol`: input the stock symbol,
* `extract_stock_price`: look up past prices for a stock within a specific timeframe,
* `optimal_portfolio`: calculate the optimal investment amounts for a diversified portfolio and report the leftover cash,
* `validation`: calculate the total profit or loss on an investment held for a specific time frame.

### `test_project.py` contains all test functions that collectively test my implementation of `project.py` thoroughly, prepended with `test_`.
* `test_check_budget_input`
* `test_check_number_of_stocks`
* `test_is_valid_date_format`
* `test_check_valid_start_end_date`
* `test_check_symbol_existence`

## Video Demo:  <URL HERE>

## Installation:
You need to install the following packages to run this program:
`$ pip install yfinance`
`$ pip install PyPortfolioOpt`

## Usage
These are following steps of you must do to help the program run smoothly:
* 1st: Input your budget amount,
* 2nd: Input the number of stock symbols,
* 3rd: Input the start date (YYYY-MM-DD),
* 4th: Input the deadline for your purchases (YYYY-MM-DD),
* 5th: Input the date you want to validate data (YYYY-MM-DD),
* 6th: Input stock symbols

Input Example:
![Input Example](/img/ex_input.png)

Output Example:
![Output Example](/img/ex_output.png)

Comment: The constructed portfolio clearly has a higher return compared to the portfolio with an equally distributed budget across all assets.

## Acknowledgements
* [Capital Asset Pricing Model](https://www.investopedia.com/terms/c/capm.asp)
* [Efficient Frontier](https://www.investopedia.com/terms/e/efficientfrontier.asp#:~:text=The%20efficient%20frontier%20is%20the,given%20level%20of%20expected%20return.)
* [PyPortfolioOpt](https://pypi.org/project/pyportfolioopt/)
* [Yahoo! Finance's API](https://pypi.org/project/yfinance/)

## Contact
Feel free to contact me on my [email](@nguyenthiminhthu.21130@gmail.com).
