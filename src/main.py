from pathlib import Path
import sys

try:
    from .auxiliar import (carregar_adjacencia, colorir_mapa, gerar_mapa_colorido, gerar_mapa_mundo_colorido, desenhar_arvore)
except ImportError:
    from auxiliar import (carregar_adjacencia, colorir_mapa, gerar_mapa_colorido, gerar_mapa_mundo_colorido, desenhar_arvore)


BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    caminho_grafo = sys.argv[1]
    adjacencia = carregar_adjacencia(BASE_DIR / caminho_grafo)
    resultado, arvore = colorir_mapa(adjacencia) #retorna o resultado e a árvore de busca
    desenhar_arvore(arvore, BASE_DIR / "outputs/arvore_backtracking.png")

    if caminho_grafo == "data/grafo_mundo.gexf":
        gerar_mapa_mundo_colorido(resultado, BASE_DIR / "outputs/mapa_mundo_colorido.png")
    else:
        gerar_mapa_colorido(resultado, BASE_DIR / "outputs/mapa_brasil_regioes_coloridas.png")


if __name__ == "__main__":
    main()