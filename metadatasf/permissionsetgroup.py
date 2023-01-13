import re, os
import xml.etree.ElementTree as ET

class PSG:

    ext: str = ".permissionsetgroup-meta.xml"
    opath: str = "/permissionsetgroups"

    def __init__(self,path: str, nom: str) -> None:

        #Définition des caractéristiques d'un objet

        self.nom: str = nom
        self.file:str = nom + PSG.ext
        if path[-1] == "/":
            self.srcpath: str = path[: -1]
        else:
            self.srcpath: str = path

        self.path: str = path + PSG.opath 

        xml_file = open(self.path + "/" + self.file, "r").read()
        self.src = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
        self.tree = ET.fromstring(self.src)


    def list_ps(self) -> list:
        ps_list = []
        ps_tree = self.tree.iter("permissionSets")

        for ps in ps_tree:
            ps_list.append(ps.text)

        return ps_list
