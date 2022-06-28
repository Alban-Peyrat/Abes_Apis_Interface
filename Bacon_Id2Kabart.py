#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import logging

class Bacon_Id2Kbart(object):
    """
    Bacon_Id2Kbart
    =======
    A set of function wich handle data returned by service 'Bacon in json' 
   http://documentation.abes.fr/aidebacon/index.html#WebserviceId2
    On init take a bib identifier in argument
    ex : https://bacon.abes.fr/id2kbart/9782807308534.json
"""

    def __init__(self,bib_id,service='bacon'):
        self.logger = logging.getLogger(service)
        self.endpoint = "https://bacon.abes.fr/id2kbart"
        self.service = service
        self.bib_id = bib_id
        self.multi_providers = False
        self.multi_kbart = False
        url =  '{}/{}.json'.format(self.endpoint, self.bib_id)
        r = requests.get(url)
        try:
            r.raise_for_status()  
        except requests.exceptions.HTTPError:
            self.status = 'Error'
            self.logger.error("{} :: XmlAbes_Init :: HTTP Status: {} || Method: {} || URL: {} || Response: {}".format(self.bib_id, r.status_code, r.request.method, r.url, r.text))
            self.error_msg = "Package inconnu ou service indisponible"
        else:
            self.record = r.json()
            if "provider" in self.record["query"] :
                # Test le nombre de providers
                if type(self.record["query"]["provider"]) is dict :
                    #Test du nombre de Kbart (on peut avoir plusieurs Kbart pour un même ISBN et provider)
                    if type(self.record["query"]["provider"]["kbart"]) is list :
                        self.multi_kbart = True
                    self.status = 'Succes'
                else : # Plusieurs providers
                    self.multi_providers = True
                    if type(self.record["query"]["provider"][0]["kbart"]) is list :
                        self.multi_kbart = True
                    self.status = 'Succes'
            else :
                self.status = 'None'
            self.logger.debug("{} :: Bacon :: Existe dans Bacon".format(bib_id))
            # self.logger.debug(self.record)

    def parse_kbart(self,field):
        if self.multi_providers :
            if self.multi_kbart :
                if self.record["query"]["provider"][0]["kbart"][0][field] :
                    return self.record["query"]["provider"][0]["kbart"][0][field]
                else :
                    return None
            if self.record["query"]["provider"][0]["kbart"][field] :
                return self.record["query"]["provider"][0]["kbart"][field]
            else :
                return None
        else :
            if self.multi_kbart :
                if self.record["query"]["provider"]["kbart"][0][field] : 
                    return self.record["query"]["provider"]["kbart"][0][field]
                else : 
                    return None
            if self.record["query"]["provider"]["kbart"][field] :
                return self.record["query"]["provider"]["kbart"][field]
            else :
                return None


    def get_publication_title(self):
        return self.parse_kbart("publication_title")

    def get_publisher_name(self):
        return self.parse_kbart("publisher_name")
        
    def get_online_pubdate(self):
        return self.parse_kbart("date_monograph_published_online")

    def get_print_pubdate(self):
        return self.parse_kbart("date_monograph_published_print")

    def get_ppn(self):
        ppn = self.parse_kbart("bestppn")
        self.logger.debug(ppn)
        if ppn == "" :
            return None
        else : 
            return ppn        
        # if self.multi_providers :
        #     if self.record["query"]["provider"][0]["kbart"]["bestppn"]:
        #         return self.record["query"]["provider"][0]["kbart"]["bestppn"]
        #     else:
        #         return 'None'
        # else :
        #     if self.record["query"]["provider"]["kbart"]["bestppn"]:
        #         return self.record["query"]["provider"]["kbart"]["bestppn"]
        #     else:
        #         return 'None'