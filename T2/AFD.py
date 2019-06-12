class AFD:
    def __init__(self,nomeArq,leArq):
        if(leArq == True):
            arq = open(nomeArq, 'r')
            self.Q = arq.readline().strip().split(' ')
            self.S = arq.readline().strip().split(' ')
            self.q0 = str(arq.readline()).strip()
            self.F = arq.readline().strip().split(' ')
            self.transicoes = arq.readlines()
            arq.close()

            matriz = []
            for i in range(len(self.transicoes)):
                matriz.append(self.transicoes[i].strip().split())
            self.deltad = {}
            for k in range(len(matriz)):
                self.deltad[(matriz[k][0], matriz[k][1])] = matriz[k][2]
        else:
            self.Q = []
            self.S = []
            self.q0 = []
            self.F = []
            self.deltad = {}

    def pertence(self, carac):
        if carac in self.S:
            return True
        return False

    def validacaocadeia(self, sequencia):
        for i in sequencia:
            if(self.pertence(i) == False):
                return False
        return True


    def percorreAFD(self, sequencia, estadoAtual):
        if sequencia == '':
            return estadoAtual in self.F
        else:
            proxcaract = sequencia[0]
            dupla = (estadoAtual, proxcaract)
            if dupla in self.deltad:
                print(dupla," -> ",self.deltad[dupla])
                return self.percorreAFD(sequencia[1:], self.deltad[dupla])
            else:
                return False


    def printAFD(self):
        print('\n\n----------\033[1;34mAUTOMATO FINITO DETERMINISTICO\033[0;0m----------\n')
        print('Estados: ', self.Q)
        print('Alfabeto: ', self.S)
        print('Estado inicial: ', self.q0)
        print('Estados finais: ', self.F)
        print('Transições:')
        print('(Estado atual, Simbolo) -> Estado resultante\n')
        for i in self.deltad:
            print(i,' -> ',self.deltad[i])
        print('\n--------------------------------------------------\n')