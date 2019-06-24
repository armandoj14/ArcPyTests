
# Impervious Calculations in a Single Watershed - ArcPy
# By: Armando Jimenez - Charlotte Mecklenburg Stormwater Services

# This is an ArcPy script designed to calculate the area and the percentage of the impervious in each subbasin in a single watershed.
# Multiple steps can be skipped if the required files already exist (watershed impervious layer, etc).
# This script calulcates the impervious in the Reedy Watershed in Mecklenburg County, NC.
# The inputs will vary from watershed to watershed but the process should remain the same if all required files are present in your workspace.
# End goal is to prepare a table to be used in EPA SWMM to perform further watershed analysis.

import arcpy

# This variable can be changed to your directory containing the Reedy data
reedyGISDir = "C:\Users\98226\Documents\ImperviousProjectArcMap\ReedyPython"
arcpy.env.workspace = reedyGISDir

# Only perform the following block if there is no specific watershed impervious layer (takes significant amount of time to process if files are large)
print("Perform a merge operation between the three impervious layers. Merged into cityImpervious")
arcpy.Merge_management(["imperviousLayers\commercialImpervious.shp", "imperviousLayers\\residentialImpervious.shp", "imperviousLayers\otherImpervious.shp"], output= reedyGISDir +reedyGISDir + "\imperviousLayers\cityImpervious.shp")
print("Merging complete")

print("Clip the city impervious to the watershed.")
arcpy.Clip_analysis(in_features="imperviousLayers\cityImpervious.shp", clip_features="reedyShape\ReedyShape.shp", out_feature_class=reedyGISDir + "\imperviousLayers\reedyImpervious.shp", cluster_tolerance="")
print("Clipping complete")

#Only perform the following block if layers don't share the same projection. Change inputs as necessary
print("Project subbasins to be consistent with impervious layer")
arcpy.Project_management(in_dataset="initDelin\ReedySubs871_Diss.shp", out_dataset=reedyGISDir + "\initDelin\ReedySubs871_DissSPNC.shp", out_coor_system="PROJCS['NAD_1983_StatePlane_North_Carolina_FIPS_3200_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',2000000.002616666],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-79.0],PARAMETER['Standard_Parallel_1',34.33333333333334],PARAMETER['Standard_Parallel_2',36.16666666666666],PARAMETER['Latitude_Of_Origin',33.75],UNIT['Foot_US',0.3048006096012192]]", transform_method="", in_coor_system="PROJCS['NAD_1983_North_Carolina',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['false_easting',2000000.002616667],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-79.0],PARAMETER['standard_parallel_1',34.33333333333334],PARAMETER['standard_parallel_2',36.16666666666666],PARAMETER['latitude_of_origin',33.75],UNIT['Foot_US',0.3048006096012192]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
print("Project complete")

print("Create geodatabase to place following table (throws error if not in geodatabase)")
arcpy.CreateFileGDB_management("reedyGISDir + "", "table.gdb")
print("Geodatabase created")

print("Use tabulate intersection to calculate area and percentage of impervious in each subbasin")
arcpy.TabulateIntersection_analysis(in_zone_features="initDelin\ReedySubs871_DissSPNC.shp", zone_fields="GRIDCODE", in_class_features="imperviousLayers\\reedyImpervious.shp", out_table=reedyGISDir + "\\table.gdb\\reedyICpct2", class_fields="", sum_fields="", xy_tolerance="-1 Unknown", out_units="UNKNOWN")
print("Tabulate intersection complete")

print("Join the previous table to the subbasin table to match up areas and percentages (using GRIDCODE)")
arcpy.JoinField_management("initDelin\ReedySubs871_DissSPNC.shp", "GRIDCODE", "table.gdb\\reedyICpct2", "GRIDCODE")
print("Table join complete")

print("Export the attribute table into a csv file to specified location")
arcpy.TableToTable_conversion("initDelin\ReedySubs871_DissSPNC.shp", reedyGISDir , "imperviousReedyTable.csv")
print("Table export complete")

# to be continued -> make it so that the resulting table is ready to be exported to R