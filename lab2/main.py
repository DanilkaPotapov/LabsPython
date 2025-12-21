from lab_python_oop.rectangle import Rectangle
from lab_python_oop.circle import Circle
from lab_python_oop.square import Square

def main():
    N = 5
    rectangle = Rectangle(N, N, 'синий')
    print(rectangle)

    circle = Circle(N, 'зеленый')
    print(circle)

    square = Square(N, 'красный')
    print(square)

    import requests
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    print(response.json())

if __name__ == '__main__':
    main()
