from AFP import *
import sys

p = AFP(sys.argv[1])                                                #  Nome do arquivo que contêm o AFP, passado pelo terminal
cadeia = sys.argv[2]                                                #  Cadeia a ser percorrida
print(p)
print(p.percorreCadeia(cadeia, p.q0, [p.Z]))
print(p.efecho(p.q0))