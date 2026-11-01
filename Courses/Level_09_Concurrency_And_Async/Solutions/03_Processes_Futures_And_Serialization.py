from concurrent.futures import ProcessPoolExecutor

def square(number):
    return number * number

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as executor:
        print(list(executor.map(square, [1, 2, 3])))
