from AFP import *
import sys

p = AFP(sys.argv[1])                                                #  Nome do arquivo que contêm o AFP, passado pelo terminal
cadeia = sys.argv[2]                                                #  Cadeia a ser percorrida
print(p)
# print(p.efecho(p.q0))
print(p.getRegraPilha('0', p.q0))
print(p.alteraPilha('&', '1', ['Z', '0', '0']))
p.efecho(p.q0, p.pilha)
# print(p.percorreCadeia(cadeia, p.q0, p.pilha))