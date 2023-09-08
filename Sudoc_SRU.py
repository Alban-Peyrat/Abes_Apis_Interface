# -*- coding: utf-8 -*- 

# external imports
import logging
import requests
import xml.etree.ElementTree as ET
import urllib.parse
from enum import Enum

# Doc : https://abes.fr/wp-content/uploads/2023/05/guide-utilisation-service-sru-catalogue-sudoc.pdf
# SRU V1.1 is used

class XML_NS(Enum):
    SRW = "http://www.loc.gov/zing/srw/"

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
        if type(record_packing) == SRU_Record_Packing:
            record_packing = record_packing.value
        url = f'{self.endpoint}?operation={operation}&version={self.version}'\
            f'&recordSchema={self.record_schema}&recordPacking={record_packing}'\
            f'&startRecord={start_record}&maximumRecords={maximum_records}&query={query}'
        
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
        
        if operation == SRU_Operations.SEARCH.value:
            return SRU_Search_Result(status, error_msg, result,
                    operation, record_packing, maximum_records,
                    start_record, query, url)

    # def get_result(self):
    #         """Return the entire result."""
    #         return self.result

    # def get_init_status(self):
    #     """Return the init status as a string."""
    #     return self.status

    # def get_error_msg(self):
    #     """Return the error message as a string."""
    #     if hasattr(self, "error_msg"):
    #         return self.error_msg
    #     else:
    #         return "Pas de message d'erreur"

    # def get_nb_results(self):
    #     """Returns the number of results as an int."""
    #     root = ET.fromstring(self.result)
    #     if root.findall("zs{}:numberOfRecords".format(self.version), NS):
    #         return root.find("zs{}:numberOfRecords".format(self.version), NS).text
    #     else: 
    #         return 0

    # def get_records(self):
    #     """Returns all records as a list"""
    #     root = ET.fromstring(self.result)
    #     return root.findall(".//zs{}:record".format(self.version), NS)

    # def get_records_id(self):
    #     """Returns all records as a list of strings"""
    #     root = ET.fromstring(self.result)
    #     records = root.findall(".//zs{}:record".format(self.version), NS)

    #     output = []
    #     for record in records:
    #         output.append(record.find(".//marc:controlfield[@tag='001']", NS).text)
        
    #     return output


# ----- Temp tests
# différer l'opération selon 
# rajouter une vérification des index 
# Créer une classe ou smontehing pour écrire la requête


# sru = Sudoc_SRU()
# res = sru.sru_request("ISB=2-905064-03-3", SRU_Operations.SEARCH, SRU_Record_Packing.XML)
# print(res.result_as_string)
# print(res.url)