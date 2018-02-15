# Script modular de python
import getingdic
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
chunks_axp = []
# anorexia_pos = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/positive_examples', '*.xml'))
# anorexia_neg = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/negative_examples', '*.xml'))
# depresion_neg = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/negative_examples_anonymous_chunks', '*.xml'))
# depresion_pos = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/positive_examples_anonymous_chunks', '*.xml'))
# # Bolsa de palabras con stopwords
# types['axp'] = getingdic.loadBags(getingdic.getBagofWords(anorexia_pos))
# print (len(types['axp']))
# for llaves in types['axp']:
#     print (llaves)
# types['axp'] = getingdic.janitor(types['axp'])
# print len(types['axp'])
# # Bolsa de palabras sin stopwors
# types['axp'] = getingdic.loadBags(getingdic.getCleanBagofWords(anorexia_pos))
# print len(types['axp'])
# types['axp'] = getingdic.janitor(types['axp'])
# print len(types['axp'])

def loadchunkXML(clase):
    for i in range(1,11):
        chunks_axp.append(list(getingdic.all_files(pb[clase]+'/chunk'+str(i), '*.xml')))
def analyzeChunk(clase, chunk=0):
    types[clase] = getingdic.inlinePost(chunks_axp[chunk])

loadchunkXML('axp')
analyzeChunk('axp')
print(len(types['axp']))
print(type(types['axp']))
# for row in types['axp']:
#     print(row)
