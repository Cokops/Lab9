import time
import subprocess
import socket
import sys
import os
import math

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ========== 1. ПОДКЛЮЧЕНИЕ RUST ==========
# Путь к скомпилированной Rust-библиотеке из zad3
rust_path = os.path.join(PROJECT_DIR, 'zad3', 'target', 'release')
sys.path.insert(0, rust_path)

# Альтернативный путь — если библиотека в debug
rust_debug_path = os.path.join(PROJECT_DIR, 'zad3', 'target', 'debug')
sys.path.insert(0, rust_debug_path)

HAS_RUST = False
try:
    import rust_python_struct
    HAS_RUST = True
    print(f"Rust-модуль загружен из {rust_python_struct.__file__}")
except ImportError as e:
    print(f"Rust-модуль не загружен: {e}")
    print(f"   Искали в: {rust_path}")
    print(f"   И в: {rust_debug_path}")


# ========== 2. PYTHON С РЕАЛЬНОЙ НАГРУЗКОЙ ==========
def python_heavy_work():
    """Тяжёлая Python операция — вычисления, чтобы время было измеримым"""
    total = 0
    # 100,000 итераций для измеримого времени
    for i in range(100000):
        # Вычисления с плавающей точкой
        total += math.sqrt(i) * math.sin(i) + math.cos(i) * math.log(i + 1)
        # Немного строковых операций
        s = f"Number_{i}"
        total += len(s) * (i % 10)
    return int(total) % 1000000


# ========== 3. RUST С РЕАЛЬНОЙ НАГРУЗКОЙ ==========
def rust_heavy_work():
    """Использует Rust-библиотеку с созданием объектов"""
    if not HAS_RUST:
        return 0
    
    total = 0
    # 10,000 объектов (меньше чем Python, так как FFI имеет накладные расходы)
    for i in range(10000):
        try:
            person = rust_python_struct.Person(f"Person_{i}", 20 + (i % 50))
            # Вызываем методы
            greeting = person.greet()
            total += len(greeting)
            if i % 2 == 0:
                person.have_birthday()
                total += person.age
        except Exception as e:
            print(f"Rust ошибка: {e}")
    return total % 1000000


# ========== 4. GO СЕРВИС ==========
def start_go_server():
    """Запускает Go-сервер и ждёт готовности"""
    go_path = os.path.join(PROJECT_DIR, 'zad4', 'server.go')
    if not os.path.exists(go_path):
        print(f"Файл не найден: {go_path}")
        return None
    
    print("Запуск Go-сервера...")
    process = subprocess.Popen(
        ['go', 'run', go_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=os.path.dirname(go_path)
    )
    
    # Ждём готовности (проверяем порт 8081)
    for attempt in range(15):
        time.sleep(0.5)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(('127.0.0.1', 8081))
                print(f"Go-сервер готов (попытка {attempt + 1})")
                return process
        except ConnectionRefusedError:
            continue
    
    print("Go-сервер не запустился")
    process.terminate()
    return None


def go_service_work():
    """Отправляет запросы к Go-сервису через TCP"""
    results = []
    for i in range(1000):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect(('127.0.0.1', 8081))
                s.sendall(f"Тест {i}\n".encode())
                response = s.recv(1024).decode()
                results.append(len(response))
        except Exception:
            results.append(0)
    return sum(results) % 1000000


# ========== 5. ЗАПУСК БЕНЧМАРКА ==========
def run_benchmark():
    print("\n" + "="*70)
    print(" БЕНЧМАРК: Сравнение производительности")
    print("="*70)
    
    results = {}
    
    # 1. Python
    print("\n1. Python нативный...")
    start = time.perf_counter()
    py_result = python_heavy_work()
    py_time = time.perf_counter() - start
    results['Python'] = py_time
    print(f"   Время: {py_time:.4f} сек ({py_time*1000:.2f} мс)")
    print(f"   Результат: {py_result}")
    
    # 2. Python + Rust
    print("\n2. Python + Rust...")
    if HAS_RUST:
        start = time.perf_counter()
        rust_result = rust_heavy_work()
        rust_time = time.perf_counter() - start
        results['Python+Rust'] = rust_time
        print(f"   Время: {rust_time:.4f} сек ({rust_time*1000:.2f} мс)")
        print(f"   Результат: {rust_result}")
        if py_time > 0:
            print(f"   Отношение: {py_time / rust_time:.2f}x (меньше = лучше)")
    else:
        print("   Недоступно (Rust-библиотека не скомпилирована)")
    
    # 3. Python + Go
    print("\n3. Python + Go (TCP сервис)...")
    server = start_go_server()
    if server:
        start = time.perf_counter()
        go_result = go_service_work()
        go_time = time.perf_counter() - start
        results['Python+Go'] = go_time
        print(f"   Время: {go_time:.4f} сек ({go_time*1000:.2f} мс)")
        print(f"   Результат: {go_result}")
        if py_time > 0:
            print(f"   Отношение к Python: {go_time / py_time:.2f}x")
        server.terminate()
    else:
        print("   Не удалось запустить Go-сервер")
    
    # Итоги
    print("\n" + "="*70)
    print(" ИТОГОВОЕ СРАВНЕНИЕ")
    print("="*70)
    
    if HAS_RUST and py_time > 0:
        if rust_time < py_time:
            speedup = py_time / rust_time
            print(f"\nPython + Rust быстрее Python в {speedup:.2f} раз")
            print(f"   Экономия времени: {(py_time - rust_time)*1000:.2f} мс")
        else:
            print(f"\nPython + Rust медленнее Python в {rust_time / py_time:.2f} раз")
            print("   (Накладные расходы FFI могут превышать выгоду для лёгких операций)")
    
    if server and py_time > 0:
        print(f"\nPython + Go медленнее Python в {go_time / py_time:.2f} раз")
        print("   Причина: сетевые вызовы, сериализация, межпроцессное взаимодействие")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    run_benchmark()