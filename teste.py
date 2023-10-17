import random
import time
from termcolor import colored

#print(colored('Error Test!!!', 'red'))
#print(colored('Warning Test!!!', 'yellow'))
#print(colored('Success Test!!!', 'green'))

GENES = "aáâàbcdeéêfghiíjklmnoóôõpqrstuúvwxyzAÁÂÀBCDEÉÈFGHIÍJKLMNOÓÔÕPQRSTUÚVWXYZ _-@!#$%¨&*()0123456789"

# Define a população inicial
def gerar_populacao(tamanho_populacao, tamanho_individuo):
    populacao = []
    for i in range(tamanho_populacao):
        individuo = ''.join(random.choice(GENES) for j in range(tamanho_individuo))
        populacao.append(individuo)
    return populacao

# Avalia a aptidão de cada indivíduo
def avaliar_populacao(populacao, objetivo):
    aptidoes = []
    for individuo in populacao:
        aptidao = 0
        for i in range(len(objetivo)):
            if individuo[i] == objetivo[i]:
                aptidao += 1
        aptidoes.append(aptidao)
    return aptidoes

# Seleciona os indivíduos mais aptos
def selecionar_populacao(populacao, aptidoes, tamanho_torneio):
    nova_populacao = []
    for i in range(len(populacao)):
        torneio = random.sample(range(len(populacao)), tamanho_torneio)
        vencedor = torneio[0]
        for j in torneio:
            if aptidoes[j] > aptidoes[vencedor]:
                vencedor = j
        nova_populacao.append(populacao[vencedor])
    return nova_populacao

# Realiza o cruzamento entre os indivíduos
def cruzar_populacao(populacao, taxa_cruzamento):
    nova_populacao = []
    for i in range(0, len(populacao), 2):
        pai = populacao[i]
        mae = populacao[i+1]
        
        if random.random() < taxa_cruzamento:
            ponto_corte = random.randint(1, len(pai)-1)
            filho1 = pai[:ponto_corte] + mae[ponto_corte:]
            filho2 = mae[:ponto_corte] + pai[ponto_corte:]
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)
            #print(f"Cruzamento [{pai} , {mae}] -> [{filho1}, {filho2}]")
        else:
            nova_populacao.append(pai)
            nova_populacao.append(mae)
    return nova_populacao  # Adicione esta linha para retornar a nova população corretamente.


def mutar_populacao(populacao, taxa_mutacao, objetivo):
    nova_populacao = []
    for individuo in populacao:
        novo_individuo = ''
        for i, gene in enumerate(individuo):
            if gene != objetivo[i] and (random.random() < taxa_mutacao):
                novo_individuo += random.choice(GENES)
                #print(f"Mutação {individuo} -> {novo_individuo}", end="")
            else:
                novo_individuo += gene
        nova_populacao.append(novo_individuo)
    return nova_populacao




# Executa o algoritmo genético
def algoritmo_genetico(objetivo, tamanho_populacao, tamanho_individuo, taxa_cruzamento, taxa_mutacao, tamanho_torneio, numero_geracoes):
    populacao = gerar_populacao(tamanho_populacao, tamanho_individuo)
    for geracao in range(numero_geracoes):
        aptidoes = avaliar_populacao(populacao, objetivo)
        melhores_individuos = [populacao[i] for i in range(len(populacao)) if aptidoes[i] == max(aptidoes)]
        #print("Geração", geracao+1, "- Melhores indivíduos:", melhores_individuos)
        
        melhor_individuo = populacao[aptidoes.index(max(aptidoes))]  # Encontre o melhor indivíduo
        
        # Verificar se algum indivíduo atingiu o objetivo
        if objetivo in melhores_individuos:
            #print(f"Geração", str(geracao+1).zfill(3), " - Solução encontrada:", objetivo)
            print(colored(f"Geração {str(geracao+1).zfill(3)} - Solução encontrada:  {objetivo}", 'green'))
            return

        print("Geração", str(geracao+1).zfill(3), "- Melhor indivíduo:", melhor_individuo)
        
        time.sleep(0.1)  # Adicione um atraso segundos
        
        populacao = selecionar_populacao(populacao, aptidoes, tamanho_torneio)
        populacao = cruzar_populacao(populacao, taxa_cruzamento)
        populacao = mutar_populacao(populacao, taxa_mutacao, objetivo)

    aptidoes = avaliar_populacao(populacao, objetivo)
    melhores_individuos = [populacao[i] for i in range(len(populacao)) if aptidoes[i] == max(aptidoes)]
    print("Geração final - Melhores indivíduos:", melhores_individuos, "\n")

while True:
    
    # Solicita a palavra ou frase do usuário
    objetivo = input(colored("Digite a palavra ou frase a ser adivinhada: ", 'yellow'))

    # Executa o algoritmo genético com os parâmetros desejados
    algoritmo_genetico(objetivo, tamanho_populacao=100, tamanho_individuo=len(objetivo), taxa_cruzamento =0.8, taxa_mutacao=0.1, tamanho_torneio=5, numero_geracoes=1000)
    
    
    if (input("Reiniciar?(r) ou sair(s): ")) == 's':
        break
