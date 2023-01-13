import re, os
import xml.etree.ElementTree as ET
import config.tag as ctag

import metadatasf.quickaction as qa
import metadatasf.flexipage as fl

class Flow:

    ''' Variable définissant l'extension des fichiers décrivant un objet '''

    ext: str = ".flow-meta.xml"
    fpath: str = "/flows"

    def __init__(self,path: str, nom: str) -> None:

        # Définition des caractéristiques d'un flow 

        if path[-1] != "/":
            path = path + "/"
        self.srcpath = path
        self.nom: str = nom
        self.path: str = path + Flow.fpath
        self.file:str = nom + Flow.ext
        
        xml_file = open(self.path + "/" + self.file, "r").read()
        self.src = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
        self.tree = ET.fromstring(self.src)

        self.label = self.tree.find("label").text
        if self.tree.find("description") != None:
            self.descr = self.tree.find("description").text
        else:
            self.descr = ""        

        self.status = self.tree.find("status").text

        self.subflow_tree = self.tree.find("subflows")

        if self.tree.find("start") != None:
            self.hastrigger = True 
        else:
            self.hastrigger = False

    #Type de flow
    def type(self) -> str:
        if self.tree.find("screens") != None:
            return "Screen Flow"
        elif self.hastrigger == True:
            if self.tree.find("start").find("schedule") != None:
                return "Scheduled Flow"
            elif self.tree.find("start").find("object") != None:
                return "Record-trigger Flow"
            else:
                return self.tree.find("processType").text  
        else:
            return self.tree.find("processType").text

    #Y a-t-il des flow appelés par ce flow
    def subflow_exists(self) -> bool:
        exist = False

        if self.type() == "Workflow":
            actions = self.tree.iter("actionCalls")
            for action in actions:
                if action.find("actionType").text == "flow":
                    exist = True
        else:
            if self.subflow_tree != None:
                exist = True 

        return exist

    #Liste de flows appelés par ce flow
    def subflow_list(self) -> list:
        sf = []

        if self.type() == "Workflow":
            actions = self.tree.iter("actionCalls")
            for action in actions:
                if action.find("actionType").text == "flow":
                    sf.append(action.find("actionName").text)
        else:
            if self.subflow_tree != None:
                subflows = self.tree.iter("subflows")  
                for subflow in subflows:
                    sf.append(subflow.find("flowName").text)  

        return sf

    #Nombre de flows appelés par ce flow
    def subflow_count(self) -> int:
        return len(self.subflow_list())

    #Objet principal sur lequel se base le flow
    def source_obj(self) -> str:
        if self.type() == "Workflow":
            metadatas = self.tree.iter("processMetadataValues")
            for metadata in metadatas:
                if metadata.find("name").text == "ObjectType":
                    return metadata.find("value").find("stringValue").text
        elif self.hastrigger:
                if self.tree.find("start").find("object") != None :
                    return self.tree.find("start").find("object").text
            
        tag = self.nom[4:7]
        for t in ctag.tags:
            if t == tag:
                return ctag.tags[t]

        return "No object found"      

    #Si Scheduled flow, à quelle fréquence
    def schedule_frequency(self) -> str:
        if self.type() == "Scheduled Flow":
            return self.tree.find("start").find("schedule").find("frequency").text
        else:
            return ""

    #Nombre d'action du flow de type décision
    def dec_count(self) -> int:
        count = 0
        steps = self.tree.iter("decisions")

        for step in steps:
            count += 1

        return count

    #Nombre d'action du flow de type boucle
    def loop_count(self) -> int:
        count = 0
        steps = self.tree.iter("loops")

        for step in steps:
            count += 1

        return count

    #Nombre d'action du flow de type assignment
    def assignment_count(self) -> int:
        count = 0
        steps = self.tree.iter("assignments")

        for step in steps:
            count += 1

        return count

    #Nombre d'action du flow de type appel à une action (envoi notification, email, Slack, etc.)
    def actioncall_count(self) -> int:
        count = 0
        steps = self.tree.iter("actionCalls")

        for step in steps:
            count += 1

        return count

    #Nombre d'action du flow de type recherche d'enregistrements
    def lookup_count(self) -> int:
        count = 0
        steps = self.tree.iter("recordLookups")

        for step in steps:
            count += 1

        return count

    #Nombre d'action du flow de type mise à jour d'enregistrements
    def update_count(self) -> int:
        count = 0
        steps = self.tree.iter("recordUpdates")

        for step in steps:
            count += 1

        return count

    def delete_count(self) -> int:
        count = 0
        steps = self.tree.iter("recordDeletes")

        for step in steps:
            count += 1

        return count

    #Nombre total d'actions du flow       
    def step_count(self) -> int:
        return self.actioncall_count() + self.assignment_count() + self.lookup_count() + self.update_count() + self.loop_count() + self.dec_count() + self.delete_count()

    #Chaine de caractère donnant le total d'étapes et le détail par type d'étape
    def step_detail(self) -> dict:
        
        steps = {
            'Actions' : self.actioncall_count(),
            'Assignments' : self.assignment_count(),
            'Decisions' : self.dec_count(),
            'Loops' : self.loop_count(),
            'Get Record' : self.lookup_count(),
            'Update Record' : self.update_count(),
            'Delete Record' : self.delete_count()
        }

        steps_to_reduce = []
        for key in steps:
            if steps[key] != 0:
                steps_to_reduce.append(key)

        dict_filter = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])

        reduced_steps = dict_filter(steps, steps_to_reduce)
        
        return reduced_steps

    def list_qa(self) -> list:
        flow_qa = []
        qa_path_str = self.srcpath + qa.QA.qapath
        qa_path = os.fsencode(qa_path_str)

        for file in os.listdir(qa_path):
            fname = re.sub(qa.QA.ext,"",os.fsdecode(file))
            if os.fsdecode(file).endswith(".xml"):
                action = qa.QA(self.srcpath,fname)
                if self.nom in action.flow():
                    flow_qa.append(action.nom)

        return flow_qa

    def list_page(self) -> list:
        fl_pages = []
        pages_path_str = self.srcpath + fl.LWP.flexpath
        pages_path = os.fsencode(pages_path_str)

        for file in os.listdir(pages_path):
            fname = re.sub(fl.LWP.ext,"",os.fsdecode(file))
            if os.fsdecode(file).endswith(".xml"):
                page = fl.LWP(self.srcpath,fname)
                if self.nom in page.flow():
                    fl_pages.append(page.nom)

        return fl_pages





        





