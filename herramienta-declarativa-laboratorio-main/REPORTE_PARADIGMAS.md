# Reporte Tecnico: Paradigmas de Programacion y Diseno Arquitectonico

> **Proyecto:** Herramienta CLI Modular para Analisis de Datos  
> **Materia:** Paradigmas de Programacion  
> **Tema:** Separacion de Preocupaciones (Separation of Concerns - SoC), Programacion Orientada a Objetos y Diseno Modular

---

## 1. Introduccion

El presente laboratorio tiene como finalidad demostrar la aplicacion practica del principio de **Separacion de Preocupaciones** (*Separation of Concerns* - SoC) en el desarrollo de software. 

A menudo, los desarrolladores novatos mezclan en un solo archivo la lectura de datos, el procesamiento matematico, la entrada por teclado y la impresion en consola con `print()`. Este documento expone las justificaciones de diseno adoptadas para desacoplar completamente la solucion en cuatro capas independientes.

---

## 2. Paradigmas de Programacion Aplicados

### 2.1. Programacion Orientada a Objetos (POO)
- **Encapsulamiento de Estado:**
  - La clase `MotorAnalisis` (`logica.py`) encapsula el estado interno del dataset (`self.dataset`, `self.columnas`, `self.archivo_actual`). El exterior no altera estas listas de forma arbitraria, sino a traves de metodos publicos como `cargar_csv()` y `descargar()`.
  - La clase `ControladorCLI` (`controlador.py`) hereda de `cmd.Cmd`, encapsulando el ciclo de vida del intérprete de comandos y su prompt interactivo.
- **Abstraccion Estatica:**
  - La clase `MensajesUI` (`presentacion.py`) funciona como un contenedor abstracto de constantes y metodos estaticos (`@staticmethod`) dedicados exclusivamente al formateo de salida.

### 2.2. Paradigma Declarativo vs. Imperativo
- **Enfoque Declarativo en la CLI:**
  - El usuario interactua declarando *que* desea obtener (`/maxmin -clean salario`, `/promedio edad`) en lugar de especificar *como* se itera el archivo o que algoritmos se ejecutan paso a paso.
- **Enfoque Declarativo en la Limpieza de Datos:**
  - El modificador `-clean` expresa una regla de negocio declarativa: "omite las celdas sucias y opera sobre el resto", delegando la estrategia de descarte al motor logico.

### 2.3. Inversion de Control (IoC)
- Al utilizar la libreria estandar `cmd.Cmd`, el flujo de ejecucion principal no es un bucle `while True` manual con `input()`, sino un despachador orientado a eventos (`cmdloop()`). El framework de Python llama a nuestros metodos `do_<comando>` cuando se detecta la orden correspondiente.

---

## 3. Justificacion Arquitectonica: Por que no usar `print()` en la Logica?

Uno de los requerimientos mas criticos del laboratorio establece:  
*`logica.py` no debe utilizar la funcion `print()`.*

### Razones Fundamentales:
1. **Acoplamiento al Canal de Salida:**
   Si `logica.py` ejecuta `print("Error...")`, el modulo queda atado de forma irrevocable a la salida estandar (`sys.stdout`) de una consola de texto.
2. **Reutilizacion Multiplataforma:**
   Al retornar tuplas tipadas (`(True, resultado)` o `(False, error)`) y lanzar excepciones tipadas (`ValueError`, `KeyError`), este mismo archivo `logica.py` puede importarse y utilizarse sin modificaciones en:
   - Una aplicacion web (Flask, FastAPI, Django).
   - Una interfaz grafica de usuario (Tkinter, PyQt).
   - Un servicio de microservicios o API REST.
   - Un pipeline de pruebas automatizadas (`unittest`).
3. **Manejo Centralizado de Errores:**
   Permite que la capa de Control decida como reaccionar ante una anomalia (por ejemplo, reintentar, registrar en un log o mostrar un mensaje formateado al usuario).

---

## 4. Estructura de Capas y Responsabilidades

| Capa | Archivo | Rol en la Arquitectura | Responsabilidad Especifica |
| :--- | :--- | :--- | :--- |
| **Vista** | `presentacion.py` | Presentacion | Textos, plantillas de formato y metodos de salida en consola. |
| **Modelo** | `logica.py` | Logica de Negocio | Lectura con `csv.DictReader`, validacion de columnas y calculos estadisticos. |
| **Controlador** | `controlador.py` | Coordinacion | Captura de entrada del usuario, parseo de banderas, manejo de excepciones y despacho a la Vista. |
| **Entrada** | `principal.py` | Bootstrapping | Comprobacion del entorno, creacion de archivos de prueba e inicio del interprete. |

---

## 5. Pruebas y Verificacion de Calidad

La separacion modular facilito la creacion de una suite de pruebas automatizadas (`test_cli.py`) que evalua cada capa de forma aislada:
- **Pruebas de Unidad (Capa Modelo):** Verifican que `calcular_maxmin`, `calcular_promedio`, `calcular_mediana`, `calcular_desviacion` y `generar_resumen` produzcan resultados matematicos exactos y lancen las excepciones correctas ante columnas inexistentes o datos no numericos.
- **Pruebas de Integracion (Capa Controlador):** Simulan la ejecucion de comandos (`/cargar`, `/maxmin -clean`, `/promedio`, `/exportar`) comprobando el cambio de estado del prompt y la salida en consola.

---

## 6. Conclusiones

La implementacion demostro que el principio de Separacion de Preocupaciones reduce la complejidad del codigo, elimina la redundancia, previene efectos secundarios indeseados y garantiza que la aplicacion sea facilmente extensible a nuevas funcionalidades (tales como exportacion, autocompletado y calculos estadisticos avanzados) sin comprometer el diseno original.

