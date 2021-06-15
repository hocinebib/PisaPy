#!/usr/bin/python3
"""
Code to 

  How to use
  ----------
First you need to have the python packages 

Then you can run the script with the following command :

 with pd ids:
    python RunPisaPy.py "6ta5 6iol" /home/meraouna/Téléchargements/naccess2.1.1/naccess

 with pd files:
    python RunPisaPy.py path_to_pdb_files/ --d 1 /home/meraouna/Téléchargements/naccess2.1.1/naccess

  Author
  ------
    Hocine Meraouna

"""

import argparse
import os
import sys
import PisaAuto_id as pai
import PisaAuto_file as paf
import Pisa_xml_parser as pxp
import Parse_Interfacetable as pi
import pandas as pd
import Auto_Naccess as an
import Download_pdbfasta as dpf
from os import listdir
from os.path import isfile
from glob import glob

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_id", help="pdb ids separated by spaces or path to a directory with pdb files", type=str)

    PARSER.add_argument("--d", help="0 if it's a pdb id and 1 if it's path to pdb files", default=0, type=int)

    PARSER.add_argument("nacc_path", help="the full path to the naccess bin", type=str)

    ARGS = PARSER.parse_args()

    PDB_ID = ARGS.pdb_id

    TYPE = ARGS.d

    NACCESS_PATH = ARGS.nacc_path

    if TYPE == 0:
        for protein in PDB_ID.split():
            pai.download_xmls(pai.launch_pdb_id(pai.start(), protein), protein)

    elif TYPE == 1:
        PDB_FILES = sorted([PDB_ID+f for f in listdir(PDB_ID) 
            if ((isfile(PDB_ID+f)) and 
                (f.split(".")[-1] == "pdb"))], key=str.lower)

        for i, file in enumerate(PDB_FILES):
            print("## pdb file "+str(i+1)+"/"+str(len(PDB_FILES)))
            driver = pai.start()
            pai.download_xmls(paf.launch_pdb_file(driver, file), file.split('/')[-1])
            driver.quit()

    else:
           sys.exit("main.py: error: --d should be 1 (for directory) or 0 (for id) nothing else.")

    print("5- Converting xml files to csv and calculating accessibility :")

    for direct in glob('Results/*/'):
        if 'xml_files' in direct:

            if TYPE == 0:
                current_pdb = direct.split('xml_files')[1].split('.')[0][:-1]
                if not os.path.exists('Results/'+current_pdb+'.pdb/'):
                    os.makedirs('Results/'+current_pdb+'.pdb/')
                pxp.create_df(pxp.interfacetable_parse('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'.pdb/'+current_pdb+"_InteractionSheet.csv")
                pd.DataFrame.from_dict(pi.parse_interface('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'.pdb/'+current_pdb+"_InterfaceTable.csv")

            elif TYPE == 1:
                current_pdb = direct.split('xml_files')[1][:-1]
                if not os.path.exists('Results/'+current_pdb):
                    os.makedirs('Results/'+current_pdb)
                pxp.create_df(pxp.interfacetable_parse('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'/'+current_pdb+"_InteractionSheet.csv")
                pd.DataFrame.from_dict(pi.parse_interface('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'/'+current_pdb+"_InterfaceTable.csv")

    print("Done.")

    if TYPE == 1:
        for file in glob('Data/*.pdb'):

            dic = an.interacting_chains("Results/"+file.split('/')[-1]+'/'+file.split('/')[-1]+"_InteractionSheet.csv")

            print("1)- Generating Solo chains files :")

            an.pdb_solo_chains("Data/"+file.split('/')[-1])

            print("Done.")

            print("2)- Generating chains with interacting partners files :")
            
            an.pdb_complex_chains("Data/"+file.split('/')[-1], dic)

            print('Done.')

            print("3)- Generating accessibility csv files :")

            an.call_naccess(dic, NACCESS_PATH, file.split('/')[-1])  

            print('Done.')

    elif TYPE == 0:
        print('- Downloading pdb files and calculating accessibility :')

        for protein in PDB_ID.split():

            dpf.download_pdb(protein)

            dic = an.interacting_chains("Results/"+protein+'.pdb/'+protein+"_InteractionSheet.csv")

            print("1)- Generating Solo chains files :")

            an.pdb_solo_chains("Results/"+protein+'.pdb/'+protein+'.pdb')

            print("Done.")

            print("2)- Generating chains with interacting partners files :")
            
            an.pdb_complex_chains("Results/"+protein+'.pdb/'+protein+'.pdb', dic)

            print('Done.')

            print("3)- Generating accessibility csv files :")

            an.call_naccess(dic, NACCESS_PATH, protein+'.pdb')  

            print('Done.')
