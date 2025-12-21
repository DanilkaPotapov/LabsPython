from lab_python_oop.figure import GeometricFigure
from lab_python_oop.color import Color
import math

class Circle(GeometricFigure):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = Color(color)

    def area(self):
        return math.pi * self.radius ** 2

    def __repr__(self):
        return "Круг: радиус = {}, цвет = {}, площадь = {}".format(self.radius, self.color.color, self.area())
