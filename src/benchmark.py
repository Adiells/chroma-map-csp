import time
from pathlib import Path
import sys

try:
    from src.auxiliar import carregar_adjacencia, colorir_mapa
except ImportError:
    from auxiliar import carregar_adjacencia, colorir_mapa

BASE_DIR = Path(__file__).resolve().parent.parent


def medir_tempo():
    caminho_grafo = sys.argv[1] if len(sys.argv) > 1 else 'data/grafo_brasil.gexf'
    adjacencia = carregar_adjacencia( BASE_DIR / caminho_grafo)
    
    inicio = time.perf_counter()
    _ = colorir_mapa(adjacencia)
    fim = time.perf_counter()
    
    tempo_total = fim - inicio
    print(f"Tempo de execução do algoritmo: {tempo_total:.6f} segundos")


if __name__ == "__main__":
    medir_tempo()
