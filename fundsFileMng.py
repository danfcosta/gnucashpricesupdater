import requests
import pandas

class FundsFileMng:
    url = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_YYYYMM.csv'

    def downloadFile(self, period):
        url = self.url.replace('YYYYMM',period)

        if requests.head(url).status_code == 200:
            return pandas.read_csv(url, delimiter=';')
        
        return None

    def getQuotesByCnpjDate(self, quotesDF, cnpj, date):
        return quotesDF[(quotesDF['CNPJ_FUNDO'] == cnpj) & (quotesDF['DT_COMPTC'] == date)]