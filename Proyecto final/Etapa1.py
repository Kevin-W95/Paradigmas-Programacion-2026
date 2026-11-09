import sqlite3
import re
from datetime import datetime
import os

# Obtiene la ruta absoluta de la carpeta donde está este script actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Une esa ruta con el nombre de la base de datos generada
DB_NAME = os.path.join(BASE_DIR, 'fintech_transacciones.db')

def etapa_1_extraccion_y_transformacion():
    print("Iniciando Etapa 1: Extracción y Transformación Funcional")
    conn = sqlite3.connect(DB_NAME)
    
    # A. Extracción (Lógica Declarativa con SQL)
    query = """
        SELECT 
            t.id AS id_transaccion,
            u.pais AS pais_usuario,
            c.categoria AS categoria_comercio,
            t.monto_original,
            t.moneda,
            t.fecha_hora,
            t.estado
        FROM Transacciones t
        LEFT JOIN Usuarios u ON t.usuario_id = u.id
        LEFT JOIN Comercios c ON t.comercio_id = c.id
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columnas = [description[0] for description in cursor.description]
    bruto_tuplas = cursor.fetchall()
    conn.close()

    # Convertir tuplas en diccionarios para facilitar el procesamiento funcional
    dataset_inicial = [dict(zip(columnas, fila)) for fila in bruto_tuplas]

    # B. Transformación (Lógica Funcional)
    
    # 1. Función pura para tratar fechas corruptas o timestamps UNIX
    def limpiar_fecha(transaccion):
        f = transaccion.get('fecha_hora')
        if f is None or f == 'N/A' or f == ' $N/A$' or f == '$N/A$':
            return None
        if str(f).isdigit():
            try:
                dt = datetime.fromtimestamp(int(f))
                t_copia = transaccion.copy()
                t_copia['fecha_hora'] = dt.isoformat()
                return t_copia
            except ValueError:
                return None
        return transaccion

    # 2. Función pura para estandarizar montos
    def limpiar_monto(transaccion):
        t_copia = transaccion.copy()
        monto_raw = t_copia.get('monto_original')
        
        if isinstance(monto_raw, str):
            limpio = re.sub(r'[^0-9.-]', '', monto_raw)
            monto_val = float(limpio) if limpio else 0.0
        else:
            monto_val = float(monto_raw) if monto_raw is not None else 0.0
            
        t_copia['monto_original'] = abs(monto_val)
        return t_copia

    # 3. Función pura para manejar datos faltantes de usuario
    def limpiar_usuario(transaccion):
        t_copia = transaccion.copy()
        if t_copia.get('pais_usuario') is None:
            t_copia['pais_usuario'] = 'Internacional'
        return t_copia

    # Aplicación combinada usando exclusivamente map y filter (Estrictamente funcional)
    paso_fechas = filter(lambda t: t is not None, map(limpiar_fecha, dataset_inicial))
    paso_montos = map(limpiar_monto, paso_fechas)
    dataset_limpio = list(map(limpiar_usuario, paso_montos))

    print(f"Etapa 1 finalizada. Transacciones limpias: {len(dataset_limpio)}")
    return dataset_limpio

if __name__ == '__main__':
    datos_limpios = etapa_1_extraccion_y_transformacion()

# Para correr el archivo, poner py "Proyecto final/Etapa1.py" en la terminal. Esto ejecutará la función principal y mostrará el resultado de la etapa 1.