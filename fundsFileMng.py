import requests
import pandas
import settings
import os.path
from time import sleep

class FundsFileMng:
    url = settings.cvm_funds_urlBase + settings.cvm_funds_fileNameBase
    __csvDf = None
    __urlBase = settings.cvm_funds_urlBase
    __fileNameBase = settings.cvm_funds_fileNameBase

    def __getFileName(self, date):
        period = date.replace('-','')[0:4] + date.replace('-','')[4:6]
        return self.__fileNameBase.replace('{YYYYMM}', period)

    def __getUrl(self, date):
        return self.__urlBase + self.__getFileName(date)

    def loadFile(self, date):
        fileName = settings.app_files_dir + self.__getFileName(date)

        if not os.path.exists(fileName):
            url = self.__getUrl(date)
            attempts = 3
            error = False

            while attempts > 0:
                try:
                    print('Requesting URL: ' + url)
                    header = requests.head(url)

                    if header.status_code == 200 and header.headers['content-type'] == 'text/csv':
                        request = requests.get(url)

                        with open(fileName, 'wb') as f:
                            f.write(request.content)
                            attempts = 0
                            error = False
                    else:
                        raise Exception("URL not found!")
                except Exception as ex:
                    attempts = attempts - 1
                    error = True
                    print(ex)
                    sleep(10)
        
            if error:
                return False

        self.__csvDf = pandas.read_csv(fileName, delimiter=';')
        return True

    def getQuotesByCnpjDate(self, cnpj, date):
        return self.__csvDf[(self.__csvDf['CNPJ_FUNDO'] == cnpj) & (self.__csvDf['DT_COMPTC'] == date)]