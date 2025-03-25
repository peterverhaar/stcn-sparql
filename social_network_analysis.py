
import os
import re
from pyvis.network import Network
from IPython.core.display import display, HTML
import networkx as nx
import pandas as pd

def rescale(val, in_min, in_max, out_min, out_max):
    return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))


nodes_df = pd.read_csv(f'nodes.csv' )
edges_df = pd.read_csv(f'edges.csv' )
edges_values = edges_df.groupby(['Source','Target'])['Source'].count().to_dict()


def make_network(color_node_type1 = '#EE7733' ,color_node_type2 = '#007788' , background_color = '#dce5f2' , font_size = 50, min_node_size = 30 , max_node_size = 200 ):

    node_size_based_on = 'degree'
    font_size = 50

    ## Choose from: 'repulsion', 'barnes_hut', 'force_atlas'
    visualisation_alogorithm = 'force_atlas'



    G = nx.MultiGraph()

    node_type1 = nodes_df.iloc[0]
    for i,row in nodes_df.iterrows():
        node = row['Id']
        label= row['Label']
        if row['Type'] == node_type1['Type']:
            c = color_node_type1
        else:
            c = color_node_type2
        G.add_node( node, title=label,  color= c )
        
        
    for i,row in edges_df.iterrows():
        edge_width = edges_values[ (row['Source'] , row['Target']) ]
        G.add_edge( row['Source'] , row['Target'] , width= edge_width )


    degree_values = []
    for node in G.nodes:
        degree_values.append(G.degree[node])
        
    in_min = min(degree_values)
    in_max = max(degree_values)

    out_min = min_node_size
    out_max = max_node_size
        
        
    for node in G.nodes:
        degree = G.degree[node] 
        node_size = rescale(degree,in_min,in_max,out_min,out_max)
        G.nodes[node]['size'] = node_size
        G.nodes[node]['label'] = G.nodes[node]['title']
        G.nodes[node]['font']={"size": font_size}
        
    net = Network(notebook=True ,  height="750px", width="100%" , bgcolor= background_color , cdn_resources='in_line' )

    if visualisation_alogorithm == 'repulsion':
        
        net.hrepulsion(
                node_distance=250,
                central_gravity=0.2,
                spring_length=200,
                spring_strength=0.05,
                damping=0.09
        )
    elif visualisation_alogorithm == 'barnes_hut':
        
        net.barnes_hut(
                gravity=-5000, 
                central_gravity=0.3, 
                spring_length=250, 
                spring_strength=0.001, 
                damping=0.09, 
                overlap=0)
        
    else:
        
        net.force_atlas_2based(
                gravity=-250,
                central_gravity=0.03,
                spring_length=100,
                spring_strength=0.08,
                damping=0.4,
                overlap= 1 )

    net.from_nx(G)
    return net
