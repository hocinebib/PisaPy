#!/usr/bin/python3
"""
Download pdb and fasta files using pdb id.

  How to use
  ----------
First you need to have the python packages .

Then you can run the script with the following command :
    python Download_pdbfasta.py "6ta5 6iol"

  Author
  ------
    Hocine Meraouna
"""

import argparse
import requests
import os


def download_pdb(file_name):
    """
    """

    url = 'https://files.rcsb.org/download/'+file_name+'.pdb'
    r = requests.get(url, allow_redirects=True)

    if not os.path.exists('Results/'+file_name+'.pdb'):
        os.makedirs('Results/'+file_name+'.pdb')

    open('Results/'+file_name+'.pdb/'+file_name+'.pdb', 'wb').write(r.content)


def download_fasta(file_name):
    """
    """

    url = 'https://www.rcsb.org/fasta/entry/'+file_name+'/display'
    r = requests.get(url, allow_redirects=True)

    if not os.path.exists('Results/'+file_name):
        os.makedirs('Results/'+file_name)

    open('Results/'+file_name+'/'+file_name+'.fasta', 'wb').write(r.content)


def parse_fasta(file_name):
    """
    """

    f = open('Results/dico_'+file_name+'.txt', 'w')
    f.write('{')
    i = 0

    with open('Results/'+file_name+'.fasta', 'r') as f_fasta:
        for line in f_fasta:
            if line.startswith('>'):
                if i > 0:
                    f2.close()
                desc = line.split('|')
                chains = desc[1].split('Chains ')[1].split(',')
                f2 = open('Results/'+desc[0][1:]+'.fasta', 'w')
                f2.write(line)
                if i > 0:
                    f.write(', ')
                for n, c in enumerate(chains):
                  if len(c) > 1:
                    chains[n] = c.split('[')[0]
                  chains[n] = chains[n].strip()
                f.write('\"'+desc[2]+'\": \"'+''.join(chains)+'\"')
                i += 1
            else :
                f2 = open('Results/'+desc[0][1:]+'.fasta', 'a')
                f2.write(line)
    
    f2.close()
    f.write('}')
    f.close()


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_files", help="the pdb file ids separated by spaces", type=str)

    ARGS = PARSER.parse_args()

    PDB_FILES = ARGS.pdb_files

    if not os.path.exists('Results'):
        os.makedirs('Results')

    for pdb in PDB_FILES.split():
        download_pdb(pdb)
        download_fasta(pdb)
        parse_fasta(pdb)
