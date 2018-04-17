# Script modular de python
import getingdic as dic
import evaluator
import normalization as norm
import sys
from sklearn.feature_extraction.text import CountVectorizer

def main(No_ch=0):
    # Adquisicion del corpus >>>>>>>> INICIO
    print("Adquisición de corpus de depresion")
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
    print('Matriz Y',len(dic.types['dp']['cols']))
    dic.types['dp']['names'] = ['Negative', 'Positive']
    # Adquisicion del corpus >>>>>>>> FIN
    # Normalizado del corpus >>>>>>>>>> INICIO
    norm_train_corpus = norm.normalize_corpus(dic.types['dp']['rows'])
    # Normalizado del corpus >>>>>>>>>> FIN
    from feature_extractor import bow_extractor, tfidf_extractor, bow_extractor_maxdf
    from sklearn.feature_selection import mutual_info_classif
    import nltk
    import gensim
    # BOW features
    bow_vectorizer, bow_train_features = bow_extractor(norm_train_corpus)
    feature_names = bow_vectorizer.get_feature_names()
    print ('Numero de caracteristicas tomadas en cuenta', len(feature_names))
    from sklearn.naive_bayes import MultinomialNB
    nb = MultinomialNB()
    from sklearn.model_selection import cross_val_predict
    y_predicted = cross_val_predict( nb, bow_train_features, dic.types['dp']['cols'], cv=10)
    evaluator.get_metrics(dic.types['dp']['cols'], y_predicted)
    bow_vectorizer, bow_train_features = bow_extractor_maxdf(norm_train_corpus)
    res = dict(zip(feature_names, mutual_info_classif(bow_train_features,dic.types['dp']['cols'], discrete_features=True)))
    for feat in res.keys():
        print(feat, str(res[feat]), '\n')
    # y_predicted = cross_val_predict( nb, bow_train_features, dic.types['dp']['cols'], cv=10)
    # evaluator.get_metrics(dic.types['dp']['cols'], y_predicted)
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
    print('Matriz Y', len(dic.types['ax']['cols']))
    dic.types['ax']['names'] = ['Negative', 'Positive']
    # Adquisicion del corpus >>>>>>>> FIN
    # Normalizado del corpus >>>>>>>>>> INICIO
    norm_train_corpus = norm.normalize_corpus(dic.types['ax']['rows'])
    # Normalizado del corpus >>>>>>>>>> FIN
    # BOW features
    bow_vectorizer, bow_train_features = bow_extractor(norm_train_corpus)
    feature_names = bow_vectorizer.get_feature_names()
    print ('Numero de caracteristicas tomadas en cuenta', len(feature_names))
    nb = MultinomialNB()
    y_predicted = cross_val_predict( nb, bow_train_features, dic.types['ax']['cols'], cv=10)
    evaluator.get_metrics(dic.types['ax']['cols'], y_predicted)
    bow_vectorizer, bow_train_features = bow_extractor_maxdf(norm_train_corpus)
    res = dict(zip(feature_names, mutual_info_classif(bow_train_features,dic.types['ax']['cols'], discrete_features=True)))
    for feat in res.keys():
        print(feat, str(res[feat]), '\n')
    # y_predicted = cross_val_predict( nb, bow_train_features, dic.types['ax']['cols'], cv=10)
    # evaluator.get_metrics(dic.types['ax']['cols'], y_predicted)


if len(sys.argv) == 2:
    nch = sys.argv[1]
    nch = int(nch)
    main(nch)
else:
    for i in range(1,11):
        main(i)
