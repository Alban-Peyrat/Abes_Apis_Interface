# -*- coding: utf-8 -*- 

# External imports
from enum import Enum
import logging
import requests
import urllib.parse
import xml.etree.ElementTree as ET
import re

# Doc : https://abes.fr/wp-content/uploads/2023/05/guide-utilisation-service-sru-catalogue-sudoc.pdf
# SRU V1.1 is used
# #AR360 pour la liste des modifs à faire

# --------------- Enums ---------------

XML_NS = {
    "srw":"http://www.loc.gov/zing/srw/"
}

class SRU_Operations(Enum):
    SCAN = "scan"
    EXPLAIN ="explain"
    SEARCH = "searchRetrieve"

class SRU_Record_Packing(Enum):
    XML = "xml"
    STRING = "string"

class Status(Enum):
    ERROR = "Error"
    SUCCESS = "Success"

class Errors(Enum):
    HTTP_ERROR = "Service unavailable"
    GENERIC = "Generic exception, read logs for more information"

class SRU_Index(Enum):
    # Index on numbers
    NUMERO_DE_NOTICE_SUDOC = "ppn"
    PPN = "ppn"
    TOUS_NUMEROS = "num"
    NUM = "num"
    ISBN_LIVRES = "isb"
    ISB = "isb"
    ISSN_PERIODIQUES = "isn"
    ISN = "isn"
    NUMERO_NATIONAL_DE_THESE = "nnt"
    NNT = "nnt"
    NUMERO_SOURCE = "sou"
    SOU = "sou"
    NUMERO_DE_NOTICE_WORLDCAT = "ocn"
    OCN = "ocn"
    # Index on title
    MOTS_DU_TITRE = "mti"
    MTI = "mti"
    TITRE_COMPLET = "tco"
    TCO = "tco"
    TITRE_ABREGE_PERIODIQUES = "tab"
    TAB = "tab"
    COLLECTION = "col"
    COL = "col"
    # Index on authors
    MOTS_AUTEUR = "aut"
    AUT = "aut"
    NOM_PERSONNE = "per"
    PER = "per"
    ORGANISME_AUTEUR = "org"
    ORG = "org"
    # Index on subject
    MOTS_SUJETS = "msu"
    MSU = "msu"
    POINT_DACCES_SUJET = "vma"
    VMA = "vma"
    FORME_GENRE = "fgr"
    FGR = "fgr"
    MOTS_SUJETS_ANGLAIS = "msa"
    MSA = "msa"
    SUJET_MESH_ANGLAIS = "mee"
    MEE = "mee"
    # Index on note fields
    NOTE_DE_THESE = "nth"
    NTH = "nth"
    RESUME_SOMMAIRE = "res"
    RES = "res"
    NOTE_DE_LIVRE_ANCIEN = "lva"
    LVA = "lva"
    SOURCE_DU_FINANCEMENT_DE_LA_RESSOURCE = "fir"
    FIR = "fir"
    NOTE_DE_RECOMPENSE = "rec"
    REC = "rec"
    # Index on item fields
    NUMERO_RCR = "rbc"
    RBC = "rbc"
    PLAN_DE_CONSERVATION_PARTAGEE = "pcp"
    PCP = "pcp"
    RELIURE_PROVENANCE_CONSERVATION = "rpc"
    RPC = "rpc"
    BOUQUET_DE_RESSOURCES_EN_LIGNE = "bqt"
    BQT = "bqt"
    # Other index
    TOUS_LES_MOTS = "tou"
    TOU = "tou"
    EDITEUR = "edi"
    EDI = "edi"

class SRU_Filters(Enum):
    TYPE_DE_DOCUMENT = "tdo"
    TDO = "tdo"
    LANGUE_DE_LA_RESSOURCE = "lan"
    LAN = "lan"
    LANGUE_RARE_DE_LA_RESSOURCE = "lai"
    LAI = "lai"
    PAYS_DE_LENTITE_DECRITE = "pay"
    PAY = "pay"
    PAYS_RARE_DE_LENTITE_DECRITE = "pai"
    PAI = "pai"
    ANNEE_DE_PUBLICATION = "apu"
    APU = "apu"

