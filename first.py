import json
from os import listdir
from os.path import isfile, join
import gensim
import re
import pandas
LabeledSentence	 = gensim.models.doc2vec.LabeledSentence
# import pandas as pd 

# Reading data
# with open('FT_Database/date_id_list.txt') as index_file:
# 	date_index =index_file.read().split('\n') 

def load_data(dir):
	with open(dir) as data_file:
		data = json.load(data_file)
	return data

class DocIterator(object):
	
	def __init__(self, doc_list, labels_list):
		self.labels_list = labels_list
		self.doc_list = doc_list

	def __iter__(self):
		for idx, doc in enumerate(self.doc_list):
			yield LabeledSentence(words=doc.split(), tags=[self.labels_list[idx]])

def train_model(data):
	combined_data = []
	labels = data.keys()
	for key in labels:
		doc = clean_doc(data[key]['content'])
		combined_data.append(doc)

	it = DocIterator(combined_data,labels)
	model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=8,alpha=0.025, min_alpha=0.025)
	model.build_vocab(it)
	for epoch in range(10):
		model.train(it)
		model.alpha -= 0.002 
		model.min_alpha = model.alpha 
		model.train(it)
	model.save("doc2vec.model")

	return model


def load_model():
	model = gensim.models.Doc2Vec.load('doc2vec.model')
	# labels = data.keys()
	# return model,labels
	return model

def clean_doc(doc):
	ret = re.sub("[^a-zA-Z0-9 \n]+","",doc)
	ret = re.sub("[\n]+"," ",ret)
	ret = ret.lower()
	return ret
	
def top_n_similar_docs(model,query_doc,n):
	query_doc = clean_doc(query_doc)	
	test_vec = model.infer_vector(query_doc.split())
	similars = model.docvecs.most_similar(positive = [test_vec],topn = n)
	# similars is ID,cosine_similarity
	return similars

def top_n_relevant_docs(model,query_word,n):
	# again format is DocID,cosine_similarity
	return model.docvecs.most_similar([model[query_word]], topn = n)


def get_vectors(model):
	return model.docvecs.doctag_syn0
	
def main():
	# data = load_data('FT_Database/filtered.json')
	# do training only when you need to train fresh. 
	# Else use load_model for a pretrained model
	# model = train_model(data)
	# model = train_model(data)
	# model,labels = load_model(data)
	model = load_model()

	model_csv = pandas.read_csv('article_dataframe.csv', sep='\t', encoding='utf-8')
	model_csv=model_csv.rename(columns = {u'Impact':u'change'})
	effect = []
	vector = []
	for i in range(len(model_csv)):
		print i
		vector.append(model.infer_vector(model_csv['content'][i].split()))
			
		if model_csv['change'][i] >= 0.02:
			effect.append('Positive')
		elif model_csv['change'][i] <= -0.02:
			effect.append('Negative')
		else:
			effect.append('Neutral')
		

	model_csv['Impact'] = effect
	model_csv['vector'] = vector
	
	for i in range(10):
		print model_csv['vector'][i]
	# vector = []

	# print model_csv[]
	# print model_csv[data.keys()[1]]
	# # finding vectors of the training docs
	# train_vecs = get_vectors(model)
	# print train_vecs[0]
	# # for finding a doc similar to other doc
	# doc = open('goog_doc.txt')
	# test_doc = doc.read()
	# similars = top_n_similar_docs(model,test_doc,10)
	# # print data[similars[0][0]]['content']

	# # for finding docs relevant to a given query word
	# docs_from_word = top_n_relevant_docs(model,'microsoft',10)
	# # print data[docs_from_word[0][0]]['content']
	model_csv.to_csv('article_dataframe.csv', sep='\t', encoding='utf-8')



	
if __name__ == '__main__':
	main()