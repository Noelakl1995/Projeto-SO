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
# print("insira sequencia de blocos")
# blocos = list(map(int, input().split(" ")))
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
#consideramos um disco cheio onde os blocos foram escritos sequencialmente em trilha, nesse caso: (0,1,2,3...719)
#
#
#
#
#
#
#

tempo_seek_adjascente = 6 #ms
tempo_seek_avg = 77 #ms
tempo_rotacao = 200 #ms
tempo_transferencia = 22 #ms
print ("Setores por disco: " + str (setores_por_disco))
print ("Capacidade do disco: " + str (capacidade_disco))

#latencia total = tempo de busca + tempo de rotação

def latenciaAcessoUnicoBloco(blocoInicial, blocoDesejado):
    trails = trailDifference(blocoInicial,blocoDesejado)
    if(trails == 0):
        return tempo_rotacao
    elif (trails == 1):
        return tempo_rotacao + tempo_seek_adjascente
    return tempo_rotacao + tempo_seek_avg


def findBlockTrail(bloco):
    return bloco//9

def trailDifference(blocoAtual, blocoDesejado):
    return abs(findBlockTrail(blocoAtual) - findBlockTrail(blocoDesejado))

print ("O tempo de latencia foi: " + str (latenciaAcessoUnicoBloco(0,20))+ " ms")

# To-Do:
# Quando ocorre um seek para um novo cilindro,
# há a possibilidade estarmos no bloco correto, eh necessario verificar esse caso
# alem disso, tem que ser testado o caso que nao eh necessario uma rotacao completa na maior parte das vezes.
# portanto, o tempo nao vai ser 200ms(que eh o tempo total para dar a volta de rotacao), mas sim
# 200/n, onde n eh a quantidade de setores que precisam ser percorridos para o setor/bloco certo 