import math
import threading
import timeit

# Глобальная переменная для хранения результата интеграла
integral_result = 0.0

# Lock для синхронизации доступа к результату
result_lock = threading.Lock()

def integrate_thread(f, a, b, n_iter, start, end):
    """
    Вычисление части интеграла в потоке.
    f: функция для интегрирования
    a, b: границы интегрирования
    n_iter: общее количество итераций
    start, end: индексы для данного потока, определяют, какие части работы он выполняет
    """
    width = (b - a) / n_iter  # ширина каждого прямоугольника
    local_area = 0.0

    for i in range(start, end):
        x = a + i * width  # левый угол прямоугольника
        local_area += f(x) * width  # вычисление площади прямоугольника

    # Синхронизируем запись в общую переменную
    with result_lock:
        global integral_result
        integral_result += local_area

def integrate(f, a, b, n_iter=1000, n_threads=4):
    """
    Численное интегрирование с использованием потоков.

    f: функция для интегрирования
    a, b: границы интегрирования
    n_iter: количество итераций
    n_threads: количество потоков
    """
    # Число итераций на каждый поток
    iterations_per_thread = n_iter // n_threads

    threads = []

    # Разделяем работу между потоками
    for i in range(n_threads):
        start = i * iterations_per_thread
        # Последний поток должен обрабатывать оставшиеся итерации
        end = (i + 1) * iterations_per_thread if i < n_threads - 1 else n_iter

        thread = threading.Thread(target=integrate_thread, args=(f, a, b, n_iter, start, end))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

    return integral_result

def integrate_sequential(f, a, b, n_iter=1000):
    """
    Последовательное численное интегрирование методом прямоугольников.
    """
    width = (b - a) / n_iter
    area = 0.0

    for i in range(n_iter):
        x = a + i * width
        area += f(x) * width

    return area

if __name__ == '__main__':
    # Пример для оценки времени последовательного интегрирования
    print("Последовательное интегрирование:")
    result_sequential = integrate_sequential(math.sin, 0, math.pi, n_iter=10000)
    print(f"Интеграл sin(x) от 0 до pi: {result_sequential}")

    # Измеряем время последовательного вычисления
    time_taken_sequential = timeit.timeit("integrate_sequential(math.sin, 0, math.pi, n_iter=10000)",
                                         setup="from __main__ import integrate_sequential, math",
                                         number=1)
    print(f"Время для последовательного решения: {time_taken_sequential} секунд")

    # Пример для многопоточного интегрирования
    print("\nМногопоточное интегрирование:")
    integral_result = 0.0  # сбрасываем глобальную переменную
    result_threaded = integrate(math.sin, 0, math.pi, n_iter=10000, n_threads=4)
    print(f"Интеграл sin(x) от 0 до pi (многопоточно): {result_threaded}")

    # Измеряем время многопоточного вычисления
    time_taken_threaded = timeit.timeit("integrate(math.sin, 0, math.pi, n_iter=10000, n_threads=4)",
                                       setup="from __main__ import integrate, math",
                                       number=1)
    print(f"Время для многопоточного решения: {time_taken_threaded} секунд")

    # Сравнение времени
    print("\nСравнение времени:")
    print(f"Последовательное время: {time_taken_sequential} секунд")
    print(f"Многопоточное время: {time_taken_threaded} секунд")
