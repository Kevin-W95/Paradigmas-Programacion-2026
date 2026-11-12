import unittest
import io
import os
import sys
from logica import MotorAnalisis
from controlador import ControladorCLI

class TestMotorAnalisis(unittest.TestCase):
    def setUp(self):
        self.motor = MotorAnalisis()
        self.filas, self.cols = self.motor.cargar_csv("datos.csv")

    def test_cargar_csv(self):
        self.assertTrue(self.motor.esta_cargado())
        self.assertGreater(self.filas, 0)
        self.assertIn("salario", self.motor.columnas)
        self.assertIn("edad", self.motor.columnas)

    def test_calcular_maxmin_sin_clean(self):
        exito, resultado = self.motor.calcular_maxmin("salario", omitir_errores=False)
        self.assertFalse(exito)
        valor, fila = resultado
        self.assertEqual(valor, "ERR")
        self.assertEqual(fila, 5)

    def test_calcular_maxmin_con_clean(self):
        exito, resultado = self.motor.calcular_maxmin("salario", omitir_errores=True)
        self.assertTrue(exito)
        max_val, min_val = resultado
        self.assertEqual(max_val, 6100.75)
        self.assertEqual(min_val, 4500.50)

    def test_calcular_promedio_con_error(self):
        with self.assertRaises(ValueError) as cm:
            self.motor.calcular_promedio("salario", omitir_errores=False)
        self.assertTrue(hasattr(cm.exception, 'valor'))
        self.assertEqual(cm.exception.valor, "ERR")

    def test_calcular_promedio_con_clean(self):
        prom = self.motor.calcular_promedio("salario", omitir_errores=True)
        # Valores validos: 4500.50, 5200.00, 6100.75, 4800.00
        # Suma: 20601.25 / 4 = 5150.3125
        self.assertAlmostEqual(prom, 5150.3125, places=3)

    def test_calcular_mediana_impar_y_par(self):
        # Cardinalidad impar
        self.motor.dataset = [{"x": "10"}, {"x": "30"}, {"x": "20"}]
        self.motor.columnas = ["x"]
        self.assertEqual(self.motor.calcular_mediana("x"), 20.0)

        # Cardinalidad par
        self.motor.dataset = [{"x": "10"}, {"x": "20"}, {"x": "30"}, {"x": "40"}]
        self.assertEqual(self.motor.calcular_mediana("x"), 25.0)

    def test_calcular_desviacion(self):
        # Conjunto [10, 20, 30] -> media = 20
        # Varianza = ((10-20)^2 + (20-20)^2 + (30-20)^2) / 2 = 200 / 2 = 100
        # Desviacion = 10.0
        self.motor.dataset = [{"x": "10"}, {"x": "20"}, {"x": "30"}]
        self.motor.columnas = ["x"]
        self.assertAlmostEqual(self.motor.calcular_desviacion("x"), 10.0, places=3)

    def test_generar_resumen(self):
        res = self.motor.generar_resumen("salario", omitir_errores=True)
        self.assertEqual(res["columna"], "salario")
        self.assertEqual(res["total_filas"], 5)
        self.assertEqual(res["valores_validos"], 4)
        self.assertEqual(res["errores"], 1)
        self.assertEqual(res["minimo"], 4500.50)
        self.assertEqual(res["maximo"], 6100.75)

    def test_delimitador_alternativo(self):
        ruta_temp = "datos_puntoycoma.csv"
        try:
            with open(ruta_temp, "w", encoding="utf-8") as f:
                f.write("id;nombre;valor\n1;A;100\n2;B;200\n")
            motor_temp = MotorAnalisis()
            filas, cols = motor_temp.cargar_csv(ruta_temp)
            self.assertEqual(filas, 2)
            self.assertEqual(cols, 3)
            self.assertIn("valor", motor_temp.columnas)
        finally:
            if os.path.exists(ruta_temp):
                os.remove(ruta_temp)

    def test_contar_nulos(self):
        self.motor.dataset = [
            {"val": "hola"},
            {"val": ""},
            {"val": "   "},
            {"val": "mundo"}
        ]
        self.motor.columnas = ["val"]
        self.assertEqual(self.motor.contar_nulos("val"), 2)


class TestControladorCLI(unittest.TestCase):
    def setUp(self):
        self.cli = ControladorCLI()

    def ejecutar_comando(self, comando):
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            linea = self.cli.precmd(comando)
            self.cli.onecmd(linea)
        finally:
            sys.stdout = sys_stdout
        return captured_output.getvalue()

    def test_flujo_extendido(self):
        # 1. Cargar datos
        out_carga = self.ejecutar_comando("/cargar datos.csv")
        self.assertIn("[OK] Dataset 'datos.csv' cargado", out_carga)

        # 2. Promedio con -clean
        out_prom = self.ejecutar_comando("/promedio -clean salario")
        self.assertIn("5150.31", out_prom)

        # 3. Mediana con -clean
        out_med = self.ejecutar_comando("/mediana -clean salario")
        self.assertIn("5000.00", out_med)

        # 4. Desviacion con -clean
        out_desv = self.ejecutar_comando("/desviacion -clean salario")
        self.assertIn("[Resultado]", out_desv)

        # 5. Resumen
        out_res = self.ejecutar_comando("/resumen -clean salario")
        self.assertIn("Resumen Estadístico: salario", out_res)

        # 6. Autocompletado
        sugerencias = self.cli.complete_columna("sal", "/promedio sal", 10, 13)
        self.assertIn("salario", sugerencias)

        # 7. Exportar
        ruta_rep = "reporte_test.txt"
        try:
            out_exp = self.ejecutar_comando(f"/exportar {ruta_rep}")
            self.assertIn("[OK] Reporte exportado", out_exp)
            self.assertTrue(os.path.exists(ruta_rep))
        finally:
            if os.path.exists(ruta_rep):
                os.remove(ruta_rep)


if __name__ == '__main__':
    unittest.main()
