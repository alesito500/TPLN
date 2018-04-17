import re

stopwords_dic = []

def main():
    stopword_file = open('stopwords', 'r')
    for line in stopword_file.readlines():
        stopwords_dic.append(line.strip())
    stopword_file.close()

def getDic():
    main()
    return stopwords_dic

if __name__ == "__main__":
    main()
