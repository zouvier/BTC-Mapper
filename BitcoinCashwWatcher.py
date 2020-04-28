'''# By Zoumana Cisse. Huge thanks to Python for trading on youtube (https://www.youtube.com/channel/UCFGPA5ZV9BZIhR7w8EbS-hg/featured)
The main purpose of this program is to get a list of bit coin addresses that are making positive gains in relation to USD/BTC by day trading
It will go through X amount of pages on the Richest bitcoin addresses and save those with a positive net balance through out the years
 '''
# TODO: add more descriptive comments and clean up the code


import datetime
import pandas as pd
import requests
from time import sleep
import re

#set these yourself
pg1 = 0
pg2 = 100

def BCHsmart_wallets(pg1, pg2):
    # do not change any of these values
    try:
        pg1 = int(pg1)
        pg2 = int(pg2)
        ttrouble_counter = 0
        trouble_counter = 0
        tracker = 0
        richWallet = []
        dollars = []
        errorWallet = []
        pgnum = []
        pgnum1 = []
        pageHolder = (int(pg2) - int(pg1))+1
        pgcount = 0

        # set which page to start on ( the program will go through the pages in ascending order)
        #page = 1
        page = int(pg1)
        # gives a unique name to a file using the date
        filename = 'BCH_smart_Wallet' + str(datetime.datetime.now().date())
        filename_error = 'BCH_error_Wallet' + str(datetime.datetime.now().date())

        while page <= int(pg2):
            page += 1
            pgcount +=1
            print('page: ' + str(pgcount) + '/' + str(pageHolder))
            sleep(5)
            url = 'https://bitinfocharts.com/top-100-richest-bitcoin%20cash-addresses-' + str(page) + '.html'
            # header is used to trick the site into thinking you're an actual person and not a program
            header = {
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"
            }
            r = requests.get(url, headers=header)
            walletlist = pd.read_html(r.text, parse_dates=True)
            wallets = walletlist[1]
            try:
                wallets.columns = ['Number', 'Address', 'Balance', '% of coins', 'First In', 'Last In', 'Number Of Ins','First Out' , 'Last Out', 'Number Of Outs']
                wallets['Number Of Outs'].dropna(how='all', inplace=True)
                traders = wallets[(wallets['Last Out'] > '2015-01-01') & (wallets['Number Of Outs'] > 10)]
                for j in range(len(traders['Address'])):
                        try:
                            sleep(2)
                            urljoin = ('https://bitinfocharts.com/bitcoin%20cash/address/' + traders['Address'].values[j]).split('wallet')[0]
                            url2 = urljoin
                            #print(url2)
                            r2 = requests.get(url2, headers=header)
                            wal1 = pd.read_html(r2.text)
                            tr = wal1[2]
                            tr['Cash'] = tr['Balance, USD'].apply(lambda x: x.split('@')[1]).replace('[$,]', '', regex=True).astype(float)
                            holder = re.compile("[\(\[].*?[\)\]]")
                            tr['Quantity'] = tr['Amount'].replace('[BCH,]', '', regex=True).replace(holder,' ', regex=True).astype(float)
                            tr['Dollar'] = -tr['Quantity']*tr['Cash']
                            profit = tr['Dollar'].sum() - (tr['Balance'].replace('[BCH,]', '', regex=True).astype(float)[0] * tr['Cash'][0])
                            print('profit in USD: '+str(profit))
                            if float(profit) > 1000.00:
                                richWallet.append(urljoin)
                                dollars.append(profit)
                                pgnum1.append(page)
                                richTrader = pd.DataFrame({'URL Link': richWallet, 'Profited': dollars, 'Page': pgnum1})
                                richTrader.to_csv('{file1}.csv'.format(file1=filename))
                        except:
                            try:
                                #Tracker is used to keep note at which point did a certain address fail
                                # (majority tend to fail after tracker 3, before tracker 4)
                                url2 = url2 + '-full'
                                tracker = 1
                                r2 = requests.get(url2, headers=header)
                                tracker = 2
                                sleep(5)
                                tracker = 3
                                wal1 = pd.read_html(r2.text)
                                tracker = 4
                                tr = wal1[2]
                                tracker = 5
                                tr['Cash'] = tr['Balance, USD'].apply(lambda x: x.split('@')[1]).replace('[$,]', '', regex=True).astype(float)
                                tracker = 6
                                holder = re.compile("[\(\[].*?[\)\]]")
                                tr['Quantity'] = tr['Amount'].replace('[BCH,]', '', regex=True).replace(holder,' ', regex=True).astype(float)
                                tracker = 7
                                tr['Dollar'] = -tr['Quantity']*tr['Cash']
                                tracker = 8
                                profit = tr['Dollar'].sum()-(tr['Balance'].replace('[BCH,]', '', regex=True).astype(float)[0]*tr['Cash'][0])
                                tracker = 9
                                print('profit in USD: '+str(profit))
                                if float(profit) > 1000.00:
                                    richWallet.append(urljoin)
                                    dollars.append(profit)
                                    pgnum1.append(page)
                                    richTrader = pd.DataFrame({'URL Link': richWallet, 'Profited': dollars, 'Page': pgnum1})
                                    # make sure that you change the name of the program each time
                                    richTrader.to_csv('{file1}.csv'.format(file1=filename))
                            except:
                                trouble_counter += 1
                                errorWallet.append(url2)
                                pgnum.append(page)
                                error_trader = pd.DataFrame({'URL LINK': errorWallet, 'Page': pgnum})
                                error_trader.to_csv('{file}.csv'.format(file=filename_error))
                                print(url2)
                                print("Failed at tracker " + str(tracker))
                                print("trouble counter at:" + str(trouble_counter))

            except:
                # Called when there is trouble with the table data
                ttrouble_counter += 1
                errorWallet.append(url)
                pgnum.append(page)
                error_trader = pd.DataFrame({'URL LINK': errorWallet, 'Page': pgnum})
                error_trader.to_csv('table_{file}.csv'.format(file=filename_error))
                print(url)
                print('Table Problem')
                print("trouble counter for table at:" + str(ttrouble_counter))
    finally:
        print('Done')

BCHsmart_wallets(pg1,pg2)

# un comment if you want to get a basic over run of which accounts are profitable
'''richTrader = pd.DataFrame({'URL Link': richWallet, 'Profited': dollars})
richTrader.to_csv('List.csv')
print(richTrader)'''
