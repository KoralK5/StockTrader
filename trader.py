from datetime import datetime as dt
import matplotlib
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr

yf.pdr_override()

def scrape(stock, start, end, site, ma1, ma2):
	data = pdr.get_data_yahoo(stock, start, end)
	data[f'SMA {ma1}'] = data['Adj Close'].rolling(window=ma1).mean()
	data[f'SMA {ma2}'] = data['Adj Close'].rolling(window=ma2).mean()
	data = data.iloc[ma2:]

	return data

def automate(data):
	buy = []
	sell = []
	state = 0
	for row in range(len(data)):
		if data[f'SMA {ma1}'].iloc[row] > data[f'SMA {ma2}'].iloc[row] and state != 1:
			buy.append(data['Adj Close'].iloc[row])
			sell.append(float('nan'))
			state = 1

		elif data[f'SMA {ma1}'].iloc[row] < data[f'SMA {ma2}'].iloc[row] and state != -1:
			buy.append(float('nan'))
			sell.append(data['Adj Close'].iloc[row])
			state = -1

		else:
			buy.append(float('nan'))
			sell.append(float('nan'))

	data['Buy'] = buy
	data['Sell'] = sell

	return data

def stats(data, stock):
	plt.style.use('dark_background')
	plt.plot(data['Adj Close'], label='Share Price', alpha=0.5)
	plt.plot(data[f'SMA {ma1}'], label=f'SMA {ma1}', color='orange', linestyle='--')
	plt.plot(data[f'SMA {ma2}'], label=f'SMA {ma2}', color='purple', linestyle='--')
	plt.scatter(data.index, data['Buy'], label='Buy', marker='^', color='green')
	plt.scatter(data.index, data['Sell'], label='Sell', marker='v', color='red')
	plt.title(stock)
	plt.legend(loc='upper left')
	plt.show()

ma1 = 30
ma2 = 100
site = 'yahoo'
stock = input('Stock: ')
start = input('Start Date: ')
end = input('End Date: ')

start, end, stock = '01-01-2018', '03-07-2021', 'TSLA'

data = scrape(stock, dt.strptime(start, '%d-%m-%Y'), dt.strptime(end, '%d-%m-%Y'), site, ma1, ma2)
data = automate(data)
stats(data, stock)
