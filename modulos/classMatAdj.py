'''
Arquivo onde está implementado a classe MatrizAdj e seus respectivos métodos, inclusive o algoritmo kMenasAdapted.
Novos dicionários foram implementados nesta classe em relação à fase 1 do trabalho.
'''
from modulos.classGrafo import Grafo
import sys
from copy import deepcopy
class MatrizAdj(Grafo):
    def __init__(self, numVertices, listaArestas, dicPosVertices, numDepositos):
        super().__init__(numVertices, listaArestas, dicPosVertices, numDepositos)
        self.__matriz = []
        for i in range(self.numVertices):
            self.__matriz.append([0] * self.numVertices)#Matriz que representa a estrutura
                                                        #de Dados Matriz de Adjacência

        i = 0 #Índice utilizado para percorrer a listaArestas e construir a matrizAdj
        while i < (len(self.listaArestas)):
            linha = self.listaArestas[i][0] #A posicao 0 de cada subLista presente na listaArestas é equivalente a linha
            coluna = self.listaArestas[i][1]#A posicao 0 de cada subLista presente na listaArestas é equivalente a coluna
            self.__matriz[linha][coluna] = self.listaArestas[i][2]
            self.__matriz[coluna][linha] = self.listaArestas[i][2]
            i += 1
        
        posicao = 0
        self.__dicPosDepositos = {}                  #Este dicionário indica, para cara depósito(chave), por qual vértice ele
        for deposito in range(0, self.numDepositos): #é representado(valor correspondente à chave)

            self.__dicPosDepositos[posicao] = deposito #Inicialmente, se existem 20 depósitos para o grafo, então os 20 primeiros
            posicao += 1                               #vértices começam sendo depósitos


        self.__dicDepositosCidades = {}#Este dicionário indica, para cada depósito(chave), quais são as cidades que ele atende(lista)
        for deposito in range(0, self.numDepositos):
            listaCidades = []
            self.__dicDepositosCidades[deposito] = listaCidades

        for vertice in range(self.numDepositos, self.numVertices): #Inicialmente, todas as cidades(vértices) são atentidas pelo
            self.__dicDepositosCidades[0].append(vertice)          #primeiro depósito(0), para que o algoritmo kMeansAdapted
                                                                   #possa inicializar sua execução

        
        self.__listaDepositos = [] #Lista onde ficam armazenados os nomes dos vértices(cidades) que são(ou onde estão) os depósitos
        for vertice in range(0, self.numDepositos):
            self.__listaDepositos.append(vertice)

        
        self.dicAuxiliar = {} #Dicionário que auxilia o algoritmo kMeansAdapted a saber em qual posicão da matriz
        posicao = 0           #estão os vértices, após uma possivel sequência de remoções de vértices

        for vertice in range(0, self.numVertices): #Cada vértice(cidade) começa em sua posição inicial(0:0, 1:1,..., n:n)
            self.dicAuxiliar[posicao] = vertice
            posicao += 1


    def imprimeDicionariosDepositos(self):
        print("\nDicionário de nomes dos vértices que são depósitos:")
        print(self.__dicPosDepositos)
        print()
        print("Dicionário de depósitos mostrando as cidades atendidas por eles:")
        print(self.__dicDepositosCidades)

    def atualizaDicAux(self, u):
        self.dicAuxiliar[u] = -1 #Seta com -1 o valor respectivo a posição atual do vértice(cidade) que foi excluído(a)
        ultimo = len(self.dicAuxiliar) -1
        while ultimo > u:
            if self.dicAuxiliar[ultimo] != -1: #Atualiza o dicionário decrementando o valor de cada posição em 1
                self.dicAuxiliar[ultimo] -= 1
            ultimo -= 1
        self.numVertices -= 1 #Decrementa o número de vértices

    def setaDicAux(self): #Atribui valores iniciais à todos os valores correspondentes as chaves no dicionário(0:1,1:1,...,n:n)
        posicao = 0       #para que ele possa ser usado posteriormente em novas sequências de exclusões de vértices
        for vertice in range(0, self.numVertices):
            self.dicAuxiliar[posicao] = vertice
            posicao += 1
    

    def delVertice(self, u):
        posRemocao = self.dicPosVertices[u] #Pega a atual posição de u no dicionário de posições dos vértices.
        if posRemocao == -1:                #Se o valor da chave u no dicionário for -1, quer dizer que este vértice já foi excluído.
            print("O vértice", u, "não existe.")
        else:
            self.__matriz.pop(posRemocao) #Removendo linha correspondente ao vértice u.
            for linha in self.__matriz:   #Para cada linha da matriz.
                linha.pop(posRemocao)     #Remove o elemento da linha na posU. Quando encerrado o laço,
                                          #a coluna toda terá sido removida.
            listaRemove = []
            for i in range(0, len(self.listaArestas)):        #Adicionando todas as arestas incidentes ao vértice
                                                              #que foi excluido da matriz a uma lista auxiliar
                for j in range(0, len(self.listaArestas[i])): 
                    if self.listaArestas[i][j] == u:
                        listaRemove.append(i)


            for i in range(0, len(listaRemove)):      #Removendo todas as arestas incidentes ao vértice que foi exluido da listaArestas
                self.listaArestas.pop(listaRemove[i])
                for j in range(0, len(listaRemove)):
                    listaRemove[j] -= 1

            self.atualizaDicVertice(u) # Atualiza dicionário de posições dos vértices

    
    def conversaoParaMatInc(self): #Converte a atual Matriz de adjacência para Matriz de Incidência ou Lista de Adjacência
        from modulos.classMatInc import MatrizInc
        matInc = MatrizInc(self.numVertices, self.listaArestas, self.dicPosVertices, self.dicListaArestas, self.numDepositos)
        return matInc
        
                        
    def floydWarshall(self): #Função utilizada para calcular o caminho mínimo entre todos os vértices da matriz         
        matrizFloyd = []     #Utilizada tanto no começo do algoritmo, como a cada iteração do algoritmo para calcular
                             #os caminho mínimo entre um dado depósito e todas as cidades que ele atende e vice-versa
        for i in range(self.numVertices):
            matrizFloyd.append([0] * self.numVertices) # Cria matriz

        for i in range(0, self.numVertices): # copia para a nova matriz o conteúdo de matriz principal
            for j in range(0, self.numVertices):
                matrizFloyd[i][j] = self.__matriz[i][j]

        for i in range(0, len(matrizFloyd)):
            for j in range(0, len(matrizFloyd)):
                if matrizFloyd[i][j] == 0:
                    matrizFloyd[i][j] = sys.maxsize #Maior número do python utilizado como representação do "infinito"

        for k in range(0, len(matrizFloyd)):
            for i in range(0, len(matrizFloyd)):
                for j in range(0, len(matrizFloyd)):
                    if matrizFloyd[i][j] > matrizFloyd[i][k] + matrizFloyd[k][j] and i != j:
                        matrizFloyd[i][j] = matrizFloyd[i][k] + matrizFloyd[k][j]
                        
        return matrizFloyd 


    def encontraDepositoAtual(self, cidade): #Busca para uma determinada cidade, qual é o deposito que a atende atualmente
        depositoAtual = -1 #inicia o depósito atual como -1(inexistente)

        for deposito in range(0, len(self.__dicDepositosCidades)): #para cada depósito existente

            if cidade in self.__dicDepositosCidades[deposito]: #verifica se a cidade está sendo atendida por algum depósito e
                depositoAtual = deposito                       #define como depósito atual este depósito

        return depositoAtual 

        
    def encontraDepositoMaisProximo(self, cidade, matriz): #Procura o depósito mais próximo à uma dada cidade

        menorCaminho = matriz[0][0] #inicia como caminho mais próximo a primeira cidade(vértice) da matriz
        
        depositoAtual = self.encontraDepositoAtual(cidade)#encontra o depósito que atende a cidade atualmente[
        
        depositoAtual = self.__dicPosDepositos[depositoAtual]#verificar
        contadorDepositos = 0 #cria um contador de depósitos para não fazer verificações desnecessárias
        for coluna in range(0, len(matriz[cidade]) or contadorDepositos < self.numDepositos):#andar pela linha da cidade
            if matriz[cidade][coluna] < menorCaminho:#se o caminho da cidade para a outra cidade for menor que o menorCaminho

                if coluna in self.__listaDepositos: #verifica se este menor caminho é para um depósito
                    contadorDepositos += 1 #incrementa o número de depósitos verificados
                    depositoAtual = coluna #muda o depósito atual para esta cidade de menor caminho
                    menorCaminho = matriz[cidade][coluna]
                     
        return depositoAtual #mudar para nome melhor


    def atualizaCidadesDepositos(self, matriz): #Atualiza o depósitos de todas as cidades. O critério utilizado é
                                                #o seguinte, para cada cidade, busca pelo depósito mais próximo, se
                                                #este depósito for diferente do depósito que a atende atualmente, então
                                                #a cidade passa a ser atendida pelo novo depósito.

        for cidade in range(0, self.numVertices): #para cada cidade existente

            if cidade not in self.__listaDepositos:#se a cidade não for um depósito

                depositoProximo = self.encontraDepositoMaisProximo(cidade, matriz) #encontra o depósito mais proximo

                atualizouDeposito = self.atualizaDeposito(cidade, depositoProximo) #coloca a cidade no depósito mais proximo
            

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

            
        
    def criaNovaMatriz(self, deposito): #Cria  uma matriz reduzida que só contem o
                                        #depósito e as cidades atendidas por ele e executa o algoritmo de
                                        #FloydWarshall nesta matriz, retornando uma matriz reduzida de caminhos
                                        #mínimos
        if len(self.__dicDepositosCidades[deposito]) > 1: 
            listaCidades = [] #cria uma lista de cidades que não serão excluidas da matriz, ou seja, as cidades
                              #que são atendidas pelo depósito e o próprio depósito
            
            for cidade in range(0, len(self.__dicDepositosCidades[deposito])):#adiciona a lista todas as cidades que farão
                listaCidades.append(self.__dicDepositosCidades[deposito][cidade])#parte da matriz reduzida

            listaCidades.append(self.__dicPosDepositos[deposito])#adiciona também à lista o depósito que fará parte
                                                                 #da matriz reduzida

            matAux = deepcopy(self) #copia para outro obj matrizAdj a matrizAdj principal, para aproveitar a construção da

            for vertice in range(0, matAux.numVertices):
                if vertice not in listaCidades: #exclui todas as cidades não pertencentes às cidades atendidas pelo depósito
                    matAux.delVertice(vertice)
            if self.__dicDepositosCidades[deposito]:     #se o depósito não está vazio(se atende alguma cidade), copia
                self.dicAuxiliar = matAux.dicPosVertices #o dicionario atual para o auxiliar

            matAux.__matriz = matAux.floydWarshall() #aplica o floydWarshall na matrizReduzida  

            return matAux.__matriz #retorna a matriz de caminhos minimos entre um depósito e as cidades que ele atende
        else:
            return False
            
    def defineDeposito(self, matrizDistancias, chaveDeposito): #Define o novo depósito para a matriz de
                                                               #distancias daquele depositos e as cidades que ele atende.
                                                               #O critério utilizado é o seguinte: dentre o depósito e as
                                                               #cidades que ele atende, quem tiver o menor somatório de
                                                               #caminhos minimos para todos os outros vértices(cidades)
                                                               #será o novo depósito.
        
        if len(self.__dicDepositosCidades[chaveDeposito]) > 1: #se o depósito atender pelo menos duas cidades, então o cálculo é feito
            
            somatorioCaminhosMinimos = 0 #inicia o somatório dos caminhos mínimos de cada cidade como 0
            menorSomatorio = sum(matrizDistancias[0]) - sys.maxsize #assume como menor somatório, o da cidade que está na linha 0
                                                                    #o sys.maxsize é subtraido para não afetar no valor do menor
                                                                    #somatório

            novoDeposito = -1 #como ainda não se sabe o novoDepósito, este inicia-se como -1(desconhecido)
            depositoParaRemover = -1 #Como não se sabe se o depósito será alterado, começa-se com -1 também

            for linha in range(1, len(matrizDistancias)):#encontra possivel depósito pelo menor somatorio de caminhos
                somatorioCaminhosMinimos = sum(matrizDistancias[linha]) - sys.maxsize #soma toda a linha subtraindo 
                                                                                      #sys.maxSize(valor da diagonal principal)
                
                if somatorioCaminhosMinimos <= menorSomatorio:#se o somatório de caminhos daquela cidade pra todas as outras
                                                              #for menor que o atual menor conhecido     
                                                                   
                    menorSomatorio = somatorioCaminhosMinimos #o menorSomatório passa a ser este
                    novoDeposito = linha                      #guarda na variavel novoDeposito, a linha que
                                                              #obteve o menor somatorio de caminhos

            for vertice in self.dicAuxiliar: #como a linha pode não corresponder a cidade correta, usamos o dicionário
                                             #que foi atualizado durante a criação da matrizReduzida, onde houve uma
                                             #sequência de exclusões de vértices(cidades),
                                             #para auxiliar qual cidade a linha corresponde
                if self.dicAuxiliar[vertice] == novoDeposito:
                    novoDeposito = vertice
                    break
                    
            if novoDeposito not in self.__listaDepositos: #Se o novo depósito ainda não estiver na lista de nomes
                                                          #dos depósitos

                if novoDeposito != self.__dicPosDepositos[chaveDeposito]: #se o novo depósito for diferente do atual
                    chaveAntigoDeposito = -1                              #variável auxiliar p/ gravar a chave que
                                                                          #guarda a cidade que será o novoDepósito

                    for deposito in self.__dicDepositosCidades: #para cada depósito existete
                        if self.dicPosVertices[novoDeposito] in self.__dicDepositosCidades[deposito]:
                            chaveAntigoDeposito = deposito #guarda na var chaveAntigoDeposito a chave do antigoDeposito
                    
                    antigoDeposito = self.__dicPosDepositos[chaveAntigoDeposito]
                    self.__listaDepositos.append(novoDeposito)   #adiciona a lista de nome de depósitos depósitos o novo depósito
                    
                    self.__listaDepositos.remove(antigoDeposito) #removendo antigoDeposito da lista de depósitos atuais
                                                                                                                                
                    self.__dicPosDepositos[chaveAntigoDeposito] = novoDeposito #atualizando dicionário de posicões dos
                                                                               #depósitos e o dicionário de Depositos e
                                                                               #cidades que atendem
                    self.__dicDepositosCidades[chaveAntigoDeposito].append(antigoDeposito)
                    self.__dicDepositosCidades[chaveAntigoDeposito].remove(novoDeposito)

                    self.setaDicAux()


    def encontraChaveDeposito(self, depositoProcurado): #Dado um depósito, retorna qual é a chave do dicPosDepositos
                                                        #e do dicDepositosCidades correspondente a este depósito
        chaveDeposito = -1
        for deposito in self.__dicPosDepositos:
            if self.__dicPosDepositos[deposito] == depositoProcurado:
                chaveDeposito = deposito
                break
        return chaveDeposito

    def calculaSomatoriosDistancias(self): #Calcula os somatórios dos caminhos mínimos entre cada depósito e as cidades
                                           #que estes atendem, e, por fim, soma todos os somatórios.
        matrizDistancias = self.floydWarshall()
        listaSomatorios = []
        for deposito in self.__listaDepositos:
            chaveDeposito = self.encontraChaveDeposito(deposito)
            somatorioDeposito = 0
            for coluna in range(0, len(matrizDistancias[deposito])):
                if coluna in self.__dicDepositosCidades[chaveDeposito]:
                    somatorioDeposito += matrizDistancias[deposito][coluna]
            if somatorioDeposito != 0:
                listaSomatorios.append(somatorioDeposito)
        somatorioTotal = 0
        somatorioTotal = sum(listaSomatorios)
        
        return somatorioTotal 

    def kMeansAdapted(self): #Algoritmo baseado no "K-means" adaptado para execução em grafos.
                             #Os depósitos iniciais são os k(número de depósitos) primeiros vértices.
                             #De início, assume-se que todas as cidades são atendidas pelo primeiro depósito.
                             #Estas informações ficam armazenadas na própria estrutura de Dados

        matrizDis = self.floydWarshall() #Começa calculando os caminhos minimos entre todas as cidades
        self.atualizaCidadesDepositos(matrizDis) #Para cada cidade, encontra o depósito mais próximo
        continuaFazendo = True #variável que controla a execução do algoritmo
        while(continuaFazendo):
            dicAtual = deepcopy(self.__dicDepositosCidades) #Mantém a cada iteração, o dicDepositosCidades da iteração
                                                            #anterior para controlar quantas vezes o laço será executado
            for deposito in range(0, self.numDepositos): #Para cada depósito existente
                matrizDistancias = self.criaNovaMatriz(deposito) #Cria matriz reduzida entre o depósito e as cidades
                                                                 #que ele atende e executa FloydWarshall nesta matriz

                if matrizDistancias is not False: #Se não foi criada a matrizReduzida, não tenta-se encontrar o novo depósito
                    self.defineDeposito(matrizDistancias, deposito) #Encontra dentre o depósito atual e as cidades que ele atende,
                                                                    #Quem é o vértice(cidade) mais viável para ser depósito, com
                                                                    #base no menor caminho minimo de cada vértice para todos
                                                                    #os outros

            self.atualizaCidadesDepositos(matrizDis) #Para cada cidade, aloca-a para o depósito mais próximo
            if self.__dicDepositosCidades == dicAtual: #Se nenhuma cidade passou a ser atendida por outro depósito
                                                       #em relação a iteração anterior, então o algoritmo para sua execução
                continuaFazendo = False
        
    

            
        
            
        
            
        
                    
                
