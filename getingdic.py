import os, fnmatch, nltk, re
import xml.etree.ElementTree as ET

# Name: all_files
# Goal: Get a list with the paths of all xml files in a given root
def all_files(root, patterns ='*', single_level = False, yield_folders = False):
    #Extrae los XML de cierto PATH
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

# Name: lineUpPost
# Goal: Imprimir un archivo tsv con los valores de
#     id de usuario, problema y posts en una sola linea
def lineUpPost( archivos, flag=0, filename='posts.tsv'):
    full_tokens = open(filename, 'a')
    # En este ciclo se va a leer cada xml dentro de la lista de entrada
    for xml in archivos:
        # Por cada xml va a organizar una cadena (string) con el formato: usuario [publicaciones]
        usuario_linea = ''
        # Analisis XML del archivo
        tree = ET.parse(xml)
        root_element = tree.getroot()
        # Extraccion del ID
        for ids in root_element.iter('ID'):
            usuario_linea = ids.text + '\t' + flag
        # Extraccion de las publicaciones
        for texto in root_element.iter('TEXT'):
            # Concatenacion por usuario
            usuario_linea = usuario_linea + '\t' + texto.text
        # Vaciado de las publicaciones por usuario
        full_tokens.write(usuario_linea + "\n")
    full_tokens.close()


# Name: getBagofWords
# Goal: Tokenize a list of xml files
def getBagofWords(archivos):
    palabras = ''
    for xml in archivos:
        usuario_linea = ''
        tree = ET.parse(xml)
        root_element = tree.getroot()
        for texto in root_element.iter('TEXT'):
            #Obtengo los posts
            palabras = palabras + texto.text
    tokens = nltk.word_tokenize(palabras)
    return tokens

from nltk.corpus import stopwords
# Name: getCleanBagofWords
# Goal: Tokenize a list of xml files
def getCleanBagofWords(archivos):
    palabras = ''
    for xml in archivos:
        usuario_linea = ''
        tree = ET.parse(xml)
        root_element = tree.getroot()
        for texto in root_element.iter('TEXT'):
            #Obtengo los posts
            palabras = palabras + texto.text
    tokens = nltk.word_tokenize(palabras)
    sw = set(stopwords.words('english'))
    cleanTokens = []
    for t in tokens:
        if t not in sw:
            cleanTokens.append(t)
    return cleanTokens
# Name: loadBags
# Goal: Load as dictionary a bag of tokens {type: ti}
def loadBags(bag):
    types = {}
    for token in bag:
        if token in types:
            types[token] = types[token] + 1
        else:
            types[token] = 1
    return types

# Name: janitor
# Goal: Take of urls and emails from the given dictionary
def janitor(dcy):
    urls = re.compile(r'\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
    mails = re.compile(r'[^@]+@[^@]+\.[^@]+')
    for llave in dcy.keys():
        # print "INTO JANITOR LOOP ", llave
        if re.match(urls, llave):
            # print "URL FOUND ", llave
            del dcy[llave]
        elif re.match(mails, llave):
            # print "MAIL FOUND ", llave
            del dcy[llave]
    return dcy

# Name: lineUpPost
# Goal: Imprimir un archivo tsv con los valores de
#     id de usuario, problema y posts en una sola linea
def inlinePost( archivos):
    full_tokens = []
    # En este ciclo se va a leer cada xml dentro de la lista de entrada
    for xml in archivos:
        # Por cada xml va a organizar una cadena (string) con el formato: usuario [publicaciones]
        usuario_linea = ''
        # Analisis XML del archivo
        tree = ET.parse(xml)
        root_element = tree.getroot()
        # Extraccion de las publicaciones
        for texto in root_element.iter('TEXT'):
                # Concatenacion por usuario
                usuario_linea = usuario_linea + ' ' + texto.text
        # Vaciado de las publicaciones por usuario
        full_tokens.append(usuario_linea)
    return full_tokens
