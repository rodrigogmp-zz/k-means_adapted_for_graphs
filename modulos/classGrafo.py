'''
Arquivo onde está implementada a classe Grafo, que é a classe mãe herdada por todas as classes de estruturas de dados, sendo
elas MatrizAdj, MatrizInc, ListaAdj
'''
class Grafo(object):
    def __init__(self, numVertices, listaArestas, dicPosVertices, numDepositos):
        self.numVertices = numVertices
        self.listaArestas = listaArestas
        self.dicPosVertices = dicPosVertices
        self.numDepositos = numDepositos
        
    def atualizaDicVertice(self, u):
        self.dicPosVertices[u] = -1 #Seta com -1 o valor respectivo a posição atual do vértice que foi deletado
        ultimo = len(self.dicPosVertices) -1
        while ultimo > u:
            if self.dicPosVertices[ultimo] != -1: #Atualiza o dicionário decrementando o valor de cada posição em 1
                self.dicPosVertices[ultimo] -= 1
            ultimo -= 1
        self.numVertices -= 1 #Decrementa o número de vértices
        
    