class SRU_Filter_TDO(Enum):
    ARTICLES = "a"
    A = "a"
    MONOGRAPHIES_IMPRIMEES = "b"
    B = "b"
    MANUSCRITS = "f"
    F = "f"
    ENREGISTREMENTS_SONORES_MUSICAUX = "g"
    G = "g"
    IMAGES_FIXES = "i"
    I = "i"
    CARTES_IMPRIMEES_ET_MANUSCRITES = "k"
    K = "k"
    PARTITIONS_MANUSCRITES_ET_IMPRIMEES = "m"
    M = "m"
    ENREGISTREMENTS_SONORES_NON_MUSICAUX = "n"
    N = "n"
    MONOGRAPHIES_ELECTRONIQUES = "o"
    O = "o"
    PERIODIQUES_ET_COLLECTIONS_TOUS_TYPES_DE_SUPPORT = "t"
    T = "t"
    DOCUMENTS_AUDIOVISUELS = "v"
    V = "v"
    OBJETS_DOCUMENTS_MULTIMEDIAS_MULTISUPPORTS = "x"
    X = "x"
    THESE_VERSION_DE_SOUTENANCE_IMPRIMEES_ET_ELECTRONIQUES = "y"
    Y = "y"

class SRU_Filter_LAN(Enum):
    ALLEMAND = "ger"
    GER = "ger"
    ANGLAIS = "eng"
    ENG = "eng"
    ESPAGNOL = "spa"
    SPA = "spa"
    FRANCAIS = "fre"
    FRE = "fre"
    ITALIEN = "ita"
    ITA = "ita"
    LATIN = "lat"
    LAT = "lat"
    NEERLANDAIS = "dut"
    DUT = "dut"
    POLONAIS = "pol"
    POL = "pol"
    PORTUGAIS = "por"
    POR = "por"
    RUSSIE = "rus"
    RUS = "rus"

# Ye LAI is a pain, maybe one day

class SRU_Filter_PAY(Enum):
    ALLEMAGNE = "de"
    DE = "de"
    BELGIQUE = "be"
    BE = "be"
    CANDA = "ca"
    CA = "ca"
    ESPAGNE = "es"
    ES = "es"
    ETATS_UNIS = "us"
    US = "us"
    FRANCE = "fr"
    FR = "fr"
    ITALIE = "it"
    IT = "it"
    PAYS_BAS = "nl"
    NL = "nl"
    ROYAUME_UNI = "gb"
    GB = "gb"
    RUSSIE = "ru"
    RU = "ru"
    SUISSE = "ch"
    CH = "ch"

# Ye PAI is a pain, maybe one day

class SRU_Relation(Enum):
    EQUALS = "="
    EXACT = " exact "
    ANY = " any "
    ALL = " all "
    STRITCLY_INFERIOR = "<"
    STRITCLY_SUPERIOR = ">"
    INFERIOR_OR_EQUAL = "<="
    SUPERIOR_OR_EQUAL = ">="
    NOT = " not "

class SRU_Boolean_Operators(Enum):
    AND = " and "
    OR = " or "
    NOT = " not "

# --------------- Class Objects ---------------

# ---------- SRU ----------

class Sudoc_SRU(object):
    """Sudoc_SRU
    =======
    A set of function to query Sudoc's SRU
    On init take as arguments :
    - [optional] service {str} : Name of the service for the logs
"""
    def __init__(self, service="Sudoc_SRU"):
        # Const
        self.endpoint = "https://www.sudoc.abes.fr/cbs/sru/"
        self.version = "1.1" # no choice possible
        self.record_schema = "unimarc" # no choice possible
        # logs
        self.logger = logging.getLogger(service)
        self.service = service

    def sru_request(self, query: str, operation: SRU_Operations, record_packing=SRU_Record_Packing.XML, maximum_records=100, start_record=1):
        # query part
        query = urllib.parse.quote(query)
        if type(operation) == SRU_Operations:
            operation = operation.value
        # Checks if the operation is valid
        if operation not in [e.value for e in SRU_Operations]:
                return None
        if type(record_packing) == SRU_Record_Packing:
            record_packing = record_packing.value
        # Checks if the record packing is valid
        if record_packing not in [e.value for e in SRU_Record_Packing]:
                return None
        # Defines the URL
        url = f'{self.endpoint}?operation={operation}&version={self.version}'
        # For the Explain operation, nothing more is needed
        if operation == SRU_Operations.SEARCH.value:
            url += f'&recordSchema={self.record_schema}&recordPacking={record_packing}'\
                f'&startRecord={start_record}&maximumRecords={maximum_records}&query={query}'
        elif operation == SRU_Operations.SCAN.value:
            url += ""
        
        status = None
        error_msg = None
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            status = Status.ERROR
            error_msg = Errors.HTTP_ERROR
            self.logger.error(f"{query} :: Sudoc_SRU :: HTTP Status: {r.status_code} || Method: {r.request.method} || URL: {r.url} || Response: {r.text}")
        except requests.exceptions.RequestException as generic_error:
            status = Status.ERROR
            self.error_msg = Errors.GENERIC
            self.logger.error(f"{query} :: Sudoc_SRU :: Generic exception || URL: {url} || {generic_error}")
        else:
            status = Status.SUCCESS
            self.logger.debug(f"{query} :: Sudoc_SRU :: Success")
            result = r.content.decode('utf-8')
        
        if operation == SRU_Operations.EXPLAIN.value:
            return SRU_Explain_Result()
        elif operation == SRU_Operations.SEARCH.value:
            return SRU_Search_Result(status, error_msg, result,
                    operation, record_packing, maximum_records,
                    start_record, query, url)
        elif operation == SRU_Operations.SCAN.value:
            return 2
        else:
            return None
    
    def generate_query(self, list: list):
        """Ignore any list element that is not a string or Part_Of_Query.
        
        Can be use to add parenthesis."""
        output = ""
        for index, query_part in enumerate(list):
            if type(query_part) == str:
                output += query_part
            elif type(query_part) == Part_Of_Query:
                if not query_part.invalid:
                    output += query_part.to_string(bool(index))
        return output

