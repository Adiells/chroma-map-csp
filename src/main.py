from pathlib import Path

try:
    from .auxiliar import carregar_adjacencia, colorir_mapa, gerar_mapa_colorido
except ImportError:
    from auxiliar import carregar_adjacencia, colorir_mapa, gerar_mapa_colorido


BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    adjacencia = carregar_adjacencia(BASE_DIR / "data/grafo_brasil.gexf")
    resultado = colorir_mapa(adjacencia)
    gerar_mapa_colorido(resultado, BASE_DIR / "outputs/mapa_brasil_regioes_coloridas.png")


if __name__ == "__main__":
    main()
