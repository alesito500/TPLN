import getingdic as GD
import readLidwic as LDW
import re

lidwc = {}
lidwc_cats = {}
lidwc = LDW.getWORDS()
lidwc_cats = LDW.getNUM()

GD.loadchunkXML('axp')

for chunk in range(1,11):
    GD.types['axp']['chunk'+str(chunk)] = GD.getBagofWords(GD.chunks_paths[chunk-1])
    print(len(GD.types['axp']['chunk'+str(chunk)]))

for chunk in range(1,11):
    GD.types['axp']['chunk'+str(chunk)] = GD.getCleanBagofWords(GD.chunks_paths[chunk-1])
    print(len(GD.types['axp']['chunk'+str(chunk)]))


for token in GD.types['axp']['chunk1']:
    if token in lidwc:
        for i in lidwc[token]:
            lidwc_cats[i] = lidwc_cats[i] + 1

fo = 0
for llave in lidwc.keys():
    p = re.compile(llave, re.IGNORECASE)
    for token in GD.types['axp']['chunk1']:
        if re.match(p,token):
            print('Match: ', token, llave)
            fo = fo + 1
            for i in lidwc[llave]:
                lidwc_cats[i] = lidwc_cats[i] + 1



pr = fo / len(GD.types['axp']['chunk1'])
print('Tokens en chunk1: ', len(GD.types['axp']['chunk1']), 'Tokens en Liwc: ', str(fo), 'Representatividad: ', str(pr))
