import socket

# Параметры подключения
HOST = '127.0.0.1'  # Адрес сервера
PORT = 8080         # Порт сервера

def main():
    # Создаем TCP-клиент
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            # Подключаемся к серверу
            client.connect((HOST, PORT))
            print(f"Подключено к серверу {HOST}:{PORT}")
            
            # Отправляем сообщения серверу
            messages = ["Привет, сервер!", "Как дела?", "Пока!"]
            
            for msg in messages:
                # Отправляем сообщение
                message = msg + '\n'  # Добавляем символ новой строки
                client.sendall(message.encode('utf-8'))
                print(f"Отправлено: {msg}")
                
                # Получаем ответ от сервера
                response = client.recv(1024).decode('utf-8')
                print(f"Ответ от сервера: {response.strip()}")
                
        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()