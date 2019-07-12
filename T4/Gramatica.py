class Gramatica:
    def __init__(self, arquivo=None):
        if arquivo is None:
            self.V = []                                                                     #* Variáveis
            self.T = []                                                                     #* Terminais
            self.P = {}                                                                     #* Conjunto de regras
            self.S = []                                                                     #* Variavel inicial

        else:
            with open(arquivo, 'r') as arq:
                self.V = arq.readline().strip().split(' ')
                self.T = arq.readline().strip().split(' ')
                self.S = arq.readline().strip()
                # self.P = arq.read().split('\n')
                self.P = {}
                temp = arq.readlines()
                print(temp)


                matriz = []
                for i in range(len(temp)):
                    matriz.append(temp[i].strip().split())
                self.P: dict = {}
                print(matriz)
                for k in range(len(matriz)):
                   
                    if (len(matriz[k]) == 2):
                        self.P[(matriz[k][0])] = [matriz[k][1]]
                    else:
                        aux = matriz[k]
                        aux = aux[1:]
                        self.P[(matriz[k][0])] = aux
                    
                print(temp)

                self.disponivel = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

                # for i in range(len(self.P)):
                #     self.P[i] = self.P[i].split(' ')
                

    def __str__(self):
        print('V -> ', self.V)
        print('T -> ', self.T)
        print('S -> ', self.S)
        print('P ::\n')

        for i in self.P:
            print(i ,'->', self.P[i])

        return ''

    def existeregra(self, simb):
        for aux in self.P:
            for regra in self.P[aux]:
                # if len(self.P[aux]) == 1 and simb in self.P[aux]:
                # if simb in self.P[aux]:
                if simb == self.P[aux]:
                    print('Dentro da funcao -> ', aux)
                    return aux

        None

  #MAIS RECENTE!!! PARECE QUE DEU CERTO, TESTA AI

   #* Remove & produções
    def removeProducaoVazia(self):
        #* Detecta se há &-produção na variável inicial
        inicial = False
        for regra in self.P[self.S]:
            if '&' in regra:
                inicial = True

        resultado = [self.S]
        self.alcanceVariavel(resultado, self.S)
        # print('Resultados -> ', resultado)
        for i in resultado:
            for j in self.P[i]:
                if '&' in j:
                    inicial = True

        for variavel in list(self.P.keys()):
            for regra in self.P[variavel]:
                if regra == '&':
                    # print(variavel, self.P[variavel])
                    #* Exclui &-produções
                    # print('exclui')
                    self.P[variavel] = list(filter(lambda x: x != '&', self.P[variavel]))
                    # print('AAA', self.P[variavel])

                    #* Aplica & nas produções da própia variável
                    # anterior
                    # for producao in self.P[variavel]:
                    #     if variavel in producao:
                    #         # print('entrou no if', producao, variavel)
                    #         #* Formatação de string das novas repgras aplicando &
                    #         temp = self.P[variavel]
                    #         aux = (filter(lambda x: x != variavel, producao))
                    #         s = ''
                    #         for i in aux:
                    #             s += i
                    #         temp.append(s)
                    #         self.P[variavel] = temp
                            # self.P[variavel] += list(filter(lambda x: x != variavel, producao)) 
                            # print(self.P[variavel])
                    #anterior

                    marcados = []
                    for var in list(self.P.keys()):
                        for prod in self.P[var] :
                            for i in prod:
                                if i==variavel and (var, prod) not in marcados:
                                    marcados.append((var, prod))
                                    # print(var, prod)

                    # print(marcados)

                    while marcados != []:
                        auxmarc = marcados.pop()
                        # print(auxmarc)
                        aplicaE = ""

                        for i in auxmarc[1]:
                            if i != variavel:
                                aplicaE += i
                        # print(auxmarc[0], aplicaE)

                        if aplicaE not in self.P[auxmarc[0]]:
                            self.P[auxmarc[0]] += [aplicaE]

                        string1 = ""
                        length = len(auxmarc[1])
                        for i in range(length) :
                            if (auxmarc[1][i] == variavel) :
                                string1 = auxmarc[1][0 :i] + auxmarc[1][i + 1 :length]
                        print(string1)
                        if string1 not in self.P[auxmarc[0]]:
                            self.P[auxmarc[0]] += [string1]
                        for i in string1:
                            if i == variavel:
                                marcados.append((auxmarc[0], string1))

                        string2 = ""
                        length = len(auxmarc[1])
                        for i in range(length) :
                            if (auxmarc[1][i] == variavel) :
                                string2 = auxmarc[1][0 :i] + auxmarc[1][i + 1 :length]
                                break
                        print(string2)
                        if string2 not in self.P[auxmarc[0]]:
                            self.P[auxmarc[0]] += [string2]
                        for i in string2:
                            if i == variavel:
                                marcados.append((auxmarc[0], string2))



        if inicial: self.P[self.S] += '&'
        #* Exclui ''

        # print('GRAMATICA TESTE')
        for variavel in list(self.P.keys()):
            self.P[variavel] = list(filter(lambda x: x != '', self.P[variavel]))
        # print(self)   

        #* Verifica se há produções do tipo A -> [], caso houver, serão excluídas

        for variavel in list(self.P.keys()):
            if self.P[variavel] == []:
                self.V.remove(variavel)
        
        #* As variáveis são removidas do conjunto V, na simplificação serão consideradas não geradoras e removidas

    #* Remove regras da forma A -> B
    def removeUnitario(self):
        alterado = False                                   
        #* Regras do tipo A -> A podem ser removidas sem qualquer efeito
        while True:
            for regra in self.P:
                if regra in self.P[regra]:
                    self.P[regra] = list(filter(lambda x: x != regra, self.P[regra]))
                    alterado = True

            #* Percorre novamente o conjunto de regras buscando as unitárias
            for regra in self.P:
                for variavel in self.P[regra]:
                    # print('variavel -> ', variavel)
                    #* Verificar se a variável está em V exclui &, que será tratado a parte
                    if len(variavel) == 1 and variavel != '&' and variavel in self.V:
                        alterado = True
                        # print('tamanho 1 = ', variavel)
                        self.P[regra] = list(filter(lambda x: x != variavel, self.P[regra]))
                        # self.P[regra] = self.P[regra] + self.P[variavel]
                        self.P[regra] = self.P[regra] + list(filter(lambda x: x != '&', self.P[variavel]))

            if alterado == False:
                break
            else:
                alterado = False
        
        print('GRAMATICA TESTE')
        print(self)

    def alcanceVariavel(self, resultado, variavel):
        for regra in self.P[variavel]:
            for simbolo in regra:
                if simbolo in self.V:
                    # print('simbolo -> ', simbolo)
                    if simbolo not in resultado:
                        resultado.append(simbolo)
                        self.alcanceVariavel(resultado, simbolo)

    def removeInuteis(self):
        #* Remove simbolos não geradores

        for regra in list(self.P.keys()):
            for variavel in self.P[regra]:
                for simbolo in variavel:
                    # if simbolo not in self.T and simbolo not in self.V:
                    if simbolo not in list(self.P.keys()) and simbolo not in self.T and simbolo != '&':
                        # print('entrou no if', simbolo, self.P[regra], regra)
                        # print('variavel -> ', variavel)
                        self.P[regra] = list(filter(lambda x: x != variavel, self.P[regra]))

        print(self)
        print('intermediario')

        #* Remove símbolos não alcançáveis

        resultados = [self.S]
        self.alcanceVariavel(resultados, self.S)
        print('resultados', resultados)
        # print('testando')
        for variavel in list(self.P.keys()):
            if variavel not in resultados:
                # print(variavel)
                self.V = list(filter(lambda x: x != variavel, self.V))
                self.P.pop(variavel, None)

    def FNC(self):
        nVar = 0

        # for variavel in self.V:
        #     for regra in self.P[variavel]:
        #         for simbolo in regra:
        #             if simbolo in self.T:
        #                 self.P['V' + str(nVar)] = simbolo
        #                 regra.replace(simbolo, 'V' + str(nVar))

        #* Para cada terminal, é criada uma nova variável

        for variavel in list(self.P.keys()):
            for i in range(len(self.P[variavel])):
                for simbolo in self.P[variavel][i]:
                    if len(self.P[variavel][i]) == 2:
                        for j in range(len(self.P[variavel][i])):
                            if self.P[variavel][i][j] in self.T:
                                print('teste', self.P[variavel][i][j])
                                existe = self.existeregra(self.P[variavel][i])
                                if existe is not None:
                                    self.P[variavel][i] = self.P[variavel][i].replace(simbolo, existe)
                                    print('novoP -> ', self.P[variavel][i])
                                else:
                                    while True:
                                        nVar = self.disponivel[0]
                                        if nVar not in self.V:
                                            self.P[nVar] = simbolo
                                            self.P[variavel][i] = self.P[variavel][i].replace(simbolo, nVar)
                                            self.V.append(nVar)
                                            break
                                        else: self.disponivel = self.disponivel[1:]
                    if simbolo in self.T and len(self.P[variavel][i]) > 2:
                        # self.P['V' + str(nVar)] = simbolo
                        # self.P[variavel][i] = self.P[variavel][i].replace(simbolo, 'V' + str(nVar))
                        # nVar += 1
                        while True:
                            # print('teste disponivel', self.disponivel)
                            nVar = self.disponivel[0]
                            if nVar not in self.V:
                                self.P[nVar] = simbolo
                                self.P[variavel][i] = self.P[variavel][i].replace(simbolo, nVar)
                                self.disponivel = self.disponivel[1:]
                                self.V.append(nVar)
                                break
                            else: self.disponivel = self.disponivel[1:]

        for variavel in list(self.P.keys()):
            for i in range(len(self.P[variavel])):
                if len(self.P[variavel][i]) > 2:
                    while True:
                        nVar = self.disponivel[0]
                        if nVar not in self.V:
                            self.P[nVar] = self.P[variavel][i][1:]
                            self.P[variavel][i] = self.P[variavel][i][0] + nVar
                            self.disponivel = self.disponivel[1:]
                            self.V.append(nVar)
                            break
                        else: self.disponivel = self.disponivel[1:]


    def FNC2(self):
        # nVar = 0
        for variavel in list(self.P.keys()):
            for i in range(len(self.P[variavel])):
                if len(self.P[variavel][i]) >= 2:
                    for simbolo in self.P[variavel][i]:
                        if simbolo in self.T and simbolo not in self.V:
                            #* Cria nova variável
                            # self.P['V' + str(nVar) + '_'] = simbolo
                            # self.P[variavel][i] = self.P[variavel][i].replace(simbolo, 'V' + str(nVar) + '_')
                            # nVar += 1
                            existe = self.existeregra(simbolo)
                            if existe is not None:
                                self.P[variavel][i] = self.P[variavel][i].replace(simbolo, existe)
                                if existe not in self.V:
                                    self.V.append(existe)
                            else:
                                while True:
                                    nVar = self.disponivel[0]
                                    if nVar not in self.V:
                                        self.P[nVar] = simbolo
                                        self.P[variavel][i] = self.P[variavel][i].replace(simbolo, nVar)
                                        self.disponivel = self.disponivel[1:]
                                        if nVar not in self.V:
                                            self.V.append(nVar)
                                        break
                                    else: self.disponivel = self.disponivel[1:]

        alterado = False
        while True:
            for variavel in list(self.P.keys()):
                for i in range(len(self.P[variavel])):
                    if len(self.P[variavel][i]) > 2:
                        alterado = True
                        # print('entrou no if', self.P[variavel][i])
                        # self.P['V' + str(nVar) + '_'] = self.P[variavel][i][1:]
                        # self.P[variavel][i] = self.P[variavel][i][0] + 'V' + str(nVar) + '_'
                        # nVar += 1
                        # alterado = True
                        existe = self.existeregra(self.P[variavel][i][1:])
                        # print('existe -> ', existe)
                        if existe is not None:
                            self.P[variavel][i] = self.P[variavel][i][0] + existe
                            if existe not in self.V: self.V.append(existe)
                        else:
                            while True:
                                nVar = self.disponivel[0]
                                if nVar not in self.V:
                                    self.P[nVar] = self.P[variavel][i][1:]
                                    self.P[variavel][i] = self.P[variavel][i][0] + nVar
                                    self.disponivel = self.disponivel[1:]
                                    if nVar not in self.V:
                                        self.V.append(nVar)
                                    break
                                else:self.disponivel = self.disponivel[1:]
            
            if alterado == False: break
            else:
                alterado = False