import parsers.parse_flow as fl
import parsers.parse_object as ob

def parse_metadata(type: str, path: str):

    if type == "flow":
#         try:
        fl.parse(path)
#            return True 
#         except:
#             return False
    elif type == "object":
#         try:
        ob.parse(path)
#             return True 
#        except:
#             return False