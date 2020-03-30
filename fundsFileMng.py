import requests
import pandas
import settings

class FundsFileMng:
    url = settings.cvm_funds_url
    __csvDf = None

    def loadFile(self, period):
        url = self.url.replace('{YYYYMM}',period)
        print('Requesting URL: ' + url)
        if requests.head(url).status_code == 200:
            self.__csvDf = pandas.read_csv(url, delimiter=';')
            return True
        else:
            return False

    def getQuotesByCnpjDate(self, cnpj, date):
        return self.__csvDf[(self.__csvDf['CNPJ_FUNDO'] == cnpj) & (self.__csvDf['DT_COMPTC'] == date)]