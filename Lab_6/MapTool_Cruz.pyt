# -*- coding: utf-8 -*-

import arcpy
import time 

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "GraduatedColor"
        self.description = "Create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        # original project name
        param0 = arcpy.Parameter(
        displayName = "Project Name",
        name = "aprxInputName",
        datatype = "DEFile",
        parameterType = "Required",
        direction = "Input"
        )
        # which layer you want to clasify to create a color map
        param1 = arcpy.Parameter(
        displayName = "Layer to Classify",
        name = "LayertoClassify",
        datatype = "GPLayer",
        parameterType = "Required",
        direction = "Input"
        )
        # output folder location
        param2 = arcpy.Parameter(
        displayName = "Output Location",
        name = "OutputLocation",
        datatype = "DEFolder",
        # parameterType = "Required",
        direction = "Input"
        )
        # output project name
        param3 = arcpy.Parameter(
        displayName = "Output Project Name",
        name = "outputProjectName",
        datatype = "GPString",
        parameterType = "Required",
        direction = "Input"
        )

        params = [param0, param1, param2, param3]
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
        
  # Define Progressor Variables
        readTime = 3
        start = 0
        max = 100
        step = 25
        # Setup Progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) # pause execution for read time
        
        # Add Message to the Results Pane
        arcpy.AddMessage("Validating Project File...")

        # Location of Project File
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)
        
        # Grabs the First Instance of a Map from the .aprx
        campus = project.listMaps("Map")[0]

        # Increment Progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Locating Map...")
        time.sleep(readTime)
        arcpy.SetProgressorLabel("Checking Map...")
        
        # Loop through the layers of the map
        for layer in campus.listLayers():

            # Check if the layer is a feature layer
            if layer.isFeatureLayer:
                # Copy the layer's symbology
                symbology = layer.symbology
                # Make sure the symbology has renderer attribute
                if hasattr(symbology, 'renderer'):
                # Check layer name
                    if layer.name == parameters[1].valueAsText:
                # Increment Progressor
                        arcpy.SetProgressorPosition(start + step * 2)
                        arcpy.SetProgressorLabel("Checking Layer...")
                        time.sleep(readTime)
                        arcpy.SetProgressorLabel("Checking Layer...")
                # Update the Copy's renderer to "Graduated Colors Renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')
                
                # Tell arcpy which field we want to base our chloropleth off of
                        symbology.renderer.classificationField = "Shape_Length" 
                # Increment Progressor
                        arcpy.SetProgressorPosition(start + step * 3)
                        arcpy.SetProgressorLabel("Checking Attributes...")
                        time.sleep(readTime)
                        arcpy.SetProgressorLabel("Checking Attributes...")

                # Set how many classes we'll have for the map
                        symbology.renderer.breakCount = 5
                # Set Color Ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Cyan to Purple')[0]
                # Set the Layer's Actual Symbology equal to the Copy's
                        layer.symbology = symbology

                # Adding a Message
                        arcpy.AddMessage("Finish Generating Layer...")
        else:
            print("No layer was found")
        
        # Increment Progressor
        arcpy.SetProgressorPosition(start + step * 4)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.SetProgressorLabel("Saving...")

        #Param 2 is the folder location and param 3 is the name of the new project.
        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx") # Saving the project as a copy

        
        return
    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
      
        
        return
