# Abes_isbn2ppn documentation

_[`Abes_isbn2ppn_test.py`](../Abes_isbn2ppn_test.py) shows some code examples, [`test_results/Abes_isbn2ppn.txt`](../test_results/Abes_isbn2ppn.txt) shows the terminal after executing the file._

This documentation is organized as a _How to use_ :

1. Instantiate the main class
2. Send a request
3. Additional information to help sending the request / using the response

## Instantiate the main class (`Abes_isbn2ppn`)

Start by importing the file classes and instantiating a `Abes_isbn2ppn` :

``` Python
import Abes_isbn2ppn as isbn2ppn

i2p = isbn2ppn.Abes_isbn2ppn()
```

This will define constants for requests (the `endpoint` and `format` (you can chose between JSON and XML with the argument `useJson={boolean}`, defaults to `True`) and give you acces to the only function of this class : [`get_matching_ppn()`](#request-the-service-abes_isbn2ppnget_matching_ppn)

## Request the service (`Abes_isbn2ppn.get_matching_ppn()`)

Search retrieve requests take [a mandatory argument and an optional arguments](#abes_isbn2ppnget_matching_ppn-parameters) and return a [`Isbn2ppn_Result` instance](#isbn2ppn_result-instances-properties-and-methods).

``` Python
# Check ISBN validity
res = i2p.get_matching_ppn("LoveColoredMasterSpark")

# Do not check ISBN validity
res = i2p.get_matching_ppn("LoveColoredMasterSpark", check_isbn_validity=False)

# ISBN with 0 PPN match
res = i2p.get_matching_ppn(2212064004)

# Incorrect ISBN with 0 PPN match
res = i2p.get_matching_ppn("2.907380.77.X", check_isbn_validity=False)

# ISBN with 1 PPN match
res = i2p.get_matching_ppn("9782862764719")

# ISBN with multiple PPN match, all matches with holds
res = i2p.get_matching_ppn(2110860723)

# ISBN with multiple PPN match, some matches do not have holds
res = i2p.get_matching_ppn("2-07-037026-7")
```

### `Abes_isbn2ppn.get_matching_ppn()` parameters

* `isbn` _mandatory, string_ : the ISBN to query. A conversion to `string` is performed first, so `integer` technically also work
* `check_isbn_validity` _optional, boolean_ : validate the ISBN before the request or not.
  * Invalid ISBNs do not send requests
  * Defaults to `True`

### `Isbn2ppn_Result` instances properties and methods

Properties :

* `status` _string_ : the request status value, see _Enum_ `Isbn2ppn_Status` for possible values. The same value can be obtained calling the `get_status()` method
* `error` *Isbn2ppn_Errors entry* : `NO_ERROR` if no error occurred, else, see the _Enum_ `Errors` for possible values.
* `error_msg` _string_ : the `error` value. The same value can be obtained calling the `get_error_msg()` method
* `format` _string_ : the requested format, used in the `accept` key of the request headers
* `input_isbn` _string_ : the ISBN used in the `Abes_isbn2ppn.get_matching_ppn()` as a string
* `isbn` _string_ : the ISBN used in the request (modified by the ISBN validation if it was active). The same value can be obtained calling the `get_isbn_used()` method
* `isbn_validity` *Isbn_Validity entry* : the ISBN validity, see _Enum_ `Isbn_Validity` for possible values. Defaults to `SKIPPED`
* `url` _string_ : the requested URL, `None` if no request was sent
* `HTTP_status_code` _integer_ : the HTTP status code __if an HTTP error was raised__. Defaults to `0`
* `result` _string_ : the responsed decoded in `UTF-8` __as a string__, `None` if the request was not a success. The same value can be obtained calling the `get_result()` method

Methods :

* `get_result()` _string_ : return the `result` property
* `get_status()` _string_ : return the `status` property
* `get_error_msg()` _string_ : return the `error_msg` property
* `get_isbn_used()` _string_ : return the `isbn` property
* `get_nb_result()` _tupple of 3 integers_ : returns :
  * The total number of results
  * The number of results with holdings
  * The number of results without holdings
* `get_results()` _list(s) of string_ :
  * Takes as optional argument `merge` (defaults to `False`) to merge records with and without holdings in a single list and return it
  * Otherwise, returns a tupple with the list of records with holdings and the list of records without holdings

## Calling the ISBN validation function

`Abes_isbn2ppn` also have 3 functions related to ISBN that can be called on their own :

* `validate_isbn()` : takes as argument an ISBN as a string and returns a tupple :
  * An `Isbn_Validity` entry, can be `VALID`, `INVALID_ISBN` or `INVALID_CHECK_ISBN`
  * The input ISBN as a `string`
  * The ISBN without separators as a `string`, or an empty string if the ISBN validity was `INVALID_ISBN`
* `compute_isbn_10_check_digit()` : takes as argument the ISBN 10 as a `list` of `strings` and return the check digit as a `string`
* `compute_isbn_13_check_digit()` : takes as argument the ISBN 13 as a `list` of `strings` and return the check digit as a `string`
