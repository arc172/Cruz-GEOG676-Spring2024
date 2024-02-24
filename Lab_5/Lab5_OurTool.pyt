# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5 Toolbox"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName = "GDB Folder",
        name = "GDBFolder",
        datatype = "DEFolder",
        parameterType = "Required",
        direction = "Input"
        )

        param1 = arcpy.Parameter(
        displayName = "GDB Name",
        name = "GDBName",
        datatype = "GPString",
        parameterType = "Required",
        direction = "Input"
        )

        param2 = arcpy.Parameter(
        displayName = "Garage CSV File",
        name = "GarageCSV",
        datatype = "DEFile",
        parameterType = "Required",
        direction = "Input"
        )

        param3 = arcpy.Parameter(
        displayName = "Garage Layer Name",
        name = "GarageLayerName",
        datatype = "GPString",
        parameterType = "Required",
        direction = "Input"
        )

        param4 = arcpy.Parameter(
        displayName = "Campus GDB",
        name = "Campus GDB",
        datatype = "DEType",
        parameterType = "Required",
        direction = "Input"
        )

        param5 = arcpy.Parameter(
        displayName = "Buffer Distance",
        name = "BufferDistance",
        datatype = "GPDouble",
        parameterType = "Required",
        direction = "Input"
        )

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Creating a geodatabase
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        gdb_path = folder_path + "\\" + gdb_name    # Path to our geodatabase
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        #reading our csv and turning it into a feature class.
        csv = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        garages = arcpy.management.MakeXYEventLayer(csv, "X", "Y", garage_layer_name)

        # Adding data to our geodatabase
        input_layers = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layers, gdb_path)
        garage_points = gdb_path + '\\' + garage_layer_name

        # Opening and Copying data from another geodatabase and adding it to ours. 
        campus = parameters[4].valueAsText
        buildings_campus = campus + "\\Structures"
        buildings = gdb_path + '\\' + "Buildings"

        arcpy.management.CopyFeatures(buildings_campus, buildings)

        # Reprojection
        spatial_ref = arcpy.Describe(buildings).spatialReference    #Grabbing the spatial reference of this layer
        arcpy.Project_management(garage_layer_name, gdb_path + "\garage_points_reprojected", spatial_ref) #Applying it here


        # Buffer Garages
        buffer_distance = int(parameters[5].value)
        garage_buffed = arcpy.Buffer_analysis(gdb_path +"\garage_points_reprojected", gdb_path + "garage_points_buffer", 150)

        # Intersection of buffer with the buildings.
        arcpy.Intersect_analysis([garage_buffed, buildings], gdb_path + "/garage_buildings_intercept", "ALL")

        # Output to Table
        arcpy.TableToTable_conversion(gdb_path + "/garage_buildings_intercept.dbf", r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_5", "nearby_buildings.csv")
        
        return None

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return