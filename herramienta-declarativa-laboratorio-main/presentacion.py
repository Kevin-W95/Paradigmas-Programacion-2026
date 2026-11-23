class MensajesUI:
    """
    CAPA 1: PRESENTACIÓN (VISTA)
    Centraliza todos los textos. Facilita traducciones y cambios de interfaz.
    """
    INTRO = (
        "========================================================\n"
        "  Bienvenido a la Herramienta de Análisis Modular\n"
        "========================================================\n"
        "Escribe 'help' o '?' para ver los comandos disponibles.\n"
        "Prueba iniciar con: /cargar datos.csv\n"
    )
    PROMPT_BASE = "dataset-cli> "
    PROMPT_ACTIVO = "({archivo})> "
    
    MENU_AYUDA = (
        "\n--- COMANDOS DISPONIBLES ---\n"
        " /cargar <archivo>         : Carga un dataset CSV en memoria.\n"
        " /listarcolumnas           : Muestra las columnas disponibles.\n"
        " /maxmin [-clean] <col>    : Muestra maximo y minimo.\n"
        " /promedio [-clean] <col>  : Calcula el promedio matematico.\n"
        " /mediana [-clean] <col>   : Calcula la mediana de la columna.\n"
        " /desviacion [-clean] <col>: Calcula la desviacion estandar muestral.\n"
        " /resumen [-clean] <col>   : Genera un reporte estadistico completo.\n"
        " /nulos <col>              : Cuenta registros vacios en la columna.\n"
        " /exportar <archivo>       : Exporta el historial/resumen a un archivo.\n"
        " /unload                   : Cierra el dataset.\n"
        " /quit                     : Sale del programa.\n"
    )

    ERR_ARG_FALTANTE = "[Error] Debes proporcionar un argumento. Ej: {ejemplo}"
    ERR_ARCHIVO_NO_EXISTE = "[Error] El archivo '{archivo}' no se encuentra."
    ERR_CARGA = "[Error] No se pudo cargar el archivo: {error}"
    ERR_NO_DATASET = "[Error] Ningún dataset cargado. Utiliza /cargar <archivo> primero."
    ERR_COLUMNA_NO_EXISTE = "[Error] La columna '{columna}' no existe."
    ERR_VALOR_INVALIDO = "[Error] Valor no numérico '{valor}' en la fila {fila}. Usa '-clean' para omitirlos."
    
    OK_CARGA = "[OK] Dataset '{archivo}' cargado. ({filas} filas, {columnas} columnas)"
    OK_UNLOAD = "[OK] Dataset '{archivo}' descargado de la memoria."
    INFO_SALIDA = "Saliendo de la herramienta de análisis... ¡Hasta luego!"
    INFO_VACIO = "[Info] No se encontraron valores procesables en la columna '{columna}'."
    
    # Nuevos mensajes para los comandos añadidos
    RES_PROMEDIO = "[Resultado] El promedio de '{columna}' es: {promedio:.2f}"
    RES_NULOS = "[Resultado] La columna '{columna}' tiene {cantidad} valores nulos o vacíos."
    RES_MEDIANA = "[Resultado] La mediana de '{columna}' es: {mediana:.2f}"
    RES_DESVIACION = "[Resultado] La desviación estándar de '{columna}' es: {desviacion:.2f}"
    OK_EXPORTAR = "[OK] Reporte exportado exitosamente a '{archivo}'."
    ERR_EXPORTAR = "[Error] No se pudo exportar el archivo: {error}"

    @staticmethod
    def imprimir_columnas(columnas):
        print("\nColumnas disponibles:")
        for col in columnas:
            print(f" - {col}")
        print()
        
    @staticmethod
    def imprimir_maxmin(columna, maximo, minimo):
        print(f"[Resultado] Columna: {columna}")
        print(f" -> Máximo: {maximo}")
        print(f" -> Mínimo: {minimo}")

    @staticmethod
    def imprimir_resumen(datos):
        columna = datos.get("columna", "")
        print(f"\n========================================================")
        print(f"  Resumen Estadístico: {columna}")
        print(f"========================================================")
        print(f" - Total de registros evaluados: {datos.get('total_filas', 0)}")
        print(f" - Valores numéricos válidos:   {datos.get('valores_validos', 0)}")
        print(f" - Celdas nulas o vacías:       {datos.get('nulos', 0)}")
        print(f" - Registros con error:         {datos.get('errores', 0)}")
        
        minimo = datos.get("minimo")
        maximo = datos.get("maximo")
        promedio = datos.get("promedio")
        mediana = datos.get("mediana")
        desviacion = datos.get("desviacion")

        print(f" - Mínimo:                      {f'{minimo:.2f}' if minimo is not None else 'N/A'}")
        print(f" - Máximo:                      {f'{maximo:.2f}' if maximo is not None else 'N/A'}")
        print(f" - Promedio:                    {f'{promedio:.2f}' if promedio is not None else 'N/A'}")
        print(f" - Mediana:                     {f'{mediana:.2f}' if mediana is not None else 'N/A'}")
        print(f" - Desviación estándar:         {f'{desviacion:.2f}' if desviacion is not None else 'N/A'}")
        print(f"========================================================\n")