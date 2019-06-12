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
                if (matriz[k][2] == '[]') :
                    self.delta[matriz[k][0], matriz[k][1]] = []
                else :
                    aux = matriz[k]
                    aux = aux[3 :]
                    self.delta[matriz[k][0], matriz[k][1], matriz[k][2]] = [tuple(aux)]

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

    def percorreAPF(self, sequencia, qAt, pilhaAt):
        if sequencia == "":
            return self.pertence(qAt,self.F)
        else:
            #TODO: RECURSAO DA ACEITAÇÃO
            return

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