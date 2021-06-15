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
* `Biopython`

PyPi installation :
```shell
$pip install selenium
$pip install halo
$pip install argparse
$pip install pandas
$pip install networkx
$pip install matplotlib
$pip install biopython
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
$conda install -c conda-forge biopython
```
### Others :
selenium requires [geckodriver](https://github.com/mozilla/geckodriver/releases) for firefox, check this [link](https://selenium-python.readthedocs.io/installation.html#drivers) for the other browsers.
[Naccess](http://www.bioinf.manchester.ac.uk/naccess/nacwelcome.html) is also needed if you want to get the accessibility (note that this part is not required as the accessibility files given by pisa are also being downloaded)

### Script files :

`RunPisaPy.py`
`PisaAuto_id.py`
`PisaAuto_file.py`
`Pisa_xml_parser.py`
`Parse_Interfacetable.py`
`Auto_Naccess.py`
`Download_pdbfasta.py`

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
$python src/PisaAuto_id.py 6ta5
```

with pdb files :
```shell
$python3 src/PisaAuto_file.py pdb_folder/
```

### Exemple of pipeline usage :
With 1 pdb id :
```shell
$cd PisaPy/
$python src/RunPisaPy.py 6ta5 naccess_bin_path
```

With many pdb ids :
```shell
$cd PisaPy/
$python src/RunPisaPy.py "6ta5 6iol 6iok" naccess_bin_path
```

with pdb files :
```shell
$python3 src/RunPisaPy.py pdb_folder/ --d 1 naccess_bin_path
```




