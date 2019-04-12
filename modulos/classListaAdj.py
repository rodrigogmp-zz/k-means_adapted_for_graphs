'''
Arquivo onde estão implementados a classe ListaAdj e seus respectivos métodos, inclusive parte do algoritmo kMeansAdapted.
Não obtivemos sucesso ao tentar implementar o algoritmo para esta classe(ListaAdj), por isso somente algumas funções que fazem parte
do algoritmo foram adaptadas, o que implica no não funcionamento do algoritmo nesta estrutura de dados.
'''
from modulos.classGrafo import Grafo
from copy import copy
from copy import deepcopy

class ListaAdj(Grafo):
    def __init__(self, numVertices, listaArestas, dicPosVertices, dicListaAresta, numDepositos):
        super().__init__(numVertices, listaArestas, dicPosVertices, dicListaAresta, numDepositos)
        self.__Lista = []
        for i in range(self.numVertices):
            self.__Lista.append([] * self.numVertices)
        for indice in range(0, len(listaArestas)):
            u = self.listaArestas[indice][0]
            v = self.listaArestas[indice][1]
            print("u:", u, "   v:", v)
            self.__Lista[self.dicPosVertices[u]].append(v)
            
        
        posicao = 0
        self.__dicPosDepositos = {} #Este dicionário indica, para cara depósito(chave), por qual vértice ele é representado(conteúdo)
        for deposito in range(0, self.numDepositos):
            self.__dicPosDepositos[posicao] = deposito
            posicao += 1


        self.__dicDepositosCidades = {}#Este dicionário indica, para cada depósito(chave), quais são as cidades que ele atende
        for deposito in range(0, self.numDepositos):
            listaCidades = []
            self.__dicDepositosCidades[deposito] = listaCidades

        for vertice in range(self.numDepositos, self.numVertices): #Inicialmente, todas as cidades(vértices) são atentidas pelo
            self.__dicDepositosCidades[0].append(vertice)          #primeiro depósito(0), para que o algoritmo kMeansAdapted
                                                                   #possa inicializar sua execução



        self.__listaDepositos = [] #Lista onde ficam armazenados os nomes dos vértices(cidades) que são(ou onde estão) os depósitos
        for vertice in range(0, self.numDepositos):
            self.__listaDepositos.append(vertice)

        
        self.dicAuxiliar = {} #Dicionário que auxilia o algoritmo kMeansAdapted a saber em qual posição da matriz
        posicao = 0           #estão os vertices, após uma possivel sequência de remoções de vértices
        
        for vertice in range(0, self.numVertices): #Cada vértice(cidade) começa em sua posição inicial(0:0, 1:1, ..., n:n)
            self.dicAuxiliar[posicao] = vertice
            posicao += 1


    def atualizaDicAux(self, u):
        self.dicAuxiliar[u] = -1 #Seta com -1 o valor respectivo a posição atual do vértice(cidade), que foi excluído(a)
        ultimo = len(self.dicAuxiliar) -1
        while ultimo > u:
            if self.dicAuxiliar[ultimo] != -1: #Atualiza o dicionário decrementando o valor de cada posição em 1
                self.dicAuxiliar[ultimo] -= 1
            ultimo -= 1
        self.numVertices -= 1 #Decrementa o número de vertices
    
    
    def delVertice(self, u):
        posU = self.dicPosVertices[u] #Pega a atual posição de u no dicionário de posições dos vértices.
        self.__Lista.pop(posU) #Retirando a linha correspondente ao vértice u.
        for vertice in range(0, len(self.__Lista)): #Percorre toda a lista procurando elementos que são predecessores
            if u in self.__Lista[vertice]:          #de u.
                self.__Lista[vertice].remove(u)

        listaRemove = []
        for i in range(0, len(self.listaArestas)): #Marcando arestas para serem removidas na listaArestas
            for j in range(0, len(self.listaArestas[i])):
                if self.listaArestas[i][j] == u:
                    listaRemove.append(i)


        for i in range(0, len(listaRemove)): #Removendo da listaArestas as arestas que ligavam u.
            self.listaArestas.pop(listaRemove[i])
            for j in range(0, len(listaRemove)):
                listaRemove[j] -= 1
        
        self.atualizaDicVertice(u)


    
    def criaListaArestasFloyd(self, matriz): #Recebe uma matriz reduzida contendo o resultado da execução
                                             #do algoritmo de FloydWarshall correspondente a um depósito
                                             #e as cidades que este atende e então, monta uma lista de arestas
                                             #que posteriormente é utilizada para converter esta matriz reduzida
                                             #para uma Matriz de Incidências
        listaArestasFloyd = []
        for linha in range(0, len(matriz)):
            for coluna in range(0, len(matriz)):
                listaArestasFloyd.append(0)
                listaArestasFloyd.append(0)
                listaArestasFloyd.append(0)

        numSubListas = len(listaArestasFloyd)//3
        listaArestasFloyd = [listaArestasFloyd[i::numSubListas] for i in range(numSubListas)]
        elemento = 0
        for linha in range(0, len(matriz)):
            for coluna in range(0, len(matriz)):
                if linha != coluna:
                    listaArestasFloyd[elemento][0] = linha
                    listaArestasFloyd[elemento][1] = coluna
                    listaArestasFloyd[elemento][2] = matriz[linha][coluna]
                    elemento +=1
                else:
                    listaArestasFloyd[elemento][0] = linha
                    listaArestasFloyd[elemento][1] = coluna
                    listaArestasFloyd[elemento][2] = 1000
                    elemento +=1

        return listaArestasFloyd
    
    
    def conversaoParaMatAdj(self): #Converte a atual Matriz de Incidência para Matriz de Adjacência ou Lista de Adjacência
        from modulos.classMatAdj import MatrizAdj
        matAdj = MatrizAdj(self.numVertices, self.listaArestas, self.dicPosVertices, self.dicListaArestas, self.numDepositos)
        matrizFloyd = MatrizAdj(self.numVertices, self.listaArestas, self.dicPosVertices, self.dicListaArestas, self.numDepositos)
        matrizFloyd.__matriz = matAdj.floydWarshall() #Aplica o floyd warshall na matriz
        return matrizFloyd
        
    def atualizaCidadesDepositos(self, matriz): #Atualiza o depósitos de todas as cidades
        for cidade in range(0, len(self.dicPosVertices)): #para cada cidade existente

            if cidade not in self.__listaDepositos:# se a cidade não for um depósito

                depositoProximo = self.encontraDepositoMaisProximo(cidade, matriz) #encontra o depósito mais proximo

                self.atualizaDeposito(cidade, depositoProximo)
    
    def encontraDepositoAtual(self, cidade): #Busca para uma determinada cidade, qual é o deposito que a atende atualmente
        depositoAtual = -1 #inicia o depósito atual como -1(inexistente)
        for deposito in range(0, len(self.__dicDepositosCidades)): #para cada depósito existente
            if cidade in self.__dicDepositosCidades[deposito]: #verifica se a cidade está sendo atendida por algum depósito
                depositoAtual = deposito #coloca como depósito atual este depósito

        return depositoAtual
        
    def encontraDepositoMaisProximo(self, cidade, lista):
        contadorCidades = cidade*(self.numVertices-1) #multiplica-se pelo numero de vértices-1 devido a listaArestas ter ligações de cada vertice com outro
        menorCaminho = self.listaArestas[contadorCidades][2] #inicia com o primeiro valor da linha para o menorCaminho
        depositoAtual = self.encontraDepositoAtual(cidade)
        depositoAtual = self.__dicPosDepositos[depositoAtual]
        contadorDepositos = 0
        for coluna in range(0, len(lista[self.dicPosVertices[cidade]]) or contadorDepositos < self.numDepositos):#tamanho de uma "linha" da listaAresta
            if self.listaArestas[contadorCidades][2] < menorCaminho:
                if coluna in self.__listaDepositos: #se for um valor menor que o atual menorCaminho e for um depósito, faz-se as alterações
                    contadorDepositos += 1
                    depositoAtual = coluna 
                    menorCaminho = self.listaArestas[contadorCidades][2]
            contadorCidades = contadorCidades+1
        for vertice in self.dicPosVertices: #confirma o valor do depósito atual
            if self.dicPosVertices[vertice] == depositoAtual:
                depositoAtual = vertice
        return depositoAtual
        
        
    def atualizaDeposito(self, cidade, novoDeposito): #Atribui ao depósito mais próximo, a cidade passada por parâmetro, e retira do depósito antigo, FALTA MELHORAR, DA PARA USAR A ENCONTRA DEPOSITO ATUAL AQUI PARA OTIMIZAR.
        depositoAtual = self.encontraDepositoAtual(cidade)#encontra o depósito que atende atualmente a cidade passada
                                                          #por parametro
        for i in range(0, len(self.__dicDepositosCidades)):#procura em qual depósito está a cidade
           
            if cidade in self.__dicDepositosCidades[i]:#se a cidade está na lista que o depósito atende
                   
                self.__dicDepositosCidades[i].remove(cidade) #remove a cidade da lista de cidades do depósito
 
        for dep in self.__dicPosDepositos:#para cada depósito(chave) no dicionário, verifica:
            if self.__dicPosDepositos[dep] == novoDeposito:#se a cidade que será novo depósito, estiver na lista daquele
                novoDeposito = dep                         #deposito, guarda a chave do depósito em que ela se encontra

        if cidade not in self.__dicDepositosCidades[novoDeposito]: #Se a cidade já não estiver no depósito, então
                                                                   #deve adicioná-la ao depósito
            self.__dicDepositosCidades[novoDeposito].append(cidade)
    
    def setaDicAux(self): #atualiza dicionario auxiliar com a situação atual dos vértices
        posicao = 0
        for vertice in range(0, self.numVertices):
            self.dicAuxiliar[posicao] = vertice
            posicao += 1
            
    def calculaSomatorio(self, cidade, listaReduzida): #calcula o menor somatório entre as linhas da lista adjacente passada
        contadorCidades = cidade*(self.numVertices-1) #inicializa o valor de acordo com a posição da listaAresta que varia no número de vértices pra cada vértice
        somatorio = 0
        for coluna in range(0, len(listaReduzida[self.dicPosVertices[cidade]])):
            somatorio = somatorio+self.listaArestas[contadorCidades][2] #
            contadorCidades = contadorCidades+1
        return somatorio
    
    def defineDeposito(self, listaReduzida, chaveDeposito): #Define o novo depósito para a matriz de distancias daquele depositos e as cidades que ele atende.
        if len(self.__dicDepositosCidades[chaveDeposito]) > 1: #se o depósito atender pelo menos duas cidades, então o cálculo é feito
            somatorioDistancias = 0 #inicia o somatório das distancias de cada cidade somo 0
            menorSomatorio = calculaSomatorio(0, listaReduzida) #assume como menor somatóriocal culado da linha 0
            novoDeposito = -1 #como ainda não se sabe o novoDepósito, este inicia-se como -1(desconhecido)
            depositoParaRemover = -1 #Como não se sabe se o depósito será alterado, começa-se com -1 também
            for linha in range(0, len(listaReduzida)): #encontra possivel deposito pelo menor somatorio de caminhos
                somatorioDistancias = calculaSomatorio(linha, listaReduzida) #calcula o valor do somatorio
                if somatorioDistancias <= menorSomatorio: #atuliza o valor do menor somatório
                    menorSomatorio = somatorioDistancias
                    novoDeposito = linha
            for vertice in self.dicAuxiliar:
                if self.dicAuxiliar[vertice] == novoDeposito:
                    novoDeposito = vertice
                    break
            if novoDeposito not in self.__listaDepositos:
                if novoDeposito != self.__dicPosDepositos[chaveDeposito]: #se o novo depósito for diferente do atual
                    chaveAntigoDeposito = -1 #variável auxiliar p/ gravar a chave que guarda a cidade que será o novoDepósito
                    for deposito in self.__dicDepositosCidades: #para cada depósito existete
                        if self.dicPosVertices[novoDeposito] in self.__dicDepositosCidades[deposito]:
                            chaveAntigoDeposito = deposito #guarda na var chaveAntigoDeposito a chave do antigoDeposito
                    antigoDeposito = self.__dicPosDepositos[chaveAntigoDeposito]#antigoDeposito
                    self.__listaDepositos.append(self.dicPosVertices[novoDeposito])#adiciona a lista de depósitos o novo depósito
                    self.__listaDepositos.remove(antigoDeposito)#removendo antigoDeposito da lista de Depositos Atuais do novo depósito
                    self.__dicPosDepositos[chaveAntigoDeposito] = self.dicPosVertices[novoDeposito]#novo dep atualizado no dicPosDepositos
                    self.__dicDepositosCidades[chaveAntigoDeposito].append(antigoDeposito)#adiciona o antigo deposito no dicDepositosCidades
                    self.__dicDepositosCidades[chaveAntigoDeposito].remove(self.dicPosVertices[novoDeposito])#remove o antigo

                
    def criaNovaMatriz(self, deposito, indice): #NÃO TERMINADA
        
        if len(self.__dicDepositosCidades[deposito]) > 1:
            listaCidades = [] #cria uma lista de cidades que ñ serão excluidas da matriz
            
            for cidade in range(0, len(self.__dicDepositosCidades[deposito])):#adiciona a lista todas as cidades que farão
                listaCidades.append(self.__dicDepositosCidades[deposito][cidade])#parte da matriz reduzida

            listaCidades.append(self.__dicPosDepositos[deposito])#adiciona também a lista o depósito que fará parte
                                                                 #da matriz reduzida
            m2 = deepcopy(self) #copia para outro obj matrizAdj a matrizAdj principal, para aproveitar a construção da
            for vertice in range(0, m2.numVertices):#matrizAdj
                if vertice not in listaCidades:#deleta todas as cidades não pertencentes às cidades atendidas pelo depósito
                    m2.delVertice(vertice)
            if self.__dicDepositosCidades[deposito]: #se o depósito não está vazio(se atende alguma cidade), copia
                self.dicAuxiliar = m2.dicPosVertices #o dicionario atual para o auxiliar
            
            m2.__matriz = m2.floydWarshall() #aplica o floydWarshall na matrizReduzida
            return m2.__matriz #retorna a matriz de caminhos minimos entre um depósito e as cidades que ele atende
        
        return False
    
    def kmeansAdapted(self): #NÃO TERMINADA
        matrizDis = self.conversaoParaMatAdj()#matriz obtida através do floydWarshall feito na matAdj
        self.criaListaArestasFloyd(matrizDis) #Cria listaAuxiliar para montar a matInc baseada na matrizFloyd
        novaLista = ListaAdj(self.numVertices, self.listaArestas, self.dicPosVertices, self.dicListaArestas, self.numDepositos)
        depProximo = self.encontraDepositoMaisProximo(14, novaLista.__Lista)
        print("dicionario de cidades dos depositos", self.__dicDepositosCidades)
        print("dicionario de posicao dos depositos", self.__dicPosDepositos)
        print("dicionario de posicao dos vertciess", self.dicPosVertices)
        print("listaDepositos", self.__listaDepositos)
        
        
