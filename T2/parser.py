from arvBin import No
from AFN_E import AFN_E
from AFD import AFD
from ast import literal_eval
import sys

def aridade ( simb ) :
    if (simb == '*') : return 1
    if (simb == '.') : return 2
    if (simb == '+') : return 2
    return 0

def pertence(simb,conjunto):
    for i in conjunto:
        if(i == simb):
            return True
    return False


numEstados = 0
pilhaIniciais= []
pilhafinais = []
pilhaSimbolos = []

# conforme o processo indutivo visto em sala
#TODO: converter da arv bin para afne
def criaAFNE(exp, afne):
    global numEstados
    global pilhaIniciais
    global pilhafinais
    global pilhaSimbolos

    # afne = AFN_E()
    if(aridade(exp.simbolo) == 0): # &, vazia ou a pertencente ao alfabeto
        if(exp.simbolo == '&'):
            #chega a um novo estado final
            Qini = 'q' + str(numEstados)
            Qf = 'q' + str(numEstados + 1)
            afne.Q.append(Qini)
            afne.q0 = Qini
            pilhaIniciais.append(Qini)
            afne.F = Qf
            afne.Q.append(Qf)
            pilhafinais.append(Qf)
            afne.transicoes[(Qini, '&')] = [Qf]
            numEstados = numEstados+2
            # afne.transicoes.append()
        elif(exp.simbolo == ''):
            #criar estado qualquer nao final
            afne.Q.append('q' + str(numEstados))
            afne.q0 = 'q' + str(numEstados)
            pilhaIniciais.append(afne.q0)
            numEstados = numEstados+1
        else:
            #estado atual lendo exp[0] vai para estado final
            Qini = 'q' + str(numEstados)
            pilhaIniciais.append(Qini)
            Qf = 'q' + str(numEstados + 1)
            pilhafinais.append(Qf)
            pilhaSimbolos.append(exp.simbolo)
            afne.Q.append(Qini)
            afne.Q.append(Qf)
            afne.q0 = Qini
            afne.F = Qf
            afne.transicoes[(Qini, exp.simbolo)] = [Qf]
            if exp.simbolo not in afne.S:
                afne.S.append(exp.simbolo)
            numEstados += 2
            return afne

    elif(aridade(exp.simbolo) == 1): # operador *
        criaAFNE(exp.direita, afne)

        afne.Q.append('q' + str(numEstados))
        ini = pilhaIniciais.pop() if pilhaIniciais != [] else ''
        aux2= []
        if pertence(('q'+ str(numEstados), '&'),afne.transicoes):
            aux2 = afne.transicoes[('q'+ str(numEstados), '&')]

        afne.transicoes[('q'+str(numEstados), '&')] = aux2 + [ini] + ['q'+str(numEstados+1)]
        afne.q0 = 'q'+str(numEstados)

        numEstados = numEstados + 1

        afne.Q.append('q' + str(numEstados))
        afne.F = 'q' + str(numEstados)
        if pilhafinais != []:
            f = pilhafinais.pop()
            aux2 = []
            if pertence((f,'&'),afne.transicoes):
                aux2 = afne.transicoes[(f,'&')]
            afne.transicoes[(f,'&')] = aux2 + [ini] + ['q' + str(numEstados)]

        pilhaIniciais.append('q' + str(numEstados-1))
        pilhafinais.append('q' + str(numEstados))
        numEstados = numEstados + 1


    else:   # entao aridade = 2
        if(exp.simbolo == '+'):
            esquerda = criaAFNE(exp.esquerda, afne)
            direita = criaAFNE(exp.direita, afne)

            Qini = 'q' + str(numEstados)
            ini1 = pilhaIniciais.pop() if pilhaIniciais != [] else ''
            ini2 = pilhaIniciais.pop() if pilhaIniciais != [] else ''
            Qf = 'q' + str(numEstados + 1)

            aux2 = []
            if pertence((Qini, '&'), afne.transicoes):
                aux2 = afne.transicoes[(Qini, '&')]
            afne.transicoes[(Qini, '&')] = aux2 + [ini2] + [ini1]

            afne.q0 = Qini
            afne.F = Qf

            f1 = pilhafinais.pop() if pilhafinais != [] else ''
            f2 = pilhafinais.pop() if pilhafinais != [] else ''

            aux2 = []
            if pertence((f2, '&'), afne.transicoes):
                aux2 = afne.transicoes[(f2, '&')]
            afne.transicoes[(f2, '&')] = aux2 + [Qf]

            aux3 = []
            if pertence((f1, '&'), afne.transicoes):
                aux3 = afne.transicoes[(f1, '&')]
            afne.transicoes[(f1, '&')] = aux3 + [Qf]

            afne.Q.append(Qini)
            afne.Q.append(Qf)


            numEstados += 2
            pilhaIniciais.append(Qini)
            pilhafinais.append(Qf)

        if(exp.simbolo == '.'):
            criaAFNE(exp.esquerda, afne)
            criaAFNE(exp.direita, afne)
            
            ini1 = pilhaIniciais.pop() if pilhaIniciais != [] else ''
            ini2 = pilhaIniciais.pop() if pilhaIniciais != [] else ''

            f1 = pilhafinais.pop() if pilhafinais != [] else ''
            f2 = pilhafinais.pop() if pilhafinais != [] else ''


            afne.q0 = ini2 #Qini
            afne.F = f1 #Qf


            afne.transicoes[(f2, '&')] = [ini1]
            pilhaIniciais.append(ini2)
            pilhafinais.append(f1)

    return afne


