import requests
import pandas
import os.path
from time import sleep
from zipfile import ZipFile
import settings

class StockQuotes:
    __urlBase = settings.b3_urlBase
    __fileNameBase = settings.b3_fileNameBase

    def __getUrl(self, date):
        return self.__urlBase + self.__getFileName(date)

    def __getFileName(self, date):
        period = date.replace('-','')[4:6] + date.replace('-','')[0:4]
        return self.__fileNameBase.replace('{MMYYYY}', period)

    def __getFileData(self, date):
        fileName = settings.app_files_dir + self.__getFileName(date)

        if not os.path.exists(fileName):
            url = self.__getUrl(date)
            attempts = 1
            error = False

            while attempts > 0:
                try:
                    print('Requesting URL: ' + url)
                    header = requests.head(url)

                    if header.status_code == 200 and header.headers['content-type'] == 'application/x-zip-compressed':
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
                return None

        with ZipFile(fileName, 'r') as zipObj:
            zipObj.extractall(settings.app_files_dir)

        df = pandas.read_fwf(fileName.replace('ZIP','TXT'), names=['type', 'date', 'stock', 'price'], header=None, colspecs=[(0,2), (2,10), (12,24), (109,121)])
        df['price'] = df['price'].map(lambda price: price / 100)
        return df

    def getPricesByMonth(self, stock, date):
        """Returns a DataFrame with prices
        stock -- code of ticker
        function -- StockQuotes.StockQuotesFunction
        """
        df = self.__getFileData(date)

        if isinstance(df, pandas.DataFrame):
            return df[(df['stock'] == stock)]
        
        return None

    def getPriceByDate(self, stock, date):
        """Returns a value or None
        stock -- code of ticker
        function -- StockQuotes.StockQuotesFunction
        date -- string formated as YYYY-MM-DD
        """
        df = self.getPricesByMonth(stock, date)

        if isinstance(df, pandas.DataFrame):
            if len(df) > 0:
                dfOnDate = df[(df['date'] == date.replace('-',''))]
                
                if(len(dfOnDate) == 1):
                    return dfOnDate['price'].iloc[0]
        
        return None

#x = StockQuotes()
#print(x.getPricesByMonth('TGAR11','2020-02-28'))