import getingdic as GD
import readLidwic as LDW
import re

lidwc = {}
lidwc_cats = {}
lidwc = LDW.getWORDS()
lidwc_cats = LDW.getNUM()
print('Cargando los chuncks\n')
GD.loadchunkXML('axn')

# for chunk in range(1,11):
#     GD.types['dpn']['chunk'+str(chunk)] = GD.getBagofWords(GD.chunks_paths[chunk-1])
#     print(len(GD.types['dpn']['chunk'+str(chunk)]))
print('Cargando los diccionarios\n')
for chunk in range(1,11):
    GD.types['dpn']['chunk'+str(chunk)] = GD.loadBags(GD.getCleanBagofWords(GD.chunks_paths[chunk-1]))
    # GD.types['dpn']['chunk'+str(chunk)] = GD.janitor(GD.types['dpn']['chunk'+str(chunk)])
    # print(len(GD.types['dpn']['chunk'+str(chunk)]))

# for token in GD.types['dpn']['chunk1']:
#     if token in lidwc:
#         for i in lidwc[token]:
#             lidwc_cats[i] = lidwc_cats[i] + 1
def resetLidwcCats():
    for i in lidwc_cats.keys():
        lidwc_cats[i] = 0

def forUserAnalysis(xml):
    tree = ET.parse(xml)
    root_element = tree.getroot()
    user_node = root_element.findall('ID')
    if len(user_node) == 1:
        usuario = user_node[0].text
    else:
        usuario = 'unkown_user'
    tokens = GD.getCleanBagofWords(xml)
    types = GD.loadBags(GD.janitor_array(tokens))
    return str(usuario+'\t'+len(types)+'\t'+len(tokens))


# print('\ttoken, patron')
def parseForTokens():
    fo = 0
    checked = 0
    for token in GD.types['dpn']['chunk1']:
        for llave in lidwc.keys():
            if '.*' in llave:
                p = re.compile(llave, re.IGNORECASE)
                if re.match(p,token):
                    if checked == 0:
                        print('Match!\tToken: ', token, '\tLidwc: ', llave)
                        fo = fo + 1
                        checked = 1
                    for i in lidwc[llave]:
                        lidwc_cats[i] = lidwc_cats[i] + 1
            elif token == llave:
                print('Match!\tToken: ', token, '\tLidwc: ', llave)
                if checked == 0:
                    fo = fo + 1
                    checked = 1
                for i in lidwc[llave]:
                    lidwc_cats[i] = lidwc_cats[i] + 1
        checked = 0


def parseForTypes(ch):
    fo = 0
    for llave in lidwc.keys():
        for token in GD.types['dpn']['chunk'+str(ch)].keys():
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
                    lidwc_cats[i] = lidwc_cats[i] + GD.types['dpn']['chunk'+str(ch)][token]
    return fo

print('Analizando los tipos:\n')
print('Chunk\tMatches\tTipos\ttokens')
for ch in range(1,11):
    fo = parseForTypes(ch)
    FH = open('../dpn_categoriasCHUNK'+str(ch)+'.tsv', 'w')
    for i in lidwc_cats.keys():
        FH.write(str(i)+'\t'+str(lidwc_cats[i])+'\n')
    FH.close()
    # pr = fo / len(GD.types['dpn']['chunk3'])
    # print('Tokens en chunk3:\t', len(GD.types['dpn']['chunk3']), '\nCoincidencias en Liwc:\t', str(fo), '\nRepresentatividad:\t', str(pr))
    numTokens = 0
    FH = open('../dpn_diccionarioCHUNK'+str(ch)+'.tsv', 'w')
    for tipo in GD.types['dpn']['chunk'+str(ch)].keys():
        numTokens = numTokens + GD.types['dpn']['chunk'+str(ch)][tipo]
        FH.write(tipo + '\t' + str(GD.types['dpn']['chunk'+str(ch)][tipo])+'\n')
    FH.close()
    print(str(ch), str(fo), str(len(GD.types['dpn']['chunk'+str(ch)].keys())), str(numTokens))
