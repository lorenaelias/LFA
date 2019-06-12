class No:
    def __init__(self, simbolo, esquerda=None, direita=None):
        self.simbolo = simbolo
        self.esquerda = esquerda
        self.direita = direita

    def printEmNivel(self):
        niveis = self.criaNiveis()
        for i in range(len(niveis)):
            for j in range(len(niveis[i])):
                print(niveis[i][j].simbolo, end='\t')
            print('')

    def criaNiveis(self):
        niveis = [[self]]
        while niveis [-1]:
            proxNivel = []
            for no in niveis [-1]:
                proxNivel.extend( [no for no in (no.esquerda, no.direita) if no])
            niveis.append(proxNivel)
        return niveis

    def insereEsquerda(self, simbolo):
        if self.simbolo:
            if self.esquerda is None:
                self.esquerda = No(simbolo)
            else:
                self.esquerda.insereEsquerda(simbolo)
        else:
            self.simbolo = simbolo

    def insereDireita(self, simbolo):
        if self.simbolo:
            if self.direita is None:
                self.direita = No(simbolo)
            else:
                self.direita.insereDireita(simbolo)
        else:
            self.simbolo = simbolo