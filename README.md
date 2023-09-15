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

## How to use

_[`Sudoc_SRU_tests.py`](./Sudoc_SRU_tests.py) shows some code examples, [test_results/Sudoc_SRU.txt](./test_results/Sudoc_SRU.txt) shows the terminal after executing the file._
_[`samples/Sudoc_SRU`](./samples/Sudoc_SRU/) contains XML files showing how returned data looks like._

### Instantiate the main class (`SRU_Sudoc`)

Start by importing the files classes and instantiating a `SRU_Sudoc` :

``` Python
import Sudoc_SRU as ssru

sru = ssru.Sudoc_SRU()
```

This will define constants for requests (the `endpoint` and `version` (only the `1.1` is implemented)) and give you acces to the 5 functions of the class :

* [`explain()`](#request-an-explain)
* [`search_retrieve()`](#request-a-search-retrieve)
* [`explain()`]
* [`generate_query()`]
* [`generate_scan_clause()`]

### Request an explain

Explain requests do not take any arguments and return a `SRU_Result_Explain` instance.

``` Python
res = sru.explain()
```

`SRU_Result_Explain` instances properties :

* `operation` _string_ : supposedly always `explain`
* `status` _string_ : if the request was a success or not, see _Enum_ `Status` for possible values. The same value can be obtained calling the `get_status()` method.
* `error` _string_ or _None_ : if an error occurred, else, `None`. See the _Enum_ `Errors` for possible values. The same value can be obtained calling the `get_error_msg()` method.
* `url` _string_ : the request URL

Properties that do not get set on error :

* `result_as_string` _string_ : the decoded content of the response to the GET request
* `result` _xml.etree.ElementTree.ElementTree instance_, the response parsed. The same value can be obtained calling the `get_result()` method.
* `grouping_indexes` *list of SRU_Index_From_Explain instances* : the list of grouping indexes returned by the request. The same value can be obtained calling the `get_grouping_indexes()` method.
  * `SRU_Index_From_Explain.title` : the index title (`index/title`)
  * `SRU_Index_From_Explain.index_set` : the index index set (`index/map/name[@indexSet]`)
  * `SRU_Index_From_Explain.key` : the index name (`index/map/name`)
  * `SRU_Index_From_Explain.as_string` : the index information as a string : `{index_set}.{key} : {title}`. The same value can be obtained calling the `to_string()` method.
* `indexes` *list of SRU_Index_From_Explain instances* : the list of indexes returned by the request. The same value can be obtained calling the `get_indexes()` method.
  * _See `SRU_Result_Explain.grouping_indexes` for more information on the `SRU_Index_From_Explain` class_
* `record_schemas` *list of SRU_Record_Schema_From_Explain instances* : the list of record schemas returned by the request. The same value can be obtained calling the `get_record_schemas()` method.
  * `SRU_Record_Schema_From_Explain.title` : the record schema title (`schema/title`)
  * `SRU_Record_Schema_From_Explain.uri` : the record schema URI (`schema[@uri]`)
  * `SRU_Record_Schema_From_Explain.sort` : the record schema sort attribute (`schema[@sort]`)
  * `SRU_Record_Schema_From_Explain.retrieve` : the record schema retrieve attribute (`schema[@retrieve]`)
  * `SRU_Record_Schema_From_Explain.key` : the record schema name (`schema[@name]`)
  * `SRU_Record_Schema_From_Explain.as_string` : the record schema information as a string : `{title} ({key}) : sort={sort}, retrieve={retrieve}, uri={uri}`. The same value can be obtained calling the `to_string()` method.
* `sort_keys` *list of SRU_Sort_Key_From_Explain instances* : the list of sort keys returned by the request. The same value can be obtained calling the `get_sort_keys()` method.
  * `SRU_Sort_Key_From_Explain.title` : the sort key title (`sortkey/title`)
  * `SRU_Sort_Key_From_Explain.uri` : the sort key uri (`sortkey[@uri]`)
  * `SRU_Sort_Key_From_Explain.sort` : the sort key sort attribute (`sortkey[@sort]`)
  * `SRU_Sort_Key_From_Explain.retrieve` : the sort key retrieve attribute (`sortkey[@retrieve]`)
  * `SRU_Sort_Key_From_Explain.key` : the sort key name (`sortkey[@name]`)
  * `SRU_Sort_Key_From_Explain.as_string` : the sort key information as a string : `{title} ({key}) : sort={sort}, retrieve={retrieve}, uri={uri}`. The same value can be obtained calling the `to_string()` method.

### Request a search retrieve

Search retrieve requests take a mandatory argument and 4 optional arguments :

* `query` _mandatory, string_ : the query. The `SRU_Sudoc.sru_request()` handles the encoding, so it is not necessary to encode it beforehand (`APU` filters with `-` __will__ crash the program)
* `record_schema` _optional, SRU_Record_Schema or string_ : the record schema wanted. A string can be use if the value is correct (ex: `unimarc`). If the provided argument is not in the value list of _Enum_ `SRU_Record_Schema`, will be defaulted to `unimarc`

``` Python
# Simple
res = sru.search_retrieve("mti=renard")

# More complex
res = sru.search_retrieve(sru.generate_query([
        ssru.Part_Of_Query(ssru.SRU_Indexes.AUT, ssru.SRU_Relations.EQUALS, "renard alice"),
        ssru.Part_Of_Query(ssru.SRU_Indexes.NOTE_DE_THESE, ssru.SRU_Relations.EQUALS, "bordeaux 20*")]),
        record_schema="isni-b",
        record_packing="xml")

# With every parameters
res = sru.search_retrieve(sru.generate_query([
        "(",
        ssru.Part_Of_Query(ssru.SRU_Indexes.MTI, ssru.SRU_Relations.EQUALS, "renard"),
        ssru.Part_Of_Query(ssru.SRU_Indexes.MTI, ssru.SRU_Relations.EQUALS, "poisson", bool_operator=ssru.SRU_Boolean_Operators.OR),
        ")",
        " and APU > 2020"]),
        record_schema=ssru.SRU_Record_Schemas.PICA_XML,
        record_packing=ssru.SRU_Record_Packings.STRING,
        maximum_records="23",
        start_record=None)
```


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