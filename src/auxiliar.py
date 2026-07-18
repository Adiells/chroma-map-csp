from pathlib import Path

import geobr
import matplotlib.pyplot as plt
import networkx as nx
import geopandas as gpd

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


def gerar_mapa_mundo_colorido(resultado, caminho_saida):
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    
    # URL for the Natural Earth low-resolution world map
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    
    print("Carregando o mapa mundi...")
    mundo = gpd.read_file(url)
    
    # Mapear as cores utilizando a coluna 'ADMIN' que bate com os nós do grafo
    mundo["cor_csp"] = mundo["ADMIN"].map(resultado)
    
    # Cor padrão para países que não receberam cor (caso haja)
    mundo["cor_hex"] = mundo["cor_csp"].map(MAPA_CORES).fillna("#e0e0e0")
    
    fig, ax = plt.subplots(figsize=(15, 10))
    mundo.plot(ax=ax, color=mundo["cor_hex"], edgecolor="white", linewidth=0.5)
    ax.set_title("Coloração do Mapa Mundi via CSP")
    ax.set_axis_off()
    
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    print(f"Mapa mundi colorido salvo em: {caminho_saida}")
    plt.close(fig)

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