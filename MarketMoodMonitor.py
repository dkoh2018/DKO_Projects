import yfinance as yf
import pandas as pd

def get_stock_data(ticker_symbol, start_date, end_date):
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    stock_data = stock_data[['Open', 'Close', 'High', 'Low']] 
    return stock_data.dropna()

def calculate_green_red_days(data):
    green_days = 0
    red_days = 0

    data['Green'] = 0
    data['Red'] = 0
    data['% Up'] = 0.0
    data['% Down'] = 0.0
    data['Previous_Green'] = 0  
    data['Previous_Red'] = 0  
    data['Chg at Open'] = 0.0  
    data['Chg at Close'] = 0.0  

    previous_close = None
    for index, row in data.iterrows():
        prev_green_days = green_days
        prev_red_days = red_days

        if previous_close is not None:
            if row['Open'] > previous_close:
                green_days += 1
            else:
                red_days += 1

            data.at[index, 'Green'] = green_days
            data.at[index, 'Red'] = red_days

            # Probability of Up/Down
            probability_green = green_days / (green_days + red_days)
            probability_red = red_days / (green_days + red_days)
            data.at[index, '% Up'] = round(probability_green, 3)
            data.at[index, '% Down'] = round(probability_red, 3)
           
            # Calculate the day's range
            daily_range = row['High'] - row['Low']
            data.at[index, 'Range'] = round(daily_range, 3)
           
            # Calculate the change at open
            chg_at_open = row['Open'] - previous_close
            data.at[index, 'Chg at Open'] = round(chg_at_open, 3)

             # Calculate the change at close
            chg_at_close = row['Close'] - row['Open']
            data.at[index, 'Chg at Close'] = round(chg_at_close, 3)

            data.at[index, 'Previous_Green'] = prev_green_days
            data.at[index, 'Previous_Red'] = prev_red_days

        previous_close = row['Close']

    return data

def main():
    stock_ticker = 'AAPL'
    start_date = '2023-07-19'
    end_date = '2023-10-27'  
    data = get_stock_data(stock_ticker, start_date, end_date).round(3)

    data_with_signals = calculate_green_red_days(data)

    column_order = ['Open', 'Close', 'Chg at Open', 'Chg at Close', 'Range', 'Green', 'Red', '% Up', '% Down']
    data_with_signals = data_with_signals[column_order]

    print(data_with_signals.tail(30))

if __name__ == "__main__":
    main()


print("hello" * 5)