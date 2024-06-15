import os
import zipfile
from datetime import datetime

import config
import download_handler
from b3_file_handler import B3FileHandler
from cvm_file_handler import CVMFileHandler
from tesouro_file_handler import TesouroFileHandler
#from custom_assets_file_handler import CustomAssetsFileHandler
from gnucash_handler import GnuCashConn
from gnucash_handler import GnuCashPrice

def numberOfDigits(value):
    return str(value)[::-1].find('.')

date = input('Last business day of month (YYYY-MM-DD): ')
date = datetime.strptime(date, '%Y-%m-%d')

gc = GnuCashConn(config.gnucash_database_path)
gcCommodities = gc.getCommodities(date.strftime('%Y%m%d'))
gcCommoditiesList = gcCommodities.iloc[:, 2].tolist()

brazilianCurrencyGuid = gc.getBrasilianCurrencyGuid()

assetPrices = []

b3Quotes = B3FileHandler()
cvmQuotes = CVMFileHandler()
tesouroQuotes = TesouroFileHandler()
#customQuotes = CustomAssetsFileHandler()

assetPrices = assetPrices + b3Quotes.getPricesForDate(gcCommoditiesList, date)
assetPrices = assetPrices + cvmQuotes.getPricesForDate(gcCommoditiesList, date)
assetPrices = assetPrices + tesouroQuotes.getPricesForDate(gcCommoditiesList, date)
#assetPrices = assetPrices + customQuotes.getPricesForDate(gcCommoditiesList, date)

newPriceList  = []

for indice, c in gcCommodities.iterrows():
    for price in assetPrices:
        if c[2] == price[1]:
            newPrice = GnuCashPrice()
            newPrice.commodity_guid = c[0]
            newPrice.commodity_fullName = c[3]
            newPrice.currency_guid = brazilianCurrencyGuid
            newPrice.date = date.strftime('%Y-%m-%d')
            
            newPrice.denom = int(10 ** numberOfDigits(price[2]))
            newPrice.value = int(price[2] * newPrice.denom)
            
            newPriceList.append(newPrice)
            break

gc.savePrices(newPriceList)

print()
print("Assets NOT found:")
assetsNotFound = [item for item in gcCommoditiesList if not any(item == sublista[1] for sublista in assetPrices)]
for row in assetsNotFound:
    print("- ", row)