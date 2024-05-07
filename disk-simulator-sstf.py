import random
import matplotlib.pyplot as plt
import numpy as np
# Problema:
#   Escreva um simulador de disco que permita indicar qual a latência de acesso
#   para uma lista de blocos indicados como dados de entrada.
#   Aqui o simulador deve receber uma configuração que inclua:

# - tamanho do setor
# - quantidade de trilhas no disco
# - quantidade de setores por trilha
# - tempo de seek, rotação e transferência de dados

# Configuração do disco.
# Valores são tomados do Disco Flexivel IBM 360KB
# Disponivel no livro Modern Operating Systems (4a edição) pag. 256
num_cilindros = 40
trilhas_por_cilindro = 2
# A quantidade de trilhas por disco pode ser calculada
quantidade_trilhas_disco = num_cilindros*trilhas_por_cilindro
# Nesse caso, há 80 trilhas
setores_por_trilha = 9
# A quantidade de setores por disco pode ser calculada
setores_por_disco = quantidade_trilhas_disco * setores_por_trilha
# Nesse caso, há 720 setores
bytes_por_setor = 512
# A capacidade do disco pode ser calculada 
capacidade_disco = (setores_por_disco * bytes_por_setor) /1024 #Divisão para obter o valor em KB
# Nesse caso, 360KB

#Tomamos que o tamanho do bloco eh igual o tamanho do setor
tamanho_bloco = bytes_por_setor
blocos_por_trilha = setores_por_trilha
#consideramos um disco cheio onde os blocos foram escritos sequencialmente na trilha, nesse caso: (0,1,2,3...719)
tempo_seek_adjascente = 6 #ms
tempo_seek_avg = 77 #ms
tempo_rotacao = 200 #ms
tempo_transferencia = 22 #ms

bloco_inicial_disco = 0

#latencia total = tempo de busca + tempo de rotação + tempo transferencia

def latenciaAcessoBloco(blocoInicial, blocoDesejado,printResults):

    diferencaDeTrails = trailDifference(blocoInicial, blocoDesejado)
    tempoRotacaoDasTrails = tempoRotacaoSameTrail(blocoInicial, blocoDesejado)
    tempoIndividualBloco = int

    if (diferencaDeTrails == 0):
        tempoIndividualBloco = tempoRotacaoDasTrails
    elif (diferencaDeTrails == 1):
        tempoIndividualBloco = tempoRotacaoDasTrails + tempo_seek_adjascente
    else:
        tempoIndividualBloco = tempoRotacaoDasTrails + tempo_seek_avg
    tempoIndividualBloco += tempo_transferencia
    if printResults:
        print(f"O tempo de acesso do bloco {blocoDesejado} saindo do bloco {blocoInicial}"
            f" foi de {tempoIndividualBloco:.2f} ms")
    return tempoIndividualBloco

def tempoRotacaoSameTrail(bloco1,bloco2):
    # Calcula o número do setor em que cada bloco está, são 9 setores por trail
    setor_bloco1 = bloco1 % setores_por_trilha
    setor_bloco2 = bloco2 % setores_por_trilha
    # Como a agulha só se move em uma direção, calcula a diferença entre os setores para 2 casos:
    # 1) Bloco desejado já passou da agulha, vai ser preciso dar outra volta
    # 2) bloco desejado está no sentido da agulha, podemos calcular normalmente
    if (setor_bloco2 < setor_bloco1):
        diferenca_setores = (setores_por_trilha - setor_bloco1)+setor_bloco2
    else:
        diferenca_setores = setor_bloco2 - setor_bloco1

    tempo_medio_rotacao = tempo_rotacao / setores_por_trilha
    
    return diferenca_setores * tempo_medio_rotacao

def findBlockTrail(bloco):
    return bloco//setores_por_trilha

def trailDifference(blocoAtual, blocoDesejado):
    return abs(findBlockTrail(blocoAtual) - findBlockTrail(blocoDesejado))

def sortBySSTF(blocos, blocoInicial):
    aux = list(blocos)  # Faz uma cópia da lista original
    lista_ordenada = []
    while aux:
        min_latency = float('inf')
        toBeRemoved = None
        for i in range(len(aux)):
            latency = latenciaAcessoBloco(blocoInicial, aux[i], False)
            if latency < min_latency:
                min_latency = latency
                toBeRemoved = i
        lista_ordenada.append(aux.pop(toBeRemoved))
        blocoInicial = lista_ordenada[-1]
    return lista_ordenada

def latenciaAcessoTotal(lista_blocos):
    latencia_total = 0 
    #Consideramos que o disco começa no bloco 0 na sua inicianiliazição
    bloco_inicial = bloco_inicial_disco
    lista_blocos = sortBySSTF(lista_blocos,bloco_inicial)
    for bloco in lista_blocos:
        latencia_total += latenciaAcessoBloco(bloco_inicial,bloco,True)
        bloco_inicial = bloco
    return latencia_total

def gerarListaLatencias(lista_blocos):
    lista_latencias = []
    bloco_inicial = bloco_inicial_disco
    lista_blocos = sortBySSTF(lista_blocos,bloco_inicial)
    for bloco in lista_blocos:
        lista_latencias.append(latenciaAcessoBloco(bloco_inicial,bloco,False))
        bloco_inicial = bloco
    return lista_latencias

def gerarBlocos(numero_blocos):
    randomlist = random.choices(range(setores_por_disco), k = numero_blocos)
    return randomlist


blocos = gerarBlocos(int(input("Digite a quantidade de blocos que voce quer gerar: ")))
list_size = len(blocos)

if any(bloco >= setores_por_disco for bloco in blocos):
    print(f"Você tentou acessar um bloco que não existe no disco."
        f"\nMaior bloco possível: {setores_por_disco-1} ")
    exit()

if(list_size == 0):
    print("lista vazia")
    exit()


tempo = latenciaAcessoTotal(blocos)
print(f"\nO tempo total de latência foi: {tempo:.2f} ms")

lista_Lat = gerarListaLatencias(blocos)
maxLatencyValue = max(lista_Lat)

#Criacao grafico
plt.scatter(blocos, lista_Lat)
plt.ylim(0, maxLatencyValue)
plt.xlim(0, setores_por_disco)
plt.text(0, maxLatencyValue * 0.9, f'Blocos acessados: {list_size}', color='blue', fontsize=10)
media_tempo = tempo / list_size
plt.axhline(y=media_tempo, color='r', linestyle='-')
plt.text(setores_por_disco - 1, media_tempo, f'Média: {media_tempo:.2f}', color='r', fontsize=10)

plt.show()