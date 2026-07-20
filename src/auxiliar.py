from pathlib import Path

import geobr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
FREQUENCIAS = {
    "Vermelho": "Frequência 1 (ex: 700MHz)",
    "Verde": "Frequência 2 (ex: 850MHz)",
    "Azul": "Frequência 3 (ex: 900MHz)",
    "Amarelo": "Frequência 4 (ex: 1800MHz)"
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
    estados.plot(ax=ax, color=estados["cor_hex"], edgecolor="white", linewidth=0.8) #type:ignore
    ax.set_title("Coloração de Mapa via CSP - Regiões Reais")
    ax.set_axis_off()
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")

    # plota frequencias
    legendas = [
        mpatches.Patch(color=MAPA_CORES[cor_nome], label=freq_nome)
        for cor_nome, freq_nome in FREQUENCIAS.items()
    ]
    # Posiciona a legenda no mapa
    ax.legend(handles=legendas, title="Frequências Alocadas", loc="lower left", frameon=True)
    # ---------------------------------------------------------

    
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")

def gerar_grafo_colorido(caminho_grafo, resultado, caminho_saida):
    
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Carrega o grafo original com todas as propriedades (arestas e posições)
    grafo = nx.read_gexf(caminho_grafo)
    
    # 2. Mapeia as posições X e Y de cada nó para que o grafo tenha o formato do mapa
    posicoes = {}
    for no, dados in grafo.nodes(data=True):
        x = float(dados['x'])
        y = float(dados['y'])
        
        # Mantendo o seu ajuste fino para o Distrito Federal não sobrepor Goiás
        if no == "Distrito Federal":
            y += 0.8
            
        posicoes[no] = (x, y)
        
    # 3. Cria uma lista sequencial de cores na mesma ordem que o NetworkX lista os nós
    cores_dos_nos = [MAPA_CORES[resultado[no]] for no in grafo.nodes()]
    
    # 4. Configura a plotagem
    fig, ax = plt.subplots(figsize=(10, 10))
    
    nx.draw(
        grafo, 
        pos=posicoes, 
        ax=ax, 
        node_color=cores_dos_nos, 
        with_labels=True, 
        node_size=900,        # Tamanho das bolinhas
        font_size=8, 
        font_weight='bold', 
        font_color='black',
        edge_color='gray',    # Cor das linhas de conexão
        linewidths=1.5,
        edgecolors='black'    # Bordinha preta em volta dos nós
    )
    
    # Adiciona a legenda de frequências
    legendas = [
        mpatches.Patch(color=MAPA_CORES[cor_nome], label=freq_nome)
        for cor_nome, freq_nome in FREQUENCIAS.items()
    ]
    ax.legend(handles=legendas, title="Frequências (Grafo)", loc="lower left", frameon=True)
    
    ax.set_title("Topologia da Rede de Restrições - Brasil")
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    print(f"Grafo de conexões salvo em: {caminho_saida}")
    plt.close(fig)