def infixa_posfixa(infixa):
    if len(infixa) <= 1: return infixa
    infixa = '(' + infixa + ')'
    pos = ''
    pilha = []

    for letra in infixa:
        if letra == ')':
            if pilha == []: return ''
            pos += pilha.pop()
            pos += ')'

        elif letra in ['+', '.', '*']:
            pilha.append(letra)

        else:
            pos += letra

    pos = pos.replace('(', '').replace(')', '')
    return pos

def criaArvore(exp):
    if len(exp) <= 1: return No(exp)

    pilha = []

    for simb in exp:
        if simb not in ['+', '.', '*']:
            noOperando = No(simb)
            pilha.append(noOperando)
        
        elif simb == '*':
            noOperando = No(simb, direita=pilha.pop())
            # direita = pilha.pop()
            pilha.append(noOperando)

        else:
            op1 = pilha.pop()
            op2 = pilha.pop()
            noOperando = No(simb, esquerda=op2, direita=op1)
            pilha.append(noOperando)
    
    return pilha.pop()

def criaAFD(afne):
    afd = AFD('none',False)
    geraQ(afne, afd)
    afd.S = afne.S

    for i in afd.Q: # i é um estado de Q (str)
        aux = literal_eval(i)       # o estado de Q como lista

        for a in aux:               # para cada elemento da lista aux
            if afne.F == a:         #afne.F é um estado! (str)
                if i not in afd.F:
                    afd.F.append(i)
    return afd

def geraQ(afne, afd):
    listaEfecho = {} # dict
    for i in afne.Q:
        listaEfecho[i] = afne.efecho(i)

    pilha = []
    efechoini = listaEfecho[afne.q0]
    afd.q0 = str(efechoini)
    pilha.append(efechoini)

    aux = []

    while pilha != []:
        conjunto = []
        naoProcessado = pilha.pop()
        afd.Q.append(str(naoProcessado))

        for simbolo in afne.S:
            resp = []
            for estado in naoProcessado:
                if (estado, simbolo) in afne.transicoes:
                    aux = listaEfecho[afne.transicoes[(estado, simbolo)][0]]
                    for item in aux:
                        if item not in resp:
                            resp.append(item)

            afd.deltad[(str(naoProcessado), simbolo)] = str(resp)
            if resp not in conjunto:
                conjunto.append(resp)

        for conj in conjunto:
            if str(conj) not in afd.Q and conj not in pilha and conj != []:
                    pilha.append(conj)

    return afd

if __name__ == '__main__':
    # e = ''
    # e = '&'
    # e = '0*'
    # e = '0+1'
    # e = '0.1'
    # e = '1.(0+1)'
    # e = '(0+1)*'

    # e = '(0.(1*))+(1.(0*))'
    # e = '(((0.1)*)+((1.0)*))+((0.((1.0)*))+(1.((0.1)*)))'
    # e = '((&+1).((0.1)*)).(&+0)'
    e = '(((0*).(1*))*).((0.(0.0)).((0+1)*))'

    no = criaArvore(infixa_posfixa(e))
    no.printEmNivel()

    afne = criaAFNE(no, AFN_E())

    afne.printAFNE()
    print("\n\n")

    afd = criaAFD(afne)

    afd.printAFD()

    while (1) :
        # inserindo uma cadeia para testar no afn e no afd
        sequencia = input('\033[1;34mInsira uma sequencia para o reconhecimento:\033[0;0m')

        # garantir que todos os caracteres pertencem ao alfabeto
        while afd.validacaocadeia(sequencia) != True :
            print(' ')
            print('\033[1;34mCadeia inválida!\033[0;0m')
            sequencia = input('\033[1;34mInsira uma sequencia para o reconhecimento:\033[0;0m')
        print(' ')

        print('\n\033[1;34mCadeia a ser testada: \033[0;0m', sequencia, '\n')

        # mostrar o percorrimento da cadeia no afd
        print("\n\033[1;34mReconhecimento da cadeia no AFD\033[0;0m\n")
        b = afd.percorreAFD(sequencia, afd.q0)

        # veredito do reconhecimento da cadeia
        if b :
            print('\n\033[1;92mA cadeia é reconhecida pelo automato!\033[0;0m\n')
        else :
            print('\n\033[1;91mA cadeia nao é reconhecida pelo automato!\033[0;0m\n')