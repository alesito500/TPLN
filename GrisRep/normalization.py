import re
import nltk
import string
import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

# Nltk's stopword list
swl = nltk.corpus.stopwords.words('english')
swl2 = stopwords.getDic()
# Lemmatizer
wnl = WordNetLemmatizer()

def tokenize_text(text):
    # tokens = nltk.word_tokenize(text)
    tokens = text.split()
    tokens = [token.strip() for token in tokens]
    return tokens

# NAME: remove_special_characters
# GOAL:
#     Remueve los caracteres especiales y tokeniza el texto de entrada
# INPUT:
#     Una cadena de texto
# OUTPUT:
#     Una cadena de texto
def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub('', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token.lower() not in swl2]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def normalize_corpus(corpus, tokenize=False):
    normalized_corpus = []
    for text in corpus:
        text = remove_special_characters(text)
        text = remove_stopwords(text)
        normalized_corpus.append(text)
        if tokenize:
            text = tokenize_text(text)
            normalized_corpus.append(text)
    return normalized_corpus

#****funciones para las palabras fuera del diccionario WordNet ****
def palabra_fuera_wordnet(text):
	tokens = tokenize_text(text)
	filtered_tokens = [token for token in tokens if not wn.synsets(token)]
	filtered_text = ' '.join(filtered_tokens)
	return filtered_text

def normalize_corpus_wordnet(corpus, tokenize=False):
	normalized_corpus = []
	for text in corpus:
		text = remove_special_characters(text)
		text = text.lower()
		text = re.sub(" \d+", "", text)
		text = re.sub(r'http\S+', '',text)
		text = palabra_fuera_wordnet(text)
		normalized_corpus.append(text)
		if tokenize:
			text = tokenize_text(text)
			normalized_corpus.append(text)
	return normalized_corpus
#*************************************************************

#*****PALABRAS LIWC******************************************
def getWordFixed(diccionario):
    dic = {}
    dic_path = open(diccionario, 'r')
    patron1 = re.compile(r'[0-9]{1,3}\t[a-z]')
    patron2 = re.compile(r'%')
    for line in dic_path.readlines():
        if not re.match(patron1,line) and not re.match(patron2, line):
            ac = line.split('\t')
            ac[-1] = ac[-1].replace('\n','')
            ac[0] = ac[0].replace('*', '')
            ac[0] = ac[0].replace('\'', '\\\'')
            dic[ac.pop(0)] = ac
    dic_path.close()
    return dic

def compararLiwcAx(texto):
    diccionario2 = '/home/alejandrorosaleslyr/Clasificador/TPLN/Dictionaries/nuevoliwc_anx.dic'
    liwc ={}
    palabras_dic = []

    tokens = tokenize_text(texto)
   # print('tamano tokens:', len(tokens))
    liwc = getWordFixed(diccionario2)
    for token in tokens:
        for llave  in liwc.keys():
           if token == llave:
               palabras_dic.append(token)
               # print(token,  'is related with', llave)
    return(palabras_dic)

def compararLiwcDp(texto):
    diccionario2 = '/home/alejandrorosaleslyr/Clasificador/TPLN/Dictionaries/nuevoliwc_dep.dic'
    liwc ={}
    palabras_dic = []

    tokens = tokenize_text(texto)
   # print('tamano tokens:', len(tokens))
    liwc = getWordFixed(diccionario2)
    for token in tokens:
        for llave  in liwc.keys():
           if token == llave:
               palabras_dic.append(token)
               # print(token,  'is related with', llave)
    return(palabras_dic)


def limpiarTextoAx(source,tokenize=False):
    normalizedCorpus = []
#    print('funciona la variable')
    for text in source:
                text = remove_special_characters(text)
                text = text.lower()
                text = re.sub(" \d+", "", text)
                text = str(text)
                text = compararLiwcAx(text)
                text = str(text)
                normalizedCorpus.append(text)
   # print(normalizedCorpus[2])
    return normalizedCorpus

def limpiarTextoDp(source,tokenize=False):
    normalizedCorpus = []
#    print('funciona la variable')
    for text in source:
                text = remove_special_characters(text)
                text = text.lower()
                text = re.sub(" \d+", "", text)
                text = str(text)
                text = compararLiwcDp(text)
                text = str(text)
                normalizedCorpus.append(text)
   # print(normalizedCorpus[2])
    return normalizedCorpus
