#!/usr/bin/python3
"""
Code to 

  How to use
  ----------
First you need to have the python packages 

Then you can run the script with the following command :

 with pd ids:
    python RunPisaPy.py "6ta5 6iol"

 with pd files:
    python RunPisaPy.py path_to_pdb_files/ --d 1

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
from os import listdir
from os.path import isfile
from glob import glob

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_id", help="pdb ids separated by spaces or path to a directory with pdb files", type=str)

    PARSER.add_argument("--d", help="0 if it's a pdb id and 1 if it's path to pdb files", default=0, type=int)

    ARGS = PARSER.parse_args()

    PDB_ID = ARGS.pdb_id

    TYPE = ARGS.d

    if TYPE == 0:
        end = ''
        for protein in PDB_ID.split():
            pai.download_xmls(pai.launch_pdb_id(pai.start(), protein), protein)

    elif TYPE == 1:
        end = '.pdb'
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

    print("5- Converting xml files to csv :")

    for direct in glob('Results/*/'):
        if 'xml_files' in direct:
            if TYPE == 0:
                current_pdb = direct.split('xml_files')[1].split('.')[0][:-1]
            elif TYPE == 1:
                current_pdb = direct.split('xml_files')[1][:-1]
            if not os.path.exists('Results/'+current_pdb):
                os.makedirs('Results/'+current_pdb)
            pxp.create_df(pxp.interfacetable_parse('Results/xml_files'+current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'/'+current_pdb+"_InteractionSheet.csv")
            pd.DataFrame.from_dict(pi.parse_interface('Results/xml_files'+current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'/'+current_pdb+"_InterfaceTable.csv")
    
    print("Done.")
