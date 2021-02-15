#app configuratin
app_files_dir = './files/'
gnucash_database_path = '...'
app_download_attempts = 3

#CVM configuration
cvm_funds_urlBase = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/'
cvm_funds_fileNameBase = 'inf_diario_fi_{YYYYMM}.csv'

#B3 configuratin
b3_urlBase = 'http://bvmf.bmfbovespa.com.br/InstDados/SerHist/'
b3_fileNameBase = 'COTAHIST_M{MMYYYY}.ZIP'

#GNUCash - Groups of Commodities
FUNDS = ['FUNDO RF','FUNDO MULTI','PREVIDENCIA']
STOCKS = ['ACAO','OPCAO','FII']