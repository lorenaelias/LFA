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
        elif d2 == pilhaAt[-1] or (d2 == '&' and a == '&'):
            return pilhaAt

        return novaPi


    def percorreAPF1(self, sequencia, qAt, pilhaAt):
        print("sequencia: ",sequencia)
        if sequencia == "":
            if qAt in self.F:
                print("sinal", qAt, " ", sequencia)
                return True
                # se chegou ate aqui e ainda nao esta em um est final, pode ser que com uma
                # etransicao consiga chegar a um
            a = '&'
            checaestado = (qAt, a, pilhaAt[-1])
            if checaestado in self.delta :
                prox = self.delta[checaestado]

                for (d1, d2) in prox :
                    print("to mandando ", (a, pilhaAt, d2))
                    piAt = self.alteraPilha(a, pilhaAt, d2)
                    print("\n(d1,d2): ", d1, d2)
                    print("piAt:  ", piAt)
                    print("pilhaAt: ", pilhaAt)
                    print(checaestado, ' -> ')
                    if self.percorreAPF("", d1, piAt):
                        return True

            for i in self.F:
                if i in self.efecho(qAt, pilhaAt[-1]):
                    print(i)
                    return True
            # return False
        else:
            a = sequencia[0]
            checaestado = (qAt, a, pilhaAt[-1])
            if checaestado in self.delta:

                prox = self.delta[checaestado]

                for (d1, d2) in prox:
                    print("to mandando ", (a, pilhaAt, d2))
                    piAt = self.alteraPilha(a, pilhaAt, d2)
                    print("\n(d1,d2): ",d1, d2)
                    print("piAt:  ", piAt)
                    print("pilhaAt: ", pilhaAt)
                    print(checaestado, ' -> ')
                    if self.percorreAPF(sequencia[1 :], d1, piAt) :
                        return True

            a = '&'
            checaestado = (qAt, a, pilhaAt[-1])
            if checaestado in self.delta:
                prox = self.delta[checaestado]

                for (d1, d2) in prox :
                    print("to mandando ", (a, pilhaAt, d2))
                    piAt = self.alteraPilha(a, pilhaAt, d2)
                    print("\n(d1,d2): ", d1, d2)
                    print("piAt:  ", piAt)
                    print("pilhaAt: ", pilhaAt)
                    print(checaestado, ' -> ')
                    if self.percorreAPF(sequencia, d1, piAt):
                        return True

        return False

    def percorreAPF2( self, estAtual, word, pi, antPi ) :
        a = word[0]
        for i in range(len(self.delta)):
            if word != "" and (
                    estAtual in self.delta[(estAtual, a, antPi)] and ( (estAtual, a, pi[-1]) in self.delta or ((estAtual, '&', pi[-1]))) and (
                    self.delta[(estAtual, any, pi[-1])] or self.delta[(estAtual, any, '&')])):
                antPi = pi[:]
                estAtual, pi = self.alteraPilha(estAtual, a, pi)


                if self.percorreAPF(estAtual, word, pi, antPi):
                    return True

                pi = antPi

        if len(pi) == 1 and estAtual in self.F and word == "&":
            return True

        return False

    pilhaux = []

    # esse ta funcionando pra 0n1n
    def percorreAPF3( self, sequencia, qAt, pilhaAt ) :
        print("\npilha ",pilhaAt)
        qAt2 = qAt

        global pilhaux


        if sequencia != "":
            a = sequencia[0]
            checaestado = (qAt, a, pilhaAt[-1])

            if checaestado in self.delta :
                prox = self.delta[checaestado]

                for (d1, d2) in prox :
                    qAt2 = d1
                    piAt = self.alteraPilha(a, pilhaAt, d2)
                    print(checaestado, "->", (d1, d2))
                    if self.percorreAPF(sequencia[1 :], d1, piAt) :
                        return True

            checaestado = (qAt, '&', pilhaAt[-1])
            if checaestado in self.delta:
                prox = self.delta[checaestado]

                for (d1, d2) in prox:
                    qAt2 = d1
                    piAt = self.alteraPilha('&', pilhaAt, d2)
                    print(checaestado, "->", (d1, d2))
                    if self.percorreAPF(sequencia, d1, piAt) :
                        return True

        elif qAt2 in self.F :
            return True
        else:
            for i in self.F :
                if i in self.efecho(qAt, pilhaAt[-1]) and sequencia == "" :
                    return True
        return False

    # esse ta funcionando pra 0n1n
    def percorreAPF ( self, sequencia, qAt, pilhaAt ) :
        print("\npilha ", pilhaAt)
        qAt2 = qAt
        for i in self.F :
            if i in self.efecho(qAt, pilhaAt[-1]) and sequencia == "" :
                return True

        if sequencia != "":
            a = sequencia[0]
            checaestado = (qAt, a, pilhaAt[-1])

            if checaestado in self.delta :
                prox = self.delta[checaestado]

                for (d1, d2) in prox :
                    qAt2 = d1
                    piAt = self.alteraPilha(a, pilhaAt, d2)
                    print(checaestado, "->", (d1, d2))
                    if self.percorreAPF(sequencia[1 :], d1, piAt) :
                        return True

            checaestado = (qAt, '&', pilhaAt[-1])
            if checaestado in self.delta :
                prox = self.delta[checaestado]

                for (d1, d2) in prox :
                    qAt2 = d1
                    piAt = self.alteraPilha('&', pilhaAt, d2)
                    print(checaestado, "->", (d1, d2))
                    if self.percorreAPF(sequencia, d1, piAt) :
                        return True

        elif qAt2 in self.F :
            return True
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