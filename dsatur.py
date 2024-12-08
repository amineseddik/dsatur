import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


# Palette de couleurs
color_palette = sns.color_palette("tab20", 20).as_hex()

def dsatur(graph):
    """
    Algorithme DSATUR pour la coloration de graphe.
    """
    colors = {}
    dsat = {}
    degree = {node: len(neighbors) for node, neighbors in graph.items()}
    uncolored = set(graph.keys())
    
    for node in graph:
        dsat[node] = 0
    
    first_vertex = max(graph.keys(), key=lambda x: degree[x])
    colors[first_vertex] = 1
    uncolored.remove(first_vertex)
    
    for neighbor in graph[first_vertex]:
        if neighbor in uncolored:
            dsat[neighbor] = len({colors[n] for n in graph[neighbor] if n in colors})
    
    while uncolored:
        next_vertex = max(uncolored, key=lambda x: (dsat[x], degree[x]))
        used_colors = {colors[neighbor] for neighbor in graph[next_vertex] if neighbor in colors}
        color = 1
        while color in used_colors:
            color += 1
        colors[next_vertex] = color
        uncolored.remove(next_vertex)
        for neighbor in graph[next_vertex]:
            if neighbor in uncolored:
                colored_neighbors = {colors[n] for n in graph[neighbor] if n in colors}
                dsat[neighbor] = len(colored_neighbors)
    return colors

def visualize_graph(graph, colors):
    """
    Visualiser le graphe avec ses couleurs
    """
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G, seed=42)
    node_colors = [color_palette[(colors[node]-1) % len(color_palette)] for node in G.nodes()]
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="black")
    plt.title("Coloration du Graphe (DSATUR)", fontsize=16, fontweight="bold")
    plt.axis('off')
    return plt

def main():
    st.set_page_config(page_title="Coloration de Graphe - DSATUR", page_icon=":art:", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f7f7f7;
            font-family: "Arial", sans-serif;
        }
        .title {
            color: #2c3e50;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.title("Algorithme DSATUR pour la Coloration de Graphe")
    num_vertices = st.number_input("Nombre de sommets", min_value=1, max_value=20, value=4, step=1)
    graph = {i+1: [] for i in range(num_vertices)}
    st.write("Définissez les voisins de chaque sommet :")
    for i in range(num_vertices):
        vertex = i + 1
        neighbors_options = [j+1 for j in range(num_vertices) if j+1 != vertex]
        selected_neighbors = st.multiselect(
            f"Sélectionnez les voisins du sommet {vertex}", 
            neighbors_options, 
            key=f"neighbors_{vertex}"
        )
        graph[vertex] = selected_neighbors
    
    if st.button("Colorer le Graphe"):
        if any(graph.values()):
            result = dsatur(graph)
            st.write("Résultat de la coloration :")
            for vertex, color in sorted(result.items()):
                st.write(f"Sommet {vertex} -> Couleur {color}")
            plt = visualize_graph(graph, result)
            st.pyplot(plt)
            plt.close()
        else:
            st.warning("Veuillez définir les connexions du graphe.")

if __name__ == '__main__':
    main()
