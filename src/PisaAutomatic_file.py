"""
small code to automaticaly use pisa web server on pdb files

how to use :

first you need to have the python packages selenium and argparse and the
PisaAutomatic_id.py script, you also need the pdb files on witch you want 
to run pisa

then you run the script with the following command :

    python PisaAutomatic_id.py path_to_pdb_files_folder/


note that right now it's made for firefox browser but adding other browsers 
isn't hard to implement
also note that I only download interfacetable.xml and each hydrogenbond.xml 
and saltbridge.xml files but if other xml files are needed adding it isn't 
hard

Hocine
"""

import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.common.exceptions import NoSuchElementException
import PisaAutomatic_id as pisa
from os import listdir
from os.path import isfile

def check_exists_by_name(name, driver):
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True

def launch_pdb_file(driver, pdb_file):
    """
    the function to run pisa web service on the pdb file
    """
    driver.find_elements_by_name('radio_source')[1].click()

    time.sleep(6)

    driver.find_element_by_name("file_upload").send_keys(os.getcwd()+"/"+pdb_file)

    time.sleep(5)

    driver.find_element_by_name("btn_upload").click()

    time.sleep(10)

    driver.find_element_by_name("btn_submit_interfaces").click()

    time.sleep(20)

    while(not check_exists_by_name('downloadXML', driver)):
        pass

    time.sleep(4)

    return driver


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_path", help="the path of the pdb files directory", type=str)

    ARGS = PARSER.parse_args()

    PDB_PATH = ARGS.pdb_path

    PDB_FILES = sorted([PDB_PATH+f for f in listdir(PDB_PATH) 
        if ((isfile(PDB_PATH+f)) and 
            (f.split(".")[-1] == "pdb"))], key=str.lower)

    for file in PDB_FILES:
        driver = pisa.start()
        pisa.download_xmls(launch_pdb_file(driver, file), file.split('/')[-1])
        driver.quit()
