import re
import nltk
import stopwords
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

# Nltk's stopword list
swl = nltk.corpus.stopwords.words('english')
swl2 = stopwords.getDic()
thousand_words = []

# Lemmatizer
wnl = WordNetLemmatizer()

def tokenize_text(text):
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

def just_thousand(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token.lower() for token in tokens if token.lower() in thousand_words]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token.lower() not in swl2]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def remove_palabrasfuncionales(text):
    tokens = tokenize_text(text)
    swl2 = stopwords.getDic('es')
    filtered_tokens = [token for token in tokens if token.lower() not in swl2]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def normalize_corpus(corpus, tokenize=False):
    normalized_corpus = []
    for text in corpus:
        print("Full:_",text)
        text = remove_special_characters(text)
        print("Clean:_",text)
        text = remove_stopwords(text)
        print("No_SW:_",text)
        if tokenize:
            text = tokenize_text(text)
            print ("tokenized")
            normalized_corpus.append(text)
    return normalized_corpus

def normalize_post(text, tokenize=False):
    text = remove_special_characters(text)
    text = remove_stopwords(text)
    if tokenize:
        text = tokenize_text(text)
    return text
