# Script modular de python
import getingdic as dic
import evaluator
import normalization as norm
from sklearn.feature_extraction.text import CountVectorizer

# Adquisicion del corpus >>>>>>>> INICIO
print("Adquisición de corpus de depresion")
dic.chunks_paths = []
dic.loadchunkXML('dpp')
for i in range(len(dic.chunks_paths)):
    dic.analyzeChunk('dpp', i + 1)


dic.chunks_paths = []
dic.loadchunkXML('dpn')
for i in range(len(dic.chunks_paths)):
    dic.analyzeChunk('dpn', i + 1)


print('Numero de chunks en types ', len(dic.types['dpp']))
print('Numero de chunks en types ', len(dic.types['dpn']))

dic.initialize_class_types('dp')

dic.appendPost('dpp','dp')
dic.appendPost('dpn','dp')
print('Numero de instancias en depresion', len(dic.types['dp']['rows']))

dic.types['dp']['cols'] = dic.fillOnesZeros('dp')
print(len(dic.types['dp']['cols']))
dic.types['dp']['names'] = ['Negative', 'Positive']

# Adquisicion del corpus >>>>>>>> FIN
# Normalizado del corpus >>>>>>>>>> INICIO
norm_train_corpus = norm.normalize_corpus(dic.types['dp']['rows'])
# Normalizado del corpus >>>>>>>>>> FIN


from feature_extractor import bow_extractor, tfidf_extractor
# from feature_extractors import averaged_word_vector   izer
# from feature_extractors import tfidf_weighted_averaged_word_vectorizer
import nltk
import gensim
# BOW features
bow_vectorizer, bow_train_features = bow_extractor(norm_train_corpus,(1,1))

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()

from sklearn.model_selection import cross_val_predict

y_predicted = cross_val_predict( nb, bow_train_features, dic.types['dp']['cols'], cv=10)
evaluator.get_metrics(dic.types['dp']['cols'], y_predicted)

# Adquisicion del corpus >>>>>>>> INICIO
print("Adquisición de corpus de anorexia")
dic.chunks_paths = []
dic.loadchunkXML('axp')
for i in range(len(dic.chunks_paths)):
    dic.analyzeChunk('axp', i + 1)


dic.chunks_paths = []
dic.loadchunkXML('axn')
for i in range(len(dic.chunks_paths)):
    dic.analyzeChunk('axn', i + 1)


print('Numero de chunks en types ', len(dic.types['axp']))
print('Numero de chunks en types ', len(dic.types['axn']))

dic.initialize_class_types('ax')

dic.appendPost('axp','ax')
dic.appendPost('axn','ax')
print('Numero de instancias en anorexia', len(dic.types['ax']['rows']))

dic.types['ax']['cols'] = dic.fillOnesZeros('ax')
print(len(dic.types['ax']['cols']))
dic.types['ax']['names'] = ['Negative', 'Positive']

# Adquisicion del corpus >>>>>>>> FIN

# Normalizado del corpus >>>>>>>>>> INICIO
norm_train_corpus = norm.normalize_corpus(dic.types['ax']['rows'])
# Normalizado del corpus >>>>>>>>>> FIN

# BOW features
bow_vectorizer, bow_train_features = bow_extractor(norm_train_corpus,(1,1))

nb = MultinomialNB()

y_predicted = cross_val_predict( nb, bow_train_features, dic.types['ax']['cols'], cv=10)
evaluator.get_metrics(dic.types['ax']['cols'], y_predicted)
# # Document-term matrix in chunk1
# vect = CountVectorizer(stop_words='english', binary=True)
# for i in range(10):
#     vect = CountVectorizer(stop_words='english', binary=True)
#     fh = open('bw'+str(i)+'tsv', 'w')
#     dtm_CH1 = vect.fit_transform(types['ax'][i])
#     for el in vect.get_feature_names():
#         fh.write(str(el)+'\t')
#     fh.write('\n')
#     for i in dtm_CH1.toarray():
#         for j in i:
#             fh.write(str(j)+'\t')
#         fh.write('\n')
# # print(dtm_CH1.toarray())
# import pandas as pd
# pd.DataFrame(dtm_CH1.toarray(), columns=vect.get_feature_names())
# # Convert sparse matrix to a dense matrix
# # fhCH1 = open('denseMatrix1', 'w')
# # fhCH1.write(dtm_CH1.toarray())
# vectSW = CountVectorizer(stop_words='english')
# # Document-term matrix in chunk1
# dtm_CH1 = vect.fit_transform(types['ax']['chunk1'])
# # print(dtm_CH1.toarray())
# pd.DataFrame(dtm_CH1.toarray(), columns=vect.get_feature_names())
