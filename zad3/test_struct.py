import unittest
import sys
import os

# Добавляем путь к скомпилированной Rust-библиотеке
sys.path.append(os.path.join(os.path.dirname(__file__), 'target', 'debug'))

try:
    import rust_python_struct
    HAS_LIBRARY = True
except ImportError as e:
    print(f"Ошибка импорта rust_python_struct: {e}")
    print("Убедитесь, что библиотека скомпилирована: cargo build")
    HAS_LIBRARY = False

@unittest.skipUnless(HAS_LIBRARY, "rust_python_struct не доступен")
class TestPerson(unittest.TestCase):
    
    def setUp(self):
        """Создаем объект Person перед каждым тестом"""
        self.person = rust_python_struct.Person("Алексей", 30)
    
    def test_create_person(self):
        """Тест: создание объекта Person"""
        self.assertEqual(self.person.name, "Алексей")
        self.assertEqual(self.person.age, 30)
    
    def test_greet(self):
        """Тест: метод greet возвращает правильное приветствие"""
        expected = "Привет, меня зовут Алексей и мне 30 лет!"
        self.assertEqual(self.person.greet(), expected)
    
    def test_have_birthday(self):
        """Тест: метод have_birthday увеличивает возраст"""
        self.person.have_birthday()
        self.assertEqual(self.person.age, 31)
    
    def test_set_name(self):
        """Тест: установка нового имени"""
        self.person.name = "Мария"
        self.assertEqual(self.person.name, "Мария")
        self.assertEqual(self.person.greet(), "Привет, меня зовут Мария и мне 30 лет!")
    
    def test_set_age(self):
        """Тест: установка нового возраста"""
        self.person.age = 25
        self.assertEqual(self.person.age, 25)
        self.assertEqual(self.person.greet(), "Привет, меня зовут Алексей и мне 25 лет!")
    
    def test_invalid_name(self):
        """Тест: ошибка при создании с пустым именем"""
        with self.assertRaises(ValueError):
            rust_python_struct.Person("", 25)
    
    def test_invalid_age(self):
        """Тест: ошибка при создании с некорректным возрастом"""
        with self.assertRaises(ValueError):
            rust_python_struct.Person("Иван", 0)
        
        with self.assertRaises(ValueError):
            rust_python_struct.Person("Иван", 151)

if __name__ == '__main__':
    unittest.main()