import nltk
import re
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import brown
import numpy as np
import pandas as pd
import string
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# url = 'https://www.bloomberg.com/news/articles/2017-03-14/singapore-tops-tokyo-as-asia-s-city-with-best-quality-of-living'
# doc=Article(url)
# doc.download()
# doc.parse()
# doc = doc.text
# doc = 'ffsfgsdfsdf'

word_punct_tokenizer = WordPunctTokenizer()
porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
# remove it if you need punctuation
stop_words.update([',', '"', '?', '!', ':', ';',
                   '(', ')', '[', ']', '{', '}', '&'])


# splits sentences of a doc where each sentence is list of words ; does
# stemming
def sentence_tokenize(doc, _type='LEMMA'):
    sent_tokenize_list = sent_tokenize(doc)
    sent_list = []

    for sentence in sent_tokenize_list:
        sentence = [word for word in nltk.word_tokenize(
            sentence.lower()) if word not in string.punctuation]
        if _type == 'STEM':
            sentence = [porter_stemmer.stem(word) for word in sentence]
        else:
            wordpos = nltk.pos_tag(sentence)
            word_root_list = []
            for word, postag in wordpos:
                tag = 'n'
                if 'VB' in postag:
                    tag = 'v'
                word_root_list.append(wordnet_lemmatizer.lemmatize(word, tag))
            sentence = word_root_list
        sent_list.append(sentence)
    return sent_list


def tokenize_sentence(sentence, _type='LEMMA'):

    word_tokenize_list = [w.lower()
                          for w in word_punct_tokenizer.tokenize(sentence)]
    # remove non alpha num hiphen using regex
    word_tokenize_list = [w for w in word_tokenize_list if re.search(
        '[A-Za-z0-9]+[._-]*[A-Za-z0-9]*', w) is not None]
    if _type is 'STEM':
        word_root_list = [porter_stemmer.stem(
            word) for word in word_tokenize_list]
    else:
        wordpos = nltk.pos_tag(word_tokenize_list)
        word_root_list = []
        for word, postag in wordpos:
            tag = 'n'
            if 'VB' in postag:
                tag = 'v'
            word_root_list.append(wordnet_lemmatizer.lemmatize(word, tag))
    return word_root_list


def tokenize_doc(doc, _type='LEMMA'):
    sent_tokenize_list = sent_tokenize(doc)
    wordlist = []

    for sentence in sent_tokenize_list:
        word_tokenize_list = [w.lower() for w in word_punct_tokenizer.tokenize(
            sentence) if w.lower() not in stop_words]
        # remove non alpha num hiphen using regex
        word_tokenize_list = [w for w in word_tokenize_list if re.search(
            '[A-Za-z0-9]+[._-]*[A-Za-z0-9]*', w) is not None]
        if _type is 'STEM':
            word_root_list = []
            for word in word_tokenize_list:
                try:
                    word_root_list.append(
                        porter_stemmer.stem(word.encode('utf8')))
                except:
                    pass
        else:
            wordpos = nltk.pos_tag(word_tokenize_list)
            word_root_list = []
            for word, postag in wordpos:
                tag = 'n'
                if 'VB' in postag:
                    tag = 'v'
                word_root_list.append(wordnet_lemmatizer.lemmatize(word, tag))
        wordlist.extend(word_root_list)
        # print word_lemmatize_list
    return wordlist

# print(sentence_tokenize(doc))

# Dow 30 Search List
D30 = {}
Dow_30 = """Apple,aapl
American Express,American_Express,Amex,axp
Boeing,ba
Caterpillar,cat
Cisco,csco
Chevron,cvx
Coca-Cola,ko
DuPont,dd
ExxonMobil,Exxon Mobil,Exxon xom
General Electric,General_Electric,ge
Goldman Sachs,Goldman_Sachs,gs
Home Depot,Home_Depot,hd
IBM,ibm
Intel,intc
Johnson & Johnson,J&J,jnj
JPMorgan Chase,jpmc,jpm
McDonald's,McDonalds,McDonald,mcd
3M Company,mmm
Merck,mrk
Microsoft,msft
Nike,nke
Pfizer,pfe
Procter & Gamble,p&g,pg
The Travelers,trv
UnitedHealth,United_Health,unh
United Technologies,United_Technologies,utx
Visa,v
Verizon,vz
Wal-Mart,Walmart,wmt
Walt Disney,Disney,dis"""
f = Dow_30.split('\n')
#f = open('Dow30.txt','r')
for line in f:
    l = [w.lower().strip() for w in line.split(',')]
    #l.extend(similar_by_vector(vector, topn=10, restrict_vocab=None)(l[0]))
    D30[l[0]] = l


def search_doc(doc, searchlist):
    for searchterm in searchlist:
        if re.search(searchterm, doc) is not None:
            return True
    return False


def tag_corpus(corpus):
    indices = []
    dow_tags = []
    for i, doc in enumerate(corpus):
        for key in D30.keys():
            found = search_doc(D30[key])
            if found is True:
                indices.append(i)
                dow_tags.append(key)
    corpus = corpus[indices]
    return (corpus, tags)


from sklearn.feature_extraction.text import CountVectorizer


def get_posneglist(corpus, labels):
    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=stop_words,
                                 max_features=5000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    WC_mat = vectorizer.fit_transform(corpus)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    WC_mat = np.asarray(WC_mat.toarray()).astype('bool')

    # doc_wcount = []
    # for doc in corpus:
    # 	wcount_dic = {}
    # 	wordlist = tokenize_doc(doc)
    # 	for word in wordlist:
    # 		if word in wcount_dic:
    # 			wcount_dic[word]+=1

    # Take a look at the words in the vocabulary
    vocab = vectorizer.get_feature_names()
    C = {}
    for i in range(WC_mat.shape[1]):
        C[vocab[i]] = WC_mat[:, i]
    C['label'] = np.asarray(labels)
    df = pd.DataFrame(C)
    dfpos = df[df.label == 1]
    dfneg = df[df.label]
