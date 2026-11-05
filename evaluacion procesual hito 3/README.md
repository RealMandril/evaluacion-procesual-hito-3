# Biblioteca – Prototipo de Préstamos

Prototipo en Python que moderniza el registro de préstamos de materiales de una biblioteca institucional.
Proyecto de la evaluación procesual Hito 3 de **Programación Fundamental (PFU-111)**, Ingeniería de Sistemas e Innovación Digital, Universidad Privada Franz Tamayo.

## Problema que busca resolver
El sistema legado de la biblioteca guarda los préstamos en archivos de texto y registros manuales. Esto produce información incompleta, datos inconsistentes, fechas incorrectas y préstamos duplicados, porque no se valida nada antes de guardar. Este prototipo registra y consulta préstamos validando cada dato y conservando la información en un archivo CSV.

## Funcionalidades
- Menú interactivo en consola: registrar préstamo, consultar préstamos y salir.
- Datos por préstamo: código del estudiante, nombre, título del material y días de préstamo.
- Validaciones:
  - Código no vacío y con formato `EST-###` (3 a 6 dígitos).
  - Nombre y título no vacíos (el nombre no admite números).
  - Días: número entero entre 1 y 30.
  - No se permiten préstamos duplicados (mismo estudiante y mismo material).
- Manejo de excepciones con `try-except`: el programa no se cierra por entradas inválidas, `Ctrl+C`/`Ctrl+D` o errores de archivo.
- Seguridad básica de la información: no se almacenan datos sensibles, solo los campos necesarios; se limpian los espacios y se neutralizan textos que Excel interpretaría como fórmula (`=`, `+`, `-`, `@`); las filas dañadas del CSV se omiten sin detener el programa.
- Persistencia en `prestamos.csv`: los préstamos se guardan al registrarlos y se recuperan al iniciar.

## Estructura
```
biblioteca-prestamos/
├── main.py                 # menú, operaciones y persistencia
├── validaciones.py         # funciones de validación
├── test_validaciones.py    # pruebas con datos correctos e incorrectos
├── README.md
└── .gitignore
```
`prestamos.csv` se crea automáticamente al registrar el primer préstamo.

## Instrucciones de ejecución
Requisitos: Python 3.8 o superior (no usa librerías externas).

```bash
git clone <URL-DEL-REPOSITORIO>
cd biblioteca-prestamos
python main.py          # en algunos sistemas: python3 main.py
```

Para ejecutar las pruebas:
```bash
python -m unittest -v
```

## Integrantes del equipo
- Nombre Apellido – código de estudiante
- Nombre Apellido – código de estudiante
- Nombre Apellido – código de estudiante

## Decisiones técnicas
- Se usó una lista de diccionarios en memoria y CSV como respaldo, por ser simple y legible.
- Las validaciones están separadas en `validaciones.py` para probarlas de forma independiente.
- `prestamos.csv` está en `.gitignore` para no subir datos de estudiantes al repositorio.
