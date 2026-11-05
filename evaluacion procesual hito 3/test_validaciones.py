"""Pruebas con datos correctos e incorrectos. Ejecutar: python -m unittest -v"""

import os
import tempfile
import unittest

import main
from validaciones import (
    es_duplicado,
    validar_codigo,
    validar_dias,
    validar_nombre,
    validar_titulo,
)


class TestValidaciones(unittest.TestCase):
    def test_codigo_valido(self):
        self.assertEqual(validar_codigo(" est-001 "), "EST-001")

    def test_codigo_invalido(self):
        for malo in ["", "   ", "ABC", "EST-1", "EST-ABC", "SIS-123456"]:
            with self.assertRaises(ValueError, msg=malo):
                validar_codigo(malo)

    def test_nombre_y_titulo(self):
        self.assertEqual(validar_nombre("  Ana   Mamani "), "Ana Mamani")
        self.assertEqual(validar_titulo("Cien años de soledad"), "Cien años de soledad")
        for malo in ["", "   "]:
            with self.assertRaises(ValueError):
                validar_nombre(malo)
            with self.assertRaises(ValueError):
                validar_titulo(malo)
        with self.assertRaises(ValueError):
            validar_nombre("Ana123")

    def test_texto_no_se_interpreta_como_formula(self):
        self.assertTrue(validar_titulo("=SUMA(A1)").startswith("'"))

    def test_dias_validos(self):
        self.assertEqual(validar_dias("1"), 1)
        self.assertEqual(validar_dias(" 30 "), 30)

    def test_dias_invalidos(self):
        for malo in ["", "0", "31", "-5", "abc", "2.5"]:
            with self.assertRaises(ValueError, msg=malo):
                validar_dias(malo)

    def test_duplicados(self):
        lista = [{"codigo": "EST-001", "titulo": "Python Básico"}]
        self.assertTrue(es_duplicado(lista, "EST-001", "python básico"))
        self.assertFalse(es_duplicado(lista, "EST-002", "Python Básico"))
        self.assertFalse(es_duplicado(lista, "EST-001", "Otro libro"))


class TestPersistencia(unittest.TestCase):
    def test_guardar_y_cargar(self):
        datos = [
            {"codigo": "EST-001", "nombre": "Ana Mamani", "titulo": "Álgebra, 2da ed.", "dias": 7}
        ]
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "p.csv")
            self.assertTrue(main.guardar_prestamos(datos, ruta))
            self.assertEqual(main.cargar_prestamos(ruta), datos)

    def test_archivo_inexistente(self):
        self.assertEqual(main.cargar_prestamos("/no/existe/p.csv"), [])

    def test_fila_danada_se_omite(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "p.csv")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("codigo,nombre,titulo,dias\n")
                f.write("EST-001,Ana,Libro,5\n")
                f.write("XXX,,,99\n")
            self.assertEqual(len(main.cargar_prestamos(ruta)), 1)


if __name__ == "__main__":
    unittest.main()
