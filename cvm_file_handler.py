import requests
import pandas
import os
from zipfile import ZipFile
import config
import download_handler
from datetime import date

class CVMFileHandler:
    url = config.cvm_funds_urlBase + config.cvm_funds_fileNameBase
    __urlBase = config.cvm_funds_urlBase
    __fileNameBase = config.cvm_funds_fileNameBase

    def __getUrl(self, date):
        return self.__urlBase + self.__getFileName(date)
        
    def __getFileName(self, date):
        period = date.strftime('%Y%m')
        return self.__fileNameBase.replace('{YYYYMM}', period)

    def __getFileData(self, date):
        filePath = config.app_files_dir + self.__getFileName(date)
        
        if not os.path.exists(filePath):
            url = self.__getUrl(date)
            download_handler.download_file(url, config.app_files_dir, config.app_download_attempts)

            with ZipFile(filePath, 'r') as zip_ref:
                zip_ref.extractall(config.app_files_dir)
                
            os.remove(filePath)

        df = pandas.read_csv(filePath.replace('zip', 'csv'), delimiter=';')

        os.remove(filePath.replace('zip', 'csv'))

        return df
        
    def getPricesForDate(self, assets, date):
        date_str = date.strftime('%Y-%m-%d')
        
        df = self.__getFileData(date)

        if isinstance(df, pandas.DataFrame):
            filtered_df = df[df['DT_COMPTC'] == date_str]
            filtered_df = filtered_df[filtered_df['CNPJ_FUNDO'].isin(assets)]
            return filtered_df[['DT_COMPTC', 'CNPJ_FUNDO', 'VL_QUOTA']].values.tolist()

        return None