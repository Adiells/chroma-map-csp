from pathlib import Path

import geobr
import matplotlib.pyplot as plt
import networkx as nx

try:
    from .solver import backtracking_search, verificar_solucao
except ImportError:
    from solver import backtracking_search, verificar_solucao


CORES = ["Vermelho", "Verde", "Azul", "Amarelo"]
MAPA_CORES = {
    "Vermelho": "#e74c3c",
    "Verde": "#2ecc71",
    "Azul": "#3498db",
    "Amarelo": "#f1c40f",
}


def carregar_adjacencia(caminho_grafo):
    grafo = nx.read_gexf(caminho_grafo)
    return {no: set(grafo.neighbors(no)) for no in grafo.nodes()}


def colorir_mapa(adjacencia):
    resultado = backtracking_search(adjacencia, CORES)

    if not verificar_solucao(resultado, adjacencia):
        raise ValueError("Não foi possível encontrar uma coloração válida.")

    return resultado


def gerar_mapa_colorido(resultado, caminho_saida):
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    estados = geobr.read_state(year=2020)
    estados["cor_csp"] = estados["name_state"].map(resultado)

    if estados["cor_csp"].isna().any():
        estados_sem_cor = estados.loc[estados["cor_csp"].isna(), "name_state"].tolist()
        raise ValueError(f"Estados sem cor correspondente: {estados_sem_cor}")

    estados["cor_hex"] = estados["cor_csp"].map(MAPA_CORES)

    fig, ax = plt.subplots(figsize=(10, 10))
    estados.plot(ax=ax, color=estados["cor_hex"], edgecolor="white", linewidth=0.8)
    ax.set_title("Coloração de Mapa via CSP - Regiões Reais")
    ax.set_axis_off()
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(fig)
