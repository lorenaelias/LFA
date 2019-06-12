class AFN_E:
    def __init__(self):
        # arq = open(nomeArq, 'r')
        # self.Q = arq.readline().strip().split(' ')
        # self.S = arq.readline().strip().split(' ')
        # self.q0 = str(arq.readline()).strip()
        # self.F = arq.readline().strip().split(' ')
        # self.transicoes = arq.readlines()
        # arq.close()

        self.Q = []
        self.S = []
        self.q0 = []
        self.F = []
        self.transicoes = {}

        # matriz = []
        # for i in range(len(self.transicoes)):
        #     matriz.append(self.transicoes[i].strip().split())
        # self.deltan: dict = {}
        # for k in range(len(matriz)):
        #     if (matriz[k][2] == '[]'):
        #         self.deltan[(matriz[k][0], matriz[k][1])] = []
        #     else:
        #         if (len(matriz[k]) == 3):
        #             self.deltan[(matriz[k][0], matriz[k][1])] = [matriz[k][2]]
        #         else:
        #             aux = matriz[k]
        #             aux = aux[2:]
        #             self.deltan[(matriz[k][0], matriz[k][1])] = aux


    def pertence(self, carac):
        if carac in self.S:
            return True
        return False

    def validacaocadeia(self, sequencia):
        for i in sequencia:
            if(self.pertence(i) == False):
                return False
        return True

    def existe(self, est):
        if (est, '&') in self.transicoes:
            return True
        return False

    def efecho( self, est ):
        efecho = [est]
        resultado = [est]
        while(efecho != []):
            est1 = efecho.pop()
            print("topo efecho: ",est1)
            if (est1, '&') in self.transicoes:
                for i in self.transicoes[(est1, '&')]:
                    if i not in efecho and i not in resultado:
                        efecho.append(i)
                    if i not in resultado:
                        resultado.append(i)
            else:
                if est1 not in resultado:
                    resultado.append(est1)
        return resultado

    def printAFNE(self):
        print('\n\n--------\033[1;34mAFN COM E TRANSICOES\033[0;0m--------\n')
        print('Estados: ',self.Q)
        print('Alfabeto: ',self.S)
        print('Estado inicial: ',self.q0)
        print('Estados finais: ',[self.F])
        print('Transições:')
        print('(Estado atual, Simbolo) -> Estados resultantes\n')
        for i in self.transicoes:
            print(i,' -> ',self.transicoes[i])
