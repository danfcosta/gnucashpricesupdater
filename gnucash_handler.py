import sqlite3
import uuid
import pandas as pd
from decimal import Decimal

class GnuCashConn:
    def __init__(self, gnucash_file):
        self.database_path = gnucash_file

    def generateGuid(self):
        return str(uuid.uuid4()).replace('-','')

    def createConn(self):
        return sqlite3.connect(self.database_path)
    
    #data in format YYYYMMDD
    def getCommodities(self, date):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            #cur.execute("select guid, namespace, mnemonic, fullname from commodities where quote_flag = 1")
            #select c.namespace, c.mnemonic, sum(1.00 * s.quantity_num / s.quantity_denom)
            #query = cur.execute("select c.guid, c.namespace, c.mnemonic, c.fullname from splits s inner join transactions t ON (s.tx_guid = t.guid) inner join accounts a ON (s.account_guid = a.guid) inner join commodities c on (c.guid = a.commodity_guid) where cast(substr(replace(replace(replace(post_date, '-', ''), ':', ''), ' ', ''), 1, 8) as integer) <= ? group by c.guid, c.namespace, c.mnemonic, c.fullname having sum(1.00 * s.quantity_num / s.quantity_denom) <> 0", (date,))
            query = cur.execute("select c.guid, c.namespace, c.mnemonic, c.fullname, s.quantity_num, s.quantity_denom from splits s inner join transactions t ON (s.tx_guid = t.guid) inner join accounts a ON (s.account_guid = a.guid) inner join commodities c on (c.guid = a.commodity_guid) where cast(substr(replace(replace(replace(post_date, '-', ''), ':', ''), ' ', ''), 1, 8) as integer) <= ?", (date,))
            df = pd.DataFrame.from_records(data = query.fetchall(), columns = [column[0] for column in query.description])
            
            df["quantity_num"] = df["quantity_num"].apply(Decimal)
            df["quantity_denom"] = df["quantity_denom"].apply(Decimal)

            # Agrupando por guid, namespace, mnemonic, fullname
            df_grouped = df.groupby(["guid", "namespace", "mnemonic", "fullname"])

            df = df_grouped.agg(qtt=('quantity_num', lambda x: (x / df['quantity_denom']).sum())).reset_index()
            return df[df['qtt'] != 0]

    def getBrasilianCurrencyGuid(self):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            cur.execute("select guid from commodities where namespace = 'CURRENCY' and mnemonic = 'BRL'")
            return cur.fetchone()[0]

    def __getPriceByCommodityDate(self, conn, commodity_guid, date):
        cur = conn.cursor()
        cur.execute("select guid, commodity_guid, currency_guid, date, source, type, value_num, value_denom from prices where commodity_guid = ? and substr(date,1, 10) = ?", (commodity_guid, date,))
        return cur.fetchall()

    def getPriceByCommodityDate(self, commodity_guid, date):
        conn = self.createConn()
        with conn:
            return self.__getPriceByCommodityDate(conn, commodity_guid, date)

    def __insertPrice(self, conn, commodity_guid, currency_guid, date, value, denom):
        cur = conn.cursor()
        #chech if guid exists
        guid = ""
        guidExists = True
        while(guidExists == True):
            guid = self.generateGuid()
            rowCount = len(cur.execute("select * from prices where guid = ?", (guid,)).fetchall())
            if rowCount == 0:
                guidExists = False

        cur.execute("insert into prices (guid, commodity_guid, currency_guid, date, source, type, value_num, value_denom) values (?, ?, ?, ?, 'user:price', 'last', ?, ?)", (guid, commodity_guid, currency_guid, date + ' 05:00:00', value, denom,))
        conn.commit()

    def __updatePrice(self, conn, price_guid, value, denom):
        cur = conn.cursor()
        cur.execute("update prices set value_num = ?, value_denom = ? where guid = ?", (value, denom, price_guid,))
        conn.commit()

    #priceList: array of GnuCashPrice
    def savePrices(self, priceList):
        conn = self.createConn()
        with conn:
            for p in priceList:
                tempPrice = self.__getPriceByCommodityDate(conn, p.commodity_guid, p.date)

                #update
                if(len(tempPrice) == 1):
                    self.__updatePrice(conn, tempPrice[0][0], p.value, p.denom)
                    print('[\033[33mU\033[0m] ' + p.commodity_fullName)
                
                #insert
                if len(tempPrice) == 0:
                    self.__insertPrice(conn, p.commodity_guid, p.currency_guid, p.date, p.value, p.denom)
                    print('[\033[34mI\033[0m] ' + p.commodity_fullName)


class GnuCashPrice:
    guid = ''
    commodity_guid = ''
    commodity_fullName = ''
    currency_guid = ''
    date = ''
    source = 'user:price'
    type = 'last'
    value = 0
    denom = 0