#  Operador unário (*) ainda não é tratado
from arvBin import No
from AFN_E import AFN_E
from AFD import AFD

def aridade ( simb ) :
    if (simb == '*') : return 1
    if (simb == '.') : return 2
    if (simb == '+') : return 2
    return 0


def prioridade ( simb ) :
    if (simb == '(') : return 0
    if (simb == '+') : return 1
    if (simb == '.') : return 2
    if (simb == '*') : return 3
    return -1

def ehOp(simb):
    return simb == '+' or simb == '.' or simb == '*' or simb == '(' or simb == ')'

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
            pilhaIniciais.append(afne.q0)
            afne.F = Qf
            afne.Q.append(Qf)
            pilhafinais.append(Qf)
            afne.transicoes[(Qini, '&')] = Qf
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
        afne.F = ['q' + str(numEstados)]
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

            print('esquerda -> ', esquerda.q0, '\ndireita -> ', direita.q0)

            aux2 = []
            if pertence((Qini, '&'), afne.transicoes):
                aux2 = afne.transicoes[(Qini, '&')]
            afne.transicoes[(Qini, '&')] = aux2 + [ini2] + [ini1]

            #afne.transicoes[(Qini, '&')] = [(ini2 + ' ' + ini1)]
            afne.q0 = Qini
            afne.F = Qf

            f1 = pilhafinais.pop() if pilhafinais != [] else ''
            f2 = pilhafinais.pop() if pilhafinais != [] else ''
            print('f1 -> ', f1, '\nf2 -> ', f2)
            #afne.transicoes[(f2, '&')] = [Qf]
            #afne.transicoes[(f1, '&')] = [Qf]

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

        #     afne.q0 = Qini
        #     afne.F = Qf

            numEstados += 2
            pilhaIniciais.append(afne.q0)
            pilhafinais.append(afne.F)

        if(exp.simbolo == '.'):
            criaAFNE(exp.esquerda, afne)
            criaAFNE(exp.direita, afne)
            
            ini1 = pilhaIniciais.pop() if pilhaIniciais != [] else ''
            ini2 = pilhaIniciais.pop() if pilhaIniciais != [] else ''

            f1 = pilhafinais.pop() if pilhafinais != [] else ''
            f2 = pilhafinais.pop() if pilhafinais != [] else ''

            #Qini = 'q' + str(numEstados)
            #Qf = 'q' + str(numEstados)

            #afne.Q.append(Qini)
            #afne.Q.append(Qf)
            afne.q0 = ini2 #Qini
            afne.F = f2 #Qf

            #afne.transicoes[(Qini, '&')] = [ini2]
            #afne.transicoes[(f1, '&')] = [Qf]

            #aux2 = []
            #if pertence((f1, '&'), afne.transicoes):
            #    aux2 = afne.transicoes[(f1, '&')]
            #afne.transicoes[(f1, '&')] = aux2 + [ini2]

            #numEstados += 2
            afne.transicoes[(f2, '&')] = [ini1]
            pilhaIniciais.append(afne.q0)
            pilhafinais.append(afne.F)

    return afne


def infixa_posfixa(infixa):
    if len(infixa) <= 1: return infixa
    infixa = '(' + infixa + ')'
    pos = ''
    pilha = []

    for letra in infixa:
        if letra == ')':
            if pilha == []: return ''
            # if pilha == []: return pos
            pos += pilha.pop()
            pos += ')'
        # elif letra == '*':

        elif letra in ['+', '.', '*']:
            # pilha += letra
            pilha.append(letra)

        else:
            pos += letra

    pos = pos.replace('(', '').replace(')', '')
    return pos

def infixa_prefixa(infixa):
    # infixa = '(' + infixa + ')'
    reversa = ''
    for i in infixa:
        # reversa = i + reversa
        if i == '(': reversa = ')' + reversa
        elif i == ')': reversa = '(' + reversa
        else: reversa = i + reversa

    aux = infixa_posfixa(reversa)[::-1]
    print('prefixa -> ', aux)
    return aux

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

def criaAFD(afne, afd):
    Qini = afne.efecho(afne.q0)
    afd.Q.append(Qini)
    afd.S = afne.S
    afd.q0 = Qini
    afd.Q = geraQ(afne, afd)
    afd.printAFD()
    #print('Novo Q -> ', afd.Q)

def geraQ(afne, afd):
    pilha = []
    Qini = afne.efecho(afne.q0)
    print(Qini)
    pilha.append(Qini)
    print('teste')
    print(afne.mudaEstado('0', 'q4'))
    #print(afne.efecho(afne.mudaEstado('0', 'q4')))

    while pilha != []:
        aux = pilha.pop()
        novoQ = []
        print('aux -> ', aux)
        for estado in aux:
            for simbolo in afne.S:
                print('Estado -> ', estado)
                temp = afne.mudaEstado(simbolo, estado)
                print('temp -> ', estado, '\t', simbolo, '\t', temp)
                #if temp == []:
                #    afd.Q.append('[vazio]')
                if temp != []:
                    temp = afne.transicoes[(temp, simbolo)]
                    temp = afne.efecho(temp)
                    afd.delta[(str(aux), simbolo)] = temp
                    print('novo temp \t->\t', temp)
                    #print('novo temp -> ', temp)
                    if temp not in novoQ:
                        novoQ.append(temp)
                        pilha.append(temp)
                    #novoQ.append(afne.mudaEstado(simbolo, estado))
                #elif temp == []:
                    #print('Entrou no if', temp, '\t', aux)
                    #for i in afne.S:
                        #afd.delta[(str(aux), i)] = '[vazio]'
            afd.Q.append(novoQ)
            print('novoQ -> ', novoQ)

    return afd.Q
                
    

if __name__ == '__main__':
    # e = 'A+(B.(C.(D*)))'
    # e = '(A+(B.C)).(D*)'
    # e = '(A+B)*'
    # e = '((0+1)*).(1.(0+1))'
    e = '0+1'
    # e = '(1*)+((0.1)*)'
    # e = '(0+1)+(2+3)'
    # e = '((0+1)*).(1.(0+1))'
    # e = '0+&'
    #print('e -> ', e)
    no = criaArvore(infixa_posfixa(e))
    no.printEmNivel()

    print("")

    afne = criaAFNE(no, AFN_E())
    print('AFNE')
    afne.printAFNE()
    print('efecho')
    #print(afne.efecho(afne.q0))

    #afne = AFN_E()
    #afne.Q = ['q0','q1']
    #afne.q0 = 'q0'
    #afne.S = ['a','b']
    #afne.F = ['q1']
    #afne.transicoes = { ('q0','a') : ['q0'],
    #                    ('q0','&') : ['q1'],
    #                    ('q1','b') : ['q1']  }
    # 
    #print('efecho 2')
    #afne.printAFNE()
    #print(afne.efecho(afne.q0))
    #print('Teste\n', afne.mudaEstado('1', afne.q0))

    afd = criaAFD(afne, AFD())
    #afd.printAFD()

    print('AFD')
    #afd.printAFD()

    # for i in range(len(a)):
    #     for j in range(len(a[i])):
    #         print(a[i][j].simbolo, end='\t')
    #     print('')
