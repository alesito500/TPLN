import Usuario as us
import Vocablo as vo
class Chunk:
    def __init__(self, number, idioma='en'):
        self.number = number
        self.idioma = idioma
        self.usuarios = {}
        self.vocablos = {}

    def newUser(self, uid, posts):
        if uid in self.usuarios:
            for el in posts:
                self.usuarios[uid].newPost(el, self.idioma)
        else:
            self.usuarios[uid] = us.Usuario(uid, posts, self.idioma)

    def UserGenre(self, uid, genre):
        self.usuarios[uid].setGenero(genre)

    def newWord(self, text):
        self.vocablos[text] = vo.Vocablo(text)

    def loadVocabulary(self):
        for k in self.usuarios.keys():
            for p in self.usuarios[k].posts:
                self.VofPost(p)

    def VofPost(self, text):
        for index, word in enumerate(text):
            if word.lower() not in self.vocablos:
                self.newWord(word.lower())
            self.vocablos[word.lower()].incPos(index)

    def userNames(self):
        return self.usuarios.keys()

    def calcIDLV(self):
        for k in self.vocablos.keys():
            self.vocablos[k].IDLV(len(self.userNames()))

    def loadUserIDLV(self):
        for k, v in self.usuarios.items():
            for p in v.posts:
                for word in p:
                    v.newEntry(self.vocablos[word.lower()].word, self.vocablos[word.lower()].IDLV(0))
        self.setUserMatrix()

    def loadUserF(self):
        for k, v in self.usuarios.items():
            for p in v.posts:
                for word in p:
                    v.newEntry(self.vocablos[word.lower()].word, 1)

    def setUserMatrix(self):
        for k,v in self.usuarios.items():
            v.idlvMATRIX()

    def getidlvMatrix(self):
        self.loadVocabulary()
        self.calcIDLV()
        self.loadUserIDLV()
        M = []
        for k, v in self.usuarios.items():
            M.append(v.vocposts)
        return M
