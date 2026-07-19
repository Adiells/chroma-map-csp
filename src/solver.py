from itertools import count #VAI SER ALTERADO
import networkx as nx
import src.heuristicas as heuristicas

# contador de IDs dos nós da árvore //VAI SER ALTERADO//
contador = count()


def consistente(no, cor, atribuicao, grafo):
    for vizinho in grafo[no]:
        if vizinho in atribuicao and atribuicao[vizinho] == cor:
            return False

    return True


def backtrack(atribuicao, grafo, cores, arvore, id_pai):
    # solução encontrada
    if len(atribuicao) == len(grafo):
        return atribuicao

    sem_atribuicao = [no for no in grafo if no not in atribuicao]

    no = heuristicas.heuristicas_agrupadas(grafo, sem_atribuicao, cores, atribuicao)

    for cor in cores:

        id_filho = next(contador)

        valido = consistente(no, cor, atribuicao, grafo)

        arvore.add_node(id_filho, label=f"{no}\n{cor}", valido=valido)

        arvore.add_edge(id_pai, id_filho)

        if not valido:
            continue

        nova_atribuicao = atribuicao.copy()
        nova_atribuicao[no] = cor

        resultado = backtrack(nova_atribuicao, grafo, cores, arvore, id_filho)

        if resultado is not None:
            return resultado


def backtracking_search(grafo, cores):

    arvore = nx.DiGraph()

    raiz = next(contador)

    arvore.add_node(
        raiz,
        label="Raiz"
    )

    resultado = backtrack({}, grafo, cores, arvore, raiz)

    return resultado, arvore


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