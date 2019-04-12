'''
Arquivo onde estão implementados a classe MatrizInc e seus respectivos métodos, inclusive parte do algoritmo kMeansAdapted.
Não obtivemos sucesso ao tentar implementar o algoritmo para esta classe(MatrizInc), por isso somente algumas funções que fazem parte
do algoritmo foram adaptadas, o que implica no não funcionamento do algoritmo nesta estrutura de dados.
'''
from modulos.classGrafo import Grafo
from modulos.classMatAdj import MatrizAdj
import sys
from copy import copy
from copy import deepcopy
class MatrizInc(Grafo):
    def __init__(self, numVertices, listaArestas, dicPosVertices, dicListaAresta, numDepositos):#listaArestas possui o valor do ponderamento
        super().__init__(numVertices, listaArestas, dicPosVertices, dicListaAresta, numDepositos)
        self.__matriz = []
        for i in range(len(self.listaArestas)):
            self.__matriz.append([0] * (self.numVertices)) #Matriz que representa a estrutura
                                                           #de dados Matriz de Incidência
        i = 0 #Indice utilizado para percorrer a listaArestas                                             
        contador = 0
       
        while contador < (len(self.listaArestas)):
            coluna1 = self.listaArestas[i][0]
            coluna2 = self.listaArestas[i][1]
            self.__matriz[contador][coluna1] = self.listaArestas[i][2]
            self.__matriz[contador][coluna2] = self.listaArestas[i][2]
            i += 1
            contador += 1

        posicao = 0
        self.__dicPosDepositos = {} #Este dicionário indica, para cara depósito(chave), por qual vértice ele é representado(conteúdo)
        for deposito in range(0, self.numDepositos):
            self.__dicPosDepositos[posicao] = deposito
            posicao += 1

        self.__dicDepositosCidades = {}#Este dicionário indica, para cada depósito(chave), quais são as cidades que ele atende
        for deposito in range(0, self.numDepositos):
            listaCidades = []
            self.__dicDepositosCidades[deposito] = listaCidades

        for vertice in range(self.numDepositos, self.numVertices):
            self.__dicDepositosCidades[0].append(vertice)

        self.__listaDepositos = []
        for vertice in range(0, self.numDepositos):
            self.__listaDepositos.append(vertice)

        
        self.dicAuxiliar = {}
        posicao = 0
        for vertice in range(0, self.numVertices):
            self.dicAuxiliar[posicao] = vertice
            posicao += 1
        
        self.listaArestasConversao = []

        
    def delVertice(self, u):
        posU = self.dicPosVertices[u]
        if posU == -1:
            print("O vértice", u, "não existe.")
        else:
            contador = 0
            for linha in range(0, len(self.__matriz)):#removendo a arestas(linhas) que são correspondentes ao vértice u
                if self.__matriz[contador][posU] != 0:
                    self.__matriz.pop(contador)
                else:
                    contador += 1
            listaRemove = []
            for i in range(0, len(self.listaArestas)):#colocando na lista que contém as arestas a serem removidas a posição do vértice u na lista de arestas
                for j in range(0, len(self.listaArestas[i])):
                    if self.listaArestas[i][j] == u:
                        listaRemove.append(i)


            for i in range(0, len(listaRemove)):#apagar o elemento na listaArestas releativo a posição guardada na listaRemove
                self.listaArestas.pop(listaRemove[i])
                for j in range(0, len(listaRemove)):#para cada elemento da listaRemove o valor é drecrementado em 1,
                    listaRemove[j] -= 1             #pois assim ele não irá apagar a posicao errada quando for retirado um elemento da linha

            self.atualizaDicVertice(u) #atualiza a posição do vértice no dicionário de posições dos vértices
            for linha in self.__matriz: #para cada linha da matriz
                linha.pop(posU) #remove o elemento da linha na posU. Quando encerrado o laço, a coluna toda terá sido removida.
    
    def conversaoParaMatAdj(self): #Converte a atual Matriz de Incidência para Matriz de Adjacência ou Lista de Adjacência
        from modulos.classMatAdj import MatrizAdj
        matAdj = MatrizAdj(self.numVertices, self.listaArestas, self.dicPosVertices, self.dicListaArestas, self.numDepositos)
        return matAdj


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
                    
        
    def encontraDepositoAtual(self, cidade): #Busca para uma determinada cidade, qual é o deposito que a atende atualmente
        depositoAtual = -1 #inicia o depósito atual como -1(inexistente)

        for deposito in range(0, len(self.__dicDepositosCidades)): #para cada depósito existente

            if cidade in self.__dicDepositosCidades[deposito]: #verifica se a cidade está sendo atendida por algum depósito e
                depositoAtual = deposito                       #define como depósito atual este depósito

        return depositoAtual 

    def atualizaDeposito(self, cidade, novoDeposito): #Atribui ao depósito mais próximo, a cidade passada por parâmetro, e retira do depósito antigo, FALTA MELHORAR, DA PARA USAR A ENCONTRA DEPOSITO ATUAL AQUI PARA OTIMIZAR.
        depositoAtual = self.encontraDepositoAtual(cidade)#encontra o depósito que atende atualmente a cidade passada
                                                          #por parametro
        
        for dep in self.__dicPosDepositos:#para cada depósito(chave) no dicionário, verifica:
            if self.__dicPosDepositos[dep] == novoDeposito:#se a cidade que será novo depósito, estiver na lista daquele
                novoDeposito = dep                         #deposito, guarda a chave do depósito em que ela se encontra

        if novoDeposito != depositoAtual: #Se o novo depósito for diferente do atual, fazer as devidas alterações
                                          #nos dicionários e listaDepositos

            for i in range(0, len(self.__dicDepositosCidades)):#procura em qual depósito está a cidade
            
                if cidade in self.__dicDepositosCidades[i]:#se a cidade está na lista que o depósito atende
                    
                    self.__dicDepositosCidades[i].remove(cidade) #remove a cidade da lista de cidades do depósito
    
            if cidade not in self.__dicDepositosCidades[novoDeposito]: #Se a cidade já não estiver no depósito, então
                                                                       #deve adicioná-la ao depósito
                self.__dicDepositosCidades[novoDeposito].append(cidade)

    def atualizaCidadesDepositos(self, matriz): #Atualiza o depósitos de todas as cidades. O critério utilizado é
                                                #o seguinte, para cada cidade, busca pelo depósito mais próximo, se
                                                #este depósito for diferente do depósito que a atende atualmente, então
                                                #a cidade passa a ser atendida pelo novo depósito.

        for cidade in range(0, self.numVertices): #para cada cidade existente

            if cidade not in self.__listaDepositos:#se a cidade não for um depósito

                depositoProximo = self.encontraDepositoMaisProximo(cidade, matriz) #encontra o depósito mais proximo

                atualizouDeposito = self.atualizaDeposito(cidade, depositoProximo) #coloca a cidade no depósito mais proximo

    def encontraDepositoMaisProximo(self, cidade, matriz): #Encontra, para a cidade recebida, qual é o depósito mais próximo
        menorCaminho = matriz[0][0] #inicia o menor caminho como sendo o valor do primeira cidade para ela mesma
        depositoAtual = self.encontraDepositoAtual(cidade) #encontra o depósito que atende esta cidade atualmente
        
        depositoAtual = self.__dicPosDepositos[depositoAtual]
        contadorDepositos = 0
        for linha in range(0, len(self.listaArestas) or contadorDepositos < self.numDepositos):
            if matriz[linha][cidade] != 0:
                for coluna in range(0, self.numVertices):
                    if coluna in self.__listaDepositos:
                        if matriz[linha][coluna] < menorCaminho and matriz[linha][coluna] != 0:
                            menorCaminho = matriz[linha][coluna]
                            depositoAtual = coluna
                            contadorDepositos += 1

        novoDeposito = depositoAtual
        for vertice in self.dicPosVertices: #Verifica qual é a chave correta do novo depósito da cidade
            if self.dicPosVertices[vertice] == depositoAtual:
                novoDeposito = vertice
        

        return novoDeposito
                        

    def defineDeposito(self, matrizDistancias, chaveDeposito): #NÃO TERMINADA
        for i in range(0, len(matrizDistancias)):
            print(matrizDistancias[i])
        if len(self.__dicDepositosCidades[chaveDeposito]) > 1: #se o depósito atender pelo menos duas cidades, então o cálculo é feito
            somatorioDistancias = 0
        

    def criaMatrizReduzida(self, deposito, chaveDeposito): #NÃO TERMINADA
       
        if len(self.__dicDepositosCidades[deposito]) > 1:
            listaCidades = [] #cria uma lista de cidades que ñ serão excluidas da matriz
            # for vertice in self.__dicPosDepositos: #para cada vertice em dicPosDepositos
            #     if self.__dicPosDepositos[vertice] == deposito: #se o dic na posicao vertices for igual ao deposito recebido
            #         chaveDeposito = vertice #a chave deposito recebe a variavel iterativa vertice
            
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
            return m2.__matriz #retorna a matriz de caminhos minimos entre um depósito e as cidades que ele atende

        return False


    def kmeansAdapted(self): #NÃO TERMINADA
        matAdj = self.conversaoParaMatAdj() 
        matrizDis = matAdj.floydWarshall()
        novaListaArestas = self.criaListaArestasFloyd(matrizDis)
        self = MatrizInc(self.numVertices, novaListaArestas, self.dicPosVertices, self.dicListaArestas, self.numDepositos)
        self.atualizaCidadesDepositos(self.__matriz)
        print(self.__dicDepositosCidades)
        print(matAdj.dicAuxiliar)
        matrizReduzida = self.criaMatrizReduzida(0,0)
        for i in range(0, len(matrizReduzida)):
            print(matrizReduzida[i])
        novaListaArestas = self.criaListaArestasFloyd(matrizReduzida)
        self.floydWarshall(matrizReduzida, novaListaArestas)

        
       

       


