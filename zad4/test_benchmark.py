import unittest
import sys
import os
import time
import subprocess
import socket

# Добавляем путь к папке zad4, чтобы можно было импортировать benchmark
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    import benchmark
    HAS_BENCHMARK = True
except ImportError as e:
    print(f"Ошибка импорта benchmark: {e}")
    HAS_BENCHMARK = False


class TestBenchmark(unittest.TestCase):
    
    @unittest.skipUnless(HAS_BENCHMARK, "Модуль benchmark не доступен")
    def test_python_heavy_work(self):
        """Тест: проверка, что тяжёлая Python-функция возвращает число"""
        result = benchmark.python_heavy_work()
        self.assertIsInstance(result, int)
        self.assertGreater(abs(result), 0)
        
    @unittest.skipUnless(HAS_BENCHMARK, "Модуль benchmark не доступен")
    def test_rust_heavy_work(self):
        """Тест: проверка, что Rust-функция возвращает число (если доступна)"""
        if benchmark.HAS_RUST:
            result = benchmark.rust_heavy_work()
            self.assertIsInstance(result, int)
            self.assertGreater(abs(result), 0)
        else:
            print("Тест Rust пропущен: модуль не загружен")
            
    @unittest.skipUnless(HAS_BENCHMARK, "Модуль benchmark не доступен")
    def test_server_connection(self):
        """Тест: проверка, что Go-сервер запускается и принимает соединения"""
        # Запускаем сервер в фоне
        server_process = None
        try:
            server_process = benchmark.start_go_server()
            self.assertIsNotNone(server_process, "Сервер не запустился")
            
            # Ждём немного, чтобы сервер точно запустился
            time.sleep(1)
            
            # Пытаемся подключиться
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect(('127.0.0.1', 8081))
                s.sendall(b"Test\n")
                response = s.recv(1024)
                self.assertGreater(len(response), 0)
                
        finally:
            if server_process:
                server_process.terminate()
                server_process.wait(timeout=5)

    @unittest.skipUnless(HAS_BENCHMARK, "Модуль benchmark не доступен")
    def test_go_service_work(self):
        """Тест: проверка, что Go-сервис возвращает результат"""
        # Запускаем сервер
        server_process = benchmark.start_go_server()
        self.assertIsNotNone(server_process, "Сервер не запустился")
        
        try:
            time.sleep(1)  # Даём серверу время на старт
            result = benchmark.go_service_work()
            self.assertIsInstance(result, int)
            self.assertGreater(abs(result), 0)
            
        finally:
            if server_process:
                server_process.terminate()
                server_process.wait(timeout=5)


if __name__ == '__main__':
    unittest.main()