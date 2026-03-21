import unittest
import sys
import os

# Добавляем путь к модулю (для локального тестирования)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import zad5 as rust_python_struct
    HAS_MODULE = True
except ImportError:
    HAS_MODULE = False
    print("⚠️ Модуль zad5 не найден")


class TestPerson(unittest.TestCase):
    
    @unittest.skipUnless(HAS_MODULE, "Rust module not available")
    def test_create_person(self):
        p = rust_python_struct.Person("Иван", 25)
        self.assertEqual(p.name, "Иван")
        self.assertEqual(p.age, 25)
    
    @unittest.skipUnless(HAS_MODULE, "Rust module not available")
    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            rust_python_struct.Person("", 25)
    
    @unittest.skipUnless(HAS_MODULE, "Rust module not available")
    def test_invalid_age_zero_raises(self):
        with self.assertRaises(ValueError):
            rust_python_struct.Person("Иван", 0)
    
    @unittest.skipUnless(HAS_MODULE, "Rust module not available")
    def test_greet_method(self):
        p = rust_python_struct.Person("Мария", 20)
        greeting = p.greet()
        self.assertIn("Мария", greeting)
        self.assertIn("20", greeting)
    
    @unittest.skipUnless(HAS_MODULE, "Rust module not available")
    def test_have_birthday(self):
        p = rust_python_struct.Person("Петр", 30)
        p.have_birthday()
        self.assertEqual(p.age, 31)


if __name__ == "__main__":
    unittest.main()