# Importing arcpy

import arcpy

# Setting workspace
arcpy.env.workspace = r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_4"

# Creating a geodatabase
folder_path = r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_4"
gdb_name = "tamu_garages.gdb"
gdb_path = folder_path + "\\" + gdb_name    # Path to our geodatabase
arcpy.CreateFileGDB_management(folder_path, gdb_name)

#reading our csv and turning it into a feature class.
csv = r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_4\garages.csv"
garage_layer_name = "Garage Points"
garages = arcpy.management.MakeXYEventLayer(csv, "X", "Y", garage_layer_name)

# Adding data to our geodatabase
input_layers = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layers, gdb_path)

# Opening and Copying data from another geodatabase and adding it to ours. 
campus = r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_4\Campus.gdb"
buildings_campus = campus + "\\Structures"
buildings = gdb_path + '\\' + "Buildings"

arcpy.management.CopyFeatures(buildings_campus, buildings)

# Reprojection
spatial_ref = arcpy.Describe(buildings).spatialReference    #Grabbing the spatial reference of this layer
arcpy.Project_management(garage_layer_name, gdb_path + "\garage_points_reprojected", spatial_ref) #Applying it here


# Buffer Garages
garage_buffed = arcpy.Buffer_analysis(gdb_path +"\garage_points_reprojected", gdb_path + "garage_points_buffer", 150)

# Intersection of buffer with the buildings.
arcpy.Intersect_analysis([garage_buffed, buildings], gdb_path + "/garage_buildings_intercept", "ALL")

# Output to Table
arcpy.TableToTable_conversion(gdb_path + "/garage_buildings_intercept.dbf", r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_4", "nearby_buildings.csv")
