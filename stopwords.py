import re

stopwords_dic = []

def main(lang='en'):
    if lang is 'es':
        stopwords_path = 'palabrasfuncionales'
    else:
        stopwords_path = 'stopwords'
    stopword_file = open(stopwords_path, 'r')
    for line in stopword_file.readlines():
        stopwords_dic.append(line.strip())
    stopword_file.close()

def getDic(lang='en'):
    main(lang)
    return stopwords_dic

if __name__ == "__main__":
    main()
