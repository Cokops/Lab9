package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"strings"
)

func main() {
	// Запуск TCP-сервера на порту 8080
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()
	fmt.Println("TCP-сервер запущен на :8080")

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

		// Убираем символ новой строки и приводим к нижнему регистру
		message = strings.TrimSpace(message)
		message = strings.ToLower(message)

		fmt.Printf("Получено от клиента: %s\n", message)

		// Отправляем ответ клиенту
		response := fmt.Sprintf("Сервер получил: %s\n", message)
		_, err = conn.Write([]byte(response))
		if err != nil {
			log.Printf("Ошибка при отправке ответа клиенту %s: %v\n", conn.RemoteAddr().String(), err)
			return
		}
	}
}