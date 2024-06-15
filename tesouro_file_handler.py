import requests
import pandas
import os
import config
import download_handler
from datetime import date

class TesouroFileHandler:
    __urlBase = config.tesouro_urlBase
    __fileNameBase = config.tesouro_fileNameBase

    def __getUrl(self):
        return self.__urlBase + self.__getFileName()
        
    def __getFileName(self):
        return self.__fileNameBase

    def __getFileData(self):
        filePath = config.app_files_dir + self.__getFileName()
        
        if not os.path.exists(filePath):
            url = self.__getUrl()
            download_handler.download_file(url, config.app_files_dir, config.app_download_attempts)

        df = pandas.read_csv(filePath, delimiter=';', decimal=',')
        os.remove(filePath)

        return df
        
    def getPricesForDate(self, assets, date):
        date_str = date.strftime('%d/%m/%Y')
        
        df = self.__getFileData()

        if isinstance(df, pandas.DataFrame):
            df['CodigoTitulo'] = df['Tipo Titulo'] + ' (' + df['Data Vencimento'] + ')'
            filtered_df = df[df['Data Base'] == date_str]
            filtered_df = filtered_df[filtered_df['CodigoTitulo'].isin(assets)]
            return filtered_df[['Data Base', 'CodigoTitulo', 'PU Venda Manha']].values.tolist()

        return None