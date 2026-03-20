import socket
import threading
import time
import unittest

# Параметры подключения
HOST = '127.0.0.1'
PORT = 8080

class TestTCPClient(unittest.TestCase):
    
    def test_server_response(self):
        """Тест: подключение к серверу и проверка ответа"""
        # Запускаем клиент в отдельном потоке
        def run_client():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((HOST, PORT))
                    
                    # Отправляем сообщение
                    message = "Test message\n"
                    client.sendall(message.encode('utf-8'))
                    
                    # Получаем ответ
                    response = client.recv(1024).decode('utf-8')
                    self.assertIn("сервер получил: test message".lower(), response.lower())
                    
            except ConnectionRefusedError:
                self.fail("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
            except Exception as e:
                self.fail(f"Ошибка при выполнении клиента: {e}")
        
        # Запускаем клиент в потоке
        client_thread = threading.Thread(target=run_client)
        client_thread.start()
        
        # Ждем немного, чтобы клиент успел подключиться (сервер должен быть запущен отдельно)
        time.sleep(1)
        
        client_thread.join(timeout=5)  # Ждем завершения потока
        if client_thread.is_alive():
            self.fail("Тест не завершился вовремя")

if __name__ == '__main__':
    unittest.main()