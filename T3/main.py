from APF import APF
from APP import APP

if __name__ == '__main__':

    apf = APF("none", False)
    apf.printAPF()

    app = APP("none", False)
    app.printAPF()

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
        b = apf.percorreAPF(sequencia, apf.q0)

        # veredito do reconhecimento da cadeia
        if b :
            print('\n\033[1;92mA cadeia é reconhecida pelo automato!\033[0;0m\n')
        else :
            print('\n\033[1;91mA cadeia nao é reconhecida pelo automato!\033[0;0m\n')