import json, os
#from tkinter.tix import CELL
from metadatasf import object as obj

import pandas as pd
from utils.bullet import mk_bullet
import config.path as p

path = os.getcwd() + "/" + p.output_path + "object/Object.xlsx"
base_path = os.getcwd() + "/" + p.output_path + "object/"

name = "API Name"
page_name = "Object Name"

color_colum = "Type"

templ = {'Object Name' : "$$NAME$$",
        'API Name' : "$$API$$",
        'Type' : "$$TYPE$$",
        'Name field' : "$$NAME_FIELD$$",
        'Lookup to' : "$$LOOKUP_BLOC$$",
        'Description' : "$$DESCR$$",
        'Field count' : "$$FIELD_BLOCK_DETAIL$$",
        'RT count' : "$$RT_BLOCK_DETAIL$$",
        'VR count' : "$$VR_BLOCK_DETAIL$$"
        }

templ_fields = {
    'Field Name' : "$$FIELD_NAME$$",
    'API Name' : "$$FIELD_API$$",
    'Description' : "$$FIELD_DESCRIPTION$$",
    'Type' : "$$FIELD_TYPE$$",
    'Lookup object' : "$$FIELD_LOOKUP$$",
    'PermSet Read' : "$$PERM_R$$",
    'PermSet Write' : "$$PERM_W$$"
}

templ_rt = {
    'RT Name' : "$$RT_NAME$$",
    'API Name' : "$$RT_API$$"
}

templ_vr = {
    'VR Name' : "$$VR_NAME$$",
    'Description' : "$$VR_DESCR$$",
    'Active' : "$$VR_ACTIVE$$"
}

parent_page_is_column = False
parent_page = "Object definitions"
parent_of_parent = "Dictionnaire de données"

specifics = {
    'Lookup to' : "lookup",
    'Field count' : "fields",
    'RT count' : "rt",
    'VR count' : "vr"
}

specifics_param = {
    'Lookup to' : 'value',
    'Field count' : "object",
    'RT count' : "object",
    'VR count' : "object"
}

def lookup(lookup: str):
    lookup = lookup.replace("[","").replace("]","").replace("'","")
    lookup_list=lookup.split(",")
    
    tag = "$$BULLET_TEMPLATE$$"
    lookup_block = "<ul>" + tag + "</ul>"


    bullets = mk_bullet(lookup_list)
    lookup_block = lookup_block.replace(tag,bullets)

    return lookup_block

def fields (customobject : obj.CustomObject) -> str:
    if customobject.has_fields:
        tag = "$$CELL_ROW_BLOCK$$"
        
        ROW_BLOCK = '''<tr><td><p>$$FIELD_NAME$$</p></td>
<td><p>$$FIELD_API$$</p></td>
<td><p>$$FIELD_DESCRIPTION$$</p></td>
<td><p>$$FIELD_TYPE$$</p></td>
<td><p>$$FIELD_LOOKUP$$</p></td>
<td><p>$$PERM_R$$</p></td>
<td><p>$$PERM_W$$</p></td></tr>'''

        FIELD_BLOCK = '''<h1><ac:emoticon ac:name="blue-star" ac:emoji-shortname=":pencil:" ac:emoji-id="1f4dd" ac:emoji-fallback="📝" /> Champs</h1>
<p />
<table data-layout="default" ac:local-id="d4426775-a8b5-4b30-82a2-d71621c87aca"><colgroup><col style="width: 170.0px;" /><col style="width: 170.0px;" /><col style="width: 170.0px;" /><col style="width: 170.0px;" /></colgroup>
<tbody>
<tr>
<th>
<p><strong>Nom du champ</strong></p></th>
<th>
<p><strong>Nom d&rsquo;API</strong></p></th>
<th>
<p><strong>Description</strong></p></th>
<th>
<p><strong>Type</strong></p></th>
<th>
<p><strong>Lookup Object</strong></p></th>
<th>
<p><strong>PS - Read</strong></p></th>
<th>
<p><strong>PS - Write</strong></p></th></tr>''' + tag + '''
</tbody>
</table>
'''

        field_path = base_path + customobject.nom + "/Fields.xlsx"

        df = pd.read_excel(field_path,engine='openpyxl')

        for row in df.index:
            CELL_ROW_BLOCK = ROW_BLOCK
            for tcol in templ_fields:
                for col in df.columns:
                    if col == tcol:
                        if pd.isnull(df.at[row,col]):
                            value = ""                        
                        elif "PermSet" in tcol and df.at[row,col] != 'nan':
                            value_prep = df.at[row,col]
                            value = "<li>" + value_prep.replace(" | ","</li><li>") + "</li>"
                        elif type(df.at[row,col]) == "str" : 
                            value = df.at[row,col]
                        else:
                            value = str(df.at[row,col])

                        CELL_ROW_BLOCK = CELL_ROW_BLOCK.replace(templ_fields[col],value)
            
            FIELD_BLOCK = FIELD_BLOCK.replace(tag, CELL_ROW_BLOCK + tag)

        value = FIELD_BLOCK.replace(tag,"")

    else:
        value = ""

    return value


