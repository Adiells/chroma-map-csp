def maior_grau(grafo, sem_atribuicao):
    return max(sem_atribuicao, key=lambda no: len(grafo[no]))

def cores_restantes(grafo, no, cores, atribuicao):
    cores_restantes = set(cores)
    for vizinho in grafo[no]:
        if vizinho in atribuicao:
            cores_restantes.discard(atribuicao[vizinho])
    return cores_restantes 

def mais_restringido(grafo, sem_atribuicao, cores, atribuicao=None):
    """
    retorna o uma lista com os nós com maior quantidade de restricoes
    """
    if atribuicao is None:
        atribuicao = {}
    
    # A restrição é o oposto do número de cores restantes (quanto menos cores, mais restringido o nó está)
    tamanhos = {no: len(cores_restantes(grafo, no, cores, atribuicao)) for no in sem_atribuicao}
    min_cores = min(tamanhos.values())
    return [no for no in sem_atribuicao if tamanhos[no] == min_cores]

def heuristicas_agrupadas(grafo, sem_atribuicao, cores, atribuicao=None):
    """
    retorna naturalmente o nó com mais restricoes, utilizando o maior grau como criteiro em caso de empatar
    """
    empatados = mais_restringido(grafo, sem_atribuicao, cores, atribuicao)
    return maior_grau(grafo, empatados)