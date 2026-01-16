# plotting
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def draw_graph(
    G,
    groups=None,
    *,
    title=None,
    seed=42,
    node_spacing=1,
    node_color="lightblue",
    node_size=500,
    show_legend="auto",
    outline_nodes=True,
    fill_nodes=False,
    layout="spring",
    figsize=(10, 8),
    groups_edge_style="solid",
    default_edge_style="dotted",
    default_edge_color="gray",
    default_colors=None,
    node_labels_key=None,
    min_edge_width=1,
    max_edge_width=1.005,
    edge_weight_key="weight",
    font_size=9,
    font_weight="normal",
    font_color="k",
    bbox=None,
    draw_node_shapes=True
):
    """
    Draw a graph emphasizing arbitrary groups of nodes and/or edges.

    Parameters
    ----------
    G : networkx.Graph
        Graph to draw.
    groups : list of dict
        Each dict represents a group with optional keys:
            - 'nodes': list of nodes to emphasize
            - 'edges': list of edges (tuples) to emphasize
            - 'color': color for this group (optional)
            - 'label': label of this group (optional), defaults to Group {index of this group}
    title : str, optional
        Figure title.
    seed : int
        Random seed for layout.
    node_spacing : int
        Spacing between nodes.
    node_color : str
        Fill color for nodes.
    node_size : int
        Node size.
    show_legend : bool | "auto"
        Show legend.
    outline_nodes : bool
        If True, nodes in groups get colored outlines.
    fill_nodes : bool
        If True, nodes in groups get colored fill.
    layout : str
        "kamada_kawai" or "spring".
    figsize : tuple
        Figure size.
    groups_edge_style: str
        Style of edges in groups.
    default_edge_style: str
        Default style of edges.
    default_edge_color: str
        Default color of all edges.
    default_colors : sequence, optional
        Sequence of colors to use for groups without specified color.
    node_labels_key : str
        Attribute which should be used as node name instead of node id.
    min_edge_width: int
        Minimal width of an edge.
    max_edge_width: int
        Maximal width of an edge.
    edge_weight_key: str | None
        Attribute used for edge width calculation
    font_size : int or dictionary of nodes to ints (default=12)
        Font size for text labels.
    font_color : color or dictionary of nodes to colors (default='k' black)
        Font color string. Color can be string or rgb (or rgba) tuple of floats from 0-1.
    font_weight : string or dictionary of nodes to strings (default='normal')
        Font weight.
    bbox : dict | None
         Matplotlib bbox, (default is Matplotlib's ax.text default)
        Specify text box properties (e.g. shape, color etc.) for node labels.
    draw_node_shapes: boolean
        Specifies if nodes should be drawn or if should be drawn just labels.
        If True, drawns nodes and labels, otherwise does not draw nodes. 
        (default=True)
    """

    if default_colors is None:
        default_colors = plt.cm.tab10.colors

    # ---------- Layout ----------
    if layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G,scale=node_spacing)
    elif layout == "spring":
        pos = nx.spring_layout(G, seed=seed, k=node_spacing * 1.5 / (G.number_of_nodes() ** 0.5))
    else:
        raise ValueError(f"Unsupported layout: {layout}")

    plt.figure(figsize=figsize)

    grouped_nodes = set()
    grouped_edges = set()
    legend_handles = []

    def get_edges_width(G,edges):
        width = min_edge_width
        if(edge_weight_key != None):
            edge_width_len = max_edge_width - min_edge_width

            def get_edge_weight(edge):
                weight = edge.get(edge_weight_key)
                return weight if weight != None else 0
                
            
            width = list(map(lambda edge: 
                        min_edge_width + int(get_edge_weight(G.edges[edge[0],edge[1]])) * edge_width_len,
                            edges
                            ))
        return width

    # ---------- Draw groups ----------
    if groups:
        for i, group in enumerate(groups):
            color = group.get("color", default_colors[i % len(default_colors)])
            nodes = group.get("nodes", [])
            edges = group.get("edges", [])
            label = group.get("label",f"Group {i+1}")

            # Draw edges
            if edges:
                nx.draw_networkx_edges(
                    G, pos,
                    edgelist=edges,
                    width=get_edges_width(G,edges),
                    edge_color=[color]*len(edges),
                    style=groups_edge_style,
                    label=label
                )
                grouped_edges.update(edges)
                legend_handles.append(Line2D([], [], color=color, label=label))

            # Draw nodes
            if nodes:
                nodes_label=None if edges else label
                nx.draw_networkx_nodes(
                    G, pos,
                    nodelist=nodes,
                    node_color=color if fill_nodes else node_color,
                    edgecolors=color if outline_nodes else default_edge_color,
                    linewidths=2 if outline_nodes else 1,
                    node_size=node_size,
                    label=nodes_label
                )
                grouped_nodes.update(nodes)
            
            


    # ---------- Draw remaining edges ----------
    other_edges = [e for e in G.edges() if e not in grouped_edges]
    nx.draw_networkx_edges(G, pos, edgelist=other_edges,
                           style=default_edge_style, 
                           width=get_edges_width(G,other_edges),
                           edge_color=default_edge_color)

    # ---------- Draw remaining nodes ----------
    if draw_node_shapes:
        other_nodes = [n for n in G.nodes() if n not in grouped_nodes]
        nx.draw_networkx_nodes(G, pos, nodelist=other_nodes,
                               node_color=node_color,
                               edgecolors=default_edge_color,
                               linewidths=1,
                               node_size=node_size)

    # ---------- Labels and legend ----------
    labels = {node:name for node,name in G.nodes(data=node_labels_key)}
    for node in G.nodes():
        if labels.get(node) == None:
            labels[node]=node
    nx.draw_networkx_labels(G, 
                            pos,
                            labels=labels, 
                            font_size=font_size,
                            font_weight=font_weight,
                            font_color=font_color,
                            bbox=bbox)
    if show_legend is True or (show_legend == "auto" and groups and len(groups) > 1):
        plt.legend(frameon=False)
    if title:
        plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()



def plot_bar(
    x,
    height,
    xlabel=None,
    ylabel=None,
    title=None,
    figsize=(10, 6),
    add_labels=False,
    xticks=None,
    rotation=0
):
    """
    Draw a bar plot with optional labels on top of bars.
    """
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(x, height, color='lightblue', edgecolor='black')

    ax.set_xlabel(xlabel if xlabel else "")
    ax.set_ylabel(ylabel if ylabel else "")
    ax.set_title(title if title else "")

    if xticks is not None:
        ax.set_xticks(xticks)
        ax.tick_params(axis='x', rotation=rotation)

    ax.grid(axis='y', linestyle='--', alpha=0.6)

    if add_labels:
        ax.bar_label(bars,
                      padding=3,
                      fmt=lambda value: '' if value == 0 else f"{value:g}"
                      )

    plt.show()
