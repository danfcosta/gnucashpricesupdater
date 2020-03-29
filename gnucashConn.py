import sqlite3
import uuid

class GnuCashConn:
    database_path = ""

    def generateGuid(self):
        return str(uuid.uuid4()).replace('-','')

    def createConn(self):
        return sqlite3.connect(self.database_path)
    
    def getCommodities(self):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            cur.execute("select guid, namespace, mnemonic, fullname from commodities where namespace in ('FUNDO RF','FUNDO MULTI','PREVIDENCIA')")
            return cur.fetchall()

    def getBrasilianCurrencyGuid(self):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            cur.execute("select guid from commodities where namespace = 'CURRENCY' and mnemonic = 'BRL'")
            return cur.fetchone()[0]

    def getPriceByCommodityDate(self, commodity_guid, date):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            cur.execute("select guid, commodity_guid, currency_guid, date, source, type, value_num, value_denom from prices where commodity_guid = ? and substr(date,1, 10) = ?", (commodity_guid, date,))
            return cur.fetchall()

    def insertPrice(self, commodity_guid, currency_guid, date, value, denom):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            #chech if guid exists
            guid = ""
            guidExists = True
            while(guidExists == True):
                guid = self.generateGuid()
                rowCount = len(cur.execute("select * from prices where guid = ?", (guid,)).fetchall())
                if rowCount == 0:
                    guidExists = False

            cur.execute("insert into prices (guid, commodity_guid, currency_guid, date, source, type, value_num, value_denom) values (?, ?, ?, ?, 'user:price', 'last', ?, ?)", (guid, commodity_guid, currency_guid, date, value, denom,))
            conn.commit()

    def updatePrice(self, price_guid, value, denom):
        conn = self.createConn()
        with conn:
            cur = conn.cursor()
            cur.execute("update prices set value_num = ?, value_denom = ? where guid = ?", (value, denom, price_guid,))
            conn.commit()