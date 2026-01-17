# graph_utils
import networkx as nx
import polars as pl

def get_graph_metrics(G,cliques=None,distance_key=None,weight_key=None):
    bridges = list(nx.bridges(G))
    articulations = list(nx.articulation_points(G))
    components = list(nx.connected_components(G))
    cliques =cliques if cliques != None else list(nx.find_cliques(G))
    cliques_number=max(map(lambda clique: len(clique),cliques))
    
    return {
        "Počet uzlů":len(nx.nodes(G)),
        "Počet hran":len(nx.edges(G)),
        "Tranzitivita":nx.transitivity(G),
        "Diametr":nx.diameter(G,weight=distance_key),
        "Hustota":nx.density(G),
        "Průměrná délka cesty":nx.average_shortest_path_length(G,weight=distance_key),
        "Klikovost":cliques_number,
        "Průměrný clustering": nx.average_clustering(G,weight=weight_key),
        "Počet artikulací":len(articulations),
        "Počet mostů":len(bridges),
        "Počet komponent": len(components),
        "Počet klik":len(cliques),
        "Kliky":cliques,
        "Artikulace":articulations,
        "Mosty":bridges,
    }

def get_graph_metrics_df(G,cliques=None,weight_key=None,distance_key=None):
    return pl.DataFrame([
        get_graph_metrics(
            G,
            cliques=cliques,
            weight_key=weight_key,
            distance_key=distance_key
            )
        ])


def count_cliques_by_vertex(G,cliques):
    clique_count_by_vertex = {node:0 for node in G.nodes()}
    for clique in cliques:
        for node in clique:
            clique_count_by_vertex[node]+=1
    return clique_count_by_vertex

def get_nodes_metrics_df(G,cliques=None,attributes=[],distance_key=None,weight_key=None,eigen_vector_alg='power'):
    degree_dict = dict(G.degree())
    eigen_vector_dict = {}
    if eigen_vector_alg == 'power':
        eigen_vector_dict = nx.eigenvector_centrality(G,weight=weight_key)
    else:
        eigen_vector_dict = nx.eigenvector_centrality_numpy(G,weight=weight_key)
    
    betweenness_dict = nx.betweenness_centrality(G,weight=distance_key)
    closeness_dict = nx.closeness_centrality(G,distance=distance_key)
    clustering_dict = nx.clustering(G,weight=weight_key)
    clique_count_by_vertex = count_cliques_by_vertex(G,cliques if cliques != None else nx.find_cliques(cliques))
   

    # Build DataFrame
    nodes = []
    attributesDict = dict.fromkeys(attributes,[])
    for node_item in G.nodes.items():
        nodes.append(node_item[0])
        node_attributes = node_item[1]
        for attr,values in attributesDict.items():
            node_attr_value = node_attributes.get(attr)
            if node_attr_value != None:
                values.append(node_attr_value)
                
    weighted_centralities_dict = {}
    if weight_key != None:
        weighted_degree_dict = dict(G.degree(weight=weight_key))
        weighted_centralities_dict['weighted degree']=[weighted_degree_dict[n] for n in nodes]
        
    df_dict = {
        "uzel": nodes,
        "klikovost": [clique_count_by_vertex[n] for n in nodes],
        "degree": [degree_dict[n] for n in nodes],
        "eigen-vector": [eigen_vector_dict[n] for n in nodes],
        "betweeness": [betweenness_dict[n] for n in nodes],
        "closeness": [closeness_dict[n] for n in nodes],
        "clustering":[float(clustering_dict[n]) for n in nodes]
    }|weighted_centralities_dict|attributesDict
    return pl.DataFrame(df_dict)
    


def tranform_weights_strength_to_cost(edges,strength_key,price_key):
    for edge in edges.items():
        edge[1][price_key]=1/edge[1][strength_key]