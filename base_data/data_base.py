import os
import pandas as pd

class BaseDeDatos:
    def __init__(self, ruta_csv="archivo.csv"):
        if not os.path.isfile(ruta_csv):
            raise FileNotFoundError(f"El archivo CSV no existe en la ruta: {ruta_csv}")

        self.ruta_csv = ruta_csv
        self.datos = pd.read_csv(ruta_csv)
        self.inventario = None

    def obtener_datos(self):

        return self.datos

    def actualizar_base(self, ruta_nuevos_datos):
        try:
            nuevos_datos = pd.read_csv(ruta_nuevos_datos)

            if self.datos.equals(nuevos_datos):
                print("Las bases de datos son iguales. No se requiere actualizar.")
                return

            self.datos = pd.concat([self.datos, nuevos_datos]).drop_duplicates()
            self.inventario = None
            print("Base de datos actualizada con éxito.")

        except Exception as e:
            print(f"Error al cargar y actualizar la base de datos: {str(e)}")

    def comparar_bases(self, base_actual, otra_base, fecha):
        datos_base_actual = base_actual.generar_datos_despues_fecha(fecha, self.datos['Fecha'])
        datos_otra_base = otra_base.generar_datos_despues_fecha(fecha, self.datos['Fecha'])

        datos_repetidos = pd.merge(datos_base_actual, datos_otra_base, how='inner', on='ID')
        print("Datos Repetidos Después de la Fecha de Cierre:")
        print(datos_repetidos)

        return datos_repetidos

    def generar_datos_despues_fecha(self, fecha, columna_fecha):
        return self.datos[self.datos[columna_fecha] > fecha]

    def obtener_inventario_datos(self):
        return self.datos.to_dict(orient="records")