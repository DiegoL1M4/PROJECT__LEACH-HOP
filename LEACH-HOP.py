
import random
import math
import numpy as np

############################### Geração de Redes ################################
def gerarCenario(qtdNodes):
    nodes = []
    for i in range(1, qtdNodes+1):
        x = round(np.random.uniform(0, 100), 2)
        y = round(np.random.uniform(0, 100), 2)
        nodes.append([i, 0.5, x, y, 142.0, 0, 0, [], [], 0])
    return nodes

############################### Functions ################################
def selecao_CH(nodes, Round):
  CH = []
  for k in nodes:
    rand = random.random()
    limiar = 0.05 / (1.0 - 0.05 * (Round % (1.0 / 0.05)))
    if(limiar > rand) and (k[6] != 1):
      k[6] = 1
      CH.append(k)
      nodes.remove(k)
  return CH

def distancia(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def gastoTx(bateria, distancia, tamPacote):
   return bateria-(0.00000005*tamPacote + 0.0000000001*tamPacote*(distancia*distancia))

def gastoRx(bateria, tamPacote):
   return bateria - 0.00000005 * tamPacote

def maiorLista(lista):
    maior = lista[0]
    for k in lista:
        if(maior < k):
            maior = k
    return maior

def menorLista(lista):
    menor = lista[0]
    for k in lista:
        if(k < menor):
            menor = k
    return menor

def contEncaminhamento(id,listaID):
    cont = 0
    for k in listaID:
        if(k == id):
            cont += 1
    return cont

def localizaObjetoCH(id, CH):
    for k in CH:
        if (k[0] == id):
            return k

def verifica_eleitos(nodes):
  total = 0
  for k in nodes:
    total = total + k[6]
  if(total == len(nodes)):
    return True
  return False

def ajuste_alcance_nodeCH(CH):
  for nodeCH in CH:
    maior = 0
    # Verifica os elementos do cluster
    for node in nodeCH[8]:
      if(maior < node[3]):
        maior = node[3]
    # Escolhe a maior distância e configura o rádio
    nodeCH[4] = maior

def setorizacao(lista,divisor):
    if(lista != []):
        # Vetor das Distâncias
        ordenado = []
        for k in lista:
            ordenado.append(k[3])
        # Calculo entre o menor e o maior
        ordenado.sort()
        valor = (ordenado[-1] - ordenado[0]) / divisor
        # Setorização
        for k in lista:
            if(k[3] <= ordenado[0] + 1*valor):
                k[4] = 1
            elif(k[3] <= ordenado[0] + 2*valor):
                k[4] = 2
            elif(k[3] <= ordenado[0] + 3*valor):
                k[4] = 3
            elif(k[3] <= ordenado[0] + 4*valor):
                k[4] = 4
            elif(k[3] <= ordenado[0] + 5*valor):
                k[4] = 5
            elif(k[3] <= ordenado[0] + 6*valor):
                k[4] = 6
            elif(k[3] <= ordenado[0] + 7*valor):
                k[4] = 7
            elif(k[3] <= ordenado[0] + 8*valor):
                k[4] = 8

    return lista

def setorizacaoCH(ordenado,distancia,divisor):
    # Calculo entre o menor e o maior
    menor = menorLista(ordenado)
    maior = maiorLista(ordenado)

    valor = (maior - menor) / divisor

    if(distancia <= menor + 1*valor):
        return 1
    elif(distancia <= menor + 2*valor):
        return 2
    elif(distancia <= menor + 3*valor):
        return 3
    elif(distancia <= menor + 4*valor):
        return 4
    elif(distancia <= menor + 5*valor):
        return 5
    elif(distancia <= menor + 6*valor):
        return 6
    elif(distancia <= menor + 7*valor):
        return 7
    elif(distancia <= menor + 8*valor):
        return 8

############################### Variables ################################
CH = []
tamPacoteConfig = 300

intraCluster = 0
interCluster = 0
modosHop = [[0,0],[0,1],[1,0],[1,1]]

qtdNodes = [100, 150, 200, 250]
qtdFrames = [1,2,4,6,8,10]
tamPacoteTransmissao = [2000, 4000, 6000, 8000]
percentualCH = [0.05, 0.10, 0.15, 0.20]
qtdSetores = [2.0,4.0,6.0,8.0]

print("CENÁRIO: " + str(qtdNodes[0]) + ' nodes, '
                  + str(qtdFrames[0]) + ' frames, '
                  + str(tamPacoteTransmissao[0]) + ' bits, '
                  + str(int(percentualCH[0]*100)) + '%, '
                  + str(int(qtdSetores[0])) + ' setores')

total_simulacoes = 33
framesSimulacao = []

BS = [0,125.0,50.0,0.0,0]

############################### Main ################################
for modoOp in modosHop:
    intraCluster = modoOp[0]
    interCluster = modoOp[1]

    framesSimulacao = []

    for simu in range(total_simulacoes):
        Round = 1
        totalFrames = 0
        nodes = gerarCenario(qtdNodes[0])

        if(interCluster == 1):
        	# CONFIGURAÇÕES INICIAIS (Setorização intercluster)
        	# Trasmite as localizações à BS
            distanciasBS = []
            for k in nodes:
                dist = distancia(k[2],k[3],BS[1],BS[2])
                distanciasBS.append( dist )
                k[1] = gastoTx(k[1],dist,tamPacoteConfig)
        	# Recebe os setores da BS
            for k in nodes:
                k[9] = setorizacaoCH(distanciasBS,distanciasBS[k[0]-1],qtdSetores[0])
                k[1] = gastoRx(k[1],tamPacoteConfig)

        # EXECUÇÃO DA SIMULAÇÃO
        while(len(nodes) != 0):
            #Verifica Reset do Round Superior
            if(verifica_eleitos(nodes)):
                for k in nodes:
                    k[6] = 0

            # Realiza seleção de CH
            CH = selecao_CH(nodes, Round)

            # Execução após seleção
            if(len(CH) != 0):

        		# TRANSMISSÃO  CH: Envio do Broadcast
                pacotesBroadcast = []
                for k in CH:
                    pacotesBroadcast.append( [k[0],k[2],k[3],0.0,k[9]] )
                    # Registro da BS para envio
                    k[7].append(BS)
                    k[1] = gastoTx(k[1],k[4],tamPacoteConfig)

                # INTERCLUSTER: Chs recebem o broadcast dos outros CHs
                if(interCluster == 1):
                    for k in CH:
                        for node in pacotesBroadcast:
                            if(node[0] != k[0]):
                                k[7].append(node)

                if(nodes != []):
            		# RECEPÇÃO    NCH: Recepção dos Pacotes de Bradcast
                    for k in nodes:
                        menorDistancia = k[4]
                        nodeMenorDistancia = []
                        # Escolha do CH (o mais próximo)
                        for nodesCH in pacotesBroadcast:
                            dist = distancia(k[2],k[3],nodesCH[1],nodesCH[2])
                            if(dist < menorDistancia):
                                menorDistancia = dist
                                nodeMenorDistancia = nodesCH
                        # Atualização dos valores
                        k[7] = [ nodeMenorDistancia ]
                        k[4] = menorDistancia
                        k[1] = gastoRx(k[1],tamPacoteConfig)

                    # TRANSMISSÃO NCH: Envio de Pacotes Resposta
                    for k in nodes:
                        node = [k[0],k[2],k[3],k[4],0]
                        # localiza o CH escolhido na lista de CH e coloca seu node em ListCL do CH
                        for nodeCH in CH:
                            if(k[7][0][0] == nodeCH[0]):
                                nodeCH[8].append(node)
                        k[1] = gastoTx(k[1],k[4],tamPacoteConfig)

                    # RECEPÇÃO     CH: Recepção de Pacotes de Resposta
                    for k in CH:
                        # Nodes atribuídos na função anterior
                        for l in range( len(k[8]) ):
                            k[1] = gastoRx(k[1],tamPacoteConfig)

                    # TRANSMISSÃO  CH: Envio da Tabela TDMA
                    ajuste_alcance_nodeCH(CH)
                    clusters = []
                    for k in CH:
                        clusters.append( [k[0], setorizacao(k[8],qtdSetores[0])] )
                        k[1] = gastoTx(k[1],k[4],tamPacoteConfig)

                    # RECEPÇÃO    NCH: Recepção da Tabela TDMA
                    for k in nodes:
                        idCH = k[7][0][0]
                        # Localiza o cluster do CH
                        for clstr in clusters:
                            if(clstr[0] == idCH):
                                k[8] = clstr[1]
                        k[1] = gastoRx(k[1],tamPacoteConfig)

                    # CONFIGURAÇÃO DE RADIO DOS CH PARA ALCANÇAR A BS
                    for k in CH:
                        k[4] = distancia(k[2],k[3], BS[1],BS[2])

                    # MULTI-HOP INTRACLUSTER
                    if(intraCluster == 1):
                        for k in nodes:
                            # Acho o setor dentro do clusters
                            for node in k[8]:
                                if(k[0] == node[0]):
                                    setor = node[4]
                            # Achar node vizinho mais proximo
                            id = k[7][0][0]
                            menor = k[4]
                            for node in k[8]:
                                dist = distancia(k[2],k[3], node[1],node[2])
                                if(dist < menor and node[4] < setor):
                                    id = node[0]
                                    menor = dist
                            k[7] = [[id,0,0,menor,0]]
                            k[4] = menor

                    # MULTI-HOP INTERCLUSTER
                    if(interCluster == 1):
                        for k in CH:
                            menor = k[4]
                            for node in k[7]:
                                dist = distancia(k[2],k[3], node[1],node[2])
                                if(dist < menor and node[4] < k[9]):
                                    menor = dist
                                    k[4] = menor
                                    k[7] = [node]

                    # MAPEAMENTO DE ENCAMINHAMENTO NCH (Ids de destino dos nodes)
                    mapaEncaminhamento = []
                    for k in nodes:
                        mapaEncaminhamento.append( k[7][0][0] )

            		# FRAMES
                    for l in range(qtdFrames[0]):
                        # NCH: Transmite Pacote
                        for k in nodes:
                            # Gasto de agregação de dados
                            k[1] = k[1] - (0.000000005*tamPacoteTransmissao[0]*(contEncaminhamento(k[0], mapaEncaminhamento) + 1))
                            k[1] = gastoTx(k[1],k[4],tamPacoteTransmissao[0])
                        # CH: Recebe Pacote
                        for k in CH:
                            for l in range( contEncaminhamento(k[0], mapaEncaminhamento) ):
                                k[1] = gastoRx(k[1],tamPacoteTransmissao[0])
                        for k in nodes:
                            for l in range( contEncaminhamento(k[0], mapaEncaminhamento) ):
                                k[1] = gastoRx(k[1],tamPacoteTransmissao[0])
                        # CH: Envia Pacote para a BS
                        for k in CH:
                            # Gasto de agregação de dados
                            k[1] = k[1] - (0.000000005*tamPacoteTransmissao[0]*contEncaminhamento(k[0], mapaEncaminhamento))
                            node = k
                            idDestino = node[7][0][0]
                            while(idDestino != 0):
                                node[1] = gastoTx(node[1],node[4],tamPacoteTransmissao[0])
                                node = localizaObjetoCH(idDestino,CH)
                                # Gasto Recepção do node destino
                                node[1] = gastoRx(node[1],tamPacoteTransmissao[0])
                                idDestino = node[7][0][0]
                            node[1] = gastoTx(node[1],node[4],tamPacoteTransmissao[0])

                '''print(Round)
                print(str(len(CH)) + " " + str(len(nodes)))
                print(CH)
                print(nodes)

                for l in CH:
                    print(str(l[0]) + ' s: ' + str(l[9]) + ' nodeDe ' + str(l[7]))
                print(str(node[0]) + ' ' + str(idDestino) + ' distancia' + str(node[4]))
                input()'''
        		# FECHAMENTO DO ROUND
                # Encerramento do Round
                for k in CH:
                    nodes.append(k)
                for k in nodes:
                    k[4] = 142.0
                    k[7] = []
                    k[8] = []

                #Exclui zerados
                for k in nodes:
                    if(k[1] <= 0):
                        nodes.remove(k)

                CH = []
                Round = Round + 1
                if(nodes != []):
                    totalFrames += qtdFrames[0]

                # FIM DE UM ROUND ##########

        #print('Simulacao ' + str(simu+1) + ": " + str(totalFrames))
        framesSimulacao.append(totalFrames)

        # FIM DE UMA SIMULAÇÃO ##########

    ############################### Estatísticas ################################
    def desvio_padrao(valores, media):
        soma = 0
        for valor in valores:
            soma += math.pow( (valor - media), 2)
        return math.sqrt( soma / float( len(valores) ) )

    media = sum(framesSimulacao) / total_simulacoes

    print('\nResultado do ' + str(modoOp[0]) + str(modoOp[1]) +"-LEACH-HOP:")
    print('Média: ' + str(media))
    print('Erro: ' + str(1.96*(desvio_padrao(framesSimulacao, media) / math.sqrt(total_simulacoes) )))

    # FIM DE TODOS OS EXPERIMENTOS DE UM MODO DE OPERAÇÃO ##########

# FIM DE TODAS AS VARIAÇÕES DO LEACH-HOP ##########