#!/usr/bin/python3
"""
Code to represent as a circular graph the interactions between chains residues.

  How to use
  ----------
First you need to have the python packages networkx, matplotlib, pandas and argparse,
and InteractionSheet.csv file created by Pisa_xml_parser.py script.

Then you can run the script with the following command :
    python Chains_Res_Graph.py InteractionSheet.csv

  Author
  ------
    Hocine Meraouna
"""

import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def get_chains(csv_file):
    """
    The function to get the interacting chains from the csv_file.

    Parameters
    ----------
    csv_file : string
        the name of the csv file

    Returns
    -------
    list
    """
    data = pd.read_csv(csv_file, usecols = [2,3,4,6,7])
    chains = []

    for r in data.iterrows():
        if r[1]['chain1']+r[1]['chain2'] not in chains:
            chains.append(r[1]['chain1']+r[1]['chain2'])

    return chains, data

def get_inter_res(chains, dataframe):
    """
    The function to get the interacting residues from the dataframe for each 2 chains.

    Parameters
    ----------
    chains : str
        2 interacting chains names
    dataframe : pandas DataFrame
        data frame of interface interacting residues

    Returns
    -------
    2 lists and a dictionary
    """
    df = dataframe.loc[(dataframe['chain1'] == chains[0]) & (dataframe['chain2'] == chains[1])]

    dico = {}
    for r in df.iterrows():
        if r[1]['res1'].split('[')[0] not in dico.keys():
            dico[r[1]['res1'].split('[')[0]] = []
        dico[r[1]['res1'].split('[')[0]].append([r[1]['res2'].split('[')[0], r[1]['distance']])

    c1_lst = list(dico.keys())
    c1_lst.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    c2_lst = []
    for i in enumerate(list(df['res2'])):
        if list(df['res2'])[i[0]].split('[')[0] not in c2_lst:
            c2_lst.append(list(df['res2'])[i[0]].split('[')[0])
    c2_lst.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    return dico, c1_lst, c2_lst

def sub_graph(graph, lst, col, color_map):
    """
    The function to create the subgraph of one chain.

    Parameters
    ----------
    graph : networkx graph
        the graph given by chains_graph() function
    lst : list
        the list of interface interacting residues
    col : string
        the color
    color_map : list
        the list of colors

    Returns
    -------
    networkx graph
    """
    for i, v in enumerate(lst[0:-1]):
        graph.add_node(v)
        color_map.append(col)
        graph.add_edge(lst[i],lst[i+1],color='g',weight=1)

    graph.add_node(lst[-1])

    return graph

def chains_graph(dico, lst1, lst2):
    """
    The function to create the graph of the interacting residues between 2 chains.

    Parameters
    ----------
    dico : dictionary
        the dictionary created by get_inter_res() function
    lst1 : list
        the list of interface interacting residues of the 1st chain
    lst2 : list
        the list of interface interacting residues of the 2nd chain

    Returns
    -------
    networkx graph and a color map list
    """
    G = nx.Graph()

    color_map = []

    G = sub_graph(G, lst1, "red", color_map)

    color_map.append("red")

    G = sub_graph(G, lst2, "orange", color_map)

    color_map.append("orange")

    for key in lst1:
        for i in dico[key]:
            G.add_edge(key,i[0],color='yellow',weight=i[1])

    return G, color_map

def plot_graph(graph, color_map, chains):
    """
    The function to save the created graph as png.

    Parameters
    ----------
    graph : networkx graph
        the graph given by chains_graph() function
    color_map : list
        the color map list
    chains : str
        the 2 interacting chains names

    Returns
    -------
    Nothing
    """
    plt.subplot()
    ax = plt.gca()
    ax.set_title(chains+' graph')

    edges = graph.edges()
    weights = [graph[u][v]['weight'] for u,v in edges]
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color=color_map, font_weight='bold', edge_color=weights, node_size=30, font_size=6)

    plt.savefig(chains+"_graph.png")
    plt.close()



if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("csv_file", help="the InteractionSheet csv file", type=str)

    ARGS = PARSER.parse_args()

    CSV_FILE = ARGS.csv_file

    CHAINS, DF = get_chains(CSV_FILE)

    for chain in CHAINS:
        DICT, C1L, C2L = get_inter_res(chain, DF)
        GRAPH, CMP = chains_graph(DICT, C1L, C2L)
        plot_graph(GRAPH, CMP, chain)
