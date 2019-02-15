import getingdic as gd
import normalization as n
class Usuario:
    def __init__(self, uid, posts):
        self.uid = uid
        self.posts = []
        self.userDic = {}
        self.vocposts = []
        self.genero = ''
        if(len(posts) > 0):
            for el in posts:
                self.newPost(el)

    def newPost(self, text):
        self.posts.append(n.normalize_post(text, True))

    def newEntry(self, text, IDLV):
        if text not in self.userDic:
            self.userDic[text] = IDLV

    def sortVocabulary(self):
        items = [(v,k) for k, v in self.userDic.items()]
        items.sort()
        items.reverse()
        items = [(k, v) for v, k in items]
        return items

    def idlvMATRIX(self):
        for k, v in self.sortVocabulary():
            self.vocposts.append(v)

    def setGenero(self, genre):
        self.genero = genre
