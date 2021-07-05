import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import pandas_datareader as pdr

def scrape(stock, days, site, ma1, ma2):
	end = dt.datetime.now()
	start = end - dt.timedelta(days=days)

	data = pdr.DataReader(stock, site, start, end)
	data[f'SMA{ma1}'] = data['Adj Close'].rolling(window=ma1).mean()
	data[f'SMA{ma2}'] = data['Adj Close'].rolling(window=ma2).mean()
	data = data.iloc[ma2:]

	return data

def automate(data):
	buy = []
	sell = []

	state = 0
	for row in range(len(data)):
		if data[f'SMA{ma1}'].iloc[row] > data[f'SMA{ma2}'].iloc[row] and state != 1:
			buy.append(data['Adj Close'].iloc[row])
			sell.append(float('nan'))
			state = 1

		if data[f'SMA{ma1}'].iloc[row] < data[f'SMA{ma2}'].iloc[row] and state != -1:
			buy.append(float('nan'))
			sell.append(data['Adj Close'].iloc[row])
			state = -1

		else:
			buy.append(float('nan'))
			sell.append(float('nan'))

	data['Buy'] = buy
	data['Sell'] = sell

	return data

def stats(data):
	plt.style.use('dark_background')
	plt.plot(data['Adj Close'], label='Share Price', alpha=0.5)
	plt.plot(data[f'SMA{ma1}'], label=f'SMA {ma1}', color='orange', linestyle='--')
	plt.plot(data[f'SMA{ma2}'], label=f'SMA {ma2}', color='purple', linestyle='--')
	plt.scatter(data.index, data['Buy'], label='Buy', marker='^', color='green')
	plt.scatter(data.index, data['Sell'], label='Sell', marker='v', color='red')
	plt.legend(loc='upper left')
	plt.show()

ma1 = 30
ma2 = 100
site = 'yahoo'
stock = input('Stock: ')
days = float(input('Days: '))

data = scrape(stock, days, site, ma1, ma2)
data = automate(data)
stats(data)
