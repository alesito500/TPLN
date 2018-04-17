# Script modular de python
import getingdic as dic
import evaluator
import normalization as norm
import sys
from sklearn.feature_extraction.text import CountVectorizer
import Chunk as ch

if len(sys.argv) == 2:
    No_ch = sys.argv[1]

No_ch = int(No_ch)
# No_ch = 1

print("Chunk ",sys.argv[1])
# Adquisicion del corpus >>>>>>>> INICIO
print("Adquisición de corpus de depresion")
dic.chunks_paths = []
dic.loadchunkXML('dpp')
dic.analyzeChunk('dpp', No_ch)
chunk = ch.Chunk(No_ch)
for v in dic.chunks_paths[No_ch - 1]:
    (uid, posts) = dic.PostForUser(v)
    chunk.newUser(uid, posts)


dic.chunks_paths = []
dic.loadchunkXML('dpn')
dic.analyzeChunk('dpn', No_ch)
for v in dic.chunks_paths[No_ch - 1]:
    (uid, posts) = dic.PostForUser(v)
    chunk.newUser(uid, posts)

print('Numero de chunks en types ', len(dic.types['dpp']))
print('Numero de chunks en types ', len(dic.types['dpn']))

dic.initialize_class_types('dp')
IDLVdic = {}

dic.appendPost('dpp','dp')
dic.appendPost('dpn','dp')
chunk.loadVocabulary()
chunk.calcIDLV()
print('Numero de instancias en depresion', len(dic.types['dp']['rows']))

dic.types['dp']['cols'] = dic.fillOnesZeros('dp')
print(len(dic.types['dp']['cols']))

# Adquisicion del corpus >>>>>>>> FIN
# Normalizado del corpus >>>>>>>>>> INICIO
norm_train_corpus = [norm.remove_special_characters(text) for text in dic.types['dp']['rows']]
train_corpus = [norm.remove_stopwords(text) for text in norm_train_corpus]
# Normalizado del corpus >>>>>>>>>> FIN

tfs = [(v.IDLV(0), k) for k,v in chunk.vocablos.items()]
tfs.sort()
tfs.reverse()
for k,v in chunk.vocablos.items():
    IDLVdic[k] = v

from feature_extractor import bow_extractor, tfidf_transformer, tfidf_extractor
import nltk
import gensim
import numpy as np
# BOW features
bow_vectorizer, bow_train_features = bow_extractor(train_corpus,(1,1))
feature_names = bow_vectorizer.get_feature_names()
# TFIDF features
# tfidf_trans, tdidf_features = tfidf_transformer(bow_train_features)
tfidf_trans, tdidf_features = tfidf_extractor(norm_train_corpus)
tfidf_weights = tdidf_features.todense()
tfidf_frame = evaluator.display_features(tfidf_weights, feature_names)

for w in feature_names:
    if w in IDLVdic:
        tfidf_frame[w] = tfidf_frame[w] * IDLVdic[w]

newArray = np.asarray(tfidf_frame)

# tokenize documents
# tokenized_train = [nltk.word_tokenize(text) for text in norm_train_corpus]

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_predict


# Tfidf test
nb_tfidf = MultinomialNB()
print('Corss fold validation of TFIDF\n')
tfidf_y_predicted = cross_val_predict( nb_tfidf, newArray, dic.types['dp']['cols'], cv=10)
print('Evaluation:\n')
evaluator.get_metrics(dic.types['dp']['cols'], tfidf_y_predicted)

# Adquisicion del corpus >>>>>>>> INICIO
print("Adquisición de corpus de anorexia")
dic.chunks_paths = []
dic.loadchunkXML('axp')
dic.analyzeChunk('axp', No_ch)


dic.chunks_paths = []
dic.loadchunkXML('axn')
dic.analyzeChunk('axn', No_ch)


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
norm_train_corpus = norm.remove_special_characters(dic.types['ax']['rows'])
norm_train_corpus = norm.remove_stopwords(norm_train_corpus)
# Normalizado del corpus >>>>>>>>>> FIN
from feature_extractor import bow_extractor, tfidf_transformer, tfidf_extractor
import nltk
import gensim
# BOW features
bow_vectorizer, bow_train_features = bow_extractor(norm_train_corpus,(1,1))
feature_names = bow_vectorizer.get_feature_names()
# TFIDF features
tfidf_trans, tdidf_features = tfidf_extractor(norm_train_corpus)
# tokenize documents
tokenized_train = [nltk.word_tokenize(text) for text in norm_train_corpus]

from sklearn.naive_bayes import MultinomialNB

from sklearn.model_selection import cross_val_predict

# Tfidf test
nb_tfidf = MultinomialNB()
print('Corss fold validation of TFIDF\n')
tfidf_y_predicted = cross_val_predict( nb_tfidf, tdidf_features, dic.types['ax']['cols'], cv=10)
print('Evaluation:\n')
evaluator.get_metrics(dic.types['ax']['cols'], tfidf_y_predicted)
