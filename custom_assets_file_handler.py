import pandas
import config
from decimal import Decimal, getcontext
from datetime import date

class CustomAssetsFileHandler:
    def __getFileName(self):
        return config.custom_assets_fileNameBase

    def __getFileData(self):
        filePath = config.app_files_dir + self.__getFileName()
        
        df = pandas.read_csv(filePath, delimiter=';', decimal='.')
        return df
        
    def getPricesForDate(self, assets, date):
        date_str = date.strftime('%d/%m/%Y')
        
        df = self.__getFileData()

        if isinstance(df, pandas.DataFrame):
            filtered_df = df[df['DATA_ATUAL'] == date_str]
            
            for index, row in filtered_df.iterrows():
                if pandas.isnull(row['PRECO']):
                    if pandas.notnull(row['VALOR_INICIO']) & pandas.notnull(row['VALOR_ATUAL']):
                        vl1 = Decimal(row['VALOR_INICIO'])
                        vl2 = Decimal(row['VALOR_ATUAL'])
                        filtered_df.at[index,'PRECO'] = round(vl2 / vl1, 8)

            #print(filtered_df)    
            filtered_df = filtered_df[filtered_df['CODIGO'].isin(assets)]
            return filtered_df[['DATA_ATUAL', 'CODIGO', 'PRECO']].values.tolist()

        return None