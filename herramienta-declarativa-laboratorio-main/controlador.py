import cmd
import os
import shlex
from presentacion import MensajesUI
from logica import MotorAnalisis

class ControladorCLI(cmd.Cmd):
    """
    CAPA 3: PROCESAMIENTO DE COMANDOS (CONTROLADOR)
    Recibe la entrada del usuario, llama a "logica.py" e imprime con "presentacion.py".
    """
    intro = MensajesUI.INTRO
    prompt = MensajesUI.PROMPT_BASE

    def __init__(self):
        super().__init__()
        self.motor = MotorAnalisis()
        self.ultimo_analisis = []

    def _parsear_columna_y_clean(self, arg, ejemplo):
        args = shlex.split(arg) if arg else []
        clean = '-clean' in args
        if clean:
            args.remove('-clean')
        if not args:
            print(MensajesUI.ERR_ARG_FALTANTE.format(ejemplo=ejemplo))
            return None, clean
        return args[0], clean

    def complete_columna(self, text, line, begidx, endidx):
        if not self.motor.esta_cargado():
            return []
        return [c for c in self.motor.columnas if c.lower().startswith(text.lower())]

    complete_maxmin = complete_columna
    complete_promedio = complete_columna
    complete_mediana = complete_columna
    complete_desviacion = complete_columna
    complete_resumen = complete_columna
    complete_nulos = complete_columna

    def precmd(self, line):
        """Permite que los comandos se escriban con o sin '/' inicial."""
        line = line.strip()
        if line.startswith('/'):
            line = line[1:] 
        return line

    def _verificar_estado(self):
        if not self.motor.esta_cargado():
            print(MensajesUI.ERR_NO_DATASET)
            return False
        return True

    def do_cargar(self, arg):
        """Comando base implementado como ejemplo."""
        if not arg:
            print(MensajesUI.ERR_ARG_FALTANTE.format(ejemplo="/cargar datos.csv"))
            return
        if not os.path.exists(arg):
            print(MensajesUI.ERR_ARCHIVO_NO_EXISTE.format(archivo=arg))
            return
        try:
            filas, cols = self.motor.cargar_csv(arg)
            print(MensajesUI.OK_CARGA.format(archivo=arg, filas=filas, columnas=cols))
            self.prompt = MensajesUI.PROMPT_ACTIVO.format(archivo=arg)
        except Exception as e:
            print(MensajesUI.ERR_CARGA.format(error=str(e)))

    def do_listarcolumnas(self, arg):
        if not self._verificar_estado(): return
        MensajesUI.imprimir_columnas(self.motor.columnas)

    def do_maxmin(self, arg):
        """Calcula el maximo y minimo de una columna."""
        if not self._verificar_estado(): return
        columna, clean = self._parsear_columna_y_clean(arg, "/maxmin [-clean] salario")
        if not columna: return

        try:
            exito, resultado = self.motor.calcular_maxmin(columna, omitir_errores=clean)
            if exito:
                maximo, minimo = resultado
                if maximo is None:
                    print(MensajesUI.INFO_VACIO.format(columna=columna))
                else:
                    MensajesUI.imprimir_maxmin(columna, maximo, minimo)
                    self.ultimo_analisis.append(f"MaxMin ({columna}): Max={maximo}, Min={minimo}")
            else:
                valor, fila = resultado
                print(MensajesUI.ERR_VALOR_INVALIDO.format(valor=valor, fila=fila))
        except KeyError:
            print(MensajesUI.ERR_COLUMNA_NO_EXISTE.format(columna=columna))

    def do_promedio(self, arg):
        """Calcula el promedio de una columna."""
        if not self._verificar_estado(): return
        columna, clean = self._parsear_columna_y_clean(arg, "/promedio [-clean] salario")
        if not columna: return
        
        try:
            promedio = self.motor.calcular_promedio(columna, omitir_errores=clean)
            print(MensajesUI.RES_PROMEDIO.format(columna=columna, promedio=promedio))
            self.ultimo_analisis.append(f"Promedio ({columna}): {promedio:.2f}")
        except KeyError:
            print(MensajesUI.ERR_COLUMNA_NO_EXISTE.format(columna=columna))
        except ValueError as e:
            if hasattr(e, 'valor') and hasattr(e, 'fila'):
                print(MensajesUI.ERR_VALOR_INVALIDO.format(valor=e.valor, fila=e.fila))
            else:
                print(f"[Error] {e}")

    def do_mediana(self, arg):
        """Calcula la mediana de una columna."""
        if not self._verificar_estado(): return
        columna, clean = self._parsear_columna_y_clean(arg, "/mediana [-clean] salario")
        if not columna: return

        try:
            mediana = self.motor.calcular_mediana(columna, omitir_errores=clean)
            print(MensajesUI.RES_MEDIANA.format(columna=columna, mediana=mediana))
            self.ultimo_analisis.append(f"Mediana ({columna}): {mediana:.2f}")
        except KeyError:
            print(MensajesUI.ERR_COLUMNA_NO_EXISTE.format(columna=columna))
        except ValueError as e:
            if hasattr(e, 'valor') and hasattr(e, 'fila'):
                print(MensajesUI.ERR_VALOR_INVALIDO.format(valor=e.valor, fila=e.fila))
            else:
                print(f"[Error] {e}")

    def do_desviacion(self, arg):
        """Calcula la desviacion estandar muestral de una columna."""
        if not self._verificar_estado(): return
        columna, clean = self._parsear_columna_y_clean(arg, "/desviacion [-clean] salario")
        if not columna: return

        try:
            desviacion = self.motor.calcular_desviacion(columna, omitir_errores=clean)
            print(MensajesUI.RES_DESVIACION.format(columna=columna, desviacion=desviacion))
            self.ultimo_analisis.append(f"Desviacion ({columna}): {desviacion:.2f}")
        except KeyError:
            print(MensajesUI.ERR_COLUMNA_NO_EXISTE.format(columna=columna))
        except ValueError as e:
            if hasattr(e, 'valor') and hasattr(e, 'fila'):
                print(MensajesUI.ERR_VALOR_INVALIDO.format(valor=e.valor, fila=e.fila))
            else:
                print(f"[Error] {e}")

    def do_resumen(self, arg):
        """Genera un resumen estadistico descriptivo completo de una columna."""
        if not self._verificar_estado(): return
        columna, clean = self._parsear_columna_y_clean(arg, "/resumen [-clean] salario")
        if not columna: return

        try:
            datos = self.motor.generar_resumen(columna, omitir_errores=clean)
            MensajesUI.imprimir_resumen(datos)
            self.ultimo_analisis.append(f"Resumen ({columna}): {datos}")
        except KeyError:
            print(MensajesUI.ERR_COLUMNA_NO_EXISTE.format(columna=columna))
        except ValueError as e:
            if hasattr(e, 'valor') and hasattr(e, 'fila'):
                print(MensajesUI.ERR_VALOR_INVALIDO.format(valor=e.valor, fila=e.fila))
            else:
                print(f"[Error] {e}")

    def do_nulos(self, arg):
        """Cuenta los registros vacios o con espacios en una columna."""
        if not self._verificar_estado(): return
        args = shlex.split(arg) if arg else []
        if not args:
            print(MensajesUI.ERR_ARG_FALTANTE.format(ejemplo="/nulos edad"))
            return
        
        columna = args[0]
        try:
            cantidad = self.motor.contar_nulos(columna)
            print(MensajesUI.RES_NULOS.format(columna=columna, cantidad=cantidad))
            self.ultimo_analisis.append(f"Nulos ({columna}): {cantidad}")
        except KeyError:
            print(MensajesUI.ERR_COLUMNA_NO_EXISTE.format(columna=columna))

    def do_exportar(self, arg):
        """Exporta el reporte de resultados acumulados a un archivo de texto."""
        if not self._verificar_estado(): return
        args = shlex.split(arg) if arg else []
        if not args:
            print(MensajesUI.ERR_ARG_FALTANTE.format(ejemplo="/exportar reporte.txt"))
            return
        
        ruta_salida = args[0]
        try:
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write("========================================================\n")
                f.write(f"  Reporte de Analisis CLI - Dataset: {self.motor.archivo_actual}\n")
                f.write("========================================================\n\n")
                f.write(f"Columnas disponibles: {', '.join(self.motor.columnas)}\n")
                f.write(f"Total de registros: {len(self.motor.dataset)}\n\n")
                f.write("--- HISTORIAL DE ANALISIS EJECUTADOS ---\n")
                if not self.ultimo_analisis:
                    f.write("No se ejecutaron analisis previos en esta sesion.\n")
                else:
                    for linea in self.ultimo_analisis:
                        f.write(f" - {linea}\n")
                f.write("\n========================================================\n")
            print(MensajesUI.OK_EXPORTAR.format(archivo=ruta_salida))
        except Exception as e:
            print(MensajesUI.ERR_EXPORTAR.format(error=str(e)))

    def do_help(self, arg):
        """TODO 4: Sobrescribe la ayuda de Python por defecto."""
        # Imprime MensajesUI.MENU_AYUDA en lugar del menú estándar de cmd.
        print(MensajesUI.MENU_AYUDA)

    def do_unload(self, arg):
        if not self._verificar_estado(): return
        nombre = self.motor.descargar()
        self.prompt = MensajesUI.PROMPT_BASE
        print(MensajesUI.OK_UNLOAD.format(archivo=nombre))

    def do_quit(self, arg):
        print(MensajesUI.INFO_SALIDA)
        return True 
        
    def do_EOF(self, arg):
        return self.do_quit(arg)