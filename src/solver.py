import src.heuristicas as heuristicas

def consistente(no, cor, atribuicao, grafo):
    for vizinho in grafo[no]:
        if vizinho in atribuicao and atribuicao[vizinho] == cor:
            return False

    return True


def backtrack(atribuicao, grafo, cores):
    if len(atribuicao) == len(grafo):
        return atribuicao

    sem_atribuicao = [no for no in grafo if no not in atribuicao]
    no = heuristicas.heuristicas_agrupadas(grafo, sem_atribuicao, cores, atribuicao)

    for cor in cores:
        if consistente(no, cor, atribuicao, grafo):
            atribuicao[no] = cor
            resultado = backtrack(atribuicao, grafo, cores)

            if resultado:
                return resultado

            del atribuicao[no]

    return None

def backtracking_search(grafo, cores):
    return backtrack({}, grafo, cores)


def verificar_solucao(atribuicao, grafo):
    if atribuicao is None:
        return False

    for no, vizinhos in grafo.items():
        if no not in atribuicao:
            return False

        for vizinho in vizinhos:
            if vizinho not in atribuicao:
                return False

            if atribuicao[no] == atribuicao[vizinho]:
                return False

    return True
