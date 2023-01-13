import re
import os
from pathlib import Path
import datetime
from pandas import DataFrame as df

import metadatasf.flow as fd
import metadatasf.quickaction as qac
import config.path as p

output_path = os.getcwd() + "/" + p.output_path + "flow"   

def parse (metadata_path: str):
    
    print("Flow - Start of parsing")

    start = datetime.datetime.now().timestamp()

    if metadata_path[-1] != "/":
        metadata_path = metadata_path + "/"

    path_fl_str = metadata_path + "flows"
    path_fl = os.fsencode(path_fl_str)

    data_fl = {'Flow Name' : [],
                'API Name' : [],
                'Type' : [],
                'Schedule' : [],
                'Source object' : [],
                'Status' : [],
                'Description' : [],
                'Step Count' : [],
                'Step Detail' : [],
                'Subflow Count' : [],
                'Subflow List' : [],
                'Quick Actions' : [],
                'Pages' : []
                }

    # Description des flows 

    for file in os.listdir(path_fl):

        # On parcourt le dossier objets contenant tous les flows 
        if os.fsdecode(file).endswith(".xml"):

            
            flfilename = os.fsdecode(file)
            flname = re.sub(fd.Flow.ext,"",flfilename)
            fl = fd.Flow(metadata_path, flname)

            data_fl["Flow Name"].append(fl.label) 
            
            data_fl["API Name"].append(fl.nom)
            
            data_fl["Description"].append(fl.descr)
            
            data_fl["Status"].append(fl.status)
            
            data_fl["Type"].append(fl.type())

            data_fl["Step Count"].append(str(fl.step_count()))

            data_fl["Step Detail"].append(fl.step_detail())
            
            data_fl["Schedule"].append(fl.schedule_frequency())
            
            data_fl["Source object"].append(fl.source_obj())

            if fl.subflow_exists() == True:
                data_fl["Subflow Count"].append(fl.subflow_count())
                data_fl["Subflow List"].append(','.join(str(f) for f in fl.subflow_list()))
            else:
                data_fl["Subflow Count"].append("")
                data_fl["Subflow List"].append("")

            #Ajout des QuickAction où le flow apparait et des pages où apparaissent ces mêmes Quick Actions
            qas = fl.list_qa()    
            list_pages = []
            if len(qas)>0:
                for qa_str in qas:
                    qa = qac.QA(metadata_path, qa_str)
                    list_pages.extend(qa.list_page())

            #Ajout des pages dans lesquelles le flow apparait directement
            list_pages.extend(fl.list_page())

            data_fl['Quick Actions'].append(','.join(str(q) for q in qas))
            data_fl['Pages'].append(','.join(str(p) for p in list_pages))

    datafl = df(data_fl)

    for row_flow in datafl.index:
        called_by = []
        for row_sub in datafl.index:
            if datafl["API Name"][row_flow] in datafl["Subflow List"][row_sub]:
                called_by.append(datafl["API Name"][row_sub])
        if len(called_by) > 0:
            datafl.at[row_flow,"Called by"] = ','.join(str(c) for c in called_by)

    output_path = os.getcwd() + "/" + p.output_path + "flow/"

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    output_file = output_path + "Flow.xlsx"

    if os.path.exists(output_file):
        if open(output_file).closed:
            os.remove(output_file)

    datafl.to_excel(output_file)

    end = datetime.datetime.now().timestamp()
    duration = round(end - start)

    print("Flow - End of parsing (" + str(duration) + " secondes")


