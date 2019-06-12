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

    def mudaEstado(self, simbolo, Qatual):
        if (Qatual, simbolo) not in self.transicoes:
            if (Qatual, '&') not in self.transicoes:
                return []
            aux = self.transicoes[(Qatual, '&')]
            for i in aux:
                if (i, simbolo) in self.transicoes:
                    return self.mudaEstado(simbolo, i)
        return self.transicoes[(Qatual, simbolo)]
        

    # TODO: percorre cadeias para AFNE
    def percorreAFNE(self, sequencia, estadoatual):
        if sequencia == '':
            return estadoatual in self.F
        proxseq = sequencia[0]
        checaestado = (estadoatual, proxseq)
        print(checaestado, ' -> ', end='')
        if checaestado in self.transicoes:
            proxest = self.transicoes[checaestado]
            for est in proxest:
                if (est not in proxest[0]):
                    print('Backtracking!')
                    print(checaestado, ' -> ', end='')
                print(est)
                if self.percorreAFNE(sequencia[1:], est):
                    return True
        return False

    def existe(self, est):
        if (est, '&') in self.transicoes:
            return True
        return False

    #acho que ta funcionando o e-fecho ;p
    def efecho(self, est):
        if(self.existe(est) == False):
            return [est]
        else:
            aux = [est]
            for i in range(len(self.transicoes[(est,'&')])):
                a = self.transicoes[(est,'&')][i]
                aux += self.efecho(a)
                #return [est] + self.efecho(a)
        return aux


    def printAFNE(self):
        print('\n\n--------\033[1;34mAFN COM E TRANSICOES\033[0;0m--------\n')
        print('Estados: ',self.Q)
        print('Alfabeto: ',self.S)
        print('Estado inicial: ',self.q0)
        print('Estados finais: ',self.F)
        print('Transições:')
        print('(Estado atual, Simbolo) -> Estados resultantes\n')
        for i in self.transicoes:
            print(i,' -> ',self.transicoes[i])
