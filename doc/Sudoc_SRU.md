# Sudoc_SRU documentation

_[`Sudoc_SRU_tests.py`](../Sudoc_SRU_tests.py) shows some code examples, [`test_results/Sudoc_SRU.txt`](../test_results/Sudoc_SRU.txt) shows the terminal after executing the file._
_[`samples/Sudoc_SRU`](../samples/Sudoc_SRU/) contains XML files showing how returned data looks like._

This documentation is organized as a _How to use_ :

1. Instantiate the main class
2. Send a request
3. Additional information to help sending the request / using the response

## Instantiate the main class (`Sudoc_SRU`)

Start by importing the file classes and instantiating a `Sudoc_SRU` :

``` Python
import Sudoc_SRU as ssru

sru = ssru.Sudoc_SRU()
```

This will define constants for requests (the `endpoint` and `version` (only the `1.1` is implemented)) and give you acces to the 5 functions of the class :

* [`explain()`](#request-an-explain-sudoc_sruexplain)
* [`search()`](#request-a-search-retrieve-sudoc_srusearch)
* [`scan()`](#request-a-scan-sudoc_sruscan)
* [`generate_query()`](#generate-a-query-sudoc_srugenerate_query)
* [`generate_scan_clause()`](#generate-a-scan-clause-sudoc_srugenerate_scan_clause)

## Request an explain (`Sudoc_SRU.explain()`)

Explain requests do not take any arguments and return a [`SRU_Result_Explain` instance](#sru_result_explain-instances-properties).

``` Python
res = sru.explain()
```

### `SRU_Result_Explain` instances properties

* `operation` _string_ : supposedly always `explain`
* `status` _string_ : if the request was a success or not, see _Enum_ `Status` for possible values. The same value can be obtained calling the `get_status()` method
* `error` _string_ or _None_ : `None` if no error occurred, else, see the _Enum_ `Errors` for possible values. The same value can be obtained calling the `get_error_msg()` method
* `url` _string_ : the requested URL

Properties that do not get set on error :

* `result_as_string` _string_ : the decoded content of the response to the request
* `result` _xml.etree.ElementTree.ElementTree instance_ : the response parsed. The same value can be obtained calling the `get_result()` method
* `grouping_indexes` *list of [SRU_Index_From_Explain](#sru_index_from_explain-instances-properties) instances* : the list of grouping indexes returned by the request. The same value can be obtained calling the `get_grouping_indexes()` method
* `indexes` *list of [SRU_Index_From_Explain](#sru_index_from_explain-instances-properties) instances* : the list of indexes returned by the request. The same value can be obtained calling the `get_indexes()` method
* `record_schemas` *list of [SRU_Record_Schema_From_Explain](#sru_record_schema_from_explain-instances-properties) instances* : the list of record schemas returned by the request. The same value can be obtained calling the `get_record_schemas()` method
* `sort_keys` *list of [SRU_Sort_Key_From_Explain](#sru_sort_key_from_explain-instances-properties) instances* : the list of sort keys returned by the request. The same value can be obtained calling the `get_sort_keys()` method

### `SRU_Index_From_Explain` instances properties

* `title` : the index title (`index/title`)
* `index_set` : the index index set (`index/map/name[@indexSet]`)
* `key` : the index name (`index/map/name`)
* `as_string` : the index information as a string : `{index_set}.{key} : {title}`. The same value can be obtained calling the `to_string()` method

### `SRU_Record_Schema_From_Explain` instances properties

* `title` : the record schema title (`schema/title`)
* `uri` : the record schema URI (`schema[@uri]`)
* `sort` : the record schema sort attribute (`schema[@sort]`)
* `retrieve` : the record schema retrieve attribute (`schema[@retrieve]`)
* `key` : the record schema name (`schema[@name]`)
* `as_string` : the record schema information as a string : `{title} ({key}) : sort={sort}, retrieve={retrieve}, uri={uri}`. The same value can be obtained calling the `to_string()` method

### `SRU_Sort_Key_From_Explain` instances properties

* `title` : the sort key title (`sortkey/title`)
* `uri` : the sort key uri (`sortkey[@uri]`)
* `sort` : the sort key sort attribute (`sortkey[@sort]`)
* `retrieve` : the sort key retrieve attribute (`sortkey[@retrieve]`)
* `key` : the sort key name (`sortkey[@name]`)
* `as_string` : the sort key information as a string : `{title} ({key}) : sort={sort}, retrieve={retrieve}, uri={uri}`. The same value can be obtained calling the `to_string()` method

## Request a search retrieve (`Sudoc_SRU.search()`)

Search retrieve requests take [a mandatory argument and 4 optional arguments](#sudoc_srusearch-parameters) and return a [`SRU_Result_Search` instance](#sru_result_search-instances-properties).

``` Python
# Simple
res = sru.search("mti=renard")

# More complex
res = sru.search(sru.generate_query([
        ssru.Part_Of_Query(ssru.SRU_Indexes.AUT, ssru.SRU_Relations.EQUALS, "renard alice"),
        ssru.Part_Of_Query(ssru.SRU_Indexes.NOTE_DE_THESE, ssru.SRU_Relations.EQUALS, "bordeaux 20*")]),
        record_schema="isni-b",
        record_packing="xml")

# With every parameters
res = sru.search(sru.generate_query([
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

### `Sudoc_SRU.search()` parameters

* `query` _mandatory, string_ : the query. The `Sudoc_SRU.sru_request()` handles the encoding, so it is not necessary to encode it beforehand
* `record_schema` *optional, SRU_Record_Schema or string* : the record schema wanted
  * A string can be use if the value is correct (ex: `unimarc`)
  * Defaults to `unimarc`, any value not in the value list of _Enum_ `SRU_Record_Schema` will be replaced by this value
  * While there are multiple options, the official documentation states that only `unimarc` can be used (and most record schemas do not work properly)
* `record_packing` *optional, SRU_Record_Packing or string* : the record packing wanted
  * A string can be used if the value is correct (ex : `xml`)
  * Defaults to `xml`, any value not in the value list of _Enum_ `SRU_Record_Packing` will be replaced by this value
* `maximum_records` _optional, integer_ : the number of returned records for this page
  * Value must be between `1` and `1000` : any value lower than `1` will be readjusted to `10`, any value greater than `1000` will be readjusted to `1000`
  * Defaults to `100`, any non integer value will be replaced by this value (except if the value can be converted  through `int(value)`)
* `start_record` _optional, integer_ : the position of the first result of returned records in the query result list
  * Value must be greater than `0` : any value lower than `1` will be readjusted to `1`
  * Defaults to `1`, any non integer value will be replaced by this value (except if the value can be converted  through `int(value)`)

### `SRU_Result_Search` instances properties

* `operation` _string_ : supposedly always `searchRetrieve`
* `status` _string_ : if the request was a success or not, see _Enum_ `Status` for possible values. The same value can be obtained calling the `get_status()` method
* `error` _string_ or _None_ : `None` if no error occurred, else, see the _Enum_ `Errors` for possible values. The same value can be obtained calling the `get_error_msg()` method
* `url` _string_ : the requested URL

Properties that do not get set on error :

* `result_as_string` _string_ : the decoded content of the response to the request
* `result_as_parsed_xml` _xml.etree.ElementTree.ElementTree instance_ : the response parsed
  * All record schemas can't be natively parsed, so [some fixes are used to parse them](#fix-unparsable-record-schemas-as-of-14092023)
* `result` _xml.etree.ElementTree.ElementTree instance or string_ : `result_as_parsed_xml` or `result_as_parsed_xml` depending on the chosen record packing. The same value can be obtained calling the `get_result()` method
  * Could be equal to `Invalid recordPacking` if the record packing is not in the value of _Enum_ `SRU_Record_Packings`, but this should not happen if this instance is returned by the `Sudoc_SRU.search()` method
* `record_schema` _string_ : the record schema used in the request
* `record_packing` _string_ : the record packing used in the request
* `maximum_records` _integer_ : the maximum records par page used in the request
* `start_record` _integer_ : the start record number used in the request
* `query` _string_ : the query used in the request (encoded)
* `nb_results` _integer_ : the number of results for the query (`srw:numberofRedcords`). The same value can be obtained calling the `get_nb_results()` method
* `records` _list of xml.etree.ElementTree.ElementTree instances or strings_ : all records of the request, the type depends on the chosen record packing. The same value can be obtained calling the `get_records()` method
* `records_id` _list of strings_ : all the unique identifier (PPN) of the records. Returns an empty list for record schemas _Dublin Core_ and _Pica short (fcv XML)_ as both do not have this information in the record. The same value can be obtained calling the `get_records_id()` method

## Request a scan (`Sudoc_SRU.scan()`)

Scan requests take [a mandatory argument and 2 optional arguments](#sudoc_sruscan-parameters) and return a [`SRU_Result_Scan` instance](#sru_result_scan-instances-properties).

``` Python
# Simple
res = sru.scan("mti=poisson")

# With every parameters
res = sru.scan(sru.generate_scan_clause(
            ssru.Part_Of_Query(ssru.SRU_Indexes.MTI,
            ssru.SRU_Relations.EQUALS, "renard")),
        maximum_terms=4,
        response_position="-1")
```

### `Sudoc_SRU.scan()` parameters

* `scan_clause` _mandatory, string_ : the query. The `Sudoc_SRU.sru_request()` handles the encoding, so it is not necessary to encode it beforehand
* `maximum_terms` _optional, integer_ : the number of returned terms
  * Value must be between `1` and `1000` : any value lower than `1` will be readjusted to `10`, any value greater than `1000` will be readjusted to `1000`
  * Defaults to `25`, any non integer value will be replaced by this value (except if the value can be converted  through `int(value)`)
* `response_position` _optional, integer_ : the position of the scan terme in the list of returned terms
  * Value must be greater than `0` and inferior to `maximum_terms` : any value lower than `1` will be readjusted to `1`, any value greater than `maximum_terms` will be readjusted to be equal to `maximum_terms`
  * Defaults to `1`, any non integer value will be replaced by this value (except if the value can be converted  through `int(value)`)

### `SRU_Result_Scan` instances properties

* `operation` _string_ : supposedly always `scan`
* `status` _string_ : if the request was a success or not, see _Enum_ `Status` for possible values. The same value can be obtained calling the `get_status()` method
* `error` _string_ or _None_ : `None` if no error occurred, else, see the _Enum_ `Errors` for possible values. The same value can be obtained calling the `get_error_msg()` method
* `url` _string_ : the requested URL

Properties that do not get set on error :

* `result_as_string` _string_ : the decoded content of the response to the request
* `result` _xml.etree.ElementTree.ElementTree instance_ : the response parsed. The same value can be obtained calling the `get_result()` method
* `maximum_terms` _integer_ : the maximum terms parameter used in the request
* `response_position` _integer_ : the response position used in the request
* `scan_clause` _string_ : the scan clause used in the request (encoded)
* `terms` *list of [SRU_Scanned_Term](#sru_scanned_term-instances-properties) instances* : the list of terms returned by the request. The same value can be obtained calling the `get_terms()` method

### `SRU_Scanned_Term` instances properties

* `term` : the term (`srw:term/srw:displayTerm`)
* `value` : the term value (`srw:term/srw:value`)
* `nb_records` : the number of records found for this term (`srw:term/srw:numberOfRecords`)
* `extra_term_data` : the extra term data for the term (`srw:term/srw:extraTermData`)
* `as_string` : the term information as a string : `{term} : {nb_records}, value={value}, extra term data={extra_term_data}`. The same value can be obtained calling the `to_string()` method

## Generate a query (`Sudoc_SRU.generate_query()`)

Takes [a mandatory argument](#sudoc_srugenerate_query-parameter) and returns a string.

``` Python
# Simple
query = sru.generate_scan_clause(
        ssru.Part_Of_Query(
            ssru.SRU_Indexes.MTI,
            ssru.SRU_Relations.EQUALS,
            "renard"))

# Combine two elements
query = sru.generate_query([
        ssru.Part_Of_Query(
            ssru.SRU_Indexes.AUT,
            ssru.SRU_Relations.EQUALS,
            "renard alice"),
        ssru.Part_Of_Query(
            ssru.SRU_Indexes.NOTE_DE_THESE,
            ssru.SRU_Relations.EQUALS,
            "bordeaux 20*")])

# Combines Part_Of_Query and strings
query = sru.generate_query([
        "(",
        ssru.Part_Of_Query(
            ssru.SRU_Indexes.MTI,
            ssru.SRU_Relations.EQUALS,
            "renard"),
        ssru.Part_Of_Query(
            ssru.SRU_Indexes.MTI,
            ssru.SRU_Relations.EQUALS,
            "poisson",
            bool_operator=ssru.SRU_Boolean_Operators.OR),
        ")",
        " and APU > 2020"])
```

### `Sudoc_SRU.generate_query()` parameter

* `list` *mandatory, list of [Part_Of_Query instances](#part_of_query-class) or strings* : the different parts of the query. The `Sudoc_SRU.sru_request()` handles the encoding, so it is not necessary to encode it beforehand (encoding `-` in the publication date filter (`APU`) __will__ crash the execution)

## Generate a scan clause (`Sudoc_SRU.generate_scan_clause()`)

Takes [a mandatory argument](#sudoc_srugenerate_scan_clause-parameter) and returns a string.
Only useful if the scan clause is to be created from a [Part_Of_Query instance](#part_of_query-class).

``` Python
scan_clause= sru.generate_scan_clause(
        ssru.Part_Of_Query(
          ssru.SRU_Indexes.MTI,
          ssru.SRU_Relations.EQUALS,
          "renard"))
```

### `Sudoc_SRU.generate_scan_clause()` parameter

* `clause` *mandatory, [Part_Of_Query instance](#part_of_query-class)* : the [Part_Of_Query instance](#part_of_query-class) to transform to string

## `Part_Of_Query` class

`Part_Of_Query` is a class that represents a part of a query, storing each information individually.
On initialization, take [3 mandatory arguments and an optional argument](#part_of_query-initialization-parameters).
__Every parameter has to be provided as the right data type__.

``` Python
# Without specifying the operator
part_one = ssru.Part_Of_Query(
        ssru.SRU_Indexes.MTI,
        ssru.SRU_Relations.EQUALS,
        "renard"))

# Specifying the operator
part_two = ssru.Part_Of_Query(
        ssru.SRU_Indexes.NOTE_DE_THESE,
        ssru.SRU_Relations.EQUALS,
        "bordeaux 20*",
        bool_operator=ssru.SRU_Boolean_Operators.OR))
```

### `Part_Of_Query` initialization parameters

* `index` *mandatory, SRU_Indexes or SRU_Filters* : the index to use
  * If the provided value is not of *SRU_Indexes* or *SRU_Filters* type, the property `invalid` will be set to `True`
  * If the provided value is of *SRU_Filters* type, the property `is_filter` will be set to `True` and some checks will be run to control the validity of this part of the query :
    * _If the check fails, sets the `invalid` property to `True`_
    * For document type (`TDO`), language (not rare) (`LAN`) and country (not rare) (`PAY`), checks if the value is in the _Enums_ *SRU_Filter_TDO*, *SRU_Filter_LAN* or *SRU_Filter_PAY*
    * For rare languages (`LAI`), checks if the value is a 3 letters word (`^[a-zA-Z]{3}$`)
    * For rare countries (`PAI`), checks if the value is a 2 letters word (`^[a-zA-Z]{2}$`)
    * For publication date (`APU`), checks if the value can be converted to an integer and if the chosen relation is equal, strictly superior / inferior ou superior / inferior or equal to (this check is the reason why the value should not be encoded if it has a `-`)
* `relation` *mandatory, SRU_Relations* : the relation to use
  * If the provided relation is not of *SRU_Relations* type, the property `invalid` will be set to `True`
* `value` *mandatory, string or integer or SRU_Filter_TDO, SRU_Filter_LAN or SRU_Filter_PAY* : the value to search in the index
* `bool_operator` *optional, SRU_Boolean_Operators* : the boolean operator to use
  * If the provided operator is not of *SRU_Boolean_Operators* type, the property `invalid` will be set to `True`
  * Defaults to `and`

### `Part_Of_Query` instances properties

* `bool_operator` *SRU_Boolean_Operators* : the boolean operator provided on initilization
* `index` *SRU_Indexes or SRU_Filters* : the index provided on initilization
* `relation` *SRU_Relations* : the relation provided on initilization
* `value` *string or integer or SRU_Filter_TDO, SRU_Filter_LAN or SRU_Filter_PAY* : the value provided on initilization
* `invalid` *boolean* : is this instance invalid
* `is_filter` *boolean* : is the provided index a filter
* `filter_value_is_manual` *boolean* : is the value a document type, language (not rare) or country (not rare) filter but the value is not an _Enum_ `SRU_Filter_TDO`, `SRU_Filter_LAN` or `SRU_Filter_PAY`
* `as_string_with_operator` _string_ : the query as a string, including the boolean operator (`{bool_operator.value}{index.value}{relation.value}{value}`). The same value can be obtained calling the `to_string(True)` method
* `as_string_without_operator` _string_ : the query as a string, excluding the boolean operator (`{index.value}{relation.value}{value}`). The same value can be obtained calling the `to_string(False)` method

## Fix unparsable record schemas (as of 14/09/2023)

Some record schemas can not be parsed by the ElementTree XML API [14/09/2023] :

* Pica XML
* Pica short (fcv XML)
* MARC21
* ISNI Basic
* ISNI Extended

### Pica XML

#### Error cause

* Some angle brackets are doubled
* Records are between `<srw:record><srw:recordData><record><ppxml:record>` but only the last one is closed

#### Fix

* Remove double angle brackets
  * Find `<\s*<+` substitute by `<`
  * Find `>\s*>+` substitute by `>`
* Then, add `</record></srw:recordData></srw:record>` between `</ppxml:record>` and (`<srw:record>` or `<srw:record>`)
  * Find `(?<=<\/ppxml:record>)\s*(?=(<srw:record>|<\/srw:records>))` substitute by `</record></srw:recordData></srw:record>`

### Pica short (fcv XML)

#### Error cause

* Records are between angle brackets but are just plain text
* Records are between `<srw:record><srw:recordData><record>` but none of them are closed

#### Fix

* Add `</record></srw:recordData></srw:record>` between `>` and (`<srw:record>` or `<srw:record>`)
  * Find `(?<!<srw:records)>\s*(?=(<srw:record>|<\/srw:records>))` substitute by `</record></srw:recordData></srw:record>`
* Then, remove the angle brackets in the record
  * Find `(?<=<record>)\s*<` substitute by nothing
  * Find `>\s*(?=<\/record>)` substitute by nothing

### MARC21

#### Error cause

* Content of some leaders have ill-formed `<TR>` and `<TD>`
* Records close too soon with `</record></srw:recordData><srw:recordPosition>leader</srw:recordPosition></srw:record>`

#### Fix

* Delete `R>` following `<leader>`
  * Find `(?<=<leader>)\s*R>` substitute by nothing
* Then, delete all `<TR>` and `<TD>`
  * Find `(<TD>|<TR>)` substitute by nothing
* Then, delete all useless `</record></srw:recordData><srw:recordPosition>leader</srw:recordPosition></srw:record>`
  * Find `(?<=<\/leader>)<\/record>\s*<\/srw:recordData>\s*<srw:recordPosition>\s*leader\s*<\/srw:recordPosition>\s*<\/srw:record>(?!\s*(<srw:record>|<\/srw:records>))` substitute by nothing

### ISNI Basic and ISNI Extended

#### Error cause

* Some angle brackets are doubled
* Records are between `<srw:record><srw:recordData><record>` but none of them are closed
* Content should look like `<TR><TD><a></a></TD></TR>` but looks like `<TR><TD><a></a><TR>`

#### Fix

* Remove double angle brackets
  * Find `<\s*<+` substitute by `<`
  * Find `>\s*>+` substitute by `>`
* Then, transform `</a><TR>` in `</a></TD></TR>`
  * Find `</a>\s*<TR>` substitute by `</a></TD></TR>`
* Then, add `</record></srw:recordData></srw:record>` between `</TR>` and (`<srw:record>` or `<srw:record>`)
  * Find `(?<=</TR>)\s*(?=(<srw:record>|<\/srw:records>))` substitute by `</record></srw:recordData></srw:record>`