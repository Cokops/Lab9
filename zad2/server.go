package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"strings"
	"time"
)

// Общий канал для получения сообщений от клиентов
var messageChan = make(chan string)

func main() {
	// Запуск TCP-сервера на порту 8080
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()
	fmt.Println("TCP-сервер запущен на :8080")

	// Запускаем фоновую горутину для обработки сообщений
	go backgroundProcessor()

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

// handleConnection читает сообщения от клиента и отправляет их в общий канал
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

		// Отправляем сообщение в канал для фоновой обработки
		messageChan <- fmt.Sprintf("[от %s] %s", conn.RemoteAddr().String(), message)

		// Отправляем подтверждение клиенту
		response := fmt.Sprintf("Сообщение передано на обработку: %s\n", message)
		_, err = conn.Write([]byte(response))
		if err != nil {
			log.Printf("Ошибка при отправке ответа клиенту %s: %v\n", conn.RemoteAddr().String(), err)
			return
		}
	}
}

// backgroundProcessor — фоновая горутина, обрабатывающая сообщения
func backgroundProcessor() {
	for {
		select {
		case msg := <-messageChan:
			// Имитация длительной обработки
			fmt.Printf("Фоновая обработка: %s\n", msg)
			time.Sleep(2 * time.Second) // Имитация работы
			fmt.Printf("Обработка завершена для: %s\n", msg)
			
		default:
			// Если нет сообщений, делаем паузу, чтобы не нагружать CPU
			time.Sleep(100 * time.Millisecond)
		}
	}
}