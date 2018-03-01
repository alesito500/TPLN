import re
import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

# Nltk's stopword list
swl = nltk.corpus.stopwords.words('english')
# Lemmatizer
wnl = WordNetLemmatizer()

def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
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
    filtered_tokens = [token for token in tokens if token not in swl]
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