def rt (customobject : obj.CustomObject) -> str:
    if customobject.has_rt:
        tag = "$$CELL_ROW_BLOCK$$"
        
        ROW_BLOCK = '''<tr>
<td>
<p><strong>$$RT_NAME$$</strong></p></td>
<td>
<p>$$RT_API$$</p></td></tr>'''

        RT_BLOCK = '''<p />
<h1><ac:emoticon ac:name="blue-star" ac:emoji-shortname=":busts_in_silhouette:" ac:emoji-id="1f465" ac:emoji-fallback="👥" /> Record Types</h1>
<table data-layout="default" ac:local-id="df4dfa0f-eb9a-4279-9cfe-d0df8b036a91"><colgroup><col style="width: 176.0px;" /><col style="width: 274.0px;" /></colgroup>
<tbody>
<tr>
<th>
<p><strong>Nom</strong></p></th>
<th>
<p><strong>API Name</strong></p></th></tr>''' + tag + '''
</tbody></table>
''' 

        rt_path = base_path + customobject.nom + "/RecordTypes.xlsx"

        df = pd.read_excel(rt_path,engine='openpyxl')

        for row in df.index:
            CELL_ROW_BLOCK = ROW_BLOCK
            for tcol in templ_rt:
                for col in df.columns:
                    if col == tcol:
                        if pd.isnull(df.at[row,col]):
                            value = ""                        
                        elif type(df.at[row,col]) == "str" : 
                            value = df.at[row,col]
                        else:
                            value = str(df.at[row,col])

                        CELL_ROW_BLOCK = CELL_ROW_BLOCK.replace(templ_rt[col],value)
            
            RT_BLOCK = RT_BLOCK.replace(tag, CELL_ROW_BLOCK + tag)

        value = RT_BLOCK.replace(tag,"")

        return value
    else:
        return ""


def vr (customobject : obj.CustomObject) -> str:
    
    if customobject.has_vr:
        tag = "$$CELL_ROW_BLOCK$$"
        
        ROW_BLOCK = '''<tr>
<td>
<p><strong>$$VR_NAME$$</strong></p></td>
<td>
<p><ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="f2ab5b40-4be0-41c9-8a07-d083827f74f0"><ac:parameter ac:name="title">$$VR_ACTIVE$$</ac:parameter><ac:parameter ac:name="colour">$$COLOR$$</ac:parameter></ac:structured-macro> </p></td>
<td>
<p>$$VR_DESCR$$</p></td></tr>'''

        VR_BLOCK = '''<p />
<h1><ac:emoticon ac:name="blue-star" ac:emoji-shortname=":busts_in_silhouette:" ac:emoji-id="1f465" ac:emoji-fallback="👥" /> Validation Rules</h1>
<table data-layout="default" ac:local-id="78e2c93d-166c-4748-99bc-10662c2cf6cf"><colgroup><col style="width: 186.0px;" /><col style="width: 194.0px;" /><col style="width: 380.0px;" /></colgroup>
<tbody>
<tr>
<th>
<p><strong>Nom</strong></p></th>
<th>
<p><strong>Active</strong></p></th>
<th>
<p><strong>Description</strong></p></th></tr>''' + tag + '''</tbody></table>'''

        vr_path = base_path + customobject.nom + "/ValidationRules.xlsx"

        df = pd.read_excel(vr_path,engine='openpyxl')

        for row in df.index:
            CELL_ROW_BLOCK = ROW_BLOCK
            for tcol in templ_vr:
                for col in df.columns:
                    if col == tcol:
                        if pd.isnull(df.at[row,col]):
                            value = ""                        
                        elif type(df.at[row,col]) == "str" : 
                            value = df.at[row,col]
                        elif type(df.at[row,col]) == "bool" :
                            if df.at[row,col] :
                                CELL_ROW_BLOCK.replace("$$COLOR$$","Green")
                                value = "Oui"
                            else:
                                CELL_ROW_BLOCK.replace("$$COLOR$$","Red")
                                value = "Non"
                        else:
                            value = str(df.at[row,col])

                        CELL_ROW_BLOCK = CELL_ROW_BLOCK.replace(templ_vr[col],value)
            
            VR_BLOCK = VR_BLOCK.replace(tag, CELL_ROW_BLOCK + tag)

        value = VR_BLOCK.replace(tag,"")

        return value
    else:
        return ""