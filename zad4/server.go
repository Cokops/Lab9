package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"strings"
)

func main() {
	// Запуск TCP-сервера на порту 8081
	listener, err := net.Listen("tcp", ":8081")
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()
	fmt.Println("Go-сервис запущен на :8081")

	for {
		// Принимаем входящее соединение
		conn, err := listener.Accept()
		if err != nil {
			log.Println(err)
			continue
		}
		// Обрабатываем подключение в отдельной горутине
		go handleConnection(conn)
	}
}

// handleConnection обрабатывает подключение от клиента
func handleConnection(conn net.Conn) {
	defer conn.Close()
	fmt.Printf("Клиент подключился: %s\n", conn.RemoteAddr().String())

	// Создаем буфер для чтения данных
	reader := bufio.NewReader(conn)

	for {
		// Читаем строку до символа новой строки
		message, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("Клиент отключился: %s\n", conn.RemoteAddr().String())
			return
		}

		// Убираем символ новой строки
		message = strings.TrimSpace(message)

		fmt.Printf("Получено: %s\n", message)

		// Простая обработка: возвращаем строку длины
		response := fmt.Sprintf("Длина строки '%s' равна %d\n", message, len(message))
		_, err = conn.Write([]byte(response))
		if err != nil {
			log.Printf("Ошибка при отправке ответа: %v\n", err)
			return
		}
	}
}
