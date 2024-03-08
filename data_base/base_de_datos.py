import os
import pandas as pd

class BaseDeDatos:
    def __init__(self, nombre_archivo="archivo.csv", ruta="C:\\Users\\MATEO\\Documents\\python\\app_z_data\\data"):
        self.ruta_csv = os.path.join(ruta, nombre_archivo)
        self.datos = None
        self.inventario = None

        self.cargar_datos()

    def cargar_datos(self):
        try:
            self.datos = pd.read_csv(self.ruta_csv)
        except FileNotFoundError:
            print(f"Error: El archivo CSV no se encontró en la ruta: {self.ruta_csv}")
        except pd.errors.EmptyDataError:
            print(f"Error: El archivo CSV está vacío: {self.ruta_csv}")
        except Exception as e:
            print(f"Error al cargar los datos: {str(e)}")

    def actualizar_base(self, ruta_nuevos_datos_1='nuevos_datos_1.csv', ruta_nuevos_datos_2='nuevos_datos_2.csv'):
        try:
            # Verifica si los archivos CSV existen en las rutas especificadas
            ruta_completa_1 = os.path.join("C:\\Users\\MATEO\\Documents\\python\\app_z_data\\data", ruta_nuevos_datos_1)
            print(f"Ruta completa del archivo 1: {ruta_completa_1}")

            if not os.path.isfile(ruta_completa_1):
                print(f"Error: El archivo CSV no existe en la ruta: {ruta_completa_1}")
                return

            ruta_completa_2 = os.path.join("C:\\Users\\MATEO\\Documents\\python\\app_z_data\\data", ruta_nuevos_datos_2)
            print(f"Ruta completa del archivo 2: {ruta_completa_2}")

            if not os.path.isfile(ruta_completa_2):
                print(f"Error: El archivo CSV no existe en la ruta: {ruta_completa_2}")
                return

            # Carga los datos de los archivos CSV en DataFrames
            nuevos_datos_1 = pd.read_csv(ruta_completa_1)
            nuevos_datos_2 = pd.read_csv(ruta_completa_2)

            # Verifica si los DataFrames están vacíos
            if nuevos_datos_1.empty or nuevos_datos_2.empty:
                print("Error: Uno o ambos archivos CSV están vacíos.")
                return

            print("Contenido de nuevos_datos_1:")
            print(nuevos_datos_1)

            print("Contenido de nuevos_datos_2:")
            print(nuevos_datos_2)

            # Continúa con el procesamiento de los datos según tus necesidades
            # ...

        except pd.errors.EmptyDataError:
            print(f"Error: El archivo CSV está vacío: {ruta_completa_1} o {ruta_completa_2}")
        except pd.errors.ParserError as pe:
            print(f"Error al analizar el archivo CSV: {str(pe)}")
        except Exception as e:
            print(f"Error al cargar y actualizar la base de datos: {str(e)}")

    def comparar_bases(self, otra_base, fecha):
        try:
            if self.datos is None or otra_base.datos is None:
                print("Error: Los datos no han sido cargados.")
                return pd.DataFrame()

            # Eliminar espacios adicionales en los nombres de las columnas
            self.datos.columns = self.datos.columns.str.strip()
            otra_base.datos.columns = otra_base.datos.columns.str.strip()

            # Imprimir las columnas de ambas bases de datos
            print("Columnas de self:", self.datos.columns)
            print("Columnas de otra_base:", otra_base.datos.columns)

            # Verificar si la columna 'Fecha' existe en ambas bases de datos
            if 'fecha' not in self.datos.columns or 'fecha' not in otra_base.datos.columns:
                print("Error: La columna 'Fecha' no está presente en ambas bases de datos.")
                return pd.DataFrame()

            datos_base_actual = self.generar_datos_despues_fecha(fecha, 'fecha')
            datos_otra_base = otra_base.generar_datos_despues_fecha(fecha, 'fecha')

            # Corregir la llamada a pd.merge() - cerrar paréntesis y proporcionar columnas en la cláusula 'on' como lista
            datos_repetidos = pd.merge(datos_base_actual, datos_otra_base, how='inner', on=['id', 'historia', 'fecha'])

            if not datos_repetidos.empty:
                print("Datos Repetidos Después de la Fecha de Cierre:")
                print(datos_repetidos)

            return datos_repetidos

        except Exception as e:
            print(f"Error al comparar las bases de datos: {str(e)}")

    def generar_datos_despues_fecha(self, fecha, columna_fecha):
        if self.datos is None:
            print("Error: Los datos no han sido cargados.")
            return pd.DataFrame()
        return self.datos[self.datos[columna_fecha] > fecha]

    def obtener_inventario_datos(self):
        return self.datos.to_dict(orient="records")

    def obtener_datos(self):
        return self.datos

    def obtener_datos_repetidos(self, otra_base, fecha):
        try:
            datos_comparados = self.comparar_bases(otra_base, fecha)
            return datos_comparados
        except Exception as e:
            print(f"Error al obtener datos repetidos: {str(e)}")
            return pd.DataFrame()
