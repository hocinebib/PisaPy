# PisaPy
Python code to automatically interact with PDBePISA (Proteins, Interfaces, Structures and Assemblies) web server.

---

## Description :
Allows to automatically run [PISA](https://www.ebi.ac.uk/pdbe/pisa/) interfaces web server and downloading the generated xml files by giving pdb files or a pdb id.

## Requirements :

### System :
* Linux : 
The code has only been tested on Linux.

### Browser :
The code has only been tested with firefox.

### Python packages :
In order to be able to run this code of course you need to have python3 but also some python packages :
* `selenium`
* `halo`
* `argparse`
* `pandas`

PyPi installation :
```shell
$pip install selenium
$pip install halo
$pip install argparse
$pip install pandas
```

Conda installation :
```shell
$conda create -n pisapy python
$source activate pisapy
$conda install -c conda-forge selenium
$conda install -c conda-forge halo
$conda install -c conda-forge argparse
$conda install pandas
```
### Others :
selenium requires [geckodriver](https://github.com/mozilla/geckodriver/releases) for firefox, check this [link](https://selenium-python.readthedocs.io/installation.html#drivers) for the other browsers.

### Script files :

`PisaAuto_id.py`
`PisaAuto_file.py`
`Pisa_xml_parser.py`

## Usage :
1. First clone this repository :
```shell
$git clone https://github.com/hocinebib/PisaPy.git
```
or download it.

### Exemple of usage :
With pdb id :
```shell
$python src/PisaAuto_id.py 6ta5
```

with pdb files :
```shell
$python3 src/PisaAuto_file.py pdb_folder/
```



