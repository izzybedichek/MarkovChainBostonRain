# NEED TO GET DISPLAY
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# https://stackoverflow.com/questions/22785849/drawing-multiple-edges-between-two-nodes-with-networkx

data = pd.read_csv('csv/transition_matrix.csv')
print(data)

def my_draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=None,
    label_pos=0.5,
    font_size=20,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="bottom",
    ax=None,
    rotate=True,
    clip_on=True,
    rad=0
):
    """Draw edge labels.

    Parameters
    ----------
    G : graph
        A networkx graph

    pos : dictionary
        A dictionary with nodes as keys and positions as values.
        Positions should be sequences of length 2.

    edge_labels : dictionary (default={})
        Edge labels in a dictionary of labels keyed by edge two-tuple.
        Only labels for the keys in the dictionary are drawn.

    label_pos : float (default=0.5)
        Position of edge label along edge (0=head, 0.5=center, 1=tail)

    font_size : int (default=10)
        Font size for text labels

    font_color : string (default='k' black)
        Font color string

    font_weight : string (default='normal')
        Font weight

    font_family : string (default='sans-serif')
        Font family

    alpha : float or None (default=None)
        The text transparency

    bbox : Matplotlib bbox, optional
        Specify text box properties (e.g. shape, color etc.) for edge labels.
        Default is {boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)}.

    horizontalalignment : string (default='center')
        Horizontal alignment {'center', 'right', 'left'}

    verticalalignment : string (default='center')
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

    ax : Matplotlib Axes object, optional
        Draw the graph in the specified Matplotlib axes.

    rotate : bool (deafult=True)
        Rotate edge labels to lie parallel to edges

    clip_on : bool (default=True)
        Turn on clipping of edge labels at axis boundaries

    Returns
    -------
    dict
        `dict` of labels keyed by edge

    Examples
    --------
     G = nx.dodecahedral_graph()
     edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    https://networkx.org/documentation/latest/auto_examples/index.html

    See Also
    --------
    draw
    draw_networkx
    draw_networkx_nodes
    draw_networkx_edges
    draw_networkx_labels
    """
    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5*pos_1 + 0.5*pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0,1), (-1,0)])
        ctrl_1 = linear_mid + rad*rotation_matrix@d_pos
        ctrl_mid_1 = 0.5*pos_1 + 0.5*ctrl_1
        ctrl_mid_2 = 0.5*pos_2 + 0.5*ctrl_1
        bezier_mid = 0.5*ctrl_mid_1 + 0.5*ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180

            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0

        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items

G = nx.DiGraph()
edge_list = [("rain", "rain", {'w': '0.600000'}), ("clear", "clear", {'w': '0.428571'}),
             ("rain", "clear", {'w': '0.400000'}), ("clear", "rain", {'w': '0.571429'})]

G.add_nodes_from(["rain", "clear"])
G.add_edges_from(edge_list)
pos = nx.spring_layout(G, seed=5)
fig, ax = plt.subplots(figsize=(15, 12))
nx.draw_networkx_nodes(G, pos, node_color="turquoise", ax=ax)
nx.draw_networkx_labels(G, pos, font_size = 18, ax=ax)

curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
straight_edges = list(set(G.edges()) - set(curved_edges))
nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges)
arc_rad = 0.25
nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges,
                       connectionstyle=f'arc3, rad = {arc_rad}')


edge_weights = nx.get_edge_attributes(G, 'w')
curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
my_draw_networkx_edge_labels(G, pos, ax=ax, font_size = 20,
                                   edge_labels=curved_edge_labels, rotate=False,
                                   rad=arc_rad)
nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=straight_edge_labels,
                             rotate=False)


plt.show()

