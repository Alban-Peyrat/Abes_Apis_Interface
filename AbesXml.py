import os
# external imports
import requests
import logging
import xml.etree.ElementTree as ET
# internal import
from mail import mail
from logs import logs


##Permet de travailler avec l'api du SUDOC qui retourne une notice en xmL

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
        self.notice = r.content.decode('utf-8')

    @property
    #Retourne la totalite de la notice
    def get_notice(self):
        # print(self.notice)
        return self.notice
    #Pour un RCR donnée retourne la liste des Etats de collection formatés (955$$r du SUDOC)
    def get_etat_col(self,rcr):
        root = ET.fromstring(self.notice)
        etatsColl = []
        for champ in root.findall(".//datafield[@tag='955']"):
            item = champ.find("subfield[@code='5']").text
            if item[:9] == rcr and champ.find("subfield[@code='r']") is not None:
                etatColl = champ.find("subfield[@code='r']").text
                etatsColl.append(etatColl)
        return etatsColl
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