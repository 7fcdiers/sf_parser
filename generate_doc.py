import os, shutil, datetime
import pandas as pd
import templates.FLOW_TEMPLATE_PAR as fl_par
import templates.OBJECT_TEMPLATE_PAR as obj_par
import templates.color_tag as color
import confluence.conf_function as cf
import config.path as p
import config.object_name as on
import metadatasf.flow  as f
import metadatasf.object as o



def create_and_send_from_template(type: str, send: bool):

    print("Generate docs for " + type)

    start = datetime.datetime.now().timestamp()

    temp_path_str = os.getcwd() + "/" + p.template_path
    md_path_str = os.getcwd() + "/" + p.markdown_path
    excel_path = os.getcwd() + "/" + p.output_path

    nb = 0

    if type == "flow":
        temp_par = fl_par
        type_obj = f.Flow
    elif type == "object":
        temp_par = obj_par
        type_obj = o.CustomObject
    
    par = temp_par.templ
    nom = temp_par.name
    pnom = temp_par.page_name
    specifics = temp_par.specifics
    specifics_param = temp_par.specifics_param
    excel_path = excel_path  + type + "/"

    parent_page_is_column = temp_par.parent_page_is_column
    parent_page = temp_par.parent_page
    parent_of_parent = temp_par.parent_of_parent

    template = type.upper() + '_TEMPLATE.html'

    src_xls = temp_par.path
    src_file = temp_path_str  + template
    dest_dir = md_path_str  + type

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    df = pd.read_excel(src_xls,engine='openpyxl')

    for row in df.index:
        
        fname = df.at[row,nom]
        pname = df.at[row,pnom]
        #Objet en tant que "variable" et non en tant que type de metadonnées
        obj = type_obj(p.metadata_path, fname)
        shutil.copy(src_file,dest_dir)

        prev_file = dest_dir + "/" + template
        new_file = dest_dir + "/" + fname + ".html"

        if os.path.exists(new_file) == True:
            os.remove(new_file)

        os.rename(prev_file, new_file)

        with open(new_file, 'r') as file:
            new_file_txt = file.read()

        #print(new_file_txt," AVANT REPLACE")

        for pcol in par:
            for col in df.columns:
                if col ==  pcol:
                    value = ""
                    hasspecifics = False
                    for spe in specifics:
                        if spe == col:   
                            method_to_call = getattr(temp_par,specifics[col])
                            if specifics_param[col] == "object":
                                value = method_to_call(obj)
                            elif specifics_param[col] == "value": 
                                value = method_to_call(df.at[row,col])
                            else:
                                value = method_to_call(df.at[row,specifics_param[spe]],df.at[row,col])

                            hasspecifics= True
                    if not hasspecifics:
                        value = str(df.at[row,col])
                        if value == "nan":
                            value = ""
                    
                    if df.at[row,col] == None:
                        new_file_txt = new_file_txt.replace(par[pcol],"")
                    else:    
                        new_file_txt = new_file_txt.replace(par[pcol],value)

        if "$$COLOR$$" in new_file_txt:
            color_tag = color.color(type,df.at[row,temp_par.color_colum])
            new_file_txt = new_file_txt.replace("$$COLOR$$",color_tag)

        with open(new_file,'w') as file:
            file.write(new_file_txt)
            nb += 1

        if send:
            if parent_page_is_column:
                if type == "flow":
                    parent_name = on.objects[df.at[row,parent_page]] + " (flow)"
            else:
                parent_name = parent_page

            pname = pname + " (" + type + ")"
            print (pname, fname)
            cf.new_or_update_page(type, pname,parent_name, fname)

    end = datetime.datetime.now().timestamp()
    duration = round(end - start)

    print("Generate docs for " + type + " - " + str(nb) + ' Fichiers générés')

    if send:
        print("Pages créées ou mise à jour sur Confluence")
    else:
        print("Aucune page mise à jour")

    print('Durée : ' + str(duration) + ' secondes.')





