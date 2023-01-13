import re
import xml.etree.ElementTree as ET

class LWP:

    ''' Variable définissant l'extension des fichiers décrivant un objet '''

    ext: str = ".flexipage-meta.xml"
    flexpath: str = "/flexipages"

    def __init__(self,path: str, nom: str) -> None:

        ''' Définition des caractéristiques d'un objet '''

        self.nom: str = nom
        self.path: str = path + LWP.flexpath
        self.file:str = nom + LWP.ext
        
        xml_file = open(self.path + "/" + self.file, "r").read()
        self.src = re.sub(' xmlns="[^"]+"', '', xml_file, count=1)
        self.tree = ET.fromstring(self.src)

        self.label = self.tree.find("masterLabel").text
        if self.tree.find("description") != None:
            self.descr = self.tree.find("description").text
        else:
            self.descr = ""      

        self.type = self.tree.find("type").text 

    #Si page d'enregistrement, à quel object elle est associée
    def object(self) -> str:
        if self.type() == "RecordPage":
            return self.tree.find("sobjectType").text
        else:
            return "Aucun objet associé"

    #liste des actions visibles sur la page
    def action(self) -> list:
        l_action = []
        hasactions = self.tree.findall(".//*componentInstanceProperties/[name='actionNames']")
        if hasactions != None:
            for actions in hasactions:
                action = actions.iter("/valueList/ValueListItems/value")
                for u_action in action:
                    if u_action.find("value") != None:
                        l_action.append(u_action.find("value").text)

        '''
        regions = self.tree.iter("flexiPageRegions")
        for region in regions:
            if region.find("name").text == "header":
                items = region.iter("itemInstances")
                for item in items:
                    if item.find("componentInstance").find("componentInstanceProperties").find("name").text == "actionNames":
                        actions = item.find("componentInstance").find("componentInstanceProperties").iter("valueListItems")
                        for action in actions:
                            l_action.append(action.find("value").text)
        '''
        return l_action

    #liste des flows directement ajouté à la page
    def flow(self) -> list:
        l_flow = []
        flows = self.tree.findall(".//*componentInstanceProperties/[name='flowName']")
        if flows != None:
            for flow in flows:
                l_flow.append(flow.find("value").text)

        return l_flow



       