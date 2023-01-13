
import parsers.parse_object as o
import metadatasf.object as obj
import metadatasf.layout as la

import config.path as p

path = "/mnt/c/Users/bigdi/cettefamille_sf/force-app/main/default"

#print(f.Flow(path,"BIC_ACT_FL01_QualifNotification").source_obj())
#print(f.Flow(path,"BIC_ACT_FL01_QualifNotification").subflow_count())

lay = la.Layout(p.metadata_path, "Account-Account Layout")

print(lay.fields_list())

co = obj.CustomObject(p.metadata_path,"Account")

name = co.field(co,"DS_TOTAL_JOUR_SOUMIS__c")

print(name.list_layouts())