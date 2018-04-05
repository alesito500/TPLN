# Script modular de python
import getingdic as dic
import evaluator
import normalization as norm
import sys
from sklearn.feature_extraction.text import CountVectorizer

if len(sys.argv) == 2:
    No_ch = sys.argv[1]

No_ch = int(No_ch)

print("Chunk ",sys.argv[1])
# Adquisicion del corpus >>>>>>>> INICIO
print("Adquisicion de corpus de depresion")
dic.chunks_paths = []
dic.loadchunkXML('dpp')
dic.analyzeChunk('dpp', No_ch)


dic.chunks_paths = []
dic.loadchunkXML('dpn')
dic.analyzeChunk('dpn', No_ch)


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
norm_train_corpus = norm.normalize_corpus_wordnet(dic.types['dp']['rows'])
# Normalizado del corpus >>>>>>>>>> FIN


from feature_extractor import bow_extractor, tfidf_transformer, tfidf_extractor
import nltk
import gensim
# BOW features
bow_vectorizer, bow_train_features = bow_extractor(norm_train_corpus,(1,3))
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
tfidf_y_predicted = cross_val_predict( nb_tfidf, tdidf_features, dic.types['dp']['cols'], cv=10)
print('Evaluation:\n')
evaluator.get_metrics(dic.types['dp']['cols'], tfidf_y_predicted)

# Adquisicion del corpus >>>>>>>> INICIO
print("Adquisicion de corpus de anorexia")
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
norm_train_corpus = norm.normalize_corpus(dic.types['ax']['rows'])
# Normalizado del corpus >>>>>>>>>> FIN
from feature_extractor import bow_extractor, tfidf_transformer, tfidf_extractor
import nltk
import gensim
# BOW features
bow_vectorizer, bow_train_features = bow_extractor(norm_train_corpus,(1,3))
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
