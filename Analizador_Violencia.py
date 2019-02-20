# @Nombre: Analizador_Violencia
# @Definición:
#   Archivo para analizar el corpus de las respuestas sobre Violencia de género
# @Autor: alesito500

import normalization as norm
from nltk import ngrams
import Chunk as ch
import Path
import csv
import os

directorios = Path.Path()
respuestas = ch.Chunk(0, 'es')
# @Nombre: extraeUNI
# @Definición:
#   Función para extraer unigramas de un documento dado
# @Entradas:
#   Dirección del archivo
# @Salidas:
#   Listado con la pareja de valores (tokens, frecuencia)
def extraeUNI(archivo, sw = False):
    contestacion = []
    if(type(archivo) is list):
        for publicacion in archivo:
            for elemento in publicacion:
                contestacion.append(elemento)
    elif( os.path.isfile(archivo) ):
        corpus = open(archivo, 'r')
        contestacion = corpus.readlines()
        corpus.close()
    else:
        print ("Error con la entrada de extraeUNI: ni archivo, ni lista")
        pass
    tokens = []
    vocabulario = {}
    for i in range(0, len(contestacion)):
        if sw:
            tokens.append(norm.tokenize_text(norm.remove_palabrasfuncionales(norm.remove_special_characters(contestacion[i].lower()))))
        else:
            tokens.append(norm.tokenize_text(norm.remove_special_characters(contestacion[i].lower())))
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
    csvfile = open(archivo)
    leeCSV = csv.reader(csvfile, delimiter=';')
    for row in leeCSV:
        (uid, respuesta) = (row[0], [row[2]])
        respuestas.newUser(uid, respuesta)
        respuestas.UserGenre(uid, row[1])
    respuestas.loadVocabulary()
    respuestas.calcIDLV()
    respuestas.loadUserF()



# @Nombre: extraeN
# @Definición:
#     Función para extraer los n-gramas de un documento dado
# @Entradas:
#     Dirección del archivo,
#     N a extraer. Por ejemplo: 2=>bigramas, 3=>trigramas
# @Salidas:
#     Listado con la pareja de datos: (ngramas, frecuencia)
def extraeN(archivo, n, sw = False):
    contestacion = []
    if(type(archivo) is list):
        for publicacion in archivo:
            for elemento in publicacion:
                contestacion.append(elemento)
    elif( os.path.isfile(archivo)):
        corpus = open(archivo, 'r')
        contestacion = corpus.readlines()
        corpus.close()
    else:
        print ("Error con la entrada de extraeUNI: ni archivo, ni lista")
        pass
    tokens = []
    ngramas = []
    vocabulario = {}
    for i in range(0, len(contestacion)):
        if(sw):
            tokens.append(norm.tokenize_text(norm.remove_palabrasfuncionales(norm.remove_special_characters(contestacion[i].lower()))))
        else:
            tokens.append(norm.tokenize_text(norm.remove_special_characters(contestacion[i].lower())))
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
    c_i = directorios.entrada
    # Extrae unigramas
    uni_i = extraeUNI(c_i, sw)
    # Archivo de salida con los unigramas
    u_i = open(directorios.suni,'w')
    # Impresión de los resultados obtenidos
    for v, k in uni_i:
        renglon = str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)

    u_i.close()
    # Extrae bigramas
    bi_i = extraeN(c_i,2, sw)
    # Archivo de salida con los bigramas
    u_i = open(directorios.sbi,'w')
    g_i = open(directorios.sbig,'w')
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
    u_i = open(directorios.stri,'w')
    g_i = open(directorios.strig,'w')
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
    c_i = directorios['entrada1']
    # Extrae unigramas
    uni_i = extraeUNI(c_i, sw)
    # Archivo de salida con los unigramas
    u_i = open(directorios['uni1'],'w')
    # Impresión de los resultados obtenidos
    for v, k in uni_i:
        renglon = str(k)+"\t"+str(v)+"\n"
        u_i.write(renglon)

    u_i.close()
    # Extrae bigramas
    bi_i = extraeN(c_i,2, sw)
    # Archivo de salida con los bigramas
    u_i = open(directorios['bi1'],'w')
    g_i = open(directorios['bigraf1'],'w')
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
    u_i = open(directorios['tri1'],'w')
    g_i = open(directorios['trigraf1'],'w')
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
    instrucciones += "\n(\t3\t)\tAnalizar las respuestas de las encuestas de febrero"
    instrucciones += "\n(\t4\t)\tAnalizar las respuestas de las encuestas de febrero sin palabras funcionales"
    instrucciones += "\n(\t5\t)\tAnalizar las respuestas de las encuestas de febrero por usuarios"
    instrucciones += "\n(\t6\t)\tAnalizar las respuestas de las encuestas de febrero por usuarios sin palabras funcionales"
    instrucciones += "\n(\t#\t)\tAnalizar la matriz conceptual"
    instrucciones += "\n(\t#\t)\tAnalizar un archivo en específico"
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
    global directorios
    if(seleccion == 1 ):
        defecto()
        directorios = Path.Path(2)
        defecto()
    elif(seleccion == 2):
        defecto(True)
        directorios = Path.Path(2)
        defecto(True)
    elif(seleccion == 3):
        directorios = Path.Path(3)
        defecto()
    elif(seleccion == 4):
        directorios = Path.Path(3)
        defecto(True)
    elif(seleccion == 5):
        directorios = Path.Path(4)
        analisiPorUsuario(directorios.entrada)
    else:
        print("Aún no esta disponible esta opción")
        main()


if __name__ == "__main__":
    main()
