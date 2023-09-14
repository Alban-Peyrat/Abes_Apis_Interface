# Abes_Apis_Interface 

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

Interfaces d'appel et de traitement des réponses des APIS du SUDOC

## [AbesXml](./AbesXml.py)

Permet de travailler avec l'api du SUDOC qui retourne une notice en XML. Prend un PPN en paramètre

### Get_etat_col

Pour un RCR donné retourne la liste des Etats de collection formatés (955$$r du SUDOC)

## [Bacon_id2Kabart](./Bacon_Id2Kabart.py)

A set of function wich handle data returned by service ['Bacon in json'](http://documentation.abes.fr/aidebacon/index.html#WebserviceId2)
On init take a bib identifier in argument (ISBN or ISSN)

## [Abes_isbn2ppn](./Abes_isbn2ppn.py)

Interroge le service de transformation d'un ISBN en PPN de l'Abes.
Attention, une validation de l'ISBN est exécutée avant d'appeler de webservice.

## [Sudoc_SRU](./Sudoc_SRU.py)

_En cours de codage [septembre 2023]_

Interroge le SRU du Sudoc

Pour les opérations `searchRetrieve` et `scan`, les valeurs de certains paramètres sont controlées et rectifiées si nécessaire :

  * `searchretrieve`
 

La requête est encodée au moment de l'appel de de `SRU_Sudoc.sru_request()`, donc pas besoin de l'encodée avant (surtout ne pas encodé le `-` d'un filtre `APU` avant).

### Known bugs

* Some record schemas can't be parsed by ET [14/09/2023] :
  * Pica XML
  * Pica short (fcv XML)
  * MARC21
  * ISNI Basic
  * ISNI Extended

### Fix

* For Pica XML :
  * Some angle brackets are doubled
  * Records are between `<srw:record><srw:recordData><record><ppxml:record>` but only the last one is closed.
  * So if we remove double angle brackets
  * Then, if we add `</record></srw:recordData></srw:record>`, between `</ppxml:record>` and (`<srw:record>` or `<srw:record>`)
  * It should work
  * Regex 1 : find "<\s*<+" subsitute "<"
  * Regex 1.5 : find ">\s*>+" subsitute ">"
  * Regex 2 : find `(?<=<\/ppxml:record>)\s*(?=(<srw:record>|<\/srw:records>))` subsitute `</record></srw:recordData></srw:record>`
* For Pica short (fcv XML) :
  * Records are bewteen angle brackets, but are just a text
  * Records are between `<srw:record><srw:recordData><record>`, but none of them are closed
  * So, if we add `</record></srw:recordData></srw:record>`, between `>` and `<srw:record>` or `<srw:record>`
  * Then remove the angle brackets in the record
  * It should work
  * Regex 1 : find `(?<!<srw:records)>\s*(?=(<srw:record>|<\/srw:records>))` substitute `</record></srw:recordData></srw:record>`
  * Regex 2.5 : find `(?<=<record>)\s*<` substitute nothing
  * Regex 2.5 : find `>\s*(?=<\/record>)` substitute nothing
* For MARC21 :
  * Content of some leaders have malformed `<TR>` and `<TD>`
  * Records close too soon with `</record></srw:recordData><srw:recordPosition>leader</srw:recordPosition></srw:record>`
  * So if we delete `R>` following `<leader>`
  * Then, we delete all `<TR>` and `<TD>`
  * Then, delete all useless `</record></srw:recordData><srw:recordPosition>leader</srw:recordPosition></srw:record>`
  * It should work
  * Regex 1 : find `(?<=<leader>)\s*R>` substitute nothing
  * Regex 2 : find `(<TD>|<TR>)` substitute nothing
  * Regex 3 : find `(?<=<\/leader>)<\/record>\s*<\/srw:recordData>\s*<srw:recordPosition>\s*leader\s*<\/srw:recordPosition>\s*<\/srw:record>(?!\s*(<srw:record>|<\/srw:records>))` substitue nothing
* For ISNI Basic and ISNI Extended :
  * Some angle brackets are doubled
  * Records are between `<srw:record><srw:recordData><record>` but, but none of them are closed
  * Content should look like `<TR><TD><a></a></TD></TR>` but looks like `<TR><TD><a></a><TR>`
  * So if we remove double angle brackets
  * Then, transform `</a><TR>` in `</a></TD></TR>`
  * Then, if we add `</record></srw:recordData></srw:record>`, between `</TR>` and (`<srw:record>` or `<srw:record>`)
  * It should work
  * Regex 1 : find "<\s*<+" subsitute "<"
  * Regex 1.5 : find ">\s*>+" subsitute ">"
  * Regex 2 : find `</a>\s*<TR>` subsitute `</a></TD></TR>`
  * Regex 3 : find `(?<=</TR>)\s*(?=(<srw:record>|<\/srw:records>))` subsitute `</record></srw:recordData></srw:record>`