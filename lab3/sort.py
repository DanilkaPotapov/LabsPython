data = [4, -30, 30, 100, -100, 123, 1, 0, -1, -4]

if __name__ == '__main__':
    result = sorted(data, key=lambda x: -abs(x))
    print("С lambda:", result)
    
    result_without_lambda = sorted(data, key=abs, reverse=True)
    print("Без lambda:", result_without_lambda)