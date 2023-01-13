import re, os
import xml.etree.ElementTree as ET


import metadatasf.permissionsetgroup as psg

class PS:

    ext: str = ".permissionset-meta.xml"
    opath: str = "/permissionsets"

    def __init__(self,path: str, nom: str) -> None:

        #Définition des caractéristiques d'un objet

        self.nom: str = nom
        self.file:str = nom + PS.ext
        if path[-1] == "/":
            self.srcpath: str = path[: -1]
        else:
            self.srcpath: str = path

        self.path: str = path + PS.opath 

        xml_file = open(self.path + "/" + self.file, "r").read()
        self.src = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
        self.tree = ET.fromstring(self.src)

    def list_fields_r(self) -> dict:  

        lst_fields = []

        fields = self.tree.iter("fieldPermissions")

        for field in fields:
            if field.find("readable").text != 'false' :
                lst_fields.append(field.find("field").text)

        return lst_fields
        
    def list_fields_w(self) -> dict:  

        lst_fields = []

        fields = self.tree.iter("fieldPermissions")

        for field in fields:
            if field.find("editable").text != 'false' :
                lst_fields.append(field.find("field").text)

        return lst_fields

    def list_in_psg(self) -> list:
        lst_psg = []
        psg_path = self.srcpath + psg.PSG.opath

        for file in os.listdir(psg_path):
            file_name = file.split(psg.PSG.ext)[0]
            file_psg = psg.PSG(self.srcpath, file_name)
            if self.nom in file_psg.list_ps():
                lst_psg.append(file_name)

        return lst_psg

