from Gramatica import Gramatica

g = Gramatica(arquivo='gr.txt')
print(g)
g.removeUnitario()
g.removeInuteis()
print(g)
print(g.P, type(g.P))
print(list(g.P.keys()))
# print(g.V, type(g.V))