import re
import xml.etree.ElementTree as ET
import config.path as p

from pandas import DataFrame as df

class Layout:

    ''' Variable définissant l'extension des fichiers décrivant un objet '''

    ext: str = ".layout-meta.xml"
    lpath: str = "/layouts"

    def __init__(self,path: str, nom: str) -> None:

        ''' Définition des caractéristiques d'un objet '''

        self.nom: str = nom
        self.path: str = p.metadata_path + Layout.lpath 
        self.file:str = nom + Layout.ext

        self.object:str = nom.split("-")[0]
        
        xml_file = open(self.path + "/" + self.file, "r").read()
        self.src = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
        self.tree = ET.fromstring(self.src)

        #self.label = self.tree.find("label").text
        if self.tree.find("description") != None:
            self.descr = self.tree.find("description").text
        else:
            self.descr = ""     

    def fields_list(self) -> list :
        #Retourne la liste des champs de la présentation de page, séparée par un "-" avec le comportement du champs sur la page
        fields = []

        field_trees = self.tree.iter('layoutItems')

        for field in field_trees:
            
            if field.find('field') != None:
                fields.append(field.find('field').text+'-'+field.find('behavior').text)

        return fields

                

        