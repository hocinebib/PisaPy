"""
small code for parsing pisa xml files and creating a csv file

how to use :

first you need to download interfacetable.xml and each hydrogenbond.xml and saltbridge.xml files
given by pisa web server

then you run the script with the following command :

    python Pisa_xml_parser.py interfacetable.xml

note that the hydrogen bond and slatbridge files must be on the same directory as interfacetable

Hocine
"""

import argparse
import pandas as pd
import re
import os.path

#this dict only works for MexAB-OprM complex
DICT_CHAINS = {'OprM': 'ABC', 'MexA': 'DEFGHI', 'MexB': 'JKL'}

def xmlbond_parser(xml_file):
    """
    parse the interaction xml files
    haven't been tested on disulfide and covalent bonds
    """
    value = []
    lst = []

    if os.path.exists(xml_file):
        with open(xml_file, "r") as f_xml:
            for line in f_xml :
                if line.startswith("<STRUCTURE1>"):
                    value.append(line[12:13])
                    value.append(line[14:27])
                elif line.startswith("<DISTANCE>"):
                    value.append(float(re.split('<|>',line[10:17])[0]))
                elif line.startswith("<STRUCTURE2>"):
                    value.append(line[13:14])
                    value.append(line[15:28])
                    lst.append(value)
                    value = []
    else:
        print("No ",xml_file, "found")

    return(lst)

def give_prot(search_chain):
    """
    just a little function to get the protein with the chain
    """
    for protein in DICT_CHAINS.keys():
        for chain in DICT_CHAINS[protein]:
            if chain == search_chain:
                return(protein)

    print("The chain corresponds to none of the proteins")
    return('')

def interfacetable_parse(xml_file):
    """
    a little function to parse interfacetable.xml and calls xmlbond_parser()
    """
    lst = []
    intern_lst = []

    with open(xml_file, "r") as f_xml:
        for line in f_xml :
            if line.startswith("<INTERFACENO>"):
                i = int(line[13:15].strip("<"))
                intern_lst.append(i)
                intern_lst.append(xmlbond_parser("hydrogenbond"+str(i-1)+".xml"))
                intern_lst.append(xmlbond_parser("saltbridge"+str(i-1)+".xml"))
            elif line.startswith("<INTERFACEAREA>"):
                intern_lst.append(float(line[15:23].strip("<")))
            elif line.startswith("<INTERFACEDELTAGPVALUE>"):
                intern_lst.append(float(line[23:31].strip("<")))
                lst.append(intern_lst)
                intern_lst = []

    return(lst)

def create_df(lst):
    """
    the function that will create the dataframe
    """
    data = {'protein1': [], 'chain1': [], 'res1': [], 
    'distance': [], 'protein2': [], 'chain2': [], 
    'res2': [], 'interaction type': [], 'ΔiG kcal/mol': [], 
    'ΔiG P-value': []}

    for c in lst:
        for i in c[1]:
            data['protein1'].append(give_prot(i[0]))
            data['chain1'].append(i[0])
            data['res1'].append(i[1])
            data['distance'].append(i[2])
            data['protein2'].append(give_prot(i[3]))
            data['chain2'].append(i[3])
            data['res2'].append(i[4])
            data['interaction type'].append("Hydrogen bond")
            data['ΔiG kcal/mol'].append(c[3])
            data['ΔiG P-value'].append(c[4])
        if c[2] != []:
            for j in c[2]:
                data['protein1'].append(give_prot(j[0]))
                data['chain1'].append(j[0])
                data['res1'].append(j[1])
                data['distance'].append(j[2])
                data['protein2'].append(give_prot(j[3]))
                data['chain2'].append(j[3])
                data['res2'].append(j[4])
                data['interaction type'].append("Salt bridge")
                data['ΔiG kcal/mol'].append(c[3])
                data['ΔiG P-value'].append(c[4])

    return(pd.DataFrame.from_dict(data))
    

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("xml_file", help="the pisa interface table xml file", type=str)

    ARGS = PARSER.parse_args()

    XML_FILE = ARGS.xml_file

    create_df(interfacetable_parse(XML_FILE)).to_csv("InteractionSheet.csv")