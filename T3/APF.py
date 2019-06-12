from APP import APP

class APF:
    def __init__(self,nomeArq,flg):
        if flg:
            arq = open(nomeArq, 'r')
            self.Q = arq.readline()[0].rstrip().split()
            self.S = arq.readline()[1].rstrip().split()
            self.T = arq.readline()[2].rstrip().split()
            self.q0 = arq.readline()[3].strip()
            self.Z = arq.readline()[4].strip()
            self.F = arq.readline()[5].rstrip().split()
            transicoes = arq.readline()[6 :]
            self.delta = {}
            for i in range(len(transicoes)):
                self.delta[i] = transicoes[i].rstrip().split()
            arq.close()
        else:
            self.Q = []
            self.S = []
            self.T = []
            self.q0 = ""
            self.Z = ""
            self.F = []
            self.delta = {}

    def pertence(self, elemento, conjunto):
        if elemento in conjunto:
            return True
        return False

    def validacaocadeia(self, sequencia):
        for i in sequencia :
            if not self.pertence(i, self.S):
                return False
        return True

    # TODO: PERCORRE CADEIA NO APF
    def percorreAPF(self, sequencia, qAt, pilhaAt):
        if sequencia == "":
            return self.pertence(qAt,self.F)

    # TODO: CONVERSAO APF PARA APP
    def converteAPFemAPP(self):
        app = APP("none",False)
        return app

    def printAPF(self):
        print('\n\n-------\033[1;34mAUTOMATO DE PILHA POR ESTADO FINAL\033[0;0m-------\n')
        print('Estados: ', self.Q)
        print('Alfabeto: ', self.S)
        print('Alfabeto da pilha: ', self.T)
        print('Estado inicial: ', self.q0)
        print('Simbolo inicial da pilha: ', self.Z)
        print('Estados finais: ', self.F)
        print('Transições:')
        print('(Estado atual\tSimbolo)->\tEstado resultante\n')
        for i in self.delta:
            print(i,' -> ',self.delta[i])
        print('\n-------------------------------------------------\n')