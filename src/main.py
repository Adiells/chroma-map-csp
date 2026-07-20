from pathlib import Path
import sys

try:
    from .auxiliar import carregar_adjacencia, colorir_mapa, gerar_mapa_colorido, gerar_mapa_mundo_colorido, gerar_grafo_colorido
except ImportError:
    from auxiliar import carregar_adjacencia, colorir_mapa, gerar_mapa_colorido, gerar_mapa_mundo_colorido, gerar_grafo_colorido


BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    caminho_grafo = sys.argv[1] if len(sys.argv) > 1 else 'data/grafo_brasil.gexf'
    adjacencia = carregar_adjacencia(BASE_DIR / caminho_grafo)
    resultado = colorir_mapa(adjacencia)

    if Path(caminho_grafo).name == 'grafo_mundo.gexf':
        gerar_mapa_mundo_colorido(resultado, BASE_DIR / "outputs/mapa_mundo_colorido.png")
    else:
        gerar_grafo_colorido(BASE_DIR / caminho_grafo, resultado, BASE_DIR / "outputs/grafo_brasil_colorido.png")
        gerar_mapa_colorido(resultado, BASE_DIR / "outputs/mapa_brasil_regioes_coloridas.png")


if __name__ == "__main__":
    main()
