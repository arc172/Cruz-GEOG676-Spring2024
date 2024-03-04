import arcpy
import arcpy.sa
from arcpy import env

#Location of data
source = r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_7"
band1 = arcpy.sa.Raster(source + r"\band1.tif") # blue
band2 = arcpy.sa.Raster(source + r"\band2.tif") # green
band3 = arcpy.sa.Raster(source + r"\band3.tif") # red
band4 = arcpy.sa.Raster(source + r"\band4.tif") # NIR

# Composite Image- True Color
composite = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\combined_bands.tif")

# hillshade
azimuth = 180
altitude = 50
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.ddd.HillShade(source + r"\DEM.tif", source + "/sm_hillshade.tif", azimuth, altitude, shadows, z_factor)

# slope
output_measurement = "DEGREE"
z_factor = 1
method = "PLANAR"
z_unit = "METER"
arcpy.ddd.Slope(source + r"\DEM.tif", source + "/sm_slope.tif",output_measurement, z_factor, method, z_unit)
print("Success")