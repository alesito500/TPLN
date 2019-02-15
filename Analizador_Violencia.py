# @Nombre: Analizador_Violencia
# @Definición:
#   Archivo para analizar el corpus de las respuestas sobre Violencia de género
# @Autor: alesito500

import normalization as norm
from nltk import ngrams
import Chunk as ch
import csv

corpus = {
            'entrada1':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Test_feb19/resglobal.txt',
            'entrada2':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Test_feb19/Respuestas_feb.csv',
            'uni1':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Test_feb19/Salida/Stats/uni_principio.csv',
            'uni2':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Piloto/Salida/Stats/uni_final.csv',
            'bi1':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Test_feb19/Salida/Stats/bi_principio.csv',
            'bigraf1':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Test_feb19/Salida/Graph/grafo_bi_principio.csv',
            'bi2':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Piloto/Salida/Stats/bi_final.csv',
            'bigraf2':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Piloto/Salida/Graph/grafo_bi_final.csv',
            'tri1':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Test_feb19/Salida/Stats/tri_principio.csv',
            'trigraf1':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Test_feb19/Salida/Graph/grafo_tri_principio.csv',
            'tri2':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Piloto/Salida/Stats/tri_final.csv',
            'trigraf2':'/home/alesito500/Documentos/Madic/Proyecto_dos/Corpus/Piloto/Salida/Graph/grafo_tri_final.csv',
            }

respuestas = ch.Chunk(1)
# @Nombre: extraeUNI
# @Definición:
#   Función para extraer unigramas de un documento dado
# @Entradas:
#   Dirección del archivo
# @Salidas:
#   Listado con la pareja de valores (tokens, frecuencia)
def extraeUNI(archivo, sw = False):
    corpus = open(archivo, 'r')
    respuestas = corpus.readlines()
    corpus.close()
    tokens = []
    vocabulario = {}
    for i in range(0, len(respuestas)):
        if sw:
            tokens.append(norm.tokenize_text(norm.remove_palabrasfuncionales(norm.remove_special_characters(respuestas[i].lower()))))
        else:
            tokens.append(norm.tokenize_text(norm.remove_special_characters(respuestas[i].lower())))
    for t in tokens:
        for o in t:
            if o in vocabulario:
                vocabulario[o] += 1
            else:
                vocabulario[o] = 1
    items = [(v,k) for k, v in vocabulario.items()]
    items.sort()
    items.reverse()
    return items


def analisiPorUsuario(archivo):
    with open(archivo) as csvfile:
        leeCSV = csv.reader(csvfile, delimiter=';')
        for row in leeCSV:
            (uid, respuesta) = (row[0], row[2])
            respuestas.newUser(uid, respuesta)
            respuestas.UserGenre(uid, row[1])
    respuestas.loadVocabulary()
    respuestas.calcIDLV()


# @Nombre: extraeN
# @Definición:
#     Función para extraer los n-gramas de un documento dado
# @Entradas:
#     Dirección del archivo,
#     N a extraer. Por ejemplo: 2=>bigramas, 3=>trigramas
# @Salidas:
#     Listado con la pareja de datos: (ngramas, frecuencia)
def extraeN(archivo, n, sw = False):
    corpus = open(archivo, 'r')
    respuestas = corpus.readlines()
    corpus.close()
    tokens = []
    ngramas = []
    vocabulario = {}
    for i in range(0, len(respuestas)):
        if(sw):
            tokens.append(norm.tokenize_text(norm.remove_palabrasfuncionales(norm.remove_special_characters(respuestas[i].lower()))))
        else:
            tokens.append(norm.tokenize_text(norm.remove_special_characters(respuestas[i].lower())))
    for t in tokens:
        ngramas.append(ngrams(t, n))
    for g in ngramas:
        for r in g:
            if r in vocabulario:
                vocabulario[r] += 1
            else:
                vocabulario[r] = 1
    items = [(v,k) for k, v in vocabulario.items()]
    items.sort()
    items.reverse()
    return items

