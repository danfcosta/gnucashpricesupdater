import pandas
import sqlite3
from gnucashConn import GnuCashConn
from fundsFileMng import FundsFileMng

date = '2020-03-31'

def numberOfDigits(value):
    return str(value)[::-1].find('.')

period = date.replace('-','')[0:6]

fundsFileMng = FundsFileMng()

df = fundsFileMng.downloadFile(period)

if not isinstance(df, pandas.DataFrame):
    exit('CVS file not available!')

gc = GnuCashConn()
brazilianCurrencyGuid = gc.getBrasilianCurrencyGuid()
commodities = gc.getCommodities()

for c in commodities:
    results = fundsFileMng.getQuotesByCnpjDate(df, c[2], date)
    if len(results) == 1:
        price = results['VL_QUOTA'].iloc[0]
        denom = int(10 ** numberOfDigits(price))
        value = int(price * denom)

        gcPrice = gc.getPriceByCommodityDate(c[0], date)

        if len(gcPrice) == 1:
            #update
            gc.updatePrice(gcPrice[0][0], value, denom)
            print(c[3] + ' - update')

        if len(gcPrice) == 0:
            #insert
            gc.insertPrice(c[0], brazilianCurrencyGuid, date + ' 05:00:00', value, denom)
            print(c[3] + ' - insert')