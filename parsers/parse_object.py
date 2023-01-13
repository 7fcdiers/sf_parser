import re, datetime
import xml.etree.ElementTree as ET
import os
from pathlib import Path
from pandas import DataFrame as df

from metadatasf.object import CustomObject
import config.path as p
 
output_path = os.getcwd() + "/" + p.output_path + "object"   

def parse (metadata_path: str):
 
    print("Object - Start of parsing")

    if not os.path.exists(output_path):
        if not os.path.exists(os.getcwd() + "/" + p.output_path):
            os.mkdir(os.getcwd() + "/" + p.output_path)
        os.mkdir(output_path)

    start = datetime.datetime.now().timestamp()

    if metadata_path[-1] != "/":
        metadata_path = metadata_path + "/"

    path_o_str = metadata_path + "objects"
    path_o = os.fsencode(path_o_str)

    data_obj = {'Object Name' : [],
                'API Name' : [],
                'Type' : [],
                'Name field' : [],
                'RT count' : [],
                'Field count' : [],
                'Lookup to' : [],
                'VR count' : []}

    ''' Description des objets '''

    for file in os.listdir(path_o):

        ''' On parcourt le dossier objets contenant tous les sous-dossiers d'objet '''
        if not os.fsdecode(file).endswith(".ini"):
            
            filename = os.fsdecode(file)
            opath_str = path_o_str + "/" + filename
            opath = os.fsencode(opath_str)

            for ofile in os.listdir(opath):
                
                ''' On parcourt les dossiers & fichiers sous la racine du dossier objets/Objet Traité '''

                if os.fsdecode(ofile).endswith(".xml"):

                    ofilename = os.fsdecode(ofile)
                    objname = re.sub(CustomObject.ext,"",ofilename)
                    obj = CustomObject(metadata_path, objname)


                    data_obj["Object Name"].append(obj.label) 
                    data_obj["API Name"].append(obj.nom)
                    data_obj["Type"].append(obj.type) 
                    if  obj.namefield != "" :
                        data_obj["Name field"].append(obj.namefield + " (" + obj.namefield_type + ")")                    
                    else:
                        data_obj["Name field"].append("")

                    if obj.has_fields:
                        lookup_to = parse_field(obj)
                    else:
                        lookup_to = []

                    data_obj["Field count"].append(len(obj.list_fields))
                    data_obj["Lookup to"].append(lookup_to)


                    if obj.has_rt:
                        parse_rt(obj)
                    data_obj["RT count"].append(len(obj.list_rt))     

                    if obj.has_vr:
                        parse_vr(obj)
                    data_obj["VR count"].append(len(obj.list_vr))      

    output_obj = os.curdir + "/Output/Object/Object.xlsx"

    if os.path.exists(output_obj):
        os.remove(output_obj)

    datao = df(data_obj)
    datao.to_excel(output_obj)

    end = datetime.datetime.now().timestamp()
    duration = round(end - start)
    print("Object - End of parsing (" + str(duration) + " secondes)")

#Gestion des champs d'un objet
def parse_field(obj: CustomObject):
    lookup_obj = []
    #Dictionnaire pour les champs
    data_field ={'Object' : [],
                        'Field Name' : [],
                        'API Name' :[],
                        'Type' :[],
                        'Description' : [],
                        'Lookup object' :[],
                        'In VR' : [],
                        'Layout' : [],
                        'PermSet Read' : [],
                        'PermSet Write' : []}

    for field_name in obj.list_fields:
        field = obj.field(obj, field_name)

        #Attribution des valeurs de champs dans le dictionnaire
        data_field["Object"].append(obj.nom)
        data_field["Field Name"].append(field.label)
        data_field["API Name"].append(field.nom)
        data_field["Type"].append(field.type)
        data_field["Description"].append(field.descr)
        data_field["Lookup object"].append(field.objLookup())       

        data_field["In VR"].append(" | ".join(field.list_vr()))  

        layouts = field.list_layouts()

        data_field["Layout"].append(" | ".join(field.list_layouts()))
            
        if not field.objLookup() in lookup_obj and field.objLookup() != None:
            lookup_obj.append(field.objLookup())

        data_field["PermSet Read"].append(" | ".join(field.list_in_ps_r()))  
        data_field["PermSet Write"].append(" | ".join(field.list_in_ps_w()))  



    #Définition du chemin de sortie du fichier de synthèse des champs de l'objet
    output_field = output_path + "/" + obj.nom + "/Fields.xlsx"

    if not os.path.exists(output_path + "/" + obj.nom):
        os.mkdir(output_path + "/" + obj.nom)

    if os.path.exists(output_field):
        os.remove(output_field)

    #Création du Dataframe sur la base du dictionnaire et écriture dans le fichier de sortie
    dataf = df(data_field)
    dataf.to_excel(output_field)

    return lookup_obj

#Gestion des RecordType d'un objet
def parse_rt(obj: CustomObject):

    data_field ={'Object' : [],
                'RT Name' : [],
                'API Name' :[]}

    for rt_name in obj.list_rt:

        rt = obj.rt(obj, rt_name) 

        data_field["Object"].append(obj.nom)
        data_field["RT Name"].append(rt.label)
        data_field["API Name"].append(rt.nom)       


    output_field = output_path + "/" + obj.nom + "/RecordTypes.xlsx"

    if not os.path.exists(output_path + "/" + obj.nom):
        os.mkdir(output_path + "/" + obj.nom)

    if os.path.exists(output_field):
        os.remove(output_field)

    dataf = df(data_field)
    dataf.to_excel(output_field)

    del dataf
    data_field.clear()


#gestion des Validation Rules d'un objet
def parse_vr(obj: CustomObject):
 
    data_field ={'Object' : [],
                'VR Name' : [],
                'Description' :[],
                'Active' : []}

    for vr_name in obj.list_vr:

        vr = obj.vr(obj, vr_name) 
 
        data_field["Object"].append(obj.nom)
        data_field["VR Name"].append(vr.nom)
        data_field["Description"].append(vr.descr) 
        data_field["Active"].append(vr.isactive)        


    output_field = output_path + "/" + obj.nom + "/ValidationRules.xlsx"

    if not os.path.exists(output_path + "/" + obj.nom):
        os.mkdir(output_path + "/" + obj.nom)

    if os.path.exists(output_field):
        os.remove(output_field)

    dataf = df(data_field)
    dataf.to_excel(output_field)

    del dataf
    data_field.clear()


