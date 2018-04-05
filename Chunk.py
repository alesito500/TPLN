import Usuario as us
import Vocablo as vo
class Chunk:
    def __init__(self, number):
        self.number = number
        self.usuarios = {}
        self.vocablos = {}

    def newUser(self, uid, posts):
        self.usuarios[uid] = us.Usuario(uid, posts)

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
