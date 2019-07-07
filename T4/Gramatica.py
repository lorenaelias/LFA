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
    
    #* Remove & produções
    def removeProducaoVazia(self):
        #* Detecta se há &-produção na variável inicial
        inicial = False
        for regra in self.P[self.S]:
            if '&' in regra:
                inicial = True

        for variavel in self.V:
            for regra in self.P[variavel]:
                if regra == '&':
                    # print(variavel, self.P[variavel])
                    #* Exclui &-produções
                    print('exclui')
                    self.P[variavel] = list(filter(lambda x: x != '&', self.P[variavel]))
                    print(self.P[variavel])

                    #* Aplica & nas produções da própia variável
                    for producao in self.P[variavel]:
                        if variavel in producao:
                            print('entrou no if', producao, variavel)
                            self.P[variavel] += list(filter(lambda x: x != variavel, producao)) 
                            print(self.P[variavel])

        if inicial: self.P[self.S] += '&'

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
                        self.P[regra] = self.P[regra] + self.P[variavel]

            if alterado == False:
                break
            else:
                alterado = False

    def alcanceVariavel(self, resultado, variavel='S'):
        for regra in self.P[variavel]:
            for simbolo in regra:
                if simbolo in self.V:
                    # print('simbolo -> ', simbolo)
                    if simbolo not in resultado:
                        resultado.append(simbolo)
                        self.alcanceVariavel(resultado, variavel=simbolo)

    def removeInuteis(self):
        #* Remove simbolos não geradores

        for regra in self.P:
            for variavel in self.P[regra]:
                for simbolo in variavel:
                    if simbolo not in self.T and simbolo not in self.V:
                        # print('variavel -> ', variavel)
                        self.P[regra] = list(filter(lambda x: x != variavel, self.P[regra]))

        #* Remove símbolos não alcançáveis

        resultados = []
        self.alcanceVariavel(resultados)
        print(resultados)
        # print('testando')
        for variavel in list(self.P.keys()):
            if variavel not in resultados:
                # print(variavel)
                self.V = list(filter(lambda x: x != variavel, self.V))
                self.P.pop(variavel, None)