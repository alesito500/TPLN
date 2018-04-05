import getingdic as GD
import readLidwic as LDW
import re
import xml.etree.ElementTree as ET

def resetLidwcCats():
    for i in lidwc_cats.keys():
        lidwc_cats[i] = 0


def parseForTypes(usr, dic):
    fo = 0
    for llave in lidwc.keys():
        for token in dic.keys():
            if '.*' in llave:
                p = re.compile(llave, re.IGNORECASE)
                if re.match(p,token):
                    # print('Match!\tToken: ', token, '\tLidwc: ', llave)
                    fo = fo + 1
                    for i in lidwc[llave]:
                        lidwc_cats[i] = lidwc_cats[i] + 1
            elif token.lower() == llave:
                # print('Match!\tToken: ', token, '\tLidwc: ', llave)
                fo = fo + 1
                for i in lidwc[llave]:
                    lidwc_cats[i] = lidwc_cats[i] + dic[token]
    return fo


lidwc = {}
lidwc_cats = {}
clases = ['axp','axn','dpp','dpn']
# clases = ['axp']
print("Cargando Lidwc: \tdiccionario\t...(1,5)\n")
lidwc = LDW.getWORDS()
print("Cargando Lidwc: \tcategorias\t...(2,5)\n")
lidwc_cats = LDW.getNUM()
print("Analisis de clases\t\t...(3,5)\n")
for clase in clases:
    GD.chunks_paths = []
    print('Cargando los chunks de ', clase, '\t\t...(4,5)\n')
    FH = open('../ForUserAnalysis/'+clase+'.tsv', 'a')
    FH.write('usuario\tchunk\tposts\tliwc\tvocabulary\ttokens\n')
    GD.loadchunkXML(clase)
    print('Estadisticas base por xml\t\t...(5,5)\n')
    for chunk in GD.chunks_paths:
        for xml in chunk:
            m = re.search('subject[0-9]+_([0-9]{1,2})\.xml',xml)
            (usuario, no_post, diccionario) = GD.typesforUser(xml)
            fo = parseForTypes(usuario, diccionario)
            CFH = open('../ForUserAnalysis/'+clase+'_categoriasCHUNK'+m.group(1)+'_'+usuario+'.tsv', 'w')
            for i in lidwc_cats.keys():
                CFH.write(str(i)+'\t'+str(lidwc_cats[i])+'\n')
            CFH.close()
            numTokens = 0
            LFH = open('../ForUserAnalysis/'+clase+'_diccionarioCHUNK'+m.group(1)+'_'+usuario+'.tsv', 'w')
            for tipo in diccionario.keys():
                numTokens = numTokens + diccionario[tipo]
                LFH.write(tipo + '\t' + str(diccionario[tipo])+'\n')
            LFH.close()
            print(usuario, '\t', m.group(1), '\t', no_post, '\t', str(fo), '\t', str(len(diccionario.keys())), '\t', str(numTokens))
            FH.write(usuario+'\t'+m.group(1)+'\t'+str(no_post)+'\t'+str(fo)+'\t'+str(len(diccionario.keys()))+'\t'+str(numTokens)+'\n')
            # Imprime: Usuario, chunk, numero de post, palabras en liwc, types, tokens
            resetLidwcCats()
    FH.close()
