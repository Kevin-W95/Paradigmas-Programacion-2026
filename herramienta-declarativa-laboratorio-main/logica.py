import csv
import math

class MotorAnalisis:
    """
    CAPA 2: LÓGICA DE NEGOCIO (MODELO)
    Esta clase procesa datos. No usa la función print(). 
    Retorna resultados o lanza errores.
    """
    def __init__(self):
        self.dataset = None
        self.columnas = []
        self.archivo_actual = None

    def esta_cargado(self):
        return self.dataset is not None

    def validar_columna(self, columna):
        """Función de ayuda para verificar el estado de los datos."""
        if not self.esta_cargado():
            raise ValueError("NO_DATASET")
        if columna not in self.columnas:
            raise KeyError(columna)

    def cargar_csv(self, ruta_archivo):
        """
        Abre el archivo en modo lectura. Usa csv.Sniffer para detectar
        delimitadores y csv.DictReader para leer registros.
        """
        with open(ruta_archivo, mode='r', encoding='utf-8') as f:
            muestra = f.read(2048)
            f.seek(0)
            delimitador = ','
            try:
                delimitador = csv.Sniffer().sniff(muestra).delimiter
            except Exception:
                delimitador = ','
            reader = csv.DictReader(f, delimiter=delimitador)
            self.columnas = list(reader.fieldnames) if reader.fieldnames else []
            self.dataset = list(reader)
            self.archivo_actual = ruta_archivo
        return len(self.dataset), len(self.columnas)

    def descargar(self):
        nombre = self.archivo_actual
        self.dataset = None
        self.columnas = []
        self.archivo_actual = None
        return nombre

    def _extraer_numeros(self, columna, omitir_errores=False):
        """Extrae lista de floats y reporta errores si omitir_errores es False."""
        self.validar_columna(columna)
        valores = []
        for fila_idx, fila in enumerate(self.dataset, start=2):
            val = fila.get(columna)
            if val is None or val.strip() == "":
                continue
            try:
                valores.append(float(val))
            except ValueError:
                if not omitir_errores:
                    err = ValueError(f"Valor no numérico '{val}' en la fila {fila_idx}.")
                    err.valor = val
                    err.fila = fila_idx
                    raise err
                continue
        return valores

    def calcular_maxmin(self, columna, omitir_errores=False):
        """
        Itera sobre self.dataset. Extrae el valor de la columna.
        Si está vacío, sáltalo. Si no se puede convertir a float():
           - Si omitir_errores es False, retorna (False, (valor_erroneo, linea))
           - Si omitir_errores es True, ignora el error y continúa.
        Si todo sale bien, retorna (True, (maximo, minimo)).
        """
        self.validar_columna(columna)
        valores = []
        for fila_idx, fila in enumerate(self.dataset, start=2):
            val = fila.get(columna)
            if val is None or val.strip() == "":
                continue
            try:
                num = float(val)
                valores.append(num)
            except ValueError:
                if not omitir_errores:
                    return False, (val, fila_idx)
                continue
        if not valores:
            return True, (None, None)
        return True, (max(valores), min(valores))

    def calcular_promedio(self, columna, omitir_errores=False):
        """Calcula el promedio de la columna con soporte opcional para omitir errores."""
        valores = self._extraer_numeros(columna, omitir_errores=omitir_errores)
        if not valores:
            raise ValueError(f"No se encontraron valores procesables en la columna '{columna}'.")
        return sum(valores) / len(valores)

    def calcular_mediana(self, columna, omitir_errores=False):
        """Calcula la mediana de la columna numérica."""
        valores = self._extraer_numeros(columna, omitir_errores=omitir_errores)
        if not valores:
            raise ValueError(f"No se encontraron valores procesables en la columna '{columna}'.")
        valores.sort()
        n = len(valores)
        medio = n // 2
        if n % 2 == 1:
            return valores[medio]
        else:
            return (valores[medio - 1] + valores[medio]) / 2.0

    def calcular_desviacion(self, columna, omitir_errores=False):
        """Calcula la desviación estándar muestral de la columna."""
        valores = self._extraer_numeros(columna, omitir_errores=omitir_errores)
        if len(valores) < 2:
            raise ValueError(f"Se requieren al menos dos valores numéricos para calcular la desviación en '{columna}'.")
        media = sum(valores) / len(valores)
        varianza = sum((x - media) ** 2 for x in valores) / (len(valores) - 1)
        return math.sqrt(varianza)

    def generar_resumen(self, columna, omitir_errores=False):
        """Genera un diccionario con todas las estadísticas descriptivas de la columna."""
        self.validar_columna(columna)
        total_filas = len(self.dataset)
        nulos = 0
        errores = 0
        valores = []

        for fila_idx, fila in enumerate(self.dataset, start=2):
            val = fila.get(columna)
            if val is None or val.strip() == "":
                nulos += 1
                continue
            try:
                valores.append(float(val))
            except ValueError:
                errores += 1
                if not omitir_errores:
                    err = ValueError(f"Valor no numérico '{val}' en la fila {fila_idx}.")
                    err.valor = val
                    err.fila = fila_idx
                    raise err

        minimo = min(valores) if valores else None
        maximo = max(valores) if valores else None
        promedio = (sum(valores) / len(valores)) if valores else None
        
        mediana = None
        if valores:
            vals_ordenados = sorted(valores)
            n = len(vals_ordenados)
            medio = n // 2
            mediana = vals_ordenados[medio] if n % 2 == 1 else (vals_ordenados[medio - 1] + vals_ordenados[medio]) / 2.0

        desviacion = None
        if len(valores) >= 2 and promedio is not None:
            varianza = sum((x - promedio) ** 2 for x in valores) / (len(valores) - 1)
            desviacion = math.sqrt(varianza)

        return {
            "columna": columna,
            "total_filas": total_filas,
            "valores_validos": len(valores),
            "nulos": nulos,
            "errores": errores,
            "minimo": minimo,
            "maximo": maximo,
            "promedio": promedio,
            "mediana": mediana,
            "desviacion": desviacion
        }
        
    def contar_nulos(self, columna):
        """Recorre el dataset y cuenta cuántas filas tienen la columna vacía o con espacios."""
        self.validar_columna(columna)
        nulos = 0
        for fila in self.dataset:
            val = fila.get(columna)
            if val is None or val.strip() == "":
                nulos += 1
        return nulos