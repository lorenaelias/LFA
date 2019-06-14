class APF:
    def __init__(self,nomeArq,flg):
        if flg:
            arq = open(nomeArq, 'r')
            self.Q = arq.readline().rstrip().split()
            self.S = arq.readline().rstrip().split()
            self.T = arq.readline().rstrip().split()
            self.q0 = arq.readline().strip()
            self.Z = arq.readline().strip()
            self.F = arq.readline().rstrip().split()
            transicoes = arq.readlines()
            self.delta = {}

            matriz = []
            for i in range(len(transicoes)) :
                matriz.append(transicoes[i].strip().split())


            for k in range(len(matriz)) :
                if matriz[k][2] == '[]' :
                    self.delta[matriz[k][0], matriz[k][1]] = []
                else:
                    aux = matriz[k]
                    aux = aux[3 :]
                    temp = []
                    if (matriz[k][0], matriz[k][1], matriz[k][2]) in self.delta:
                        temp = self.delta[matriz[k][0], matriz[k][1], matriz[k][2]]
                    self.delta[matriz[k][0], matriz[k][1], matriz[k][2]] = [tuple(aux)] + temp
                    # esse ultimo if serve para nao sobrescrever uma transicao quando existir
                    # mais de uma com a mesma key
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

    def efecho(self, est):
        efecho = [est]
        resultado = [est]
        while(efecho != []):
            est1 = efecho.pop()
            qq = any
            print("topo efecho: ",est1)
            if (est1, '&', qq) in self.delta:
                for i in self.delta[(est1, '&', qq)]:
                    if i not in efecho and i not in resultado:
                        efecho.append(i)
                    if i not in resultado:
                        resultado.append(i)
            else:
                if est1 not in resultado:
                    resultado.append(est1)
        return resultado

    def alteraPilha(self, estAt, a, pilhaAt, d2):
        novaPi = pilhaAt
        if d2 == '&':
            novaPi.pop()
        # elif d2 == pilhaAt.top():
        #     #nao modifica a pilha
        else:
            novaPi.append(d2.top())
        return novaPi


    def percorreAPF(self, sequencia, qAt, pilhaAt):
        if sequencia == "":
            if qAt in self.F:
                return True
            for i in self.F:
                if i in self.efecho(qAt):
                    return True
        else:
            a = sequencia[0]
            checaestado = (qAt, a, pilhaAt)
            print(checaestado, ' -> ', end='')

            if checaestado in self.delta:
                estAt = checaestado[0]
                for (d1, d2) in self.delta[(qAt,'&',pilhaAt.top())]:
                    estAt2 = d1
                    piAt = self.alteraPilha(estAt2, a, pilhaAt, d2)
                    self.percorreAPF(sequencia,d1,piAt)

                    if (d1, '&', pilhaAt):
                        estAt = d1
                        for (d1, d2) in self.delta[(qAt, '&', pilhaAt.top())]:
                            estAt2 = d1
                            piAt = self.alteraPilha(estAt2, a, pilhaAt, d2)
                            self.percorreAPF(sequencia,estAt2,piAt)

        return False

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