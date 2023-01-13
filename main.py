import parse as p
import generate_doc as doc

path = "/mnt/c/Users/bigdi/cettefamille_sf/force-app/main/default"

#p.parse_metadata("flow", path)
p.parse_metadata("object", path)

#doc.create_and_send_from_template("flow",True)
#doc.create_and_send_from_template("object",True)
