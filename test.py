import sys
sys.path.append('../')
import pandas

import quandl
quandl.ApiConfig.api_key = 'KfAoeT8ysydZySAKGaE9'

# data = quandl.get('BSE/BOM533171')
data = quandl.get('BSE/SENSEX')

data.to_csv('sensex.csv', sep='\t', encoding='utf-8')


