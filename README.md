# PisaPy
## Python PDBePISA Wrapper
Python code to automatically interact with PDBePISA (Proteins, Interfaces, Structures and Assemblies) web server.

---

## Description :
Allows to automatically run [PISA](https://www.ebi.ac.uk/pdbe/pisa/) interfaces web server and downloading the generated xml files by giving pdb files or a pdb id.

## Requirements :

### System :
* Linux : 
The code has only been tested on Ubuntu.

### Browser :
The code has only been tested with firefox.

### Python packages :
In order to be able to run this code of course you need to have python3 but also some python packages :
* `selenium`
* `halo`
* `argparse`
* `pandas`
* `networkx`
* `matplotlib`

PyPi installation :
```shell
$pip install selenium
$pip install halo
$pip install argparse
$pip install pandas
$pip install networkx
$pip install matplotlib
```

Conda installation :
```bash
$conda create -n pisapy python
$source activate pisapy
$conda install -c conda-forge selenium
$conda install -c conda-forge halo
$conda install -c conda-forge argparse
$conda install pandas
$conda install -c anaconda networkx
$conda install -c conda-forge matplotlib
```
### Others :
selenium requires [geckodriver](https://github.com/mozilla/geckodriver/releases) for firefox, check this [link](https://selenium-python.readthedocs.io/installation.html#drivers) for the other browsers.

### Script files :

`RunPisaPy.py`
`PisaAuto_id.py`
`PisaAuto_file.py`
`Pisa_xml_parser.py`
`Parse_Interfacetable.py`

## Usage :
1. First clone this repository :
```shell
$git clone https://github.com/hocinebib/PisaPy.git
```
or download it.

### Exemple of usage :
With 1 pdb id :
```shell
$cd PisaPy/
$python src/RunPisaPy.py 6ta5
```

With many pdb ids :
```shell
$cd PisaPy/
$python src/RunPisaPy.py "6ta5 6iol 6iok"
```

with pdb files :
```shell
$python3 src/RunPisaPy.py pdb_folder/ --d 1
```




