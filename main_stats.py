# Script modular de python
import getingdic
types = {'axp':{},'axn':{},'dpp':{},'dpn':{},'ax':{}, 'dp':{}}
anorexia_pos = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/positive_examples', '*.xml'))
anorexia_neg = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/negative_examples', '*.xml'))
depresion_neg = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/negative_examples_anonymous_chunks', '*.xml'))
depresion_pos = list(getingdic.all_files('../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/positive_examples_anonymous_chunks', '*.xml'))

types['axp'] = getingdic.loadBags(getingdic.getBagofWords(anorexia_pos))
len(types['axp'])
types['axp'] = getingdic.janitor(types['axp'])
len(types['axp'])
