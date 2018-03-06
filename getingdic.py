import os, fnmatch, nltk, re, normalization
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
# Diccionario de clases
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
'dpp': '../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/positive_examples_anonymous_chunks',
'dpn': '../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/negative_examples_anonymous_chunks'
}
# Arreglo de chunks
chunks_paths = []

def initialize_class_types(clase):
    types[clase]['rows'] = []
    types[clase]['cols'] = []
    types[clase]['names'] = []

# **** Zona de lectura del path ****
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


# Name:   analyzeChunk
# Goal:   Analizar un chunk para extraer: los posts en línea o
#         los tokens por separado.
# In:     clase => [axp, axn, dpp, dpn], chunk => [1..10]
# Out:    None
def analyzeChunk(clase, chunk=1):
    types[clase]['chunk'+str(chunk)] = inlinePost(chunks_paths[chunk - 1])

# Name:   loadchunkXML
# Goal:   Cargar la estructura de archivo XML
#         por chunk de una cierta clase (axp, axn, dpp, dpn).
#         Trabaja sobre la variable global de chunks_paths
# In:     clase => [axp, axn, dpp, dpn]
# Out:    None
def loadchunkXML(clase):
    for i in range(1,11):
        chunks_paths.append(list(all_files(pb[clase]+'/chunk'+str(i), '*.xml')))

# ***Zona de analisis de los textos***
# ------TOKENS------
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

# Name: getCleanBagofWords
# Goal: Tokenize a list of xml files
def getCleanBagofWords(archivos):
    palabras = ''
    if(isinstance(archivos, list)):
        for xml in archivos:
            tree = ET.parse(xml)
            root_element = tree.getroot()
            for texto in root_element.iter('TEXT'):
                #Obtengo los posts
                palabras = palabras + texto.text
    elif(isinstance(archivos, str)):
        tree = ET.parse(archivos)
        root_element = tree.getroot()
        for texto in root_element.iter('TEXT'):
            #Obtengo los posts
            palabras = palabras + texto.text
    # tokens = nltk.word_tokenize(palabras)
    tokens = normalization.remove_special_characters(palabras)
    sw = set(stopwords.words('english'))
    cleanTokens = []
    for t in tokens:
        if t not in sw:
            cleanTokens.append(t)
    return cleanTokens

# ---------TYPES----------------
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

# Name: janitor
# Goal: Take of urls and emails from the given dictionary
def janitor_array(dcy):
    urls = re.compile(r'\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
    mails = re.compile(r'[^@]+@[^@]+\.[^@]+')
    c = 0
    for llave in dcy:
        # print "INTO JANITOR LOOP ", llave
        if re.match(urls, llave):
            # print "URL FOUND ", llave
            del dcy[c]
        elif re.match(mails, llave):
            # print "MAIL FOUND ", llave
            del dcy[c]
        c = c + 1
    return dcy


# Name: forUserAnalysis
# Goal: realizar el analisis de tipos y tokens por usuario.
def forUserAnalysis(xml):
    tree = ET.parse(xml)
    root_element = tree.getroot()
    user_node = root_element.findall('ID')
    if len(user_node) == 1:
        usuario = user_node[0].text
    else:
        usuario = 'unkown_user'
    tokens = getCleanBagofWords(xml)
    types = loadBags(janitor_array(tokens))
    return str(usuario)+'\t'+str(len(types))+'\t'+str(len(tokens))

# Name: typesforUser
# Goal: realizar el analisis de tipos y tokens por usuario.
def typesforUser(xml):
    tree = ET.parse(xml)
    root_element = tree.getroot()
    user_node = root_element.findall('ID')
    if len(user_node) == 1:
        usuario = user_node[0].text
    else:
        usuario = 'unkown_user'
    tokens = getCleanBagofWords(xml)
    types = loadBags(janitor_array(tokens))
    return (usuario, types)

# Name: lineUpPost
# Goal: Imprimir un archivo tsv con los valores de
#     id de usuario, problema y posts en una sola linea
def lineUpPost( archivos, flag='ax', filename='posts.tsv'):
    full_tokens = open(filename, 'a')
    # En este ciclo se va a leer cada xml dentro de la lista de entrada
    for xml in archivos:
        # Por cada xml va a organizar una cadena (string) con el formato: usuario [publicaciones]
        usuario_linea = flag
        # Analisis XML del archivo
        tree = ET.parse(xml)
        root_element = tree.getroot()
        # Extraccion de las publicaciones
        for texto in root_element.iter('TEXT'):
            # Concatenacion por usuario
            usuario_linea = usuario_linea + '\t' + texto.text
        # Vaciado de las publicaciones por usuario
        full_tokens.write(usuario_linea + "\n")
    full_tokens.close()

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


# -------Procesamiento conjunto-----------------
# Junta todos los post (positivos y negativos) en un solo arreglo. Esto prepara los
# datos para la vectorización
def appendPost(clasef, clased):
    for chunk in types[clasef]:
        types[clased]['rows'] = types[clased]['rows'] + types[clasef][chunk]

# Llena un vector con unos y ceros para el entrenamiento de los algoritmos de ML
def fillOnesZeros(prefclase):
    tmp_matrix = [ 1 for chunk in types[prefclase+'p'].keys() for post in types[prefclase+'p'][chunk] ]
    tmp_matrix = tmp_matrix + [ 0 for chunk in types[prefclase+'n'].keys() for post in types[prefclase+'n'][chunk] ]
    return tmp_matrix