# ---------- SRU Results ----------

class SRU_Explain_Result(object):
    a = 3
    # voir le résltats dans files/explain_response.xml, puis au sein de ze:explain
    # dans zr:metaInfo
    # dans indexInfo
    # dans schemaInfo
    # dans sortkeyInfo
    # dans configInfo

class SRU_Search_Result(object):
    def __init__(self, status: Status, error: Errors, result: str, operation: str, record_packing: str, maximum_records: int, start_record: int, query: str, url: str):
        self.operation = "searchRetrieve"
        self.status = status.value
        if error:
            self.error = error.value
        else:
            self.error = None
        self.result_as_string = result
        # Generate the result property
        if record_packing == SRU_Record_Packing.XML.value:
            self.result = ET.fromstring(result)
        elif record_packing == SRU_Record_Packing.STRING.value:
            self.result = self.result_as_string
        else:
            self.result = "Invalid recordPacking"
        # Original query parameters
        self.operation = operation
        self.record_packing = record_packing
        self.maximum_record = maximum_records
        self.start_record = start_record
        self.query = query
        self.url = url

    def get_result(self):
            """Return the result as a string or ET Element depending the chosen recordPacking"""
            return self.result

    def get_status(self):
        """Return the init status as a string."""
        return self.status

    def get_error_msg(self):
        """Return the error message."""
        return str(self.error)

    def get_nb_results(self):
        """Return the number of results as an int."""
        if self.result.findall("srw:numberOfRecords", XML_NS):
            return int(self.result.find("srw:numberOfRecords", XML_NS).text)
        else: # Prbly not encessary in this SRU
            return 0

    def get_records(self):
        """Returns all records as a list"""
        if self.record_packing == SRU_Record_Packing.XML.value:
            return self.result.findall(".//srw:record", XML_NS)
        elif self.record_packing == SRU_Record_Packing.STRING.value:
            output = []
            for record in ET.fromstring(self.result).findall(".//srw:record", XML_NS):
                output.append(ET.tostring(record))
            return output
        else:
            return []
    
    def get_records_id(self):
        """Returns all records as a list of strings"""
        records = self.get_records()
        output = []
        
        for record in records:
            if self.record_packing == SRU_Record_Packing.STRING.value:
                record = ET.fromstring(record)
            output.append(record.find(".//controlfield[@tag='001']").text)
        return output

class SRU_Scan_Result(object):
    a = 3

# ---------- SRU Query ----------

