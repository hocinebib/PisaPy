#!/usr/bin/python3
"""
Code to automatically run PDBePISA web server on the given pdb id and downloading the
generated xml files.

  How to use
  ----------
First you need to have the python packages selenium, halo and argparse installed.

Then you can run the script with the following command :

    python PisaAuto_id.py pdb_id

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
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from halo import Halo


def start():
    """
    The function to access to the pisa web server.
    I'm using firefox but it can be changed for other browsers.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    selenium webdriver
    """
    print("1- Accessing to PISA website :")

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.ebi.ac.uk/pdbe/pisa/")

    launch = driver.find_element_by_name("start_server")
    launch.click()

    print("Done")

    return driver


def launch_pdb_id(driver, pdb_id):
    """
    The function to run pisa web service on the pdb id.
    
    Parameters
    ----------
    driver : selenium webdriver
        given by the function start()
    pdb_id : string
        pdb id given by the user
    
    Returns
    -------
    selenium webdriver
    """
    print("2- Submitting "+pdb_id+" to PISA :")

    pdb_entry = driver.find_element_by_name("edt_pdbcode")
    pdb_entry.clear()
    pdb_entry.send_keys(pdb_id)

    time.sleep(10)

    print("Done")

    print("3- Running PISA on "+pdb_id+" :")

    spinner = Halo(text='Running PISA', spinner='dots')
    spinner.start()

    interface = driver.find_element_by_name("btn_submit_interfaces")
    interface.click()

    time.sleep(20)

    spinner.stop()

    return driver

def download_xmls(driver, pdb_id):
    """
    The function to download the xml files.

    Parameters
    ----------
    driver : selenium webdriver
    pdb_id : string
    
    Returns
    -------
    Nothing
    """
    print("Done")

    print("4- Downloading xml files :")

    spinner = Halo(text='Downloading interface table', spinner='dots')
    spinner.start()

    driver.find_element_by_name('downloadXML').click()

    time.sleep(10)

    driver.switch_to.window(driver.window_handles[1])
    xml = driver.current_url

    if not os.path.exists('xml_files'+pdb_id):
        os.makedirs('xml_files'+pdb_id)

    with open('xml_files'+pdb_id+'/'+xml.split('/')[-1], 'w') as f:
        f.write(driver.page_source)

    time.sleep(6)

    driver.close()

    time.sleep(6)

    driver.switch_to.window(driver.window_handles[0])

    inter_lst = []

    with open('xml_files'+pdb_id+'/'+xml.split('/')[-1], "r") as f_xml:
        for line in f_xml:
            if line.strip().startswith("<INTERFACENO>"):
                inter_lst.append(line[13:15].strip("<"))

    spinner.stop()

    for i in inter_lst:

        spinner = Halo(text="Downloading files "+i+"/"+str(len(inter_lst)), spinner='dots')
        spinner.start()

        driver.find_element_by_link_text(i).click()

        time.sleep(6)

        xmls = driver.find_elements_by_name('downloadXML')

        for i in range(2,len(xmls)):
            xmls[i].click()

            time.sleep(10)

            driver.switch_to.window(driver.window_handles[1])
            xml = driver.current_url

            with open('xml_files'+pdb_id+'/'+xml.split('/')[-1], 'w') as f:
                f.write(driver.page_source)

            time.sleep(6)

            driver.close()

            time.sleep(6)

            driver.switch_to.window(driver.window_handles[0])

        driver.back()

        time.sleep(5)

        spinner.stop()

    spinner.stop()

    print("Done")


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_id", help="the id of the pdb you want to run pisa on", type=str)

    ARGS = PARSER.parse_args()

    PDB_ID = ARGS.pdb_id

    download_xmls(launch_pdb_id(start(), PDB_ID), PDB_ID)

