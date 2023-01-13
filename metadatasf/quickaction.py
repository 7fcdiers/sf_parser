import re
import os
import xml.etree.ElementTree as ET

from metadatasf import flexipage as flex

class QA:

    ''' Variable définissant l'extension des fichiers décrivant un objet '''

    ext: str = ".quickAction-meta.xml"
    qapath: str = "/quickActions"

    def __init__(self,path: str, nom: str) -> None:

        ''' Définition des caractéristiques d'un objet '''

        self.nom: str = nom
        self.srcpath = path
        self.file:str = nom + QA.ext
        self.path: str = self.srcpath + QA.qapath        
        if os.path.exists(self.path + "/" + self.file):
            xml_file = open(self.path + "/" + self.file, "r").read()
            self.exist = True 
        else:
            self.exist = False

        self.src = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
        self.tree = ET.fromstring(self.src)

        if self.tree.find("label") != None:
            self.label = self.tree.find("label").text
        elif self.tree.find("standardLabel") != None:
            self.label = self.tree.find("standardLabel").text  
        else:
            self.label == "No label"
                       
        if self.tree.find("description") != None:
            self.descr = self.tree.find("description").text
        else:
            self.descr = ""     
        
        self.type = self.tree.find("type").text   

    def flow(self) -> str:
        if self.type == "Flow":
            return self.tree.find("flowDefinition").text 
        else:
            return "Pas de flow associé"

    def list_page(self) -> list:
        qa_pages = []
        pages_path_str = self.srcpath + flex.LWP.flexpath
        pages_path = os.fsencode(pages_path_str)

        for file in os.listdir(pages_path):
            fname = re.sub(flex.LWP.ext,"",os.fsdecode(file))
            if os.fsdecode(file).endswith(".xml"):
                page = flex.LWP(self.srcpath,fname)
                if self.nom in page.action():
                    qa_pages.append(page.nom)

        return qa_pages


 

        



    
            





