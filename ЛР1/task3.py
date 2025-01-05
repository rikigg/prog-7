import math
import timeit
import time  # Добавить импорт модуля time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from functools import partial
from threading import Lock, Event, Barrier
import requests
import threading
import os
import random

# 2.1: Интегрирование с использованием многопоточности/многопроцессности
def integrate(f, a, b, *, n_iter=1000):
    step = (b - a) / n_iter
    return sum(f(a + i * step) for i in range(n_iter))

def integrate_async(f, a, b, *, n_jobs=2, n_iter=1000):
    # Создаем пул потоков/процессов перед тем, как отправлять задачи
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        spawn = partial(integrate, f, n_iter=n_iter // n_jobs)
        step = (b - a) / n_jobs
        fs = [executor.submit(spawn, a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
        return sum(f.result() for f in as_completed(fs))

def time_integration():
    n_iter = 10**6
    for n_jobs in [2, 4, 6]:
        # Thread pool
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            start_time = timeit.default_timer()
            result = integrate_async(math.atan, 0, math.pi / 2, n_jobs=n_jobs, n_iter=n_iter)
            elapsed = timeit.default_timer() - start_time
            print(f"Thread pool with {n_jobs} jobs: {elapsed:.4f} seconds")

        # Process pool
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            start_time = timeit.default_timer()
            result = integrate_async(math.atan, 0, math.pi / 2, n_jobs=n_jobs, n_iter=n_iter)
            elapsed = timeit.default_timer() - start_time
            print(f"Process pool with {n_jobs} jobs: {elapsed:.4f} seconds")

# 2.2: Банк с использованием потоков и Lock для синхронизации
class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.lock = Lock()

    def deposit(self, amount):
        with self.lock:
            self.balance += amount

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
            else:
                print("Insufficient funds")

def simulate_bank():
    account = BankAccount()
    threads = []
    for _ in range(10):
        t = threading.Thread(target=account.deposit, args=(random.randint(1, 100),))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final balance: {account.balance}")

# 2.3: Асинхронное скачивание изображений с использованием Future и Semaphore
def download_image(url, semaphore):
    with semaphore:
        print(f"Downloading {url}")
        response = requests.get(url)
        with open(url.split("/")[-1], 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {url}")

def download_images():
    urls = [
        "https://i.pinimg.com/originals/92/d9/63/92d9635810a41f3e8aa292dd11b7fc51.jpg",
        "https://avatars.mds.yandex.net/get-mpic/6434027/img_id2799273281828521393.png/orig",
        "https://main-cdn.sbermegamarket.ru/big2/hlr-system/-12/044/576/642/717/34/600000325185b0.jpg"
    ]
    semaphore = threading.Semaphore(2)  # Limit to 2 concurrent downloads
    futures = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for url in urls:
            futures.append(executor.submit(download_image, url, semaphore))
        for future in futures:
            future.result()

# 2.4: Запись и чтение файла с синхронизацией с использованием Future
def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)

def read_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def file_operations():
    file_name = "file.txt"
    data = "This is a test."

    with ThreadPoolExecutor(max_workers=2) as executor:
        write_future = executor.submit(write_to_file, file_name, data)
        write_future.result()  # Wait until writing is complete
        read_future = executor.submit(read_from_file, file_name)
        print(f"File content: {read_future.result()}")

# 2.5: Синхронизация потоков с использованием Event
def event_simulation():
    event = Event()

    def thread1():
        while not event.is_set():
            print("Thread 1: Event not occurred")
            time.sleep(1)
        print("Thread 1: Event occurred")

    def thread2():
        time.sleep(3)
        event.set()
        print("Thread 2: Event set")

    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

# 2.6: Очередь с использованием RLock для синхронизации
class QueueWithRLock:
    def __init__(self):
        self.queue = []
        self.lock = threading.RLock()

    def enqueue(self, item):
        with self.lock:
            self.queue.append(item)

    def dequeue(self):
        with self.lock:
            if self.queue:
                return self.queue.pop(0)
            return None

def queue_operations():
    q = QueueWithRLock()
    for i in range(5):
        threading.Thread(target=q.enqueue, args=(i,)).start()
    for _ in range(5):
        threading.Thread(target=q.dequeue).start()

# 2.7: Барьер для синхронизации серверного и клиентского потоков
def server():
    print("Server is ready")
    barrier.wait()

def client():
    print("Client is waiting for the server")
    barrier.wait()
    print("Client sending request to server")

barrier = threading.Barrier(2)

def server_client_simulation():
    t1 = threading.Thread(target=server)
    t2 = threading.Thread(target=client)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

# 2.8: Параллельный поиск файла в директории с использованием потоков
def search_file_in_directory(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern in file:
                print(f"Found: {file}")
                return True
    return False

def parallel_file_search():
    directory = "."
    pattern = "test"
    found_event = threading.Event()  # Event для синхронизации поиска

    def search_thread():
        if not found_event.is_set():
            result = search_file_in_directory(directory, pattern)
            if result:
                found_event.set()  # Если найдено, установить Event

    threads = []
    for _ in range(3):
        t = threading.Thread(target=search_thread)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Основной запуск программы
if __name__ == '__main__':
    # 2.1: Замеры времени интегрирования с использованием многопоточности и многопроцессности
    print("Benchmarking integration...")
    time_integration()

    # 2.2: Банк
    print("\nSimulating bank transactions...")
    simulate_bank()

    # 2.3: Скачивание изображений
    print("\nDownloading images...")
    download_images()

    # 2.4: Запись и чтение файла
    print("\nFile operations...")
    file_operations()

    # 2.5: Синхронизация с Event
    print("\nEvent simulation...")
    event_simulation()

    # 2.6: Очередь с RLock
    print("\nQueue with RLock operations...")
    queue_operations()

    # 2.7: Сервер и клиент
    print("\nServer-client simulation...")
    server_client_simulation()

    # 2.8: Параллельный поиск файла
    print("\nParallel file search...")
    parallel_file_search()
