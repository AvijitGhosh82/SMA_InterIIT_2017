'''
Python code for predicting the relevance class for new news articles using the Boosted Trees Model trained previously
'''
import pandas as pd
import graphlab as gl
import pysentiment as py
from nltk.tokenize import sent_tokenize
import re
from textstat.textstat import textstat
from gensim import corpora, models
import data_clean as dc
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

#Function to take input a dataframe and return a dataframe with all the features as columns
def predict_relevance(df):
	if df.empty:
		return pd.DataFrame()
	
	#Loading data into SFrame
	df[[a for a in df.columns.values]] = df[[a for a in df.columns.values]].astype(str)
	tf = gl.SFrame(data=df)

	#Removing duplicate content and/or headline articles
	tf = tf.add_row_number()
	sf_url = tf[['id','url']]
	sf_other = tf[[a for a in tf.column_names() if a.strip() != 'url']]
	sf_other = sf_other.unique() 
	tf = sf_url.join(sf_other)
	tf = tf.remove_column('id')

	#Removing rows with either content or title as NA/None
	tf = tf.dropna('content', how="any")
	tf = tf.dropna('title', how="any")

	#Loading LDA model for topic modeling, pysentiment module for financial sentiment analysis and the relevance prediction model
	lda = models.ldamodel.LdaModel.load('lda1.model')
	lm = py.LM()
	model = gl.load_model('relevance_model_64feat')

	#Building the LDA model using news articles
	tf['tokens'] = tf['content'].apply(lambda x: dc.tokenize_doc(x,'STEM'))
	tokens_text = [unicode('|'.join(i), errors='replace').split('|') for i in tf['tokens']]
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
		tf['T'+str(i)] = gl.SArray(data=x,dtype=float)


	#Polarity feature extraction from content of news articles
	tf['Polarity_text'] = tf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Polarity'])
	tf['Subjectivity_text'] = tf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Subjectivity'])
	tf['Positive_text_wc'] = tf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Positive'])
	tf['Negative_text_wc'] = tf['content'].apply(lambda x: lm.get_score(lm.tokenize(x))['Negative'])
	tf['Total_text_wc'] = tf['content'].apply(lambda x: len(lm.tokenize(x)))
	tf['Negative_text_rate'] = tf['Negative_text_wc']/tf['Total_text_wc']
	tf['Positive_text_rate'] = tf['Positive_text_wc']/tf['Total_text_wc']
	tf['Max_Polarity'] = tf['content'].apply(lambda x: max([lm.get_score(lm.tokenize(y))['Polarity'] for y in sent_tokenize(x)]))
	tf['Min_Polarity'] = tf['content'].apply(lambda x: min([lm.get_score(lm.tokenize(y))['Polarity'] for y in sent_tokenize(x)]))
	tf['Sentences_wc'] = tf['content'].apply(lambda x: len(sent_tokenize(x)))
	tf['Positive_sentrate'] = tf['Positive_text_wc']/tf['Sentences_wc']
	tf['Negative_sentrate'] = tf['Negative_text_wc']/tf['Sentences_wc']

	#Readability feature extraction from content of news articles
	tf['FRE_text'] = tf['content'].apply(lambda x: textstat.flesch_reading_ease(x))
	tf['FRE_tagged_text'] = tf['FRE_text'].apply(lambda x: 1 if x<100 and x>=90 else 2 if x<90 and x>=80 else 3 if x<80 and x>= 70 else 4 if x<70 and x>=60 else 5 if x<60 and x>=50 else 6 if x<50 and x>=30 else 7)
	tf['FK_text'] = tf['content'].apply(lambda x: int(textstat.flesch_kincaid_grade(x)))
	tf['GFI_text'] = tf['content'].apply(lambda x: textstat.gunning_fog(x))
	tf['SMI_text'] = tf['content'].apply(lambda x: textstat.smog_index(x))
	tf['CLI_text'] = tf['content'].apply(lambda x: textstat.coleman_liau_index(x))
	tf['ARI_text'] = tf['content'].apply(lambda x: int(textstat.automated_readability_index(x)))
	tf['DC_text'] = tf['content'].apply(lambda x: textstat.dale_chall_readability_score(x))
	tf['Difficult_text_wc'] = tf['content'].apply(lambda x: textstat.difficult_words(x))

	#Hand-picked quantitative features - # of percentage occurrences 
	percent_pattern = re.compile('((?:|0|[1-9]\d\d?)(?:\.\d{1,3})?)%')
	tf['Percent_occurrences'] = tf['content'].apply(lambda x: len(percent_pattern.findall(x)))

	#Polarity feature extraction from news headlines
	tf['Polarity_head'] = tf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Polarity'])
	tf['Subjectivity_head'] = tf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Subjectivity'])
	tf['Positive_head_wc'] = tf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Positive'])
	tf['Negative_head_wc'] = tf['title'].apply(lambda x: lm.get_score(lm.tokenize(x))['Negative'])
	tf['Total_head_wc'] = tf['title'].apply(lambda x: len(lm.tokenize(x)))
	tf['Negative_head_rate'] = tf['Negative_head_wc']/tf['Total_head_wc']
	tf['Positive_head_rate'] = tf['Positive_head_wc']/tf['Total_head_wc']

	#Readability feature extraction from news headlines
	tf['FRE_head'] = tf['title'].apply(lambda x: textstat.flesch_reading_ease(x))
	tf['FRE_tagged_head'] = tf['FRE_head'].apply(lambda x: 1 if x<100 and x>=90 else 2 if x<90 and x>=80 else 3 if x<80 and x>= 70 else 4 if x<70 and x>=60 else 5 if x<60 and x>=50 else 6 if x<50 and x>=30 else 7)
	tf['FK_head'] = tf['title'].apply(lambda x: int(textstat.flesch_kincaid_grade(x)))
	tf['GFI_head'] = tf['title'].apply(lambda x: textstat.gunning_fog(x))
	tf['SMI_head'] = tf['title'].apply(lambda x: textstat.smog_index(x))
	tf['CLI_head'] = tf['title'].apply(lambda x: textstat.coleman_liau_index(x))
	tf['ARI_head'] = tf['title'].apply(lambda x: int(textstat.automated_readability_index(x)))
	tf['DC_head'] = tf['title'].apply(lambda x: textstat.dale_chall_readability_score(x))
	tf['Difficult_head_wc'] = tf['title'].apply(lambda x: textstat.difficult_words(x))

	#Predicting relevance class using these features in sorted order of confidence
	tf = tf.add_row_number()
	pred = model.classify(tf)
	pred = pred.add_row_number()
	relevant = pred[pred['class']==1].sort('probability',ascending=False)
	non_relevant = pred[pred['class']==0].sort('probability')
	if relevant.num_rows()>10:
		relevant_news_out = relevant.join(tf)[:10]
	else:
		req_num_non_relevant_news = 10 - relevant.num_rows()
		non_relevant_news = non_relevant[:req_num_non_relevant_news]
		relevant_news = relevant.append(non_relevant_news)
		relevant_news_out = relevant_news.join(tf)

	relevant_out = relevant_news_out[relevant_news_out['class']==1].sort('probability',ascending=False)
	non_relevant_out = relevant_news_out[relevant_news_out['class']==0].sort('probability')
	output_df = relevant_out.append(non_relevant_out)
	output_dataframe = output_df.to_dataframe()
	return output_dataframe
