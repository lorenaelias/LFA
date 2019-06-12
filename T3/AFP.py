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

    #     return resultado

    def efecho(self, estado):
        efecho = [estado]                                                   #? Entender melhor a função dessa variável
        resultado = [estado]                                                #* Resultado da função, inclui o estado de entrada
        dic = {}                                                            #* Nova função delta que exclui o elemento da pilha das tuplas

        for i in self.delta:
            dic[(i[0], i[1])] = (self.delta[i])[0]                          #* (Simbolo, Estado) -> Novo Estado

        while efecho != []:                                                 #* Enquanto não houver novos estados a serem processados...
            naoProcessado = (efecho.pop())                                  #* Desempilha um estado não processado
            print('Topo efecho: ', naoProcessado, type(naoProcessado))
            if ('&', naoProcessado) in dic:                                 #* Se existir uma E-transição a partir do estado pego...
                for i in dic[('&', naoProcessado)]:                         #* Percorra todas as possibilidades
                    if i not in efecho and i not in resultado:              #* Se for encontrado um estado novo para todos os contextos...
                        efecho.append(i)
                    if i not in resultado:                                  #* Adicionar ao conjunto de resultados
                        resultado.append(i)
            elif naoProcessado not in resultado:                            #* Caso o estado pego ainda não tenha sido adicionado...
                resultado.append(naoProcessado)
        print('Resultado efecho -> ', resultado)
        return resultado

    
    def percorreCadeia(self, cadeia, estadoAtual, pilha):
        if cadeia == '':
            return estadoAtual in self.F or pilha == [] #or pilha == [self.Z]   #! pilha == [self.Z] é usado apenas pra teste
        
        carAtual = cadeia[0]
        verEstado = (carAtual, estadoAtual, pilha[-1])                      #* Tupla a ser processada pela função delta: (Simbolo, Estado, Topo da pilha)
        print('verEstado -> ', verEstado)

        if verEstado in self.delta:                                         #* Caso exista a tupla dentro do conjunto de regras
            proxEstado = self.delta[verEstado]                              #* Aplicando delta
            transicao = self.efecho(proxEstado[0])
            print('transicao -> ', transicao)
            print('ProxEstado -> ', proxEstado, end='\n\n\n')

            if proxEstado[1] == '&': pilha.pop()                            #* Caso a regra de delta seja &, desempilhar o topo da pilha
            if len(proxEstado[1]) == 2: pilha.append(proxEstado[1][1])      #* Caso o tamanho seja 2 (XX, YY, XZ, ...), empilhar o segundo simbolo
            
            #! Regras em que o topo permanece inalterado são escritas no arquivo como um único caractere, aquele que se espera
            #! que permaneça no topo

            print('pilha -> ', pilha)
            for estado in proxEstado:                                       #* Percorra o conjunto de estados gerado por delta
                if estado not in proxEstado[0]:                             #? Entender melhor a condição de backtracking!
                    print('Backtracking!')
                    print(verEstado, ' -> ', end='')
                print(estado, '\t', type(estado))

                if self.percorreCadeia(cadeia[1:], estado[0], pilha):
                    return True

        return False