class Path:
    def __init__(self, opcion=1):
        if(opcion == 1):
            #Corpus: piloto, con palabras funcionales y la pregunta al principio
            self.piloto()
        elif(opcion == 2):
            self.piloto(2)
        elif(opcion == 3):
            self.feb19()
        elif(opcion == 4):
            self.feb19(4)
        elif(opcion == 5):
            self.may19()
        elif(opcion == 6):
            self.may19(6)
        else:
            pass
        pass

    def piloto(self, opcion=1):
        if(opcion == 1):
            self.entrada = 'Corpus/Piloto/r_principio.txt'
            self.suni = 'Corpus/Piloto/Salida/Stats/uni_principio.csv'
            self.sbi = 'Corpus/Piloto/Salida/Stats/bi_principio.csv'
            self.stri = 'Corpus/Piloto/Salida/Stats/tri_principio.csv'
            self.sbig = 'Corpus/Piloto/Salida/Graph/grafo_bi_principio.csv'
            self.strig = 'Corpus/Piloto/Salida/Graph/grafo_tri_principio.csv'
        else:
            self.entrada = 'Corpus/Piloto/r_final.txt'
            self.suni = 'Corpus/Piloto/Salida/Stats/uni_final.csv'
            self.sbi = 'Corpus/Piloto/Salida/Stats/bi_final.csv'
            self.stri = 'Corpus/Piloto/Salida/Stats/tri_final.csv'
            self.sbig = 'Corpus/Piloto/Salida/Graph/grafo_bi_final.csv'
            self.strig = 'Corpus/Piloto/Salida/Graph/grafo_tri_final.csv'


    def feb19(self, opcion=3):
        if(opcion == 3):
            self.entrada = 'Corpus/Test_feb19/resglobal.txt'
            self.suni = 'Corpus/Test_feb19/Salida/Stats/uni_general.csv'
            self.sbi = 'Corpus/Test_feb19/Salida/Stats/bi_general.csv'
            self.stri = 'Corpus/Test_feb19/Salida/Stats/tri_general.csv'
            self.sbig = 'Corpus/Test_feb19/Salida/Graph/grafo_bi_general.csv'
            self.strig = 'Corpus/Test_feb19/Salida/Graph/grafo_tri_general.csv'
        else:
            self.entrada = 'Corpus/Test_feb19/Respuestas_feb.csv'
            self.suni = 'Corpus/Test_feb19/Salida/Stats/uni_porusuario.csv'
            self.sidlp = 'Corpus/Test_feb19/Salida/Stats/idlp_general.csv'
            self.sgen = 'Corpus/Test_feb19/Salida/Stats/s_genero.csv'
            self.sbigen = 'Corpus/Test_feb19/Salida/Stats/s_bi_genero.csv'
            self.strigen = 'Corpus/Test_feb19/Salida/Stats/s_tri_genero.csv'
            self.sbig = 'Corpus/Test_feb19/Salida/Graph/grafo_bi_genero.csv'
            self.strig = 'Corpus/Test_feb19/Salida/Graph/grafo_tri_genero.csv'
            

    def may19(self, opcion=5):
        if(opcion == 5):
            self.entrada = 'Corpus/Mayo19/resglobal.txt'
            self.suni = 'Corpus/Mayo19/Salida/Stats/uni_general.csv'
            self.sbi = 'Corpus/Mayo19/Salida/Stats/bi_general.csv'
            self.stri = 'Corpus/Mayo19/Salida/Stats/tri_general.csv'
            self.sbig = 'Corpus/Mayo19/Salida/Graph/grafo_bi_general.csv'
            self.strig = 'Corpus/Mayo19/Salida/Graph/grafo_tri_general.csv'
        else:
            self.entrada = 'Corpus/Mayo19/Respuestas_vT.csv'
            self.suni = 'Corpus/Mayo19/Salida/Stats/uni_porusuario.csv'
            self.sidlp = 'Corpus/Mayo19/Salida/Stats/idlp_general.csv'
            self.sgen = 'Corpus/Mayo19/Salida/Stats/s_genero.csv'
            self.sbigen = 'Corpus/Mayo19/Salida/Stats/s_bi_genero.csv'
            self.strigen = 'Corpus/Mayo19/Salida/Stats/s_tri_genero.csv'
            self.sbig = 'Corpus/Mayo19/Salida/Graph/grafo_bi_genero.csv'
            self.strig = 'Corpus/Mayo19/Salida/Graph/grafo_tri_genero.csv'


    def baseline(self, opcion=7):
        self.entrada = 'Corpus/BaseLine/CorpusVdeG.csv'
        self.suni = 'Corpus/BaseLine/Salida/Stats/uni_general.csv'
