import threading
import requests

# 1.1 Программа, которая создаёт несколько потоков, а затем выводит их имена изнутри каждого потока
def print_thread_name():
    # Каждый поток выводит своё имя
    print(f"Поток с именем: {threading.current_thread().name}")

def part_1_1():
    threads = []
    # Создаём несколько потоков
    for i in range(5):
        thread = threading.Thread(target=print_thread_name, name=f"Поток-{i+1}")
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

# 1.2 Программа для одновременной загрузки нескольких файлов (например, картинок) с использованием потоков
def download_file(url, file_name):
    print(f"Скачивание файла с URL: {url} в {file_name}")
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f"Файл {file_name} скачан!")

def part_1_2():
    urls = [
        "https://i.pinimg.com/originals/92/d9/63/92d9635810a41f3e8aa292dd11b7fc51.jpg",
        "https://avatars.mds.yandex.net/get-mpic/6434027/img_id2799273281828521393.png/orig",
        "https://main-cdn.sbermegamarket.ru/big2/hlr-system/-12/044/576/642/717/34/600000325185b0.jpg"
    ]

    threads = []
    for idx, url in enumerate(urls):
        thread = threading.Thread(target=download_file, args=(url, f"image{idx+1}.jpg"))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

# 1.3 Программа для одновременных HTTP-запросов с использованием потоков
def send_request(url):
    print(f"Отправка HTTP-запроса на {url}")
    response = requests.get(url)
    print(f"Ответ от {url}: {response.status_code}")

def part_1_3():
    urls = [
        "https://www.google.com",
        "https://www.google.com",
        "https://www.google.com"
    ]

    threads = []
    for url in urls:
        thread = threading.Thread(target=send_request, args=(url,))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

# 1.4 Программа для вычисления факториала числа с использованием нескольких потоков
def factorial(n, result, idx):
    fact = 1
    for i in range(1, n + 1):
        fact *= i
    result[idx] = fact

def part_1_4():
    numbers = [5, 7, 10]  # Пример чисел для вычисления факториала
    result = [None] * len(numbers)
    threads = []

    for idx, number in enumerate(numbers):
        thread = threading.Thread(target=factorial, args=(number, result, idx))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

    # Выводим результаты
    for idx, number in enumerate(numbers):
        print(f"Факториал числа {number} = {result[idx]}")

# 1.5 Программа для реализации многопоточного алгоритма быстрой сортировки
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def quicksort_thread(arr, result, idx):
    sorted_arr = quicksort(arr)
    result[idx] = sorted_arr

def part_1_5():
    arrays = [
        [10, 7, 8, 9, 1, 5],
        [3, 6, 2, 8, 4, 7],
        [50, 23, 9, 18, 61, 32]
    ]

    result = [None] * len(arrays)
    threads = []

    for idx, array in enumerate(arrays):
        thread = threading.Thread(target=quicksort_thread, args=(array, result, idx))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

    # Выводим отсортированные массивы
    for idx, array in enumerate(arrays):
        print(f"Отсортированный массив {idx+1}: {result[idx]}")

# Основной запуск программы
if __name__ == '__main__':
    print("Часть 1.1: Потоки, выводящие свои имена")
    part_1_1()

    print("\nЧасть 1.2: Одновременная загрузка нескольких файлов")
    part_1_2()

    print("\nЧасть 1.3: Одновременные HTTP-запросы")
    part_1_3()

    print("\nЧасть 1.4: Вычисление факториала числа с использованием нескольких потоков")
    part_1_4()

    print("\nЧасть 1.5: Многопоточный алгоритм быстрой сортировки")
    part_1_5()
