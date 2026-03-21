import socket
import threading
import time
import unittest

# Параметры подключения
HOST = '127.0.0.1'
PORT = 8080

class TestTCPServer(unittest.TestCase):
    
    def test_background_processing(self):
        """Тест: проверка, что сервер корректно передает сообщения в фоновую обработку"""
        # Флаг для отслеживания получения ожидаемого ответа
        response_received = False
        
        def run_client():
            nonlocal response_received
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((HOST, PORT))
                    
                    # Отправляем сообщение
                    message = "Test background processing\n"
                    client.sendall(message.encode('utf-8'))
                    
                    # Получаем ответ
                    response = client.recv(1024).decode('utf-8')
                    
                    # Проверяем, что ответ содержит ожидаемый текст
                    if "сообщение передано на обработку" in response.lower():
                        response_received = True
                    
            except Exception as e:
                print(f"Ошибка в клиенте: {e}")
                return
        
        # Запускаем клиент в отдельном потоке
        client_thread = threading.Thread(target=run_client)
        client_thread.start()
        
        # Ждем, пока клиент получит ответ (с таймаутом)
        client_thread.join(timeout=5)
        
        # Проверяем результат
        self.assertTrue(response_received, "Сервер не подтвердил передачу сообщения на обработку")

if __name__ == '__main__':
    unittest.main()