"""Prototipo de modernización del sistema de préstamos de la biblioteca.

Menú interactivo en consola para registrar y consultar préstamos, con
validaciones, manejo de excepciones y persistencia en un archivo CSV.
"""

import csv
import os

from validaciones import (
    es_duplicado,
    validar_codigo,
    validar_dias,
    validar_nombre,
    validar_titulo,
)

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prestamos.csv")
CAMPOS = ["codigo", "nombre", "titulo", "dias"]


# ---------------------------------------------------------------- persistencia
def cargar_prestamos(ruta=ARCHIVO):
    """Lee los préstamos guardados. Ignora filas dañadas sin detener el programa."""
    prestamos = []
    if not os.path.exists(ruta):
        return prestamos
    try:
        with open(ruta, newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                try:
                    prestamos.append(
                        {
                            "codigo": validar_codigo(fila["codigo"]),
                            "nombre": validar_nombre(fila["nombre"]),
                            "titulo": validar_titulo(fila["titulo"]),
                            "dias": validar_dias(fila["dias"]),
                        }
                    )
                except (ValueError, KeyError, TypeError):
                    print("Aviso: se omitió un registro inválido del archivo.")
    except OSError:
        print("Aviso: no se pudo leer el archivo de préstamos.")
    return prestamos


def guardar_prestamos(prestamos, ruta=ARCHIVO):
    """Guarda todos los préstamos en CSV. Devuelve True si tuvo éxito."""
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(prestamos)
        return True
    except OSError:
        print("Error: no se pudo guardar el archivo de préstamos.")
        return False


# ------------------------------------------------------------------ operaciones
def pedir_dato(mensaje, validador):
    """Repite la pregunta hasta que el dato sea válido (o el usuario cancele)."""
    while True:
        try:
            return validador(input(mensaje))
        except ValueError as error:
            print(f"  ✗ {error}")


def registrar_prestamo(prestamos):
    print("\n--- Registrar nuevo préstamo ---")
    codigo = pedir_dato("Código del estudiante (EST-###): ", validar_codigo)
    nombre = pedir_dato("Nombre del estudiante: ", validar_nombre)
    titulo = pedir_dato("Título del material: ", validar_titulo)
    dias = pedir_dato("Días de préstamo (1-30): ", validar_dias)

    if es_duplicado(prestamos, codigo, titulo):
        print("  ✗ Ese estudiante ya tiene registrado este material. No se guardó.")
        return

    prestamos.append(
        {"codigo": codigo, "nombre": nombre, "titulo": titulo, "dias": dias}
    )
    if guardar_prestamos(prestamos):
        print("  ✓ Préstamo registrado correctamente.")
    else:
        prestamos.pop()  # no dejar en memoria algo que no quedó guardado


def consultar_prestamos(prestamos):
    print("\n--- Préstamos registrados ---")
    if not prestamos:
        print("No hay préstamos registrados.")
        return
    print(f"{'N°':<4}{'Código':<12}{'Estudiante':<26}{'Material':<30}{'Días':>5}")
    print("-" * 77)
    for i, p in enumerate(prestamos, start=1):
        print(
            f"{i:<4}{p['codigo']:<12}{p['nombre'][:24]:<26}"
            f"{p['titulo'][:28]:<30}{p['dias']:>5}"
        )
    print(f"\nTotal: {len(prestamos)} préstamo(s).")


def mostrar_menu():
    print("\n===== BIBLIOTECA - PRÉSTAMOS =====")
    print("1. Registrar un nuevo préstamo")
    print("2. Consultar los préstamos registrados")
    print("3. Salir")


def main():
    prestamos = cargar_prestamos()
    while True:
        mostrar_menu()
        try:
            opcion = input("Elija una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            break

        try:
            if opcion == "1":
                registrar_prestamo(prestamos)
            elif opcion == "2":
                consultar_prestamos(prestamos)
            elif opcion == "3":
                print("Hasta pronto.")
                break
            else:
                print("  ✗ Opción inválida. Elija 1, 2 o 3.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")


if __name__ == "__main__":
    main()
