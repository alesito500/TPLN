import getingdic as gd
import Chunk as ch
import evaluator as ev
import sys

ildpp = []
ildpn = []
ilaxp = []
ilaxn = []

def info(version=1):
    print('DEFINICIÓN\n')
    print('\tRepresentación final v',version,'\n')
    print('En este script voy a buscar representar mis datos\n')
    print('mediante las relaciones semánticas de las palabras\n')
    print('contenidas en el Corpus de entrenamiento.\n')
    print('\t\tAutor: Ing. Alejandro Rosales Martínez')

def parsing(illness='dp',cat=0,No_ch=0):
    ilM = []
    if(No_ch!=0):
        gd.chunks_paths = []
        if(illness=='dp' and cat == 0):
            print('DEBUGG:__Depresion negativo')
            gd.loadchunkXML('dpn')
            ilchunk = ch.Chunk(No_ch)
            for v in gd.chunks_paths[No_ch - 1]:
                (uid, posts) = gd.PostForUser(v)
                ilchunk.newUser(uid,posts)
            ilM = ilchunk.getidlvMatrix()
        elif(illness=='dp' and cat == 1):
            print('DEBUG:__Depresion positivo')
            gd.loadchunkXML('dpp')
            ilchunk = ch.Chunk(No_ch)
            for v in gd.chunks_paths[No_ch - 1]:
                (uid, posts) = gd.PostForUser(v)
                ilchunk.newUser(uid,posts)
            ilM = ilchunk.getidlvMatrix()
        elif(illness=='ax' and cat == 0):
            print('DEBUG:__Anorexia negativo')
            gd.loadchunkXML('axn')
            ilchunk = ch.Chunk(No_ch)
            for v in gd.chunks_paths[No_ch - 1]:
                (uid, posts) = gd.PostForUser(v)
                ilchunk.newUser(uid,posts)
            ilM = ilchunk.getidlvMatrix()
        else:
            print('DEBUG:__Anorexia positivo')
            gd.loadchunkXML('axp')
            ilchunk = ch.Chunk(No_ch)
            for v in gd.chunks_paths[No_ch - 1]:
                (uid, posts) = gd.PostForUser(v)
                ilchunk.newUser(uid,posts)
            ilM = ilchunk.getidlvMatrix()
    return ilM

def main(ch=0):
    info()
    if ch > 0:
        # funcion para un chunk
        ildpp = parsing('dp',1,ch)
        ildpn = parsing('dp',0,ch)
        ilaxp = parsing('ax',1,ch)
        ilaxn = parsing('ax',0,ch)
        yax = [1]*len(ilaxp) + [0]*len(ilaxn)
        il = ilaxp + ilaxn
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.model_selection import cross_val_predict
        nb = MultinomialNB()
        y_predicted = cross_val_predict( nb, il, yax, cv=10)
        ev.get_metrics(yax, y_predicted)
    else:
        for ch in range(1,11):
            # funcion para todos
            gd.chunks_paths = []
            parsing('dp',1,ch)
            parsing('dp',0,ch)
            parsing('ax',1,ch)
            parsing('ax',0,ch)

if __name__ == "__main__":
    ch=0
    if len(sys.argv) == 2:
        ch = sys.argv[1]
        ch = int(ch)
    main(ch)
