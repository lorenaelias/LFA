from Gramatica import Gramatica

g = Gramatica(arquivo='t4.txt')
print(g)
g.removeProducaoVazia()
g.removeUnitario()
g.removeInuteis()
print(g)
input()
g.FNC2()
# g.FNC2()
print(g)
# print(g.P, type(g.P))
# print(list(g.P.keys()))
# teste = []
# g.alcanceVariavel(teste, variavel=g.S)
# print('alcanceVariavel')
# print(teste)
# print(g.V, type(g.V))