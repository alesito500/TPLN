# Este es el archivo del master en mi compu y le hice un cambio y quiero que aparezca en el master
import os, fnmatch, nltk

# types es el diccionario base en el que se van a guardar las bolsas de palabras.
# la simbologia que uso es:
# axp => Anorexia positivo
# axn => Anorexia negativo
# ax => Anorexia
# dpp => Depresion positivo
# dpn => Depresion negativo
# dp => Depresion

types = {'axp':{},'axn':{},'dpp':{},'dpn':{},'ax':{}, 'dp':{}}

# Nombre: all_files
# Objetivo:
#     Iterar dentro de un diccionario raiz para extraer todos sus documentos xml
# Parametros de entrada:
#     root => Directorio raiz
#     patterns => Patron a encontrar
#     single_level => Cantidad de niveles para la recursividad | opcional
#     yield_folders => Considera si los folders seran incluidos en el analisis
# Parametros de salida:
#     Los archivos coincidentes con el patron dado
def all_files(root, patterns ='*', single_level = False, yield_folders = False):
    # Ejecuta el split en caso de que se hayan dado mas de un patron a encontrar
    patterns = patterns.split(';')
    # En este ciclo se hace la lectura del contenido del directorio
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    # Si el patron dado coincide con el nombre del archivo examinado, entonces se agrega a la lista de archivos
                    yield os.path.join(path, name)
                    break
        if single_level:
            break

# Nombre: getBagofWords
# Objetivo:
#     Obtener la bolsa de palabras de la lista de archivos xml de entrada.
#     Esta bolsa de palabras incluye aun palabras funcionales
# Parametros de entrada:
#     archivos => Lista de archivos xml a tokenizar
# Parametros de salida:
#     tokens => Bolsa de palabras extraida de los archivos analizados
def getBagofWords(archivos):
    palabras = ''
    # full_tokens es una variable para escribir en un archivo la información: usuario [publicaciones]
    full_tokens = open('tokens_en_linea/tokens_en_linea_x', 'a')
    # En este ciclo se va a leer cada xml dentro de la lista de entrada
    for xml in archivos:
        # Por cada xml va a organizar una cadena (string) con el formato: usuario [publicaciones]
        usuario_linea = ''
        # Analisis XML del archivo
        root_element = parser.Parse(xml)
        # Extraccion del ID
        for ids in root_element.getElements('ID'):
            usuario_linea = ids.getData()
        # Extraccion de las publicaciones
        for escrito in root_element.getElements('WRITING'):
            for texto in escrito.getElements('TEXT'):
                # Concatenacion global de los textos
                palabras = palabras + texto.getData()
                # Concatenacion por usuario
                usuario_linea = usuario_linea + texto.getData()
        # Vaciado de las publicaciones por usuario
        full_tokens.write(usuario_linea + "\n")
    full_tokens.close()
    # tokenizado de todas las publicaciones extraidas de los archivos recibidos
    tokens = nltk.word_tokenize(palabras)
    return tokens

# Nombre: loadBags
# Objetivo:
#     Generar un diccionario de palabras con la forma {seccion: {token: frecuencia_absoluta}}
# Parametros de entrada:
#     bag => Bolsa de palabras (tokens)
#     section => Seccion a la que pertenecen los tokens (axp, axn, ax, dpp, dpn, dp)
# Parametros de salida:
#     bag => La misma bolsa de palabras, sin cambios

def loadBags(bag, section):
    for token in bag:
        if token in types[section]:
            types[section][token] = types[section][token] + 1
        else:
            types[section][token] = 1
    return bag

# La siguiente clase la copie tal cual de un libro, asi que no podria
# explicarla a detalle. Pero es la que hace el procesamiento del documento XML
# y su transformacion a nodos de python
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

# Declaracion del objeto Xml2Obj para ser usado en las funciones de analisis
parser = Xml2Obj( )

# Extraccion de las listas de archivos XML por secciones (axp, axn, dpp, dpn)
anorexia_pos = list(all_files('../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/positive_examples', '*.xml'))
anorexia_neg = list(all_files('../Corpus/TrainingCorpus_eRisk_2018/task2/eRisk 2018 - train/negative_examples', '*.xml'))
depresion_neg = list(all_files('../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/negative_examples_anonymous_chunks', '*.xml'))
depresion_pos = list(all_files('../Corpus/TrainingCorpus_eRisk_2018/task1/eRisk 2018 - training/2017 train/positive_examples_anonymous_chunks', '*.xml'))
print "Analisys Anorexia"
print "Analisys ANOREXIA positivo"
# Extraccion de la bolsa de palabras y del diccionario para axp
bag = loadBags(getBagofWords(anorexia_pos), 'axp')
# Extraccion del diccionario para ax
loadBags(bag, 'ax')
print "Number of tokens: ", len(bag)
print "Number of types: ", len(types.get('axp'))
print "Analisys ANOREXIA negativo"
# Extraccion de la bolsa de palabras y del diccionario para axn
bag = loadBags(getBagofWords(anorexia_neg), 'axn')
# Actualizacion del diccionario de ax
loadBags(bag, 'ax')
print "Number of tokens: ", len(bag)
print "Number of types: ", len(types.get('axn'))

print "Number of global types: ", len(types.get('ax'))

print "Analisys DEPRESION"
print "Analisys DEPRESION positivo"
bag = loadBags(getBagofWords(depresion_pos), 'dpp')
loadBags(bag, 'dp')
print "Number of tokens: ", len(bag)
print "Number of types: ", len(types.get('dpp'))

print "Analisys DEPRESION negativo"
bag = loadBags(getBagofWords(depresion_neg), 'dpn')
loadBags(bag, 'dp')
print "Number of tokens: ", len(bag)
print "Number of types: ", len(types.get('dpn'))

print "Number of global types: ", len(types.get('dp'))
