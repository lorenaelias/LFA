class Gramatica:
    def __init__(self, arquivo=None):
        if arquivo is None:
            self.V = []                                               #* Variaveis
            self.T = []                                               #* Terminais
            self.P = {}                                               #* Regras de produção
            self.S = []                                               #* Variavel inicial

        else:
            with open(arquivo, 'r') as arq:
                self.V = arq.readline().strip().split(' ')
                self.T = arq.readline().strip().split(' ')
                self.S = arq.readline().strip()
                # self.P = arq.read().split('\n')
                self.P = {}
                temp = arq.readlines()

                matriz = []
                for i in range(len(temp)):
                    matriz.append(temp[i].strip().split())
                self.P: dict = {}

                for k in range(len(matriz)):
                    if (len(matriz[k]) == 2):
                        self.P[(matriz[k][0])] = [matriz[k][1]]
                    else:
                        aux = matriz[k]
                        aux = aux[1:]
                        self.P[(matriz[k][0])] = aux

                # for i in range(len(self.P)):
                #     self.P[i] = self.P[i].split(' ')

    def __str__(self):
        print('V -> ', self.V)
        print('T -> ', self.T)
        print('S -> ', self.S)
        print('P ::')

        for i in self.P:
            print("\t",i ,'->', self.P[i])

        return ''

    # def fechoVariavel(self, var):
    #     for regra in self.P:
    #         if var != regra[0] and 

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
                    if len(variavel) == 1 and variavel in self.V:
                        alterado = True
                        # print('tamanho 1 = ', variavel)
                        self.P[regra] = list(filter(lambda x: x != variavel, self.P[regra]))
                        self.P[regra] = self.P[regra] + self.P[variavel]

            if alterado == False:
                break
            else:
                alterado = False

    def removeInuteis(self):
        #* Remove simbolos não geradores

        inicio = self.S
        prox = self.P[inicio]
        pilhaux = []

        for regra in self.P:
            for i in regra:
                if i in self.P:
                    pilhaux.append(i)

        for regra in self.P:
            for axb in self.P[regra]:
                for i in axb:
                    if i not in self.P and i in self.V:
                        #print(regra," ->",axb," ->",i)      # os i's sao os nao geradores
                        self.P[regra].remove(axb)

        #* Remove símbolos não alcançáveis


        # for variavel in self.V:
