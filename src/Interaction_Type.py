#!/usr/bin/python3
"""
Code to get the major interaction type between two chains.

  How to use
  ----------
First you need to have the python packages pandas and argparse, and and InteractionSheet.csv
file created by Pisa_xml_parser.py script.

Then you can run the script with the following command :
  1- to specify the cutoff :
    python Interaction_Type.py InteractionSheet.csv

  Author
  ------
    Hocine Meraouna
"""

import argparse
import pandas as pd

def get_chains(dataframe):
    """
    the function to get the interacting chains.
    """
    chains = []

    for r in dataframe.iterrows():
        if str(r[1]['chain1'])+str(r[1]['chain2']) not in chains:
            chains.append(str(r[1]['chain1'])+str(r[1]['chain2']))

    return chains

def dict_inter_type(chains, dataframe):
    """
    the function that creates a dictionary with number of each interaction type for every 2 chains.
    """
    dico = {}
    for c in chains:
        dico2 = {}
        dico2[dataframe.loc[(dataframe['chain1'] == c[0]) & (dataframe['chain2'] == c[1])]['interaction type'].value_counts().index[0]] = dataframe.loc[(dataframe['chain1'] == c[0]) & (dataframe['chain2'] == c[1])]['interaction type'].value_counts()[0]
        if len(dataframe.loc[(dataframe['chain1'] == c[0]) & (dataframe['chain2'] == c[1])]['interaction type'].value_counts()) > 1:
            dico2[dataframe.loc[(dataframe['chain1'] == c[0]) & (dataframe['chain2'] == c[1])]['interaction type'].value_counts().index[1]] = dataframe.loc[(dataframe['chain1'] == c[0]) & (dataframe['chain2'] == c[1])]['interaction type'].value_counts()[1]
        dico[c] = dico2

    return dico

def inter_type_prct(dico):
    """
    the function to calculate the pourcentage of interaction type for eache 2 chains.
    """
    new_dict = {'chains': [], 'interaction type': [], 'pourcentage': []}
    for k in dico:
        if 'Salt bridge' in dico[k]:
            new_dict['chains'].append(k)
            if dico[k]['Hydrogen bond'] > dico[k]['Salt bridge']:
                new_dict['interaction type'].append('Hydrogen bond')
                new_dict['pourcentage'].append(dico[k]['Hydrogen bond']*100/(dico[k]['Hydrogen bond']+dico[k]['Salt bridge']))
            else :
                new_dict['interaction type'].append('Salt bridge')
                new_dict['pourcentage'].append(dico[k]['Salt bridge']*100/(dico[k]['Hydrogen bond']+dico[k]['Salt bridge']))
        else :
            new_dict['chains'].append(k)
            new_dict['interaction type'].append('Hydrogen bond')
            new_dict['pourcentage'].append(100.0)

    return new_dict


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("csv_file", help="the InteractionSheet csv file", type=str)

    ARGS = PARSER.parse_args()

    CSV_FILE = ARGS.csv_file

    DATA = pd.read_csv(CSV_FILE, usecols = [2,3,4,5,6,7,8])

    pd.DataFrame.from_dict(inter_type_prct(dict_inter_type(get_chains(DATA), DATA))).to_csv("MajorInteractionType.csv")
