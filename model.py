import os
import json
from os import listdir
from os.path import isfile, join
import gensim
import re
os.chdir('/Users/Avijit/Desktop/SMA_InterIIT_2017')

import pandas as pd 

model_csv = pd.read_csv('article_dataframe.csv', sep='\t', encoding='utf-8')

model_csv=model_csv.rename(columns = {u'Impact':u'change'})
effect = []
for i in range(len(model_csv)):
    print i
    try:
        if model_csv['change'][i] >= 0.02:
            effect.append('Positive')
        elif model_csv['change'][i] <= -0.02:
            effect.append('Negative')
        else:
            effect.append('Neutral')
    except:
        continue
model_csv['Impact'] = effect
model = gensim.models.Doc2Vec.load('doc2vec.model')