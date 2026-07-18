# Map Coloring CSP Solver

This repository implements the classic map coloring algorithm as a Constraint Satisfaction Problem (CSP) for an introductory Artificial Intelligence course. It converts geographic boundaries into a mathematical topology graph and applies backtracking search to ensure no adjacent states share the same color.

## 👥 Team Members
* Adiel Emilson
* Carlos Adauto
* Guilherme Rocha
* Ricardo Pistori

## ⚙️ Instalação e Requisitos

Para instalar as dependências do projeto, utilize o arquivo `requeriments.txt`. Para evitar conflitos de versão com a biblioteca `shapely` no Python 3.14+, instale as dependências executando o comando a seguir:

```bash
pip install -r requeriments.txt && pip install --no-deps geobr
```

## 🧠 Heurísticas Utilizadas

O solver de backtracking utiliza técnicas de ordenação de variáveis para otimizar a busca:

* **Maior Grau (Degree Heuristic)**: Seleciona o nó que possui a maior quantidade de vizinhos (maior grau no grafo) para tentar reduzir o fator de ramificação o quanto antes.
* **Mais Restringido (Minimum Remaining Values - MRV)**: Prioriza os nós com a menor quantidade de cores válidas restantes no seu domínio.
* **Heurísticas Agrupadas**: Combina ambas as heurísticas. Seleciona o nó mais restringido (MRV) e, em caso de empate, escolhe aquele com o maior grau (Degree Heuristic) como critério de desempate.

## 🚀 Como Rodar o Solver

Você pode executar o solver para colorir os mapas passando o caminho do arquivo do grafo (como `data/grafo_brasil.gexf` ou `data/grafo_mundo.gexf`) como argumento:

```bash
# Para colorir o mapa do Brasil
python -m src.main data/grafo_brasil.gexf

# Para colorir o mapa mundi
python -m src.main data/grafo_mundo.gexf
```

Os mapas gerados serão salvos no diretório `outputs/`.

## ⏱️ Medição de Tempo (Benchmark)

Para rodar o benchmark e ver o tempo de execução do algoritmo para um determinado grafo:

```bash
# Medir tempo no grafo do Brasil (padrão)
python -m src.benchmark data/grafo_brasil.gexf

# Medir tempo no grafo do mundo
python -m src.benchmark data/grafo_mundo.gexf
```

## 📊 Carregamento Manual do Grafo

Caso queira carregar e manipular os grafos diretamente em seus scripts Python usando `networkx`:

```python
import networkx as nx

# Carregar o grafo diretamente do arquivo
G = nx.read_gexf("data/grafo_brasil.gexf")

# Reconstruir o dicionário de posições (pos) a partir dos atributos salvos
pos = {node: (G.nodes[node]['x'], G.nodes[node]['y']) for node in G.nodes()}

print(f"Grafo carregado! Nós: {len(G.nodes)}, Arestas: {len(G.edges)}")
```
