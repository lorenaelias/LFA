from APF import APF
from APP import APP

def converteAPFemAPP (apf):
    app = APP("none", False)
    app.Q = apf.Q
    app.Q.append('q')
    app.Q.append('f')

    app.S = apf.S

    app.T = apf.T
    app.T.append('X')

    app.q0 = 'q'
    app.F = ['f']

    app.Z = 'X'

    app.delta[(app.q0, '&', app.Z)] = [(apf.q0, apf.Z+app.Z)]
    for i in apf.F:
        qq = any
        apf.delta[(i, '&', qq)] = [(app.F[0], '&')]

    return app

def converteAPPemAPF(app):
    apf = APF("none",False)
    apf.Z = "X"
    apf.Q = app.Q
    apf.Q.append("q")
    apf.Q.append("f")

    apf.S = app.S

    apf.T = app.T
    apf.T.append(apf.Z)

    apf.q0 = "q"
    apf.F = ["f"]

    apf.delta[('p', '&', 'X')] = [(app.q0, app.Z+apf.Z)]
    for i in app.Q:
        apf.delta[(i, '&', 'X')] = [(apf.F[0], '&')]
    return apf

if __name__ == '__main__':

    apf = APF("wwR.txt", True)
    apf.printAPF()

    # app = APP("none", False)
    # app.printAPF()

    app = converteAPFemAPP(apf)
    app.printAPP()

    while (1):
        sequencia = input('\033[1;34mInsira uma sequencia para o reconhecimento:\033[0;0m')

        # garantir que todos os caracteres pertencem ao alfabeto
        while apf.validacaocadeia(sequencia) != True :
            print(' ')
            print('\033[1;34mCadeia inválida!\033[0;0m')
            sequencia = input('\033[1;34mInsira uma sequencia para o reconhecimento:\033[0;0m')
        print(' ')

        print('\n\033[1;34mCadeia a ser testada: \033[0;0m', sequencia, '\n')

        print("\n\033[1;34mReconhecimento da cadeia no APF\033[0;0m\n")
        b = apf.percorreAPF(sequencia, apf.q0, [apf.Z])

        # veredito do reconhecimento da cadeia
        if b :
            print('\n\033[1;92mA cadeia é reconhecida pelo automato!\033[0;0m\n')
        else :
            print('\n\033[1;91mA cadeia nao é reconhecida pelo automato!\033[0;0m\n')