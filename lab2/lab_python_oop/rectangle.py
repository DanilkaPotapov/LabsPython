from lab_python_oop.figure import GeometricFigure
from lab_python_oop.color import Color

class Rectangle(GeometricFigure):
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = Color(color)

    def area(self):
        return self.width * self.height

    def __repr__(self):
        return "Прямоугольник: ширина = {}, высота = {}, цвет = {}, площадь = {}".format(self.width, self.height, self.color.color, self.area())
