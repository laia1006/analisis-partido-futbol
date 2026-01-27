# Proyecto: El FC Barcelona como Sistema Biológico Complejo
# Autora: Laia Zamora Parras
# Background: Bioinformática + Redes + IA Generativa

# OBJETIVO DEL PROYECTO:
# Principal --> modelar un equipo de fútbol como una red biológica compleja
# 1. Construir una red de pases (grafo)
# 2. Analizar nodos clave y robustez del sistema
# 3. Generar un diagnóstico táctico usando IA generativa

# -----------------------------
# PASO 0: LIBRERÍAS
# -----------------------------
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# PASO 1: CARGA DE DATOS
# -----------------------------
# Esperamos un CSV con al menos:
# passer, receiver, minute

df = pd.read_csv("passes.csv")

# -----------------------------
# PASO 2: CONSTRUCCIÓN DE LA RED (RED METABÓLICA)
# -----------------------------
G = nx.DiGraph()

for _, row in df.iterrows():
    if G.has_edge(row['passer'], row['receiver']):
        G[row['passer']][row['receiver']]['weight'] += 1
    else:
        G.add_edge(row['passer'], row['receiver'], weight=1)

# -----------------------------
# PASO 3: MÉTRICAS DE RED (BIOINFORMÁTICA PURA)
# -----------------------------
betweenness = nx.betweenness_centrality(G, weight='weight')
degree = nx.degree_centrality(G)

metrics = pd.DataFrame({
    "betweenness": betweenness,
    "degree": degree
}).sort_values("betweenness", ascending=False)

print("\n--- MÉTRICAS DE NODOS (JUGADORES) ---")
print(metrics.head(5))

# -----------------------------
# PASO 4: ROBUSTEZ DEL SISTEMA (KNOCK-OUT)
# -----------------------------
def system_efficiency(graph):
    try:
        return nx.global_efficiency(graph)
    except:
        return 0

baseline_eff = system_efficiency(G)

# Evitar división por cero en grafos pequeños o no conectados
if baseline_eff == 0:
    baseline_eff = 1e-6

robustness = {}
for node in G.nodes():
    G_tmp = G.copy()
    G_tmp.remove_node(node)
    robustness[node] = system_efficiency(G_tmp) / baseline_eff

robustness_df = (
    pd.DataFrame.from_dict(robustness, orient="index", columns=["relative_efficiency"])
    .sort_values("relative_efficiency")
)

print("\n--- IMPACTO DE KNOCK-OUT ---")
print(robustness_df.head(5))


# -----------------------------
# PASO 5: VISUALIZACIÓN SIMPLE
# -----------------------------

edges_to_draw = [
    (u, v) for u, v, d in G.edges(data=True)
    if d["weight"] >= 3
]


G_vis = G.edge_subgraph(edges_to_draw)

plt.figure(figsize=(7,7))


pos = nx.spring_layout(
    G_vis,
    seed=42,
    k=2.5,
)

nx.draw(
    G_vis, pos,
    with_labels=True,
    node_size=2500,
    node_color="lightpink",
    font_size=9
)
widths = [
    G_vis[u][v]["weight"] * 0.3
    for u, v in G_vis.edges()
]

nx.draw_networkx_edges(G_vis, pos, width=widths)


plt.title("Red de pases como sistema biológico")
plt.show()
