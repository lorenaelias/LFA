from AFP import AFP
import sys

p = AFP(sys.argv[1])                                                #  Nome do arquivo que contêm o AFP, passado pelo terminal
cadeia = sys.argv[2]                                                #  Cadeia a ser percorrida
print(p)
# print(p.efecho(p.q0))
# print(p.getRegraPilha('0', p.q0))
# print(p.alteraPilha('&', '1', ['Z', '0', '0']))
# p.efecho(p.q0, p.pilha)
print(p.percorre(cadeia, p.q0, p.pilha))
# A = p.efechoRecursivo(p.q0, p.pilha, [])
# for i in A:
    # print(i)
# print(p.percorreCadeia(cadeia, p.q0, p.pilha))