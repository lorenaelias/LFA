"""
    TODO: Falta concertar o efecho, a ideia é retornar uma lista de tuplas que contém (Estado, Nova pilha alterada, Topo antigo)
    *   Percorrimento funcionando e utilizando a pilha
"""
class AFP:
    def __init__(self, nomeArq):
        with open(nomeArq, 'r') as arq:
            self.Q     = arq.readline().strip().split(' ')                 #*  Estados
            self.S     = arq.readline().strip().split(' ')                 #*  Alfabeto de símbolos
            self.T     = arq.readline().strip().split(' ')                 #*  Alfabeto da pilha
            self.Z     = arq.readline().strip()                            #*  Simbolo inicial da pilha
            self.q0    = arq.readline().strip()                            #*  Estado inicial
            self.F     = arq.readline().strip().split(' ')                 #*  Estados Finais
            self.pilha = [self.Z]                                          #*  Pilha do automato

            # TODO: IMPLEMENTAR DELTA
            # TODO: IMPLEMENTAR EFECHO E CORRIGIR A FUNÇÃO DE PERCORRIMENTO DA CADEIA

            self.delta = {}                                              #*  Sintaxe: (Simbolo, Estado atual, Topo da pilha) -> (Estados / Ação da pilha)

            transicoes = arq.read().split('\n')
            for i in range(len(transicoes)):
                transicoes[i] = transicoes[i].split(' / ')
                transicoes[i][0] = transicoes[i][0].strip().split(' ')
                print(transicoes[i])
            

            for i in transicoes:
                self.delta[(i[0][0], i[0][1], i[0][2])] = (i[0][2:][1:], i[1])


    def __str__(self):
        Q  = 'Q  -> '   + str(self.Q)
        S  = '\nS  -> ' + str(self.S)
        T  = '\nT -> '  + str(self.T)
        Z  = '\nZ  -> ' + str(self.Z)
        q0 = '\nq0 -> ' + str(self.q0)
        F  = '\nF  -> ' + str(self.F)

        print(Q, S, T, Z, q0, F)

        for i in self.delta:
            print(i, ' -> ', self.delta[i])

        return ''

    # TODO: Efecho de um estado com pilha

    """
    * Se a regra tiver tamnaho 1 (regra == X), retornar pilha inalterada
    * Se a regra tiver tamanho 1, mas for o simbolo especial (regra == '&'), desempilhar a pilha e retornar ela junto com o pop
    * Se a regra tiver tamanho 2, mas retornar a pilha após empilhar o simbolo recebido
    * Caso seja empilhado, o antigo topo será irrelevante, nesse caso será retornado None na tupla
    """

    def alteraPilha(self, regra, simbolo, pilha):
        if regra == '&':
            print('Regra & -> ', regra)
            antigoTopo = pilha.pop()
            return pilha
            #return (pilha, antigoTopo)

        elif len(regra) == 1:
            print('Teste -> ', regra)
            return pilha
            # return (pilha, pilha[-1])

        elif len(regra) == 2:
            print('Regra que entrou na função = ', regra)
            pilha.append(simbolo)
            return pilha
            # return (pilha, None)

    def efecho(self, estado, pilha):
        efecho    = [ (estado, self.getRegraPilha('&', estado)) ]
        resultado = [ (estado, self.getRegraPilha('&', estado)) ]
        dic = {}

        for i in self.delta:
            dic [ (i[0], i[1]) ] = self.delta[i]

        # for i in dic:
            # print(i, '->', dic[i])
        # return

        while efecho != []:
            naoProcessado = efecho.pop()
            print('Nao processado -> ', naoProcessado, type(naoProcessado))
            if ('&', naoProcessado[0], self.getRegraPilha('&', naoProcessado[0])) in self.delta:
                for i in self.delta[ ('&', naoProcessado[0], self.getRegraPilha('&', naoProcessado[0])) ]:
                    print('i -> ', i, self.getRegraPilha('&', naoProcessado[0]))
                    print(self.delta[('&', naoProcessado[0], self.getRegraPilha('&', naoProcessado[0]))])
                    if (i[0], i[1]) not in resultado:
                        efecho.append( (i[1], self.getRegraPilha('&', naoProcessado[0])) )
                        print('A', i[1], self.getRegraPilha('&', naoProcessado[0]))
                    if (i[0], i[1]) not in resultado:
                        resultado.append( (i[1], self.getRegraPilha('&', naoProcessado[0])) )
                        print('B', i[1], self.getRegraPilha('&', naoProcessado[0]))

            elif naoProcessado[0] not in resultado:
                resultado.append( (self.delta[ ('&', i[1], i[2]) ][0], self.getRegraPilha('&', naoProcessado[0])) )
        print(resultado)
        return resultado

    def efechoRecursivo(self, estado, pilha, res):
        if ('&', estado, self.getTopoDelta('&', estado)) not in self.delta:
            return res
        resultado = [ (estado, pilha) ]
        for i in self.delta[ ('&', estado, self.getTopoDelta('&', estado)) ]:
            print('i -> ', i)
            resultado += ( (self.efechoRecursivo(i[0], self.alteraPilha(self.getRegraPilha('&', estado), '&', pilha)[0], resultado)) )
        return resultado

    def getTopoDelta(self, simbolo, estado):
        for i in self.delta:
            if i[0] == simbolo and i[1] == estado:
                return i[2]

    def getRegraPilha(self, simbolo, estado):
        resultado = []
        for i in self.delta:
            if simbolo == i[0] and estado == i[1]:
                # print(i)
                return self.delta[i][1]
                # resultado.append(i[2])
        print('regraPilha -> ', resultado)
        return resultado

    #? TESTAR ALTERAR O RETORNO DO EFECHO PARA ({Estados}, {Regras de pilha correspondentes})
    # def efecho(self, estado):
    #     efecho = [estado]
    #     resultado = [estado]
    #     dic = {}

    #     for i in self.delta:
    #         dic[(i[0], i[1])] = (self.delta[i])[0]

    #     print('dic\n', dic)
        
    #     while efecho != []:
    #         naoProcessado = (efecho.pop())
    #         print('Topo efecho = ', naoProcessado)
    #         if ('&', naoProcessado) in dic:
    #             for i in dic[('&', naoProcessado)]:
    #                 print('i -> ', i)
    #                 if i not in efecho and i not in resultado:
    #                     efecho.append( (i[1], self.getRegraPilha(i[0], i[1])) )
    #                 if i not in resultado:
    #                     resultado.append( (i[1], self.getRegraPilha(i[0], i[1])) )

    #                 elif naoProcessado not in resultado:
    #                     resultado.append( (naoProcessado, self.getRegraPilha(i[0], i[1])) )

    #     print('Resultado efecho -> ', resultado)
    #     return resultado
    
    # def percorreCadeia(self, cadeia, estadoAtual, pilha):
        # #* CONDIÇÃO DE PARADA DA RECURSÃO
        # if cadeia == '':
        #     return estadoAtual in self.F or pilha == [] #or pilha == [self.Z]   #! pilha == [self.Z] é usado apenas pra teste
        
        # carAtual = cadeia[0]
        # verEstado = (carAtual, estadoAtual, pilha[-1])                      #* Tupla a ser processada pela função delta: (Simbolo, Estado, Topo da pilha)
        # print('verEstado -> ', verEstado)

        # if verEstado in self.delta:                                         #* Caso exista a tupla dentro do conjunto de regras...
        #     proxEstado = self.delta[verEstado]                              #* Aplicando delta
        #     print('ProxEstado -> ', proxEstado, end='\n\n\n')

        #     if proxEstado[1] == '&': pilha.pop()                            #* Caso a regra de delta seja &, desempilhar o topo da pilha...
        #     if len(proxEstado[1]) == 2: pilha.append(proxEstado[1][1])      #* Caso o tamanho seja 2 (XX, YY, XZ, ...), empilhar o segundo simbolo...
            
        #     #! Regras em que o topo permanece inalterado são escritas no arquivo como um único caractere, aquele que se espera
        #     #! que permaneça no topo

        #     print('pilha -> ', pilha)
        #     for estado in proxEstado:                                                                     #* Percorra o conjunto de estados gerado por delta
        #         for q in self.efecho(estado[0]):                                                          #* Percorra o efecho do estado escolhido
        #             print('proxEstado[0] = ', proxEstado[0])
        #             if q not in proxEstado and pilha[-1] == verEstado[2]:                                 #? Entender melhor a condição de backtracking!
        #                 print('Backtracking!')
        #                 print(verEstado, ' -> ', end='')
        #                 print(q, '\t', type(estado))

        #             if self.percorreCadeia(cadeia[1:], q, pilha):
        #                 return True

        # return False

    def percorre(self, cadeia, estadoAtual, pilha):
        if cadeia == '':
            return estadoAtual in self.F or pilha == []

        carAtual = cadeia[0]
        verEstado = (carAtual, estadoAtual, pilha[-1])
        print('verEstado = ', verEstado)
        if verEstado in self.delta:
            proxEstado = self.delta[verEstado]
            print('proxEstado = ', proxEstado)
            regraPilha = proxEstado[1]
            for estado in proxEstado[0]:
                print('Estado1 -> ', estado[1])
                # print('estado = ', estado)
                # print('regraPilha = ', regraPilha)
                if (carAtual, estado, pilha[-1]) not in self.delta:
                    print('Backtracking')
                    print(verEstado, '->', end='', sep='\t')
                print(estado, carAtual, self.alteraPilha(self.getRegraPilha(carAtual, estado), carAtual, pilha))
                print('getRegraPilha = ', self.getRegraPilha(carAtual, estado))
                print(carAtual)
                # if self.percorre(cadeia[1:], estado, self.alteraPilha(self.getRegraPilha(carAtual, estado), carAtual, pilha)):
                if (carAtual, estado, pilha[-1]) in self.delta and self.percorre(cadeia[1:], estado, self.alteraPilha(self.delta[ (carAtual, estado, pilha[-1]) ][0], carAtual, pilha)):
                    return True
        
        return False