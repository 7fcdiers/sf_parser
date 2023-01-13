import json, os
from utils.bullet import mk_bullet
import config.path as p

path = os.getcwd() + "/" + p.output_path + "/flow/Flow.xlsx"

name = "API Name"
page_name = name

color_colum = "Status"

templ = {'Flow Name' : "$$NOM$$",
        'API Name' : "$$API$$",
        'Type' : "$$TYPE$$",
        'Schedule' : "$$SCHEDULE$$",
        'Source object' : "$$OBJ$$",
        'Status' : "$$STATUS$$",
        'Description' : "$$DESCR$$",
        'Step Count' : "$$STEPS$$",
        'Step Detail' : "$$STEP_BLOCK_DETAIL$$",
        'Subflow List' : "$$SUBFL$$",
        'Quick Actions' : "$$QA$$",
        'Pages' : "$$PAGES$$",
        'Called by' : "$$CALLED$$"
        }

parent_page_is_column = True
parent_page = "Source object"
parent_of_parent = "Process automation"

specifics = {'Step Detail' : "steps"}

specifics_param = {'Step Detail' : 'Step Count'}

def steps(total: int, detail: str) -> str:
        detail_dict = json.loads(detail.replace("'",'"'))
        dict_as_list = []
        tag = "$$BULLET_TEMPLATE$$"
        step_block = "<ul>" + tag + "</ul>"

        if total == 0 :
                return ""
        else:
                for key in detail_dict:
                        dict_as_list.append(key + " : " + str(detail_dict[key]))

        bullets = mk_bullet(dict_as_list)
        step_block = step_block.replace(tag,bullets)

        return step_block



