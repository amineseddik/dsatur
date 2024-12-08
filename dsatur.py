import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# Palette de couleurs
color_palette = sns.color_palette("tab20", 20).as_hex()

def dsatur(graph):
    """
    DSATUR algorithm for graph coloring.

    :param graph: Dictionary representing the graph, where keys are nodes and values are lists of neighbors.
    :return: Dictionary mapping each vertex to its assigned color.
    """
    # Initialization
    colors = {}  # Stores the colors of vertices
    dsat = {}    # Degree of saturation (DSAT) for each vertex
    degree = {node: len(neighbors) for node, neighbors in graph.items()}  # Degree of each vertex
    uncolored = set(graph.keys())  # Set of uncolored vertices

    # Initialize DSAT for each vertex
    for node in graph:
        dsat[node] = degree[node]  # Initially DSAT is the degree for all vertices

    # Color the vertex with the maximum degree
    first_vertex = max(graph.keys(), key=lambda x: degree[x])
    colors[first_vertex] = 1
    uncolored.remove(first_vertex)

    # Update DSAT values after coloring the first vertex
    for neighbor in graph[first_vertex]:
        if neighbor in uncolored:
            dsat[neighbor] = len({colors[n] for n in graph[neighbor] if n in colors})

    # Process remaining vertices
    while uncolored:
        # Select vertex with maximum DSAT; in case of tie, choose the one with highest degree
        next_vertex = max(uncolored, key=lambda x: (dsat[x], degree[x]))

        # Find the smallest available color
        used_colors = {colors[neighbor] for neighbor in graph[next_vertex] if neighbor in colors}
        color = 1
        while color in used_colors:
            color += 1

        # Assign color to the vertex
        colors[next_vertex] = color
        uncolored.remove(next_vertex)

        # Update DSAT values for all uncolored neighbors
        for neighbor in graph[next_vertex]:
            if neighbor in uncolored:
                colored_neighbors = {colors[n] for n in graph[neighbor] if n in colors}
                if colored_neighbors:
                    dsat[neighbor] = len(colored_neighbors)
                else:
                    dsat[neighbor] = degree[neighbor]  # If no neighbor is colored, DSAT is the degree

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
            background-color: #f5f5dc;
            font-family: "Verdana", sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 36px;
            color: #1f618d;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 24px;
            color: #117864;
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Titre principal
    st.markdown('<div class="main-title">Algorithme DSATUR pour la Coloration de Graphe</div>', unsafe_allow_html=True)
    
    # Saisie du nombre de sommets
    st.markdown('<div class="section-title">1. Configuration de votre graphe</div>', unsafe_allow_html=True)
    num_vertices = st.number_input("Nombre de sommets", min_value=1, max_value=20, value=4, step=1)
    graph = {i+1: [] for i in range(num_vertices)}
    
    # Définir les voisins
    st.markdown('<div class="section-title">2. Définir les voisins de chaque sommet</div>', unsafe_allow_html=True)
    for i in range(num_vertices):
        vertex = i + 1
        neighbors_options = [j+1 for j in range(num_vertices) if j+1 != vertex]
        selected_neighbors = st.multiselect(
            f"Sélectionnez les voisins du sommet {vertex}", 
            neighbors_options, 
            key=f"neighbors_{vertex}"
        )
        graph[vertex] = selected_neighbors
    
    # Exécution et affichage
    st.markdown('<div class="section-title">3. Résultats</div>', unsafe_allow_html=True)
    if st.button("Colorer le Graphe"):
        if any(graph.values()):
            result = dsatur(graph)
            st.subheader("Coloration obtenue :")
            result_text = "\n".join([f"Sommet {vertex:02d} -> Couleur {color}" for vertex, color in sorted(result.items())])
            st.text(result_text)
            
            st.subheader("Visualisation du graphe :")
            plt = visualize_graph(graph, result)
            st.pyplot(plt)
            plt.close()
        else:
            st.warning("Veuillez définir les connexions du graphe.")

if __name__ == '__main__':
    main()
