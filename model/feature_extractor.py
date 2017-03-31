import pandas as pd
import graphlab as gl
import pysentiment as py
from nltk.tokenize import sent_tokenize
import re
from textstat.textstat import textstat
from gensim import corpora, models
import data_clean as dc
import numpy as np

#Loading data into SFrame
df = pd.read_csv('key_dev_news.txt',sep='\t',encoding='latin-1')
sf = gl.SFrame(data=df)

#Loading LDA model for topic modeling and pysentiment module for financial sentiment analysis
lm = py.LM()
lda = models.ldamodel.LdaModel.load('lda1.model')

#Building the LDA model using news articles
sf['tokens'] = sf['content'].apply(lambda x: dc.tokenize_doc(x,'STEM'))
tokens_text = [unicode('|'.join(i), errors='replace').split('|') for i in sf['tokens']]
dictionary = corpora.Dictionary(tokens_text)
corpus = [dictionary.doc2bow(text) for text in tokens_text]
ldamat = lda[corpus]

#Building LDA topic arrays per topic
topic_arrays = np.zeros((30,len(ldamat)))
for i,x in enumerate(ldamat):
	for topic_no,contrib in x:
 		topic_arrays[topic_no,i] = contrib

#Adding LDA topic arrays as feature columns as 'Tx'
for i,x in enumerate(topic_arrays):
	sf['T'+str(i)] = gl.SArray(data=x,dtype=float)

#Setting the threshold for 'relevancy' i.e. if %change in Abnormal Return is within the threshold then 0 (irrelevant news) otherwise 1 (relevant news)
sf['Output'] = sf['abnormal_return'].apply(lambda x: 1 if x>1.25 or x<-5 else 0)

#Polarity feature extraction from content of news articles
sf['Polarity_text'] = sf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Polarity'])
sf['Subjectivity_text'] = sf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Subjectivity'])
sf['Positive_text_wc'] = sf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Positive'])
sf['Negative_text_wc'] = sf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Negative'])
sf['Total_text_wc'] = sf['content'].apply(lambda x: len(lm.tokenize(x)))
sf['Negative_text_rate'] = sf['Negative_text_wc']/sf['Total_text_wc']
sf['Positive_text_rate'] = sf['Positive_text_wc']/sf['Total_text_wc']
sf['Max_Polarity'] = sf['content'].apply(lambda x: max([lm.get_score(lm.tokenize(y))['Polarity'] for y in sent_tokenize(x)]))
sf['Min_Polarity'] = sf['content'].apply(lambda x: min([lm.get_score(lm.tokenize(y))['Polarity'] for y in sent_tokenize(x)]))
sf['Sentences_wc'] = sf['content'].apply(lambda x: len(sent_tokenize(x)))
sf['Positive_sentrate'] = sf['Positive_text_wc']/sf['Sentences_wc']
sf['Negative_sentrate'] = sf['Negative_text_wc']/sf['Sentences_wc']

#Readability feature extraction from content of news articles
sf['FRE_text'] = sf['content'].apply(lambda x: textstat.flesch_reading_ease(x))
sf['FRE_tagged_text'] = sf['FRE_text'].apply(lambda x: 1 if x<100 and x>=90 else 2 if x<90 and x>=80 else 3 if x<80 and x>= 70 else 4 if x<70 and x>=60 else 5 if x<60 and x>=50 else 6 if x<50 and x>=30 else 7)
sf['FK_text'] = sf['content'].apply(lambda x: int(textstat.flesch_kincaid_grade(x)))
sf['GFI_text'] = sf['content'].apply(lambda x: textstat.gunning_fog(x))
sf['SMI_text'] = sf['content'].apply(lambda x: textstat.smog_index(x))
sf['CLI_text'] = sf['content'].apply(lambda x: textstat.coleman_liau_index(x))
sf['ARI_text'] = sf['content'].apply(lambda x: int(textstat.automated_readability_index(x)))
sf['DC_text'] = sf['content'].apply(lambda x: textstat.dale_chall_readability_score(x))
sf['Difficult_text_wc'] = sf['content'].apply(lambda x: textstat.difficult_words(x))

#Hand-picked quantitative features - # of percentage occurrences 
percent_pattern = re.compile('((?:|0|[1-9]\d\d?)(?:\.\d{1,3})?)%')
sf['Percent_occurrences'] = sf['content'].apply(lambda x: len(percent_pattern.findall(x)))

#Polarity feature extraction from news headlines
sf['Polarity_head'] = sf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Polarity'])
sf['Subjectivity_head'] = sf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Subjectivity'])
sf['Positive_head_wc'] = sf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Positive'])
sf['Negative_head_wc'] = sf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Negative'])
sf['Total_head_wc'] = sf['title'].apply(lambda x: len(lm.tokenize(x)))
sf['Negative_head_rate'] = sf['Negative_head_wc']/sf['Total_head_wc']
sf['Positive_head_rate'] = sf['Positive_head_wc']/sf['Total_head_wc']

#Readability feature extraction from news headlines
sf['FRE_head'] = sf['title'].apply(lambda x: textstat.flesch_reading_ease(x))
sf['FRE_tagged_head'] = sf['FRE_head'].apply(lambda x: 1 if x<100 and x>=90 else 2 if x<90 and x>=80 else 3 if x<80 and x>= 70 else 4 if x<70 and x>=60 else 5 if x<60 and x>=50 else 6 if x<50 and x>=30 else 7)
sf['FK_head'] = sf['title'].apply(lambda x: int(textstat.flesch_kincaid_grade(x)))
sf['GFI_head'] = sf['title'].apply(lambda x: textstat.gunning_fog(x))
sf['SMI_head'] = sf['title'].apply(lambda x: textstat.smog_index(x))
sf['CLI_head'] = sf['title'].apply(lambda x: textstat.coleman_liau_index(x))
sf['ARI_head'] = sf['title'].apply(lambda x: int(textstat.automated_readability_index(x)))
sf['DC_head'] = sf['title'].apply(lambda x: textstat.dale_chall_readability_score(x))
sf['Difficult_head_wc'] = sf['title'].apply(lambda x: textstat.difficult_words(x))

#List of features used to train the Boosted Trees Classifier with optimal parameters obtained using grid search
features_list = ['Polarity_text', 'Subjectivity_text','Polarity_head', 'Subjectivity_head','Positive_text_wc','Negative_text_wc','Positive_head_wc','Negative_head_wc','Negative_head_rate','Positive_head_rate','Positive_text_rate','Negative_text_rate','Max_Polarity','Min_Polarity','Sentences_wc','Positive_sentrate','Negative_sentrate','Percent_occurrences','FRE_tagged_text','FK_text','GFI_text','SMI_text','CLI_text','ARI_text','DC_text','Difficult_text_wc','FRE_tagged_head','FK_head','GFI_head','SMI_head','CLI_head','ARI_head','DC_head','Difficult_head_wc']
for i in range(0,30):
	features_list.append('T'+str(i))	

train, test = sf.random_split(0.8)
model = gl.boosted_trees_classifier.create(train, target='Output', max_iterations=15, class_weights='auto', verbose=True, random_seed=18, features= features_list)
results = model.evaluate(test)
print(results)
#model = gl.classifier.create(sf, target='Output',features=features_list)
#results = model.evaluate(sf)
#print(results)