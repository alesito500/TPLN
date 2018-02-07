import os, fnmatch, re

def all_files(root, patterns ='*', single_level = False, yield_folders = False):
    #Extrae los XML de cierto PATH
    print "Path " + root
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if single_level:
            break

path_s = '../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 test'
xmls = list(all_files(path_s, '*.xml'))
entrada = open('../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 test/test_golden_truth.txt', 'r')
pattern = re.compile(r'\s[0,1]')
for linea in entrada:
    if re.match(r'\s[1]', linea):
        usuario = linea.split(pattern)
