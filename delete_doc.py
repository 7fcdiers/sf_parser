import os, shutil, re
import pandas as pd
import templates.FLOW_TEMPLATE_PAR as fl_par
import templates.color_tag as color
import confluence.conf_function as cf
import config.path as p



def delete_docs(type: str):

    print("Deleting docs for " + type)

    md_path_str = os.getcwd() + "/" + p.markdown_path

    nb = 0

    if type == "flow":
        md_path_str = md_path_str + "/flow"
    elif type == "object" :
        md_path_str = md_path_str + "/object"

    for file in os.listdir(md_path_str):

        if file.endswith(".html"):

            file_name = re.sub(".html","",os.fsdecode(file))

            if cf.delete_page(file_name) != "Page introuvable dans l'espace SI BI":
                nb += 1

            


    print("Deleted docs for " + type + " - " + str(nb) + ' pages supprimées')