class Part_Of_Query(object):
    """Must provide the right data type"""

    def __init__(self, bool_operator: SRU_Boolean_Operators, index: SRU_Index | SRU_Filters, relation: SRU_Relation, value: str | int | SRU_Filter_TDO | SRU_Filter_LAN | SRU_Filter_PAY):
        self.bool_operator = bool_operator
        self.index = index
        self.relation = relation
        self.value = value 
        self.invalid = False
        if (
                type(self.bool_operator) != SRU_Boolean_Operators
                or type(self.relation) != SRU_Relation
            ):
            self.invalid = True
        # Checks if it's a filter
        self.is_filter = False
        self.filter_value_is_manual = False
        if type(self.index) == SRU_Filters:
            self.is_filter = True
            # Checks if filters value are OK
            self.is_filter_valid()
        elif type(self.index) != SRU_Index:
            self.invalid = True

    def is_filter_valid(self):
        # Document type filter
        if self.index.value == SRU_Filters.TDO.value:
            self.is_valid_filter_TDO()
        # Language filter
        elif self.index.value == SRU_Filters.LAN.value:
            self.is_valid_filter_LAN()
        # Rrare languages filter, no Enum so only a form check
        elif self.index.value == SRU_Filters.LAI.value:
            self.is_valid_filter_LAI()
        # Country filter
        elif self.index.value == SRU_Filters.PAY.value:
            self.is_valid_filter_PAY()
        # Rare countries filter, no Enum so only a form check
        elif self.index.value == SRU_Filters.PAI.value:
            self.is_valid_filter_PAI()
        # Publication date filter
        elif self.index.value == SRU_Filters.APU.value:
            self.is_valid_filter_APU()

    def is_valid_filter_TDO(self):
        if type(self.value) != SRU_Filter_TDO:
            if self.value not in [e.value for e in SRU_Filter_TDO]:
                self.invalid = True
            else:
                self.filter_value_is_manual = True

    def is_valid_filter_LAN(self):
        if type(self.value) != SRU_Filter_LAN:
            if self.value not in [e.value for e in SRU_Filter_LAN]:
                self.invalid = True
            else:
                self.filter_value_is_manual = True
    
    def is_valid_filter_LAI(self):
        if not re.search("^[a-zA-Z]{3}$", self.value):
            self.invalid = True
    
    def is_valid_filter_PAY(self):
        if type(self.value) != SRU_Filter_LAN:
            if self.value not in [e.value for e in SRU_Filter_PAY]:
                self.invalid = True
            else:
                self.filter_value_is_manual = True

    def is_valid_filter_PAI(self):
        if not re.search("^[a-zA-Z]{2}$", self.value):
                self.invalid = True

    def is_valid_filter_APU(self):
        try:
            int(self.value) # Works with 2000-2023
        except ValueError:
            self.invalid = True
        # Only if ot's not already invalid
        # Inf/sup or equal is not valid absed on APU doc : https://documentation.abes.fr/sudoc/manuels/interrogation/interrogation_professionnelle/index.html#apu
        # Well, WinIBW is fine with it soooooooooo
        if not self.invalid:
            if self.relation.value not in [
                    SRU_Relation.EQUALS.value,
                    SRU_Relation.STRITCLY_SUPERIOR.value,
                    SRU_Relation.STRITCLY_INFERIOR.value,
                    SRU_Relation.SUPERIOR_OR_EQUAL.value,
                    SRU_Relation.INFERIOR_OR_EQUAL.value
                ]:
                self.invalid = True

    def to_string(self, include_operator=True):
        val = self.value
        # If the filter value was set manually
        if not self.filter_value_is_manual and type(val) not in [str, int]:
            val = val.value
        if not include_operator:
            return f"{self.index.value}{self.relation.value}{val}"
        else:
            return f"{self.bool_operator.value}{self.index.value}{self.relation.value}{val}"


# Tests
sru = Sudoc_SRU()
# p1 = Part_Of_Query(SRU_Boolean_Operators.AND, SRU_Index.MOTS_DU_TITRE, SRU_Relation.EQUALS, "short")
# p2 = Part_Of_Query(SRU_Boolean_Operators.AND, SRU_Index.AUT, SRU_Relation.EQUALS, "Renard Alice")
# res = sru.sru_request(sru.generate_query(["(", p1, p2, ")"]), SRU_Operations.SEARCH, SRU_Record_Packing.XML)
# res = sru.sru_request("ISB=2-905064-03-3", SRU_Operations.SEARCH, SRU_Record_Packing.XML)
# p1 = Part_Of_Query(SRU_Boolean_Operators.AND, SRU_Index.AUT, SRU_Relation.EQUALS, "Renard Alice")
# p2 = Part_Of_Query(SRU_Boolean_Operators.AND, SRU_Filters.APU, SRU_Relation.SUPERIOR_OR_EQUAL, 2020)
# res = sru.sru_request(sru.generate_query([p1, p2]), SRU_Operations.SEARCH, SRU_Record_Packing.XML)
# res = sru.sru_request("aut=renard alice", "a", SRU_Record_Packing.XML)
res = sru.sru_request("", SRU_Operations.EXPLAIN, SRU_Record_Packing.XML)
print(res.get_records_id())
