import requests
import pandas
import os
from zipfile import ZipFile
import config
import download_handler
from datetime import date

class B3FileHandler:
    __urlBase = config.b3_urlBase
    __fileNameBase = config.b3_fileNameBase

    def __getUrl(self, date):
        return self.__urlBase + self.__getFileName(date)

    def __getFileName(self, date):
        period = date.strftime('%m%Y')
        return self.__fileNameBase.replace('{MMYYYY}', period)

    def __getFileData(self, date):
        filePath = config.app_files_dir + self.__getFileName(date)

        if not os.path.exists(filePath):
            url = self.__getUrl(date)
            download_handler.download_file(url, config.app_files_dir, config.app_download_attempts)

            with ZipFile(filePath, 'r') as zip_ref:
                zip_ref.extractall(config.app_files_dir)
                
            os.remove(filePath)

        # Lê o arquivo e armazena os dados em um dicionário
        df = pandas.read_fwf(filePath.replace('ZIP', 'TXT'), names=['type', 'date', 'stock', 'price'], header=None,
                             colspecs=[(0, 2), (2, 10), (12, 24), (108, 121)])
        df['price'] = df['price'].map(lambda price: price / 100)

        os.remove(filePath.replace('ZIP', 'TXT'))
        
        return df

    def getPricesForDate(self, assets, date):
        date_str = date.strftime('%Y%m%d')
        
        df = self.__getFileData(date)

        if isinstance(df, pandas.DataFrame):
            filtered_df = df[df['date'] == date_str]
            filtered_df = filtered_df[filtered_df['stock'].isin(assets)]
            return filtered_df[['date', 'stock', 'price']].values.tolist()

        return None
