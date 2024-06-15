#app configuratin
app_files_dir = './download/'
app_download_attempts = 3
gnucash_database_path = 'LOCAL_PATH_FILE.gnucash' #only SQLite Format

#CVM configuration
cvm_funds_urlBase = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/'
cvm_funds_fileNameBase = 'inf_diario_fi_{YYYYMM}.zip'

#B3 configuration
b3_urlBase = 'http://bvmf.bmfbovespa.com.br/InstDados/SerHist/'
b3_fileNameBase = 'COTAHIST_M{MMYYYY}.ZIP'

#Tesouro Direto configuration
tesouro_urlBase = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/'
tesouro_fileNameBase = 'PrecoTaxaTesouroDireto.csv'

#Custom Assets
custom_assets_fileNameBase = 'custom_assets.csv'