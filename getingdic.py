import os, fnmatch, nltk, re


from xml.parsers import expat
class Element(object):
    ''' A parsed XML element '''
    def __init__(self, name, attributes):
        # Record tagname and attributes dictionary
        self.name = name
        self.attributes = attributes
        # Initialize the element's cdata and children to empty
        self.cdata = ''
        self.children = [ ]
    def addChild(self, element):
        self.children.append(element)
    def getAttribute(self, key):
        return self.attributes.get(key)
    def getData(self):
        return self.cdata
    def getElements(self, name=''):
        if name:
            return [c for c in self.children if c.name == name]
        else:
            return list(self.children)
class Xml2Obj(object):
    ''' XML to Object converter '''
    def __init__(self):
        self.root = None
        self.nodeStack = [ ]
    def StartElement(self, name, attributes):
        'Expat start element event handler'
        # Instantiate an Element object
        element = Element(name.encode( ), attributes)
        # Push element onto the stack and make it a child of parent
        if self.nodeStack:
            parent = self.nodeStack[-1]
            parent.addChild(element)
        else:
            self.root = element
        self.nodeStack.append(element)
    def EndElement(self, name):
        'Expat end element event handler'
        self.nodeStack.pop( )
    def CharacterData(self, data):
        'Expat character data event handler'
        if data.strip( ):
            data = data.encode('ascii', 'ignore')
            element = self.nodeStack[-1]
            element.cdata += data
    def Parse(self, filename):
        # Create an Expat parser
        Parser = expat.ParserCreate( )
        # Set the Expat event handlers to our methods
        Parser.StartElementHandler = self.StartElement
        Parser.EndElementHandler = self.EndElement
        Parser.CharacterDataHandler = self.CharacterData
        # Parse the XML File
        ParserStatus = Parser.Parse(open(filename).read( ), 1)
        return self.root

parser = Xml2Obj( )
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
        root_element = parser.Parse(xml)
        # Extraccion del ID
        for ids in root_element.getElements('ID'):
            usuario_linea = ids.getData() + '\t' + flag
        # Extraccion de las publicaciones
        for escrito in root_element.getElements('WRITING'):
            for texto in escrito.getElements('TEXT'):
                # Concatenacion por usuario
                usuario_linea = usuario_linea + '\t' + texto.getData()
        # Vaciado de las publicaciones por usuario
        full_tokens.write(usuario_linea + "\n")
    full_tokens.close()


# Name: getBagofWords
# Goal: Tokenize a list of xml files
def getBagofWords(archivos):
    palabras = ''
    for xml in archivos:
        usuario_linea = ''
        root_element = parser.Parse(xml)
        for escrito in root_element.getElements('WRITING'):
            #Obtengo los elementos de la altura jerarquica de ID y WRITING
            for texto in escrito.getElements('TEXT'):
                #Obtengo los posts
                palabras = palabras + texto.getData()
    tokens = nltk.word_tokenize(palabras)
    return tokens

from nltk.corpus import stopwords
# Name: getCleanBagofWords
# Goal: Tokenize a list of xml files
def getCleanBagofWords(archivos):
    palabras = ''
    for xml in archivos:
        usuario_linea = ''
        root_element = parser.Parse(xml)
        for escrito in root_element.getElements('WRITING'):
            #Obtengo los elementos de la altura jerarquica de ID y WRITING
            for texto in escrito.getElements('TEXT'):
                #Obtengo los posts
                palabras = palabras + texto.getData()
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
