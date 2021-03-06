class APP:
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
            for i in range(len(transicoes)):
                matriz.append(transicoes[i].strip().split())

            for k in range(len(matriz)):
                if matriz[k][2] == '[]':
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


    def efecho(self, est, pi):
        efecho = [est]
        resultado = [est]
        while(efecho != []):
            qq : str
            est1 = efecho.pop()
            if (est1, '&', pi) in self.delta:
                for i in self.delta[(est1, '&', pi)]:
                    if i not in efecho and i not in resultado:
                        efecho.append(i[0])
                    if i not in resultado:
                        resultado.append(i[0])
            else:
                if est1 not in resultado:
                    resultado.append(est1)
        return resultado


    def alteraPilha(self, a, pilhaAt, d2):
        novaPi = pilhaAt
        if d2 == '&':
            novaPi.pop()
        elif len(d2) == 2:
            novaPi.append(d2[0])
        elif d2 == pilhaAt[-1]:
            return pilhaAt

        return novaPi

    pilhaux = []
    def esvaziapilha ( self ) :
        global pilhaux
        pilhaux = []


    def percorreAPP(self, sequencia, qAt, pilhaAt):
        print("\npilha ",pilhaAt)
        qAt2 = qAt

        if sequencia == "":
            if len(pilhaAt) == 0:
                print(qAt)
                return True
            else:
                checaestado = (qAt, '&', pilhaAt[-1])
                if checaestado in self.delta :
                    pilhaux.append(checaestado)
                    prox = self.delta[checaestado]

                    for (d1, d2) in prox :
                        qAt2 = d1
                        piAt = self.alteraPilha('&', pilhaAt, d2)
                        print(checaestado, "->", (d1, d2))
                        if self.percorreAPP(sequencia, d1, piAt):
                            return True

        if sequencia != "":
            a = sequencia[0]

            if len(pilhaAt) > 0:
                checaestado = (qAt, a, pilhaAt[-1])
                if checaestado in self.delta:
                    pilhaux.append(checaestado)
                    prox = self.delta[checaestado]

                    for (d1, d2) in prox :
                        qAt2 = d1
                        if len(pilhaAt) > 0 :
                            piAt = self.alteraPilha(a, pilhaAt, d2)
                        else: return False
                        print(checaestado, "->", (d1, d2))
                        if self.percorreAPP(sequencia[1 :], d1, piAt) :
                            return True
                        else:
                            if d2 == '&':
                                if len(pilhaAt) > 0 :
                                    piAt = self.alteraPilha('&', pilhaAt, d2)
                                else:
                                    return False
                                print(checaestado, "->", (d1, d2))
                                if self.percorreAPP(sequencia, d1, piAt) :
                                    return True

            if len(pilhaAt) > 0:

                checaestado = (qAt, '&', pilhaAt[-1])
                if checaestado in self.delta :
                    pilhaux.append(checaestado)
                    prox = self.delta[checaestado]

                    for (d1, d2) in prox:
                        qAt2 = d1
                        if len(pilhaAt) > 0 :
                            piAt = self.alteraPilha('&', pilhaAt, d2)
                        else: return False
                        print(checaestado, "->", (d1, d2))
                        if self.percorreAPP(sequencia, d1, piAt) :
                            return True


        #TODO: MUDAR O SIMBOLO DE DESEMPILHAR P NAO DAR PROB NO ALTERAPILHA

        return False

    registro = []

    def percorreAPP2 ( self, sequencia, qAt, pilhaAt ):
        global registro
        print("\npilha ", pilhaAt)
        qAt2 = qAt

        if sequencia == "":
            if len(pilhaAt) == 0 :
                print(qAt)
                return True
            else :
                checaestado = (qAt, '&', pilhaAt[-1])
                if checaestado in self.delta :
                    pilhaux.append(checaestado)
                    prox = self.delta[checaestado]

                    for (d1, d2) in prox :
                        qAt2 = d1
                        piAt = self.alteraPilha('&', pilhaAt, d2)
                        print(checaestado, "->", (d1, d2))
                        if self.percorreAPP(sequencia, d1, piAt) :
                            return True

        if sequencia != "":
            a = sequencia[0]
            if pilhaAt == []: return False

            checaestado = (qAt, '&', pilhaAt[-1])
            if checaestado in self.delta:

                pilhaux.append(checaestado)
                prox = self.delta[checaestado]

                if prox[0][1] == '&':

                    prox.append(pilhaAt[-1])
                    pilhaAt.pop()
                    registro.append(prox)

                else:
                    if len(prox) >= 3:
                        for i in range(1,len(prox)-1):
                            pilhaAt.append(prox[i])

                    registro.append(prox)

                qAt2 = prox[0]
                print(checaestado, "->", (prox[0], prox[1]))
                piAt = self.alteraPilha(a, pilhaAt, prox[1])
                if self.percorreAPP(sequencia, qAt2, piAt):
                    return True

            if pilhaAt == [] : return False
            checaestado = (qAt, a, pilhaAt[-1])
            if checaestado in self.delta:
                pilhaux.append(checaestado)
                prox = self.delta[checaestado]

                if prox[1] == '&':

                    prox.append(pilhaAt[-1])
                    pilhaAt.pop()
                    registro.append(prox)

                else:
                    if len(prox) >= 3:
                        for i in range(1,len(prox)-1):
                            pilhaAt.append(prox[i])


                if prox[1] == '&' and len(pilhaAt) > 0:
                    prox.append(pilhaAt[-1])
                    registro.append(prox)
                else:
                    registro.append(prox)


                qAt2 = prox[0]
                piAt = self.alteraPilha(a, pilhaAt, prox[1])
                print(checaestado, "->", (prox[0], prox[1]))
                if self.percorreAPP(sequencia[1:], qAt2, piAt) :
                    return True

        # TODO: MUDAR O SIMBOLO DE DESEMPILHAR P NAO DAR PROB NO ALTERAPILHA

        return False

    def printAPP(self):
        print('\n\n-------\033[1;34mAUTOMATO DE PILHA POR PILHA VAZIA\033[0;0m-------\n')
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