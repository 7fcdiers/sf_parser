from cmath import nan
import re, os
import xml.etree.ElementTree as ET
import config.path as p

import metadatasf.layout as la
import metadatasf.permissionset as ps

import pandas as pd
from pandas import DataFrame as df



class CustomObject:

    #Variable définissant l'extension des fichiers décrivant un objet

    ext: str = ".object-meta.xml"
    opath: str = "/objects"

    def __init__(self,path: str, nom: str) -> None:

        #Définition des caractéristiques d'un objet

        self.nom: str = nom
        self.file:str = nom + CustomObject.ext

        if path[-1] == "/":
            self.srcpath: str = path[: -1]
        else:
            self.srcpath: str = path

        self.path: str = path + CustomObject.opath + "/" + nom   

        xml_file = open(self.path + "/" + self.file, "r").read()
        self.src = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
        self.tree = ET.fromstring(self.src)

        if self.nom.endswith("__c"):
            self.type = "Custom"
        else:
            self.type = "Standard"
        
        if self.type == "Custom":
            self.label = self.tree.find("label").text
        else:
            self.label = self.nom

        if self.tree.find("nameField") != None:
            self.namefield = self.tree.find("nameField").find("label").text
            self.namefield_type = self.tree.find("nameField").find("type").text
        else:
            self.namefield = ""
            self.namefield_type = ""

        self.has_fields = os.path.exists(self.path + CustomObject.field.fpath)
        self.has_rt = os.path.exists(self.path + CustomObject.rt.rtpath)
        self.has_vr = os.path.exists(self.path + CustomObject.vr.vrpath)

        if self.has_fields:
            self.list_fields = [f.replace(self.field.ext,"") for f in os.listdir(self.path + self.field.fpath) if str(f).endswith(self.field.ext)]
        else:
            self.list_fields = []

        if self.has_rt:
            self.list_rt = [f.replace(self.rt.ext,"") for f in os.listdir(self.path + self.rt.rtpath) if str(f).endswith(self.rt.ext)]
        else:
            self.list_rt = []

        if self.has_vr:
           self.list_vr = [f.replace(self.vr.ext,"") for f in os.listdir(self.path + self.vr.vrpath) if str(f).endswith(self.vr.ext)]
        else:
            self.list_vr = []

    class field:

        #Variable définissant l'extension des fichiers décrivant un champs

        ext: str = ".field-meta.xml"
        fpath: str = "/fields"

        def __init__(self, customobject, nom: str) -> None:

            #Définition des caractéristiques d'un champs

            self.customobject: CustomObject = customobject
            self.nom: str = nom
            self.path: str = self.customobject.path +  self.fpath
            self.file: str = self.nom + self.customobject.field.ext
            xml_file = open(self.path + "/" + self.file, "r").read()
            self.src: str = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
            self.tree = ET.fromstring(self.src)

            if self.tree.find("description") != None:
                self.descr = self.tree.find("description").text
            else:
                self.descr = ""
    
            if self.nom.endswith("__c"):
                self.iscustom = True
            else:
                self.iscustom = False

            if self.iscustom:
                self.type: str = self.tree.find("type").text
                self.label: str = self.tree.find("label").text
            else:
                self.type: str = "Salesforce DataType"
                self.label: str = self.nom

            if self.tree.find("trackHistory") != None:
                self.history = bool(self.tree.find("trackHistory").text)
            else:
                self.history = False

        def isLookup(self) -> bool:

            #Est-ce que le champs est une jointure vers un autre objet ?

            if self.type == "MasterDetail" or self.type == "Lookup":
                return True
            else:
                return False

        def objLookup(self) -> str:

            #Si le champs est une jointure, vers quel objet ?
            if self.type == "MasterDetail" or self.type == "Lookup":
                return self.tree.find("referenceTo").text

        def hasLookupFilter(self) -> bool:

            #Si le champs est une jointure, y a-t-il des conditions sur cette jointure ?

            self.lup = self.tree.find("lookupFilter")
            if self.lup == None:
                return False
            else:
                return True

        def countLookupFilter(self) -> int:
            
            #S'il y a une condition de jointure, combien de membre comporte cette condition ?

            self.lup = self.tree.find("lookupFilter")
            nb_filter: int = 0

            if self.lup != None:
                self.lup_filter = self.lup.iter("filterItems")
                for filter in self.lup_filter:
                        nb_filter += 1

            return nb_filter

        def list_vr(self) -> list:

            field_vr = []
            vr_path_str = self.customobject.path + self.customobject.vr.vrpath

            if os.path.exists(vr_path_str):
                for file in os.listdir(vr_path_str):
                    fname = re.sub(self.customobject.vr.ext,"",os.fsdecode(file))
                    if os.fsdecode(file).endswith(".xml"):
                        vr = self.customobject.vr(self.customobject,fname)
                        if self.nom in vr.formula:
                            field_vr.append(vr.nom)

            return field_vr

        def list_layouts(self) -> list:

            layout = []

            layout_path = p.metadata_path + la.Layout.lpath

            if os.path.exists(layout_path):
                for file in os.listdir(layout_path):
                    if os.fsdecode(file).startswith(self.customobject.nom) and os.fsdecode(file).endswith(".xml"):
                        fname = re.sub(la.Layout.ext,"",os.fsdecode(file))
                        
                        field_in_layout = [x.split('-')[0] for x in la.Layout(p.metadata_path,fname).fields_list()]
                        field_behavior = [x.split('-')[1] for x in la.Layout(p.metadata_path,fname).fields_list()]

                        if self.nom in field_in_layout:
                            if field_behavior[field_in_layout.index(self.nom)] == "Edit" :
                                layout.append(fname + ' (edit)')
                            elif field_behavior[field_in_layout.index(self.nom)] == "Required" :
                                layout.append(fname + ' (req)')
                            else: 
                                layout.append(fname + ' (read)')

            return layout

        def list_in_ps_r(self) -> list:

            list_ps = [ ]

            path_ps = self.customobject.srcpath + ps.PS.opath

            for file in os.listdir(path_ps) : 
                filename = file.split(ps.PS.ext)[0]
                file_ps = ps.PS(self.customobject.srcpath, filename)
                if self.customobject.nom + '.' + self.nom in file_ps.list_fields_r():
                    list_ps.append(filename)

            return list_ps

        def list_in_ps_w(self) -> list:

            list_ps = [ ]

            path_ps = self.customobject.srcpath + ps.PS.opath

            for file in os.listdir(path_ps) : 
                filename = file.split(ps.PS.ext)[0]
                file_ps = ps.PS(self.customobject.srcpath, filename)
                if self.customobject.nom + '.' + self.nom in file_ps.list_fields_w():
                    list_ps.append(filename)

            return list_ps

        def list_ps(self) -> list : 

            return list(set(self.list_in_ps_r() + self.list_in_ps_w()))

    #Sous classe Record Type de l'objet
    class rt:

        #Variable définissant l'extension des fichiers décrivant un champs

        ext: str = ".recordType-meta.xml"
        rtpath: str = "/recordTypes"

        def __init__(self, customobject, nom: str) -> None:

            #Définition des caractéristiques d'un champs

            self.customobject: CustomObject = customobject
            self.nom: str = nom
            self.path: str = self.customobject.path +  self.rtpath
            self.file: str = self.nom + self.customobject.rt.ext
            xml_file = open(self.path + "/" + self.file, "r").read()
            self.src: str = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
            self.tree = ET.fromstring(self.src)

            self.label = self.tree.find("label").text 
            #self.descr = self.tree.find("description").text

            self.active = bool(self.tree.find("active").text)


    #Sous classe Validation Rule de l'objet
    class vr:

        #Variable définissant l'extension des fichiers décrivant un champs

        ext: str = ".validationRule-meta.xml"
        vrpath = "/validationRules"

        def __init__(self, customobject, nom: str) -> None:

            #Définition des caractéristiques d'un champs

            self.customobject: CustomObject = customobject
            self.nom: str = nom
            self.path: str = self.customobject.path +  self.vrpath
            self.file: str = self.nom + self.customobject.vr.ext
            xml_file = open(self.path + "/" + self.file, "r").read()
            self.src: str = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
            self.tree = ET.fromstring(self.src)

            if self.tree.find("description") != None:
                self.descr = self.tree.find("description").text
            else:
                self.descr = ""

            self.isactive = bool(self.tree.find("active").text)

            self.formula = self.tree.find("errorConditionFormula").text