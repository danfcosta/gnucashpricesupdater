import pandas
import sqlite3
import settings
from gnucashConn import GnuCashConn
from gnucashConn import GnuCashPrice
from fundsFileMng import FundsFileMng
from stockQuotes import StockQuotes

#date = '2020-12-30'
date = input('Data de final de mes (YYYY-MM-DD): ')

def numberOfDigits(value):
    return str(value)[::-1].find('.')

period = date.replace('-','')[0:6]

fundsFileMng = FundsFileMng()

if not fundsFileMng.loadFile(period):
    exit('CVS file not available!')

gc = GnuCashConn()
stockQuotes = StockQuotes()

brazilianCurrencyGuid = gc.getBrasilianCurrencyGuid()
commodities = gc.getCommodities(date.replace('-',''))
newPriceList = []

for c in commodities:
    newPrice = GnuCashPrice()
    newPrice.commodity_guid = c[0]
    newPrice.commodity_fullName = c[3]
    newPrice.currency_guid = brazilianCurrencyGuid
    newPrice.date = date

    if c[1] in settings.FUNDS:
        results = fundsFileMng.getQuotesByCnpjDate(c[2], date)
        if len(results) == 1:
            price = results['VL_QUOTA'].iloc[0]
            newPrice.denom = int(10 ** numberOfDigits(price))
            newPrice.value = int(price * newPrice.denom)
            newPriceList.append(newPrice)
            print('Price found: ' + newPrice.commodity_fullName)
        else:
            print('\33[31mPrice NOT found: ' + newPrice.commodity_fullName)

    if c[1] in settings.STOCKS:
        result = stockQuotes.getPriceByDate(c[2], date)
        if result != None:
            newPrice.denom = int(10 ** numberOfDigits(result))
            newPrice.value = int(result * newPrice.denom)
            newPriceList.append(newPrice)
            print('Price found: ' + newPrice.commodity_fullName + '\033[0m')
        else:
            print('\33[31mPrice NOT found: ' + newPrice.commodity_fullName + '\033[0m')


if len(newPriceList) > 0:
    gc.savePrices(newPriceList)