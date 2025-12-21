from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    @abstractmethod
    def area(self):
        """Метод для вычисления площади фигуры"""
        pass

    @abstractmethod
    def __repr__(self):
        """Метод для строкового представления фигуры"""
        pass