#!/usr/bin/python3
"""
Code to automatically run PDBePISA web server on pdb files and downloading the
generated xml files.

  How to use
  ----------

First you need to have the python packages selenium, halo and argparse installed 
and the PisaAuto_id.py script, you also need the pdb files on witch you want to 
run pisa.

Then you can run the script with the following command :

    python PisaAuto_file.py path_to_pdb_files_folder/


Note that right now it's made for firefox browser but adding other browsers 
isn't hard to implement (ex: driver = webdriver.Chrome() for chrome).
Also note that only the interface table, the residues interaction and interfacing 
residues xml files are downloaded. 
hard

  Author
  ------
    Hocine Meraouna

"""

import time
import os
import sys
from os import listdir
from os.path import isfile
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from halo import Halo
import PisaAuto_id as pisa

def check_exists_by_name(name, driver):
    """
    The function to check if an element is present on the webdriver.

    Parameters
    ----------
    driver : selenium webdriver
    name : string
        the name of the element

    Returns
    -------
    boolean
    """
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True

def launch_pdb_file(driver, pdb_file):
    """
    The function to run pisa web service on the pdb file.

    Parameters
    ----------
    driver : selenium webdriver
        given by the function PisaAuto_id.start()
    pdb_file : string
        corresponding to the pdb given by the user

    Returns
    -------
    selenium webdriver
    """
    print("2- Uploading "+pdb_file+" :")

    spinner = Halo(text='Uploading pdb file', spinner='dots')
    spinner.start()

    driver.find_elements_by_name('radio_source')[1].click()

    time.sleep(6)

    driver.find_element_by_name("file_upload").send_keys(os.getcwd()+"/"+pdb_file)

    time.sleep(5)

    driver.find_element_by_name("btn_upload").click()

    while(not check_exists_by_name('btn_submit_interfaces', driver)):
        pass

    driver.find_element_by_name("btn_submit_interfaces").click()

    spinner.stop()

    print("Done")

    print("3- Running PISA on "+pdb_file+" :")

    spinner = Halo(text='Running Pisa', spinner='dots')
    spinner.start()

    time.sleep(4)

    if driver.find_element_by_class_name("phead").text.startswith("No"):

        spinner.stop()
        
        print('No Contacts found')

        return driver, False

    else:
        while(not check_exists_by_name('downloadXML', driver)):
            pass

        time.sleep(4)

        spinner.stop()

        return driver, True


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_path", help="the path of the pdb files directory", type=str)

    ARGS = PARSER.parse_args()

    PDB_PATH = ARGS.pdb_path

    PDB_FILES = sorted([PDB_PATH+f for f in listdir(PDB_PATH) 
        if ((isfile(PDB_PATH+f)) and 
            (f.split(".")[-1] == "pdb"))], key=str.lower)

    for i, file in enumerate(PDB_FILES):
        print("## pdb file "+str(i+1)+"/"+str(len(PDB_FILES)))
        driver = pisa.start()
        driver, boo = launch_pdb_file(driver, file)
        if boo:
            pisa.download_xmls(driver, file.split('/')[-1])
        driver.quit()
