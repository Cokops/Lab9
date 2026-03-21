use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

#[pyclass]
#[derive(Debug, Clone)]
pub struct Person {
    #[pyo3(get, set)]
    name: String,
    #[pyo3(get, set)]
    age: u32,
}

#[pymethods]
impl Person {
    #[new]
    fn new(name: &str, age: u32) -> PyResult<Self> {
        if name.is_empty() {
            return Err(PyValueError::new_err("Имя не может быть пустым"));
        }
        if age == 0 || age > 150 {
            return Err(PyValueError::new_err("Возраст должен быть между 1 и 150"));
        }
        Ok(Person { name: name.to_string(), age })
    }
    
    fn greet(&self) -> String {
        format!("Привет, меня зовут {} и мне {} лет!", self.name, self.age)
    }
    
    fn have_birthday(&mut self) {
        self.age += 1;
    }
}

#[pymodule]
fn zad4(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Person>()?;
    Ok(())
}