# Herramienta CLI para Analisis de Datos (CSV)

Una aplicacion de consola interactiva en Python disenada para explorar y calcular estadisticas en archivos CSV de forma rapida, sencilla y modular.

---

## 1. Proposito del Proyecto

Permite explorar y consultar una tabla de datos (archivo CSV) de manera interactiva a traves de una consola de comandos:
- Consultar las columnas disponibles.
- Obtener el valor maximo y minimo de columnas numericas.
- Calcular el promedio aritmetico de una columna (con soporte de limpieza).
- Calcular la mediana y la desviacion estandar muestral.
- Generar un resumen estadistico descriptivo completo en una sola llamada.
- Identificar y cuantificar registros nulos o celdas vacias.
- Exportar reportes de analisis a archivos de texto.
- Autocompletar nombres de columnas con la tecla Tab.

---

## 2. Arquitectura del Sistema

El proyecto implementa el principio de **Separacion de Responsabilidades** (*Separation of Concerns* - SoC) dividiendo la solucion en cuatro capas desacopladas:

```
+--------------------------------------------------------+
|                      principal.py                      |
|        (Punto de partida: arranca la aplicacion)       |
+--------------------------+-----------------------------+
                           |
                           v
+--------------------------------------------------------+
|                     controlador.py                     |
|    (Controlador: procesa comandos e interactua con UI) |
+--------------------------+-----------------------------+
               |                           |
               v                           v
+------------------------------+ +----------------------+
|          logica.py           | |   presentacion.py    |
| (Modelo / Logica de negocio: | | (Vista: textos,      |
|  calculos y lectura sin UI)  | |  mensajes y formato) |
+------------------------------+ +----------------------+
```

1. **`presentacion.py` (Vista):**  
   Centraliza todos los mensajes y cadenas de texto desplegados en pantalla. No procesa datos ni ejecuta calculos.

2. **`logica.py` (Modelo):**  
   Encapsula la logica de procesamiento, analisis y lectura de archivos. No contiene llamadas a `print()`, comunicando resultados y errores mediante excepciones y tuplas tipadas. Soporta delimitadores flexibles mediante `csv.Sniffer`.

3. **`controlador.py` (Controlador):**  
   Interpreta la entrada del usuario (`cmd.Cmd`), valida argumentos y banderas (`-clean`), ofrece autocompletado con Tab, coordina la ejecucion de metodos en `logica.py` y envia la respuesta a `presentacion.py`.

4. **`principal.py` (Punto de entrada):**  
   Verifica el entorno de ejecucion, genera datos de prueba en caso de ausencia e inicia el ciclo de lectura de comandos.

---

## 3. Instrucciones de Uso

### Requisitos Previos
- Python 3.8 o superior.
- Modulos estandar incluidos en la distribucion oficial de Python (`csv`, `cmd`, `shlex`, `os`, `math`, `unittest`).

### Ejecucion de la Aplicacion
Para iniciar la interfaz interactiva, ejecute en la terminal:

```bash
python principal.py
```

Tambien puede ejecutarse en Windows mediante el script:
```cmd
iniciar.bat
```

Al iniciar, se mostrara el prompt de comandos:

```text
========================================================
  Bienvenido a la Herramienta de Analisis Modular
========================================================
Escribe 'help' o '?' para ver los comandos disponibles.
Prueba iniciar con: /cargar datos.csv

dataset-cli> 
```

---

## 4. Referencia de Comandos

Los comandos admiten sintaxis con prefijo `/` o sin el. Tambien cuentan con soporte de **autocompletado presionando Tab** para nombres de columnas.

| Comando | Descripcion | Ejemplo |
| :--- | :--- | :--- |
| `/cargar <archivo>` | Carga un archivo CSV en memoria (detecta comas, punto y coma, etc.). | `/cargar datos.csv` |
| `/listarcolumnas` | Muestra los nombres de las columnas disponibles. | `/listarcolumnas` |
| `/maxmin [-clean] <col>` | Calcula el valor maximo y minimo. | `/maxmin -clean salario` |
| `/promedio [-clean] <col>` | Calcula la media aritmetica. | `/promedio -clean salario` |
| `/mediana [-clean] <col>` | Calcula la mediana del conjunto numerico. | `/mediana -clean salario` |
| `/desviacion [-clean] <col>` | Calcula la desviacion estandar muestral. | `/desviacion -clean salario` |
| `/resumen [-clean] <col>` | Genera una ficha tecnica con todas las metricas. | `/resumen -clean salario` |
| `/nulos <col>` | Cuenta registros con celdas vacias o solo espacios. | `/nulos edad` |
| `/exportar <archivo>` | Guarda el historial de analisis en un archivo de texto. | `/exportar reporte.txt` |
| `/unload` | Libera el dataset activo de memoria y restituye el prompt base. | `/unload` |
| `/help` o `?` | Despliega el menu de ayuda con la lista de operaciones. | `/help` |
| `/quit` | Finaliza la sesion y cierra el programa. | `/quit` |

---

## 5. Ejemplos de Salida

### Calculo de Promedio con Limpieza de Errores
```text
(datos.csv)> /promedio -clean salario
[Resultado] El promedio de 'salario' es: 5150.31
```

### Resumen Estadistico Integral
```text
(datos.csv)> /resumen -clean salario

========================================================
  Resumen Estadistico: salario
========================================================
 - Total de registros evaluados: 5
 - Valores numericos validos:   4
 - Celdas nulas o vacias:       0
 - Registros con error:         1
 - Minimo:                      4500.50
 - Maximo:                      6100.75
 - Promedio:                    5150.31
 - Mediana:                     5000.00
 - Desviacion estandar:         694.02
========================================================
```

### Exportar Resultados a Disco
```text
(datos.csv)> /exportar reporte.txt
[OK] Reporte exportado exitosamente a 'reporte.txt'.
```

---

## 6. Suite de Pruebas

El repositorio incluye pruebas unitarias y de integracion:

```bash
python test_cli.py
```

Valida:
- Carga y lectura correcta de estructuras tabulares (delimitadores comma y semicolon).
- Deteccion e interrupcion ante tipos no numericos.
- Filtro y calculo correcto bajo la bandera `-clean`.
- Metricas de promedio, mediana, desviacion estandar y resumen descriptivo.
- Autocompletado de columnas mediante Tab.
- Exportacion de reportes.
- Flujo interactivo del controlador CLI.

---

## 7. Indice de Archivos

| Archivo | Funcion |
| :--- | :--- |
| `principal.py` | Inicializacion y punto de entrada de la CLI. |
| `controlador.py` | Gestion de comandos, autocompletado y coordinacion de capas. |
| `logica.py` | Motor matematico, estadisticas y lectura con deteccion de delimitadores. |
| `presentacion.py` | Repositorio de mensajes y formateo de tablas/salida. |
| `datos.csv` | Dataset de prueba base. |
| `datos_ejemplo_con_nulos.csv` | Dataset de prueba con valores vacios y espacios en blanco. |
| `test_cli.py` | Suite de verificacion automatizada completa. |
| `iniciar.bat` | Script de ejecucion rapida para Windows. |
| `README.md` | Documentacion tecnica del sistema. |
