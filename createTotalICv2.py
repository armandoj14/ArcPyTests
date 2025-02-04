#### File to take cross sections, make maps

## Import modules
import arcpy
import csv
import os
import shutil

## Set workspace
arcpy.env.workspace = 'C:\Users\98226\Documents\\testPythonFiles\\testIC'

## Create Total IC Layer
# Set local variables
xy_tol = ""

## IC Layers from X:\
ic_comm = "X:\stormdat\public\impervious_surface\old\Commercial_Impervious.shp"
ic_sf = "X:\stormdat\public\impervious_surface\old\Singlefamily_Impervious.shp"
ic_other = "X:\stormdat\public\impervious_surface\old\Impervious_Surface_Other.shp"

## Merge them to...
out_feat = "TotalIC_31July2017.shp"

## Need to do this field mapping thing to get around a write error, suspected
## related to non matching fields in the IC layers to merged. To-do: learn pyth
fieldMappings = arcpy.FieldMappings()
fieldMappings.addTable(ic_comm)
fieldMappings.addTable(ic_sf)
fieldMappings.addTable(ic_other)

for field in fieldMappings.fields:
    if field.name not in ["impervious", "st_area_sh", "subtheme", "Shape_STAr", "Subtheme", "jurisdicti"]:
        fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(field.name))

arcpy.Merge_management([ic_comm, ic_sf, ic_other], out_feat, fieldMappings)

######################### Geometry ##########################################
arcpy.AddField_management("TotalIC_31July2017.shp", "areaSF", "FLOAT", 16, 1, "",
                          "temp", "NULLABLE", "REQUIRED")

arcpy.CalculateField_management("TotalIC_31July2017.shp", "areaSF",
                                "!shape.area@squarefeet!", "PYTHON_9.3", "")



