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

for i in lidwc_cats.keys():
    lidwc_cats[i] = 0


fo = 0
for llave in lidwc.keys():
    p = re.compile(llave, re.IGNORECASE)
    for token in GD.types['axp']['chunk5']:
        if re.match(p,token):
            # print('Match: ', token, llave)
            fo = fo + 1
            for i in lidwc[llave]:
                lidwc_cats[i] = lidwc_cats[i] + 1


for i in lidwc_cats.keys():
    print(i,'\t', lidwc_cats[i])


pr = fo / len(GD.types['axp']['chunk5'])
print('Tokens en chunk5:\t', len(GD.types['axp']['chunk5']), '\nCoincidencias en Liwc:\t', str(fo), '\nRepresentatividad:\t', str(pr))
