"""Funciones de validación de datos para el sistema de préstamos.

Cada función recibe el valor ingresado, devuelve el valor limpio y lanza
ValueError con un mensaje claro cuando el dato no es válido.
"""

import re

# Formato del código de estudiante: EST- seguido de 3 a 6 dígitos (ej. EST-001)
PATRON_CODIGO = re.compile(r"^EST-\d{3,6}$")
DIAS_MIN = 1
DIAS_MAX = 30
LARGO_MAX_TEXTO = 100


def limpiar_texto(texto):
    """Quita espacios sobrantes y evita que Excel interprete el texto como fórmula."""
    texto = " ".join(texto.split())
    if texto and texto[0] in "=+-@":
        texto = "'" + texto
    return texto


def validar_codigo(codigo):
    codigo = codigo.strip().upper()
    if not codigo:
        raise ValueError("El código del estudiante no puede estar vacío.")
    if not PATRON_CODIGO.match(codigo):
        raise ValueError("Formato de código inválido. Use EST-### (ej. EST-001).")
    return codigo


def validar_nombre(nombre):
    nombre = limpiar_texto(nombre)
    if not nombre:
        raise ValueError("El nombre del estudiante no puede estar vacío.")
    if len(nombre) > LARGO_MAX_TEXTO:
        raise ValueError(f"El nombre no puede superar {LARGO_MAX_TEXTO} caracteres.")
    if any(c.isdigit() for c in nombre):
        raise ValueError("El nombre no puede contener números.")
    return nombre


def validar_titulo(titulo):
    titulo = limpiar_texto(titulo)
    if not titulo:
        raise ValueError("El título del material no puede estar vacío.")
    if len(titulo) > LARGO_MAX_TEXTO:
        raise ValueError(f"El título no puede superar {LARGO_MAX_TEXTO} caracteres.")
    return titulo


def validar_dias(dias):
    dias = str(dias).strip()
    if not dias:
        raise ValueError("La cantidad de días no puede estar vacía.")
    try:
        valor = int(dias)
    except ValueError:
        raise ValueError("La cantidad de días debe ser un número entero.")
    if not DIAS_MIN <= valor <= DIAS_MAX:
        raise ValueError(f"Los días deben estar entre {DIAS_MIN} y {DIAS_MAX}.")
    return valor


def es_duplicado(prestamos, codigo, titulo):
    """Un préstamo está duplicado si el mismo estudiante ya tiene ese material."""
    return any(
        p["codigo"] == codigo and p["titulo"].lower() == titulo.lower()
        for p in prestamos
    )
