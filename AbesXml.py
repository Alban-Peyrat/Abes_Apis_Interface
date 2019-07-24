import os
# external imports
import requests
import logging
import xml.etree.ElementTree as ET
# internal import
from mail import mail
from logs import logs

"""
    AbesXml
    =======
    A set of function wich handle data returned by service 'Sudoc in Xml' 
    http://documentation.abes.fr/sudoc/manuels/administration/aidewebservices/index.html#SudocMarcXML
    On init take a PPN (sudoc identifier) in argument
    ex : https://www.sudoc.fr/178565946.xml   
"""


class AbesXml(object):

    def __init__(self,ppn,service='AbesXml'):
        self.endpoint = "https://www.sudoc.fr"
        self.service = service
        self.logger = logging.getLogger(service)
        self.ppn = ppn
        url =  '{}/{}.xml'.format(self.endpoint, self.ppn)
        r = requests.get(url)
        try:
            r.raise_for_status()  
        except requests.exceptions.HTTPError:
            raise HTTPError(r,self.service)
        self.record = r.content.decode('utf-8')

    @property
    
    def get_record(self):
        """
        Return the entire record
        
        Returns:
            string -- the record in unimarc_xml 
        """
        return self.record
    
    def get_textual_holdings(self,rcr):
        """
        For a given library return all the text holdings present in the record (955$$r in unimarc SUDOC)
        
        Arguments:
            rcr {string} -- the libray's id in Sudoc
        
        Returns:
            list -- a list of text holdings
        """
        root = ET.fromstring(self.notice)
        textual_holdings = []
        for field in root.findall(".//datafield[@tag='955']"):
            item = field.find("subfield[@code='5']").text
            if item[:9] == rcr and field.find("subfield[@code='r']") is not None:
                textual_holdings.append(field.find("subfield[@code='r']").text)
        return textual_holdings


#Gestion des erreurs
class HTTPError(Exception):

    def __init__(self, response, service):
        super(HTTPError,self).__init__(self.msg(response, service))

    def msg(self, response, service):
        logger = logging.getLogger(service)
        msg = "\n  HTTP Status: {}\n  Method: {}\n  URL: {}\n  Response: {}"
        sujet = service + 'Erreur'
        message = mail.Mail()
        message.envoie(os.getenv('ADMIN_MAIL'),os.getenv('ADMIN_MAIL'),sujet, msg.format(response.status_code, response.request.method, response.url, response.text) )
        logger.error("HTTP Status: {} || Method: {} || URL: {} || Response: {}".format(response.status_code, response.request.method,
                          response.url, response.text))