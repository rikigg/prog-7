import asyncio
import time
import json
from termcolor import cprint
from pynput.keyboard import Listener, Key
import aiohttp
import ssl

stop_program = False

# 1.1: Простая асинхронная функция для отображения текущего времени
async def display_time():
    try:
        for _ in range(5):  # Для теста ограничим выполнение 5 циклами
            print(time.strftime("%H:%M:%S", time.localtime()), end="\r")
            await asyncio.sleep(1)
        print("\nTask 1.1 completed.")
    except KeyboardInterrupt:
        print("\nExiting...")

# 1.2: Улучшение программы с цветным выводом и обработкой клавиши Esc
def on_press(key):
    global stop_program
    if key == Key.esc:
        stop_program = True
        print("\nExiting program...")
        return False  # Остановить слушатель

async def display_time_with_color():
    while not stop_program:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        cprint(f"Current Time: {current_time}", "yellow", end="\r")
        await asyncio.sleep(1)
    print("\nTask 1.2 completed.")

async def main_1_2():
    listener = Listener(on_press=on_press)
    listener.start()
    await display_time_with_color()

# 1.3: Использование asyncio.gather для выполнения параллельных задач
async def task1():
    await asyncio.sleep(2)
    return "Task 1 completed"

async def task2():
    await asyncio.sleep(3)
    return "Task 2 completed"

async def main_1_3():
    result = await asyncio.gather(task1(), task2())
    print(f"Task 1.3 results: {result}")

# 1.4: Параллельные HTTP-запросы и запрос к базе данных
WEB_SERVER_URL = "https://rnacentral.org/api/v1/rna/"

async def fetch_rna_data():
    # Отключаем проверку сертификатов для тестирования
    async with aiohttp.ClientSession() as session:
        async with session.get(WEB_SERVER_URL, ssl=False) as response:
            data = await response.json()
            print("RNA Data:", json.dumps(data, indent=2))

async def fetch_db_data():
    print("Mock DB Data: [{'column1': 'value1', 'column2': 'value2'}]")

async def main_1_4():
    await asyncio.gather(fetch_rna_data(), fetch_db_data())
    print("Task 1.4 completed.")

# 1.5: Асинхронный веб-скрапер
class AsyncWebScraper:
    def __init__(self, urls):
        self.urls = urls

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:  # Отключаем проверку SSL
                return await response.text()

    async def scrape(self):
        tasks = [self.fetch(url) for url in self.urls]
        return await asyncio.gather(*tasks)

async def main_1_5():
    urls = [
        "https://httpbin.org/get",  # Заменяем URL на рабочий
        "https://jsonplaceholder.typicode.com/posts/1"
    ]
    scraper = AsyncWebScraper(urls)
    pages = await scraper.scrape()
    for i, page in enumerate(pages, 1):
        print(f"Page {i} (first 100 characters): {page[:100]}")
    print("Task 1.5 completed.")

# 1.6: Улучшение веб-скрапера с асинхронным менеджером контекста
class AsyncWebScraperWithContext:
    def __init__(self, urls):
        self.urls = urls

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:  # Отключаем проверку SSL
                return await response.text()

    async def scrape(self):
        tasks = [self.fetch(url) for url in self.urls]
        return await asyncio.gather(*tasks)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

async def main_1_6():
    urls = [
        "https://httpbin.org/get",  # Заменяем URL на рабочий
        "https://jsonplaceholder.typicode.com/posts/2"
    ]
    async with AsyncWebScraperWithContext(urls) as scraper:
        pages = await scraper.scrape()
        for i, page in enumerate(pages, 1):
            print(f"Page {i} (first 100 characters): {page[:100]}")
    print("Task 1.6 completed.")

# 1.7: Асинхронный сервер и клиент
async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message} from {addr}")

    response = json.dumps({"message": "Echo: " + message})
    writer.write(response.encode())
    await writer.drain()
    print("Closing the connection")
    writer.close()

async def server():
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888, ssl=ssl_context)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

async def client():
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, ssl=ssl_context)
    message = "Hello, Server!"
    writer.write(message.encode())
    await writer.drain()
    response = await reader.read(100)
    print(f"Received: {response.decode()}")
    writer.close()

async def main_1_7():
    server_task = asyncio.create_task(server())
    await asyncio.sleep(1)  # Даем серверу время запуститься
    await client()
    server_task.cancel()
    print("Task 1.7 completed.")

# Основная функция для запуска всех задач последовательно
async def main():
    # Задача 1.1
    print("Running task 1.1 (Display time in infinite loop)")
    await display_time()

    # Задача 1.2
    print("\nRunning task 1.2 (Display time with color and Esc key detection)")
    await main_1_2()

    # Задача 1.3
    print("\nRunning task 1.3 (Use asyncio.gather for concurrent tasks)")
    await main_1_3()

    # Задача 1.4
    print("\nRunning task 1.4 (Parallel requests to web server and DB)")
    await main_1_4()

    # Задача 1.5
    print("\nRunning task 1.5 (Asynchronous Web Scraper)")
    await main_1_5()

    # Задача 1.6
    print("\nRunning task 1.6 (Improved Async Web Scraper with context manager)")
    await main_1_6()

    # Задача 1.7
    print("\nRunning task 1.7 (Async HTTPS server and client for echo)")
    await main_1_7()

if __name__ == "__main__":
    asyncio.run(main())