H = nx.DiGraph()
edge_list = [("No rain", "No rain", {'w': '0.42857'}), ("No rain", "Only Friday", {'w': '0.04762'}),
             ("No rain", "Only Saturday", {'w': '0.47619'}), ("No rain", "Only Sunday", {'w': '0.142857'}),
             ("No rain", "Friday and Saturday", {'w': '0.142857'}), ("No rain", "Friday and Sunday", {'w': '0.095238'}),
             ("No rain", "Saturday and Sunday", {'w': '0.0'}), ("No rain", "Rain all weekend", {'w': '0.095238'}),
             ("Only Friday", "No rain", {'w': '0.0'}), ("Only Friday", "Only Friday", {'w': '0.0'}),
             ("Only Friday", "Only Saturday", {'w': '0.0'}), ("Only Friday", "Only Sunday", {'w': '0.0'}),
             ("Only Friday", "Friday and Saturday", {'w': '0.33333'}), ("Only Friday", "Friday and Sunday", {'w': '0.0'}),
             ("Only Friday", "Saturday and Sunday", {'w': '0.66667'}), ("Only Friday", "Rain all weekend", {'w': '0.0'}),
             ("Only Saturday", "No rain", {'w': '0.42857'}), ("Only Saturday", "Only Friday", {'w': '0.04762'}),
             ("Only Saturday", "Only Saturday", {'w': '0.5'}), ("Only Saturday", "Only Sunday", {'w': '0.25'}),
             ("Only Saturday", "Friday and Saturday", {'w': '0.0'}), ("Only Saturday", "Friday and Sunday", {'w': '0.0'}),
             ("Only Saturday", "Saturday and Sunday", {'w': '0.25'}), ("Only Saturday", "Rain all weekend", {'w': '0.0'}),
             ("Only Sunday", "No rain", {'w': '0.6'}), ("Only Sunday", "Only Friday", {'w': '0.4'}),
             ("Only Sunday", "Only Saturday", {'w': '0.0'}), ("Only Sunday", "Only Sunday", {'w': '0.0'}),
             ("Only Sunday", "Friday and Saturday", {'w': '0.0'}), ("Only Sunday", "Friday and Sunday", {'w': '0.0'}),
             ("Only Sunday", "Saturday and Sunday", {'w': '0.0'}), ("Only Sunday", "Rain all weekend", {'w': '0.0'}),
             ("Friday and Saturday", "No rain", {'w': '0.5'}), ("Friday and Saturday", "Only Friday", {'w': '0.0'}),
             ("Friday and Saturday", "Only Saturday", {'w': '0.16667'}), ("Friday and Saturday", "Only Sunday", {'w':'0.16667'}),
             ("Friday and Saturday", "Friday and Saturday", {'w': '0.0'}), ("Friday and Saturday", "Friday and Sunday", {'w': '0.0'}),
             ("Friday and Saturday", "Saturday and Sunday", {'w': '0.0'}), ("Friday and Saturday", "Rain all weekend", {'w': '0.16667'}),
             ("Friday and Sunday", "No rain", {'w': '0.5'}), ("Friday and Sunday", "Only Friday", {'w': '0.0'}),
             ("Friday and Sunday", "Only Saturday", {'w': '0.0'}), ("Friday and Sunday", "Only Sunday", {'w': '0.0'}),
             ("Friday and Sunday", "Friday and Saturday", {'w': '0.5'}), ("Friday and Sunday", "Friday and Sunday", {'w': '0.0'}),
             ("Friday and Sunday", "Saturday and Sunday", {'w': '0.0'}), ("Friday and Sunday", "Rain all weekend", {'w': '0.0'}),
             ("Saturday and Sunday", "No rain", {'w': '0.6'}), ("Saturday and Sunday", "Only Friday", {'w': '0.0'}),
             ("Saturday and Sunday", "Only Saturday", {'w': '0.0'}), ("Saturday and Sunday", "Only Sunday", {'w': '0.0'}),
             ("Saturday and Sunday", "Friday and Saturday", {'w': '0.0'}), ("Saturday and Sunday", "Friday and Sunday", {'w': '0.0'}),
             ("Saturday and Sunday", "Saturday and Sunday", {'w': '0.2'}), ("Saturday and Sunday", "Rain all weekend", {'w': '0.2'}),
             ("Rain all weekend", "No rain", {'w': '0.4'}), ("Rain all weekend", "Only Friday", {'w': '0.0'}),
             ("Rain all weekend", "Only Saturday", {'w': '0.0'}), ("Rain all weekend", "Only Sunday", {'w': '0.0'}),
             ("Rain all weekend", "Friday and Saturday", {'w': '0.2'}), ("Rain all weekend", "Friday and Sunday", {'w': '0.0'}),
             ("Rain all weekend", "Saturday and Sunday", {'w': '0.2'}), ("Rain all weekend", "Rain all weekend", {'w': '0.2'})
             ]

H.add_nodes_from(["No rain", "Only Friday", "Only Saturday", "Only Sunday", "Friday and Saturday", "Friday and Sunday",
                  "Saturday and Sunday", "Rain all weekend"])
H.add_edges_from(edge_list)
pos = nx.spring_layout(H, seed=5)
fig, ax = plt.subplots(figsize=(30, 30))
nx.draw_networkx_nodes(H, pos, node_color="turquoise", ax=ax)
nx.draw_networkx_labels(H, pos, font_size = 18, ax=ax)

curved_edges = [edge for edge in H.edges() if reversed(edge) in H.edges()]
straight_edges = list(set(H.edges()) - set(curved_edges))
nx.draw_networkx_edges(H, pos, ax=ax, edgelist=straight_edges)
arc_rad = 0.25
nx.draw_networkx_edges(H, pos, ax=ax, edgelist=curved_edges,
                       connectionstyle=f'arc3, rad = {arc_rad}')


edge_weights = nx.get_edge_attributes(H, 'w')
curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
my_draw_networkx_edge_labels(G, pos, ax=ax, font_size = 20,
                                   edge_labels=curved_edge_labels, rotate=False,
                                   rad=arc_rad)
nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=straight_edge_labels,
                             rotate=False)


plt.show()