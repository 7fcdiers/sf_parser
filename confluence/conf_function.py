from atlassian import Confluence 
import os, re
import templates.FLOW_TEMPLATE_PAR as fl_par
import templates.OBJECT_TEMPLATE_PAR as obj_par
import config.path as p

def login():
    par_user = "cdiers@sibylone.com"
    par_api_token_str = "8jMiBO9THK5fbQ1xkuqJ69A9"
    par_url = "https://sibylone.atlassian.net"

    cf = Confluence(
        url = par_url,
        username = par_user,
        password = par_api_token_str,
        cloud = True
    )

    return cf

def new_or_update_page(type: str, page_name: str, parent_name: str, file_name: str):

    path = os.getcwd() + "/" + p.markdown_path
    path = path + type
    file_name = file_name + ".html"

    with open(path + "/" + file_name,'r') as file :
        text = file.read()

    if type == "flow":
        temp_par = fl_par
    elif type == "object" :
        temp_par = obj_par

    parent_of_parent = temp_par.parent_of_parent

    cf = login()

    try :
        cf.get_page_by_title(space="SB",title=parent_name,start=None,limit=None)
        parent_page = cf.get_page_by_title(space="SB",title=parent_name,start=None,limit=None)
        parent_page_id = parent_page["id"]
    except:
        parent_of_parent_id = cf.get_page_by_title(space="SB",title=parent_of_parent,start=None,limit=None)["id"]
        cf.update_or_create(parent_id=parent_of_parent_id, title=parent_name, body="", representation='storage')
        parent_page = cf.get_page_by_title(space="SB",title=parent_name,start=None,limit=None)
        parent_page_id = parent_page["id"]
        
    cf.update_or_create(parent_id=parent_page_id, title=page_name, body=text, representation='storage')
    new_page_id = cf.get_page_by_title(space="SB",title=page_name,start=None,limit=None)["id"]

    cf.set_page_label(new_page_id, "salesforce")
    cf.set_page_label(new_page_id, type)

def delete_page(page_name: str):

    cf = login()

    if cf.get_page_by_title(space="SB",title=page_name,start=None,limit=None) != None:
        page_id = cf.get_page_by_title(space="SB",title=page_name,start=None,limit=None)["id"]
        cf.remove_page(page_id, status=None,recursive=False)

        return "Page " + page_name + " supprimée"
        
    else:
        return "Page introuvable dans l'espace SI BI"
