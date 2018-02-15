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

def loadchunkXML(clase):
    for i in range(1,11):
        chunks_axp.append(list(getingdic.all_files(pb[clase]+'/chunk'+str(i), '*.xml')))
def analyzeChunk(clase, chunk=0):
    types[clase]['chunk'+str(chunk)] = getingdic.inlinePost(chunks_axp[chunk])

loadchunkXML('axp')
analyzeChunk('axp')
