#Importing math module
import math

# Creating classes
class Shape():
    def __init__(self):
       pass
    
    def getArea(): # We cannot calculate area if we do not know the shape
        pass

class Rectangle(Shape):
    def __init__(self, l, w):
        self.length = l
        self.width = w

    def getArea(self):
        return self.length * self.width

class Circle(Shape):
    def __init__(self, r):
          self.radius = r

    def getArea(self):
        return self.radius * self.radius * math.pi
    
class Triangle(Shape):
    def __init__(self, b, h):
        self.base = b
        self.height = h
    
    def getArea(self):
        return self.base * self.height / 2
 
# read txt file
file = open(r"C:\Users\barca\OneDrive\Desktop\School\24_Spring\GEOG676\Cruz-GEOG676-Spring2024\Lab_3\Lab3_code.txt", "r")

polygons = file.readlines()

file.close()

for line in polygons:
    content = line.split(",")
    shape =  content[0]

    if shape == 'Rectangle':
        rect = Rectangle(int(content[1]), int(content[2]))
        print("Area of Rectangle = ", rect.getArea())
    
    elif shape == "Circle":
        cir = Circle(int(content[1]))
        print("Area of a Circle = ", cir.getArea())
    
    elif shape == 'Triangle':
        tri = Triangle(int(content[1]), int(content[2]))
        print("Area of a Triangle = ", tri.getArea())
    else:
        pass