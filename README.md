# Abes_Apis_Interface 

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

Interfaces d'appel et de traitement des réponses des APIS du SUDOC

# [AbesXml](./AbesXml.py)

Permet de travailler avec l'api du SUDOC qui retourne une notice en XML. Prend un PPN en paramètre

## Get_etat_col

Pour un RCR donné retourne la liste des Etats de collection formatés (955$$r du SUDOC)

# [Bacon_id2Kabart](./Bacon_Id2Kabart.py)

A set of function wich handle data returned by service ['Bacon in json'](http://documentation.abes.fr/aidebacon/index.html#WebserviceId2)
On init take a bib identifier in argument (ISBN or ISSN)

# [Abes_isbn2ppn](./Abes_isbn2ppn.py)

Interroge le service de transformation d'un ISBN en PPN de l'Abes.
Attention, une validation de l'ISBN est exécutée avant d'appeler de webservice.

# [Sudoc_SRU](./Sudoc_SRU.py)

_En cours de codage [septembre 2023]_

A set of function to request [Sudoc's SRU service](https://abes.fr/reseau-sudoc/reutiliser-les-donnees-sudoc/service-sru/) ([documentation](https://abes.fr/wp-content/uploads/2023/05/guide-utilisation-service-sru-catalogue-sudoc.pdf)).
All 3 operations are handled (`explain`, `searchRetrieve` and `scan`).
See [doc/SRU_Sudoc.md](./doc/Sudoc_SRU.md) for the documentation.

_[`Sudoc_SRU_tests.py`](./Sudoc_SRU_tests.py) shows some code examples, [test_results/Sudoc_SRU.txt](./test_results/Sudoc_SRU.txt) shows the terminal after executing the file._
_[`samples/Sudoc_SRU`](./samples/Sudoc_SRU/) contains XML files showing how returned data looks like._