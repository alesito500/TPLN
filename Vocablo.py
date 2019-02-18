from math import exp
class Vocablo:
    def __init__(self, word):
        self.word = word
        self.tf = 0
        self.position = []
        self.DPj = 0

    def incTF(self):
        self.tf = self.tf + 1

    def fillZeros(self, position):
        lb = len(self.position)
        self.position = self.position + ([0]*(position-lb))

    def incPos(self, position):
        self.incTF()
        if position == 0 and len(self.position) == 0:
            self.position.append(1)
        elif len(self.position) < position:
            self.fillZeros(position)
            self.position.append(1)
        elif len(self.position) == position:
            self.position.append(1)
        else:
            self.position[position] = self.position[position] + 1

    def getTF(self):
        return self.tf

    def n(self):
        return len(self.position)

    def indice( self, i):
        return ((i+1)//self.n())*100

    def IDLV( self, I):
        if I > 0:
            for i, v in enumerate(self.position):
                if self.n() > 1:
                    self.DPj = self.DPj + (exp(-2.3*(self.indice(i)/(self.n() - 1)))*(v/I))
                else:
                    continue
        return self.DPj
