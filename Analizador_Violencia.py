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
resgeneros = {'unigramas':{'Masculino':{}, 'Femenino':{}, 'SIN_DEFINIR':{}}, 'bigramas':{'Masculino':{}, 'Femenino':{}, 'SIN_DEFINIR':{}}, 'trigramas':{'Masculino':{}, 'Femenino':{}, 'SIN_DEFINIR':{}}}
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


def analisiPorUsuario():
    csvfile = open(directorios.entrada)
    print("Entrada ", directorios.entrada, "\n")
    leeCSV = csv.reader(csvfile, delimiter=';')
    for row in leeCSV:
        try:
            (uid, respuesta) = (row[0], [row[2]])
        except IndexError:
            (uid, respuesta) = (row[0], [""])
        respuestas.newUser(uid, respuesta)
        respuestas.UserGenre(uid, row[1])
    respuestas.loadVocabulary()
    respuestas.calcIDLV()
    respuestas.loadUserF()
    with open(directorios.suni, 'w', newline='') as csvfile:
        fieldnames = ['Usuario', 'Vocablo', 'Frecuencia']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k,v in respuestas.usuarios.items():
            for l, c in v.userDic.items():
                writer.writerow({'Usuario':k, 'Vocablo':l, 'Frecuencia':c})
    IDLVdic = {}
    tfs = [(v.IDLV(0), k) for k,v in respuestas.vocablos.items()]
    tfs.sort()
    tfs.reverse()
    for i in range(0,len(tfs)):
        IDLVdic[tfs[i][1]] = tfs[i][0]
    with open(directorios.sidlp,'w', newline='') as csvfile:
      fieldnames=['palabra', 'IDLP']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for llave in IDLVdic.keys():
          writer.writerow({'palabra': llave, 'IDLP':IDLVdic[llave]})

def analisisPorGenero():
    for k, v in respuestas.usuarios.items():
        for l in extraeUNI(v.posts):
            if l[1] in resgeneros['unigramas'][v.genero]:
                resgeneros['unigramas'][v.genero][l[1]] = resgeneros['unigramas'][v.genero][l[1]] + l[0]
            else:
                resgeneros['unigramas'][v.genero][l[1]] = l[0]
        for l in extraeN(v.posts, 2):
            if l[1] in resgeneros['bigramas'][v.genero]:
                resgeneros['bigramas'][v.genero][l[1]] = resgeneros['bigramas'][v.genero][l[1]] + l[0]
            else:
                resgeneros['bigramas'][v.genero][l[1]] = l[0]
        for l in extraeN(v.posts, 3):
            if l[1] in resgeneros['trigramas'][v.genero]:
                resgeneros['trigramas'][v.genero][l[1]] = resgeneros['trigramas'][v.genero][l[1]] + l[0]
            else:
                resgeneros['trigramas'][v.genero][l[1]] = l[0]
    with open(directorios.sgen, 'w', newline='') as csvfile:
        fieldnames = ['Genero', 'Vocablo', 'Frecuencia']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k in resgeneros['unigramas'].keys():
            for p in resgeneros['unigramas'][k].keys():
                writer.writerow({'Genero':k,'Vocablo':p, 'Frecuencia':resgeneros['unigramas'][k][p]})
    csvfile = open(directorios.sbigen, 'w', newline='')
    fieldnames = ['Genero', 'Bigrama', 'Frecuencia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for k in resgeneros['bigramas'].keys():
        for p in resgeneros['bigramas'][k].keys():
            writer.writerow({'Genero':k,'Bigrama':p, 'Frecuencia':resgeneros['bigramas'][k][p]})
    with open(directorios.strigen, 'w', newline='') as csvfile:
        fieldnames = ['Genero', 'Trigrama', 'Frecuencia']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k in resgeneros['trigramas'].keys():
            for p in resgeneros['trigramas'][k].keys():
                writer.writerow({'Genero':k,'Trigrama':p, 'Frecuencia':resgeneros['trigramas'][k][p]})



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
    espacio = ' '
    if(type(archivo) is list):
        for publicacion in archivo:
            contestacion.append(espacio.join(publicacion))
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
    instrucciones += "\n(\t5\t)\tAnalizar las respuestas de las encuestas de febrero por usuarios, sin palabras funcionales"
    instrucciones += "\n(\t6\t)\tAnalizar las respuestas de las encuestas de febrero por género, sin palabras funcionales"
    instrucciones += "\n(\t7\t)\tAnalizar las respuestas de las encuestas de mayo sin palabras funcionales"
    instrucciones += "\n(\t8\t)\tAnalizar las respuestas de las encuestas de mayo por género, sin palabras funcionales"
    instrucciones += "\n(\t9\t)\tAnalizar la matriz conceptual"
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
        analisiPorUsuario()
    elif(seleccion == 6):
        directorios = Path.Path(4)
        analisiPorUsuario()
        analisisPorGenero()
    elif(seleccion == 7):
        directorios = Path.Path(5)
        defecto(True)
    elif(seleccion == 8):
        print("\nElegiste la opción 8")
        directorios = Path.Path(6)
        print("\nDirectorios cargados")
        print("\nAnalisis por usuario")
        analisiPorUsuario()
        print("\nAnalisis por género")
        analisisPorGenero()
    elif(seleccion == 9):
        directorios = Path.Path(7)
        defecto(True)
    else:
        print("Aún no esta disponible esta opción")
        main()


if __name__ == "__main__":
    main()
