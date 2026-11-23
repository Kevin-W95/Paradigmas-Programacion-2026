import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
import numpy as np
import pandas as pd

# Ruta segura relativa a este archivo (funciona sin importar desde dónde se ejecute)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'fintech_transacciones.db')


def etapa_2_analisis_vectorial_y_paralelo(dataset_limpio):
    print("Iniciando Etapa 2: Análisis Vectorial de Riesgo y Concurrencia...")

    df = pd.DataFrame(dataset_limpio)

    # A. Operaciones Vectoriales (NumPy)

    # Conversión de Divisas (Broadcasting)
    # Tasas sintéticas: 1 USD = 500 CRC, 17 MXN, 4000 COP; USD = 1.0
    tasas_cambio = {
        'USD': 1.0,
        'CRC': 1.0 / 500.0,
        'MXN': 1.0 / 17.0,
        'COP': 1.0 / 4000.0,
    }
    vector_tasas = df['moneda'].map(tasas_cambio).fillna(1.0).to_numpy(dtype=np.float64)
    montos_originales = df['monto_original'].to_numpy(dtype=np.float64)

    # M_USD = M_original * T_cambio
    montos_usd = montos_originales * vector_tasas
    df['monto_usd'] = montos_usd
    # Índice de Anomalía por Monto (Z-Score)
    # Z_i = (M_USD,i - mu_M) / sigma_M
    mu_m = np.mean(montos_usd)
    sigma_m = np.std(montos_usd)
    sigma_seguro = sigma_m if sigma_m != 0 else 1.0
    df['score_z'] = (montos_usd - mu_m) / sigma_seguro

    # Volumen Transaccional Acumulado (V_acum)
    # Ordenar por fecha y calcular suma acumulada de transacciones 'COMPLETADA'
    df['fecha_dt'] = pd.to_datetime(df['fecha_hora'], format='ISO8601')
    df = df.sort_values('fecha_dt').drop(columns=['fecha_dt']).reset_index(drop=True)

    montos_completados = np.where(df['estado'].to_numpy() == 'COMPLETADA', df['monto_usd'].to_numpy(), 0.0)
    df['v_acumulado'] = np.cumsum(montos_completados)

    # B. Paralelismo (Map/Reduce) para Fraude

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reclamos_Fraude")
    cols_reclamos = [desc[0] for desc in cursor.description]
    reclamos = [dict(zip(cols_reclamos, fila)) for fila in cursor.fetchall()]
    conn.close()

    # Dividir la lista de reclamos en fragmentos para asignar a distintos hilos
    num_chunks = 4
    tam_chunk = max(1, (len(reclamos) + num_chunks - 1) // num_chunks)
    fragmentos = list(
        map(lambda idx: reclamos[idx:idx + tam_chunk], range(0, len(reclamos), tam_chunk))
    )

    # MAP: cada hilo procesa su fragmento y emite pares (Resolucion, (Tiempo_Dias, 1))
    def map_fragmento(fragmento):
        validos = filter(
            lambda r: r.get('tiempo_investigacion_dias') is not None and r.get('resolucion') is not None,
            fragmento
        )
        return list(
            map(
                lambda r: (r['resolucion'], (float(r['tiempo_investigacion_dias']), 1)),
                validos
            )
        )

    with ThreadPoolExecutor(max_workers=num_chunks) as executor:
        resultados_por_hilo = list(executor.map(map_fragmento, fragmentos))

    # Aplanar pares emitidos sin bucles for
    pares_mapeados = reduce(lambda acc, sublista: acc + sublista, resultados_por_hilo, [])

    # Filtrar outliers extremos (> 1000 días) antes/durante la reducción
    pares_filtrados = filter(lambda par: par[1][0] <= 1000.0, pares_mapeados)

    # REDUCE: consolidar suma de días y conteo por tipo de resolución
    def reducir_par(acc, par):
        resolucion, (dias, conteo) = par
        suma_actual, conteo_actual = acc.get(resolucion, (0.0, 0))
        return {
            **acc,
            resolucion: (suma_actual + dias, conteo_actual + conteo)
        }

    acumulado_por_resolucion = reduce(reducir_par, pares_filtrados, {})

    # Calcular tiempo promedio de resolución por categoría
    tiempos_promedio_resolucion = {
        resolucion: (totales[0] / totales[1]) if totales[1] > 0 else 0.0
        for resolucion, totales in acumulado_por_resolucion.items()
    }

    print("Etapa 2 finalizada con éxito.")
    return df, tiempos_promedio_resolucion

if __name__ == '__main__':
    from Etapa1 import etapa_1_extraccion_y_transformacion

    datos_limpios = etapa_1_extraccion_y_transformacion()
    df_riesgo, promedios_fraude = etapa_2_analisis_vectorial_y_paralelo(datos_limpios)

    print("Promedio de resolución de fraude (días):", promedios_fraude)
    print(df_riesgo[['id_transaccion', 'moneda', 'monto_original', 'monto_usd', 'score_z', 'v_acumulado']].head())