def defecto(sw = False):
    # Archivo de entrada
    c_i = corpus['entrada1']
    # Extrae unigramas
    uni_i = extraeUNI(c_i, sw)
    # Archivo de salida con los unigramas
    u_i = open(corpus['uni1'],'w')
    # Impresión de los resultados obtenidos
    for v, k in uni_i:
        renglon = str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)

    u_i.close()
    # Extrae bigramas
    bi_i = extraeN(c_i,2, sw)
    # Archivo de salida con los bigramas
    u_i = open(corpus['bi1'],'w')
    g_i = open(corpus['bigraf1'],'w')
    g_i.write("Source\tTarget\n")
    # Impresión de los resultados obtenidos
    for v, k in bi_i:
        renglon=str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)
        renglon = str(k[0])+"\t"+str(k[1])+"\n"
        g_i.write(renglon)
    u_i.close()
    g_i.close()
    # Extrae trigramas
    tri_i = extraeN(c_i,3, sw)
    # Archivo de salida con los trigramas
    u_i = open(corpus['tri1'],'w')
    g_i = open(corpus['trigraf1'],'w')
    g_i.write("Source\tTarget\n")
    # Impresión de los resultados obtenidos
    for v, k in tri_i:
        renglon=str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)
        renglon = str(k[0])+"\t"+str(k[1])+"\n"
        g_i.write(renglon)
        renglon = str(k[1])+"\t"+str(k[2])+"\n"
        g_i.write(renglon)
    u_i.close()
    g_i.close()
    # Archivo de entrada
    c_i = corpus['entrada2']
    # Extrae unigramas
    uni_i = extraeUNI(c_i, sw)
    # Archivo de salida con los unigramas
    u_i = open(corpus['uni2'],'w')
    # Impresión de los resultados obtenidos
    for v, k in uni_i:
        u_i.write(str(k))
        u_i.write("\t")
        u_i.write(str(v))
        u_i.write("\n")
    u_i.close()
    # Extrae bigramas
    bi_i = extraeN(c_i,2, sw)
    # Archivo de salida con los bigramas
    u_i = open(corpus['bi2'],'w')
    g_i = open(corpus['bigraf2'],'w')
    g_i.write("Source\tTarget\n")
    # Impresión de los resultados obtenidos
    for v, k in bi_i:
        renglon=str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)
        renglon = str(k[0])+"\t"+str(k[1])+"\n"
        g_i.write(renglon)
    u_i.close()
    g_i.close()
    # Extrae trigramas
    tri_i = extraeN(c_i,3, sw)
    # Archivo de salida con los trigramas
    u_i = open(corpus['tri2'],'w')
    g_i = open(corpus['trigraf2'],'w')
    g_i.write("Source\tTarget\n")
    # Impresión de los resultados obtenidos
    for v, k in tri_i:
        renglon=str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)
        renglon = str(k[0])+"\t"+str(k[1])+"\n"
        g_i.write(renglon)
        renglon = str(k[1])+"\t"+str(k[2])+"\n"
        g_i.write(renglon)
    u_i.close()
    g_i.close()

def personalizado(sw = False):
    # Archivo de entrada
    c_i = corpus['entrada1']
    # Extrae unigramas
    uni_i = extraeUNI(c_i, sw)
    # Archivo de salida con los unigramas
    u_i = open(corpus['uni1'],'w')
    # Impresión de los resultados obtenidos
    for v, k in uni_i:
        renglon = str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)

    u_i.close()
    # Extrae bigramas
    bi_i = extraeN(c_i,2, sw)
    # Archivo de salida con los bigramas
    u_i = open(corpus['bi1'],'w')
    g_i = open(corpus['bigraf1'],'w')
    g_i.write("Source\tTarget\n")
    # Impresión de los resultados obtenidos
    for v, k in bi_i:
        renglon=str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)
        renglon = str(k[0])+"\t"+str(k[1])+"\n"
        g_i.write(renglon)
    u_i.close()
    g_i.close()
    # Extrae trigramas
    tri_i = extraeN(c_i,3, sw)
    # Archivo de salida con los trigramas
    u_i = open(corpus['tri1'],'w')
    g_i = open(corpus['trigraf1'],'w')
    g_i.write("Source\tTarget\n")
    # Impresión de los resultados obtenidos
    for v, k in tri_i:
        renglon=str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)
        renglon = str(k[0])+"\t"+str(k[1])+"\n"
        g_i.write(renglon)
        renglon = str(k[1])+"\t"+str(k[2])+"\n"
        g_i.write(renglon)
    u_i.close()
    g_i.close()





def menu():
    instrucciones = "Menú del archivo para hacer un primer análisis de los documentos sobre violencia de género"
    instrucciones += "\nIngresa el número de una de las siguientes opciones"
    instrucciones += "\n(\t1\t)\tAnalizar las respuestas de las encuestas piloto"
    instrucciones += "\n(\t2\t)\tAnalizar las respuestas de las encuestas piloto sin palabras funcionales"
    instrucciones += "\n(\t3\t)\tAnalizar la matriz conceptual"
    instrucciones += "\n(\t4\t)\tAnalizar un archivo en específico"
    instrucciones += "\n:__"
    seleccion = 1
    try:
        seleccion = int(input(instrucciones))
    except ValueError:
        print("Error de entrada")
        seleccion = 1
    return seleccion

def main():
    seleccion = menu()
    if(seleccion == 1 ):
        defecto()
    elif(seleccion == 2):
        defecto(True)
    elif(seleccion == 3):
        matriz()
    elif(seleccion == 4):
        personalizado(True)


if __name__ == "__main__":
    main()
