from Gramatica import Gramatica

# SIMPLIFICACAO DE GRAMATICAS
# SEGUIR OS PASSOS NA ORDEM:
#
# 1. ELIMINAR E-PRODUCOES           [ ]
# 2. ELIMINAR PRODUCOES UNITARIAS   [ ]
# 3. ELIMINAR SIMBOLOS INUTEIS      [x]


if __name__ == '__main__':

    g = Gramatica(arquivo='gr.txt') # gr por enquanto é só uma gramatica qq para teste
    print(g)

    g.removeInuteis()
    g.removeUnitario()

    print(g)

    # print(g.P, type(g.P))
    # print(list(g.P.keys()))
    # print(g.V, type(g.V))