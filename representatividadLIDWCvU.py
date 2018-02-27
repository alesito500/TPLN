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
print("Cargando Lidwc: \tdiccionario\t...(1,5)\n")
lidwc = LDW.getWORDS()
print("Cargando Lidwc: \tcategorias\t...(2,5)\n")
lidwc_cats = LDW.getNUM()
print("Analisis de clases\t\t...(3,5)\n")
for clase in clases:
    print('Cargando los chuncks de ', clase, '\t\t...(3,5)\n')
    GD.loadchunkXML(clase)
    print('Estadisticas base por xml\t\t...(4,5)\n')
    contador = 1
    for chunk in GD.chunks_paths:
        FH = open('../user_analysisV2_chunk'+str(contador)+'_'+clase+'.ods','w')
        contador = contador + 1
        for xml in chunk:
            (usuario, diccionario) = GD.typesforUser(xml)
            fo = parseForTypes(usuario, diccionario)
            CFH = open('../'+clase+'_categoriasCHUNK'+str(contador)+usuario+'.tsv', 'w')
            for i in lidwc_cats.keys():
                CFH.write(str(i)+'\t'+str(lidwc_cats[i])+'\n')
            CFH.close()
            numTokens = 0
            LFH = open('../'+clase+'_diccionarioCHUNK'+str(contador)+usuario+'.tsv', 'w')
            for tipo in diccionario.keys():
                numTokens = numTokens + diccionario[tipo]
                LFH.write(tipo + '\t' + str(diccionario[tipo])+'\n')
            LFH.close()
            print(str(contador), str(fo), str(len(diccionario.keys())), str(numTokens))
            resetLidwcCats()
            # FH.write(GD.forUserAnalysis(xml))
            # FH.write('\n')
        FH.close()
