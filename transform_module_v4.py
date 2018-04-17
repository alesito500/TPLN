# Script modular de python
import getingdic as dic
import evaluator
import normalization as norm
import sys
from sklearn.feature_extraction.text import CountVectorizer
import Chunk as ch

if len(sys.argv) == 2:
    No_ch = sys.argv[1]

# No_ch = 1
No_ch = int(No_ch)

print("Chunk ",sys.argv[1])
# Adquisicion del corpus >>>>>>>> INICIO
print("Adquisición de corpus de anorexia")
dic.chunks_paths = []
dic.loadchunkXML('axp')
dic.analyzeChunk('axp', No_ch)
chunk = ch.Chunk(No_ch)
for v in dic.chunks_paths[No_ch - 1]:
    (uid, posts) = dic.PostForUser(v)
    chunk.newUser(uid, posts)

dic.chunks_paths = []
dic.loadchunkXML('axn')
dic.analyzeChunk('axn', No_ch)
for v in dic.chunks_paths[No_ch - 1]:
    (uid, posts) = dic.PostForUser(v)
    chunk.newUser(uid, posts)

print('Numero de chunks en types ', len(dic.types['axp']))
print('Numero de chunks en types ', len(dic.types['axn']))

IDLVdic = {}
dic.initialize_class_types('ax')

dic.appendPost('axp','ax')
dic.appendPost('axn','ax')
chunk.loadVocabulary()
chunk.calcIDLV()
print('Numero de instancias en depresion: ', len(dic.types['ax']['rows']))
print('Vocabulario en el chunk: ', len(chunk.vocablos.keys()))

dic.types['ax']['cols'] = dic.fillOnesZeros('ax')
print(len(dic.types['ax']['cols']))
tfs = [(v.IDLV(0), k) for k,v in chunk.vocablos.items()]
tfs.sort()
tfs.reverse()
for i in range(0,1000):
    IDLVdic[tfs[i][1]] = tfs[i][0]

norm.thousand_words = IDLVdic.keys()
# Adquisicion del corpus >>>>>>>> FIN
# Normalizado del corpus >>>>>>>>>> INICIO
corpus = [norm.remove_special_characters(text) for text in dic.types['ax']['rows']]
train_corpus = [norm.remove_stopwords(text) for text in corpus]
thousand_corpus = [norm.just_thousand(text) for text in train_corpus]

# Normalizado del corpus >>>>>>>>>> FIN

from feature_extractor import bow_extractor, tfidf_transformer, tfidf_extractor
import nltk
import gensim
import pandas as pd
import numpy as np
# BOW features
bow_vectorizer, bow_train_features = bow_extractor(thousand_corpus,(1,1))
feature_names = bow_vectorizer.get_feature_names()
print ('Numero de caracteristicas tomadas en cuenta', len(feature_names))
# TFIDF features
tfidf_trans, tdidf_features = tfidf_transformer(bow_train_features)
# tfidf_trans, tdidf_features = tfidf_extractor(norm_train_corpus)
tfidf_weights = tdidf_features.todense()
tfidf_frame = evaluator.display_features(tfidf_weights, feature_names)

FH = open('mixed_thousand_words_'+str(No_ch),'w')
for i in range(0,1000):
    FH.write(str(i+1)+"\t"+str(tfs[i][1])+"\t"+str(tfs[i][0])+"\n")
FH.close()

for w in feature_names:
    if w in IDLVdic:
        tfidf_frame[w] = tfidf_frame[w] * IDLVdic[w]

newArray = np.asarray(tfidf_frame)

# tokenize documents
# tokenized_train = [nltk.word_tokenize(text) for text in norm_train_corpus]

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_predict
from sklearn.feature_selection import mutual_info_classif


# Tfidf test
nb_tfidf = MultinomialNB()
print('Corss fold validation of TFIDF\n')
tfidf_y_predicted = cross_val_predict( nb_tfidf, newArray, dic.types['ax']['cols'], cv=10)
print('Evaluation:\n')
evaluator.get_metrics(dic.types['ax']['cols'], tfidf_y_predicted)

res = dict(zip(feature_names, mutual_info_classif(newArray, dic.types['ax']['cols'], discrete_features=True)))
for feat in res.keys():
    print(feat, str(res[feat]), '\n')
