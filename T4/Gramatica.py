class Gramatica:
    def __init__(self, arquivo=None):
        if arquivo is None:
            self.V = []                                                                     #* Variáveis
            self.T = []                                                                     #* Terminais
            self.P = {}                                                                     #* Conjunto de regras
            self.S = []                                                                     #* Variavel inicial

        else:
            with open(arquivo, 'r') as arq:
                self.V = arq.readline().strip()
                self.T = arq.readline().strip()
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

    # def fechoVariavel(self, var):
    #     for regra in self.P:
    #         if var != regra[0] and 

    #* Remove regras da forma A -> B
    def removeUnitario(self):                                   
        for regra in self.P:
            if regra in self.P[regra]:
                # print('teste', regra, self.P[regra])
                self.P[regra] = list(filter(lambda x: x != regra, self.P[regra]))

        # for i in self.P:
        #     print('teste, ', i)
        #     i = list(filter(lambda x, y: x == y, i))