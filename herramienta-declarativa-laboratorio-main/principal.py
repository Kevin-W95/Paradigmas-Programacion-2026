import csv
import os
from controlador import ControladorCLI

def generar_csv_prueba():
    """Genera un archivo de prueba si no existe en el directorio."""
    nombre_archivo = "datos.csv"
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # Fila de cabeceras
            writer.writerow(["id", "nombre", "edad", "salario", "departamento"])
            # Datos de prueba (algunos tienen errores a propósito para probar -clean)
            writer.writerow(["1", "Ana", "28", "4500.50", "Ventas"])
            writer.writerow(["2", "Juan", "35", "5200.00", "IT"])
            writer.writerow(["3", "Maria", "", "6100.75", "Ventas"]) # Edad vacía
            writer.writerow(["4", "Pedro", "42", "ERR", "RRHH"]) # Salario inválido
            writer.writerow(["5", "Lucia", "31", "4800.00", "IT"])
            writer.writerow(["6", "Carlos", " ", "4900.00", ""]) # Nulos y vacíos
        print(f"[*] Se ha generado automáticamente un archivo de prueba '{nombre_archivo}'.\n")

if __name__ == '__main__':
    generar_csv_prueba()
    cli = ControladorCLI()
    try:
        # Esto inicia el bucle infinito esperando comandos del usuario
        cli.cmdloop()
    except KeyboardInterrupt:
        # Captura si el usuario presiona Ctrl+C
        print("\nSaliendo abruptamente...")