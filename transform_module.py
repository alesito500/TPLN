# Script modular de python
import getingdic
from sklearn.feature_extraction.text import CountVectorizer
types = {
'axp':{},
'axn':{},
'dpp':{},
'dpn':{},
'ax':{},
'dp':{}
}
# Estructura para guardar el path base de cada clase
pb = {
'axp': '../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/positive_examples',
'axn': '../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/negative_examples',
'dpp': '../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/negative_examples_anonymous_chunks',
'dpn': '../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/positive_examples_anonymous_chunks'
}
chunks_ax = []

def loadchunkXML(clase):
    for i in range(1,11):
        chunks_ax.append(list(getingdic.all_files(pb[clase]+'/chunk'+str(i), '*.xml')))

def analyzeChunk(clase, chunk=1):
    types[clase]['chunk'+str(chunk)] = getingdic.inlinePost(chunks_ax[chunk - 1])

def runForAll():
    chunks_ax = []
    loadchunkXML('axp')
    # print('Numero de carpetas chunks ', len(chunks_ax))
    for i in range(len(chunks_ax)):
        analyzeChunk('axp', i + 1)
        # print('Numero de chunks en types ', len(types['axp']))
    chunks_ax = []
    loadchunkXML('axn')
    # print('Numero de carpetas chunks ', len(chunks_ax))
    for i in range(len(chunks_ax)):
        analyzeChunk('axn', i + 1)
        # print('Numero de chunks en types ', len(types['axn']))
    # for i in range(1,11):
    #     types['ax']['chunk'+str(i)] = types['axp']['chunk'+str(i)] + types['axn']['chunk'+str(i)]
# print('Numero de renglones', len(types['ax']['chunk1']))


# # Document-term matrix in chunk1
vect = CountVectorizer(stop_words='english', binary=True)
for i in range(10):
    vect = CountVectorizer(stop_words='english', binary=True)
    fh = open('bw'+str(i)+'tsv', 'w')
    dtm_CH1 = vect.fit_transform(types['ax'][i])
    for el in vect.get_feature_names():
        fh.write(str(el)+'\t')
    fh.write('\n')
    for i in dtm_CH1.toarray():
        for j in i:
            fh.write(str(j)+'\t')
        fh.write('\n')
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
