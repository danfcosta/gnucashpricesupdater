import sqlite3
import uuid
import settings

class GnuCashConn:
    database_path = settings.gnucash_database_path

    def generateGuid(self):
        return str(uuid.uuid4()).replace('-','')

    def createConn(self):
        return sqlite3.connect(self.database_path)
    
    def getCommodities(self):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            cur.execute("select guid, namespace, mnemonic, fullname from commodities")
            return cur.fetchall()

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

    def savePrices(self, priceList):
        conn = self.createConn()
        with conn:
            for p in priceList:
                tempPrice = self.__getPriceByCommodityDate(conn, p.commodity_guid, p.date)

                #update
                if(len(tempPrice) == 1):
                    self.__updatePrice(conn, tempPrice[0][0], p.value, p.denom)
                    print(p.commodity_fullName + ' - update')
                
                #insert
                if len(tempPrice) == 0:
                    self.__insertPrice(conn, p.commodity_guid, p.currency_guid, p.date, p.value, p.denom)
                    print(p.commodity_fullName + ' - insert')


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