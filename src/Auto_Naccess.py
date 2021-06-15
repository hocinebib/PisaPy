#!/usr/bin/python3
"""
Code to get accessibility

  How to use
  ----------
First you need to have the python packages  

Then you can run the script with the following command :

    python Auto_Naccess.py pdb_name.pdb csv_file.csv /home/meraouna/Téléchargements/naccess2.1.1/naccess

  Author
  ------
    Hocine Meraouna

"""

import pandas as pd
import os
import argparse
from Bio.PDB import NACCESS 
from Bio.PDB import PDBParser
import warnings
warnings.filterwarnings("ignore")


def keep_nbr(x):
    return x.split('[')[0].split()[1]


def interacting_chains(csv):
    """
    """

    df = pd.read_csv(csv, usecols = [2,3,6,7]).drop_duplicates()

    df['res1'] = df['res1'].apply(keep_nbr)
    df['res2'] = df['res2'].apply(keep_nbr)

    dico = {}

    for r in df.iterrows():
        if r[1]['chain1'] not in dico:
            dico[r[1]['chain1']] = []
        if r[1]['chain2'] not in dico:
            dico[r[1]['chain2']] = []
        for i in range(-3,4):
            rn1 = str(int(r[1]['res2'])+i)
            rn2 = str(int(r[1]['res1'])+i)
            if (r[1]['chain2']+' '+rn1) not in dico[r[1]['chain1']]:
                dico[r[1]['chain1']].append((r[1]['chain2']+' '+rn1))
            if (r[1]['chain1']+' '+rn2) not in dico[r[1]['chain2']]:
                dico[r[1]['chain2']].append((r[1]['chain1']+' '+rn2))

    return dico


def pdb_solo_chains(pdb):
    """
    """

    chains_lst = []

    with open(pdb, 'r') as pdb_file:
        for line in pdb_file:
            if line.startswith('ATOM'):
                if len(line.split()[4]) > 1:
                    chain = line.split()[4][0]
                else:
                    chain = line.split()[4]
                if not os.path.exists('Results/'+pdb.split('/')[-1]+'/chain_'+chain):
                    os.makedirs('Results/'+pdb.split('/')[-1]+'/chain_'+chain)
                if chain not in chains_lst:
                    f = open('Results/'+pdb.split('/')[-1]+'/chain_'+chain+'/'+chain+'_solo.pdb', 'w')
                    chains_lst.append(chain)
                else :
                    f = open('Results/'+pdb.split('/')[-1]+'/chain_'+chain+'/'+chain+'_solo.pdb', 'a')
                f.write(line)
                f.close()


def pdb_complex_chains(pdb, dico):
    """
    """

    for k in dico:
        f = open('Results/'+pdb.split('/')[-1]+'/chain_'+k+'/'+k+'_complex.pdb', 'w')#'_'+''.join(dico[k])+
        with open(pdb, 'r') as pdb_file:
            for line in pdb_file:
                if line.startswith('ATOM'):
                    if len(line.split()[4]) > 1:
                        chain = line.split()[4][0]
                        rsn = line.split()[4][1:]
                    else:
                        chain = line.split()[4]
                        rsn = line.split()[5]
                    if chain == k:
                        f.write(line)
                    elif chain+' '+rsn in dico[k]:
                        f.write(line)
        f.close()


def run_naccess(k, sol_comp, naccess_path, pdb):
    """
    """
    chain_csv_solo = {'chain': [], 'res': [], sol_comp+' access': []}

    pdb_file = os.getcwd()+'/Results/'+pdb+'/chain_'+k+'/'+k+'_'+sol_comp+'.pdb'
    p = PDBParser()
    s = p.get_structure("X", pdb_file)
    model = s[0]
    n = NACCESS.NACCESS(model, pdb_file, naccess_binary=naccess_path)
    
    for e in n:
        res = e[0].xtra['EXP_NACCESS']['res_name']
        chain = e[0].full_id[2]
        resnbr = str(e[0].full_id[3][1])
        acc = e[0].xtra['EXP_NACCESS']['all_atoms_abs']
        chain_csv_solo['chain'].append(chain)
        chain_csv_solo['res'].append(res+' '+resnbr)
        chain_csv_solo[sol_comp+' access'].append(acc)

    return pd.DataFrame.from_dict(chain_csv_solo)


def call_naccess(dico, naccess_path, pdb):
    """
    """
    for keyy in dico:
        print(" - Naccess on solo chains", keyy)
        df_solo = run_naccess(keyy, 'solo', naccess_path, pdb)
        print(" - Naccess on complex chains", keyy)
        df_comp = run_naccess(keyy, 'complex', naccess_path, pdb)

        both = pd.merge(df_solo, df_comp, on=["chain", "res"])
        both.to_csv(os.getcwd()+'/Results/'+pdb+'/chain_'+keyy+'/'+keyy+'_access.csv')



if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_file", help="the pdb file", type=str)

    PARSER.add_argument("csv_file", help="the csv interactions file", type=str)

    PARSER.add_argument("naccess_path", help="the full path to the naccess bin", type=str)

    ARGS = PARSER.parse_args()

    PDB = ARGS.pdb_file

    CSV = ARGS.csv_file

    NACCESS_PATH = ARGS.naccess_path

    dic = interacting_chains(CSV)

    print("1)- Generating Solo chains files :")

    pdb_solo_chains(PDB)

    print("Done.")

    print("2)- Generating chains with interacting partners files :")

    pdb_complex_chains(PDB, dic)

    print('Done.')

    print("3)- Generating accessibility csv files :")

    call_naccess(dic, NACCESS_PATH, PDB)

    print('Done.')
