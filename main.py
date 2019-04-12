'''
Fase 2 do trabalho de Algoritmos em Grafos
Problema: B
Implementado por: Rodrigo G. Marafelli Pereira, Vinícius G. Spinelli, Giovani F. Andrade Botelho

Arquivo principal do programa, onde as estruturas de dados são instanciadas e a função do algoritmo kMeansAdapted é chamada.
Todo o tratamento de leitura do arquivo.txt e colheta de atributos contidos no arquivo para construção do grafo nas estruturas
de dados são feitos aqui.
'''
from modulos.classGrafo import Grafo
from modulos.classMatAdj import MatrizAdj
from modulos.classMatInc import MatrizInc
from modulos.classListaAdj import ListaAdj
import sys
import time

inicio = time.time()

def obtemNumVertices(listaArquivo):       #Obtem a quantidades de vértice do grafo a ser construido, para posteriormente passar
    numVertices = int(listaArquivo[0][0]) #por parâmetro para o construtor da classe da estrutura de dados a ser utilizada
    return numVertices

def leArquivo(nomeArquivo): #função responsável por ler os dados do grafo no arquivo e retornar uma lista com os dados
    arquivo = open(nomeArquivo, 'r')
    listaArquivo = []
    for linha in arquivo:
        listaArquivo.append(linha)

    listaArquivo = [s.rstrip() for s in listaArquivo]         #procedimento para tirar os espaços e os \n das strings 
    listaArquivo = [_str.split(' ') for _str in listaArquivo] #obtidas na leitura do arquivo

    for subLista in range(0, len(listaArquivo)):
        listaArquivo[subLista] = listaArquivo[subLista][1:4]

    return listaArquivo

def criaDicPosVertices(listaArquivo, numVertices):#Como no inicio do programa o grafo ainda está íntegro(não passou por nenhuma
    dicPosVertices = {}#Possui nome do vértice como chave, e a linha em que se encontra como valor.
    posicao = 0
    for vertice in range(0, numVertices):
        dicPosVertices[posicao] = vertice
        posicao += 1
    
    return dicPosVertices

def obtemNumDepositos(listaArquivo):
    numDepositos = int(listaArquivo[0][2])
    return numDepositos

def aumentaValorVertices(listaArestas):
    for aresta in range(0, len(listaArestas)):
        listaArestas[aresta][0] = listaArestas[aresta][0]-1
        listaArestas[aresta][1] = listaArestas[aresta][1]-1

def calculaGap(somatorioDistanciasDepositos, nomeArquivo):
    if nomeArquivo == 'P1.txt':
        gap = ((somatorioDistanciasDepositos - 3034)/3034)*100
    if nomeArquivo == 'P2.txt':
        gap = ((somatorioDistanciasDepositos - 4445)/4445)*100
    if nomeArquivo == 'P3.txt':
        gap = ((somatorioDistanciasDepositos - 6634)/6634)*100
    if nomeArquivo == 'P4.txt':
        gap = ((somatorioDistanciasDepositos - 8162)/8162)*100
    if nomeArquivo == 'P5.txt':
        gap = ((somatorioDistanciasDepositos - 1789)/1789)*100
    if nomeArquivo == 'P6.txt':
        gap = ((somatorioDistanciasDepositos - 2961)/2961)*100
    if nomeArquivo == 'P7.txt':
        gap = ((somatorioDistanciasDepositos - 4498)/4498)*100
    if nomeArquivo == 'P8.txt':
        gap = ((somatorioDistanciasDepositos - 9297)/9297)*100
    if nomeArquivo == 'P9.txt':
        gap = ((somatorioDistanciasDepositos - 9934)/9934)*100
    if nomeArquivo == 'P10.txt':
        gap = ((somatorioDistanciasDepositos - 5128)/5128)*100
    
    return gap

nomeArquivo = input("Digite o nome do arquivo: ")
lista = leArquivo(nomeArquivo)
numVertices = obtemNumVertices(lista)
numDepositos = obtemNumDepositos(lista)
lista = lista[1:]
lista = [[int(a), int(b), int(c)] for a,b,c in lista]
aumentaValorVertices(lista)
dicPosVertices = criaDicPosVertices(lista, numVertices)
matriz = MatrizAdj(numVertices, lista, dicPosVertices, numDepositos)
matriz.kMeansAdapted()
fim = time.time()
somatorioDistanciasDepositos = matriz.calculaSomatoriosDistancias()
gap = calculaGap(somatorioDistanciasDepositos, nomeArquivo)
print("Somatório das distancias entre os depósitos e as cidades que eles atendem para o arquivo", nomeArquivo,
      ":", somatorioDistanciasDepositos, "\nTempo de execução:", fim-inicio, "segundos\n", "Gap:", gap, "%")
matriz.imprimeDicionariosDepositos()
