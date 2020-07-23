import pandas as pd
import requests
from time import sleep
import re

pg1 = 2
pg2 = 100
global counter

def smart_wallets(pg1, pg2 ):
	counter = 0
	pd.set_option("display.max_rows", None, "display.max_columns", None)
	sleep(5)
	url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html'
	# header is used to trick the site into thinking you're an actual person and not a program
	header = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}
	r = requests.get(url, headers=header)
	walletlist = pd.read_html(r.text, parse_dates=True)
	Address = walletlist[2]['Address']
	parseNofN = re.compile("\d-.*$")
	parseWallet = re.compile("wallet.*$")
	Address = Address.replace(parseNofN, '', regex=True).replace(parseWallet, '', regex=True)
	print(Address)
	for items in Address:
		sleep(2)
		url_of_BTC_Address = ('https://bitinfocharts.com/bitcoin/address/'+items.strip()+'-full')
		print(url_of_BTC_Address)
		try:
			BTC_Address = requests.get(url_of_BTC_Address, headers=header)
			info_of_BTC_Address = pd.read_html(BTC_Address.text, parse_dates=True)
			tr = info_of_BTC_Address[2]
			tr['Cash'] = tr['Balance, USD'].apply(lambda x: x.split('@')[1]).replace('[$,]', '', regex=True).astype(float)
			holder = re.compile("[\(\[].*?[\)\]]")
			tr['Quantity'] = tr['Amount'].replace('[BTC,]', '', regex=True).replace(holder, ' ', regex=True).astype(float)
			tr['Dollar'] = -tr['Quantity'] * tr['Cash']
			profit = tr['Dollar'].sum() - (tr['Balance'].replace('[BTC,]', '', regex=True).astype(float)[0] * tr['Cash'][0])
			print('profit in USD: ' + str(profit))
			if float(profit) > 1000.00:
				info_of_BTC_Address[2].to_csv('{BTC_filename1}.csv'.format(filename1=items))
		except ValueError:
			error_list = []
			error_list.append(url_of_BTC_Address)
			pass

	while pg1 < pg2:
		pd.set_option("display.max_rows", None, "display.max_columns", None)
		sleep(5)
		url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-' + str(pg1) + '.html'
		# header is used to trick the site into thinking you're an actual person and not a program
		header = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
			"X-Requested-With": "XMLHttpRequest"
		}
		r = requests.get(url, headers=header)
		walletlist = pd.read_html(r.text, parse_dates=True)
		Address = walletlist[0]['Address']
		parseNofN = re.compile("\d-.*$")
		parseWallet = re.compile("wallet.*$")
		Address = Address.replace(parseNofN,'',regex=True).replace(parseWallet,'',regex=True)
		print('page: ' + str(pg1))
		print(Address)

		for item in Address:
			sleep(2)
			filename = 'BTC_Cash_positive'+str(counter)
			counter += 1
			url_of_BTC_Address = ('https://bitinfocharts.com/bitcoin/address/'+item.strip()+'-full')
			print(url_of_BTC_Address)
			try:
				BTC_Address = requests.get(url_of_BTC_Address, headers=header)
				info_of_BTC_Address = pd.read_html(BTC_Address.text, parse_dates=True)
				tr = info_of_BTC_Address[2]
				try:
					tr['Cash'] = tr['Balance, USD'].apply(lambda x: x.split('@')[1]).replace('[$,]', '', regex=True).astype(float)
					holder = re.compile("[\(\[].*?[\)\]]")
					tr['Quantity'] = tr['Amount'].replace('[BTC,]', '', regex=True).replace(holder, ' ', regex=True).astype(float)
					tr['Dollar'] = -tr['Quantity'] * tr['Cash']
					profit = tr['Dollar'].sum() - (tr['Balance'].replace('[BTC,]', '', regex=True).astype(float)[0] * tr['Cash'][0])
					print('profit in USD: ' + str(profit))
					if float(profit) > 1000.00:
						info_of_BTC_Address[2].to_csv('BTC_{filename1}.csv'.format(filename1=item))
				except AttributeError:
					error_list = []
					error_list.append(url_of_BTC_Address)
					pass
			except ValueError:
				error_list = []
				error_list.append(url_of_BTC_Address)
				pass




		#wallets = walletlist[1]
		#print("wallet list: " + str(walletlist))

		pg1 += 1
	BTC_address_with_table_error = pd.Dataframe({'Link': error_list, 'Page': pg1})
	BTC_address_with_table_error.to_csv('BTC_address_with_table_error.csv')
smart_wallets(73,100)
