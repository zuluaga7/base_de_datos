import os
import pandas as pd
import matplotlib.pyplot as plt
from data_base.base_de_datos import BaseDeDatos
from flujo_integracion.flujo_integracion import FlujoIntegracion
from dashboard.dashboard import  app

def cargar_datos_desde_ruta(ruta, nombre_archivo):
    ruta_csv = os.path.join(ruta, nombre_archivo)

    if not os.path.isfile(ruta_csv):
        raise FileNotFoundError(f"El archivo CSV no existe en la ruta: {ruta_csv}")

    try:
        datos = pd.read_csv(ruta_csv)
        # Convertir la columna 'fecha' al formato datetime
        datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')
        return datos
    except Exception as e:
        raise Exception(f"Error al cargar los datos desde {ruta_csv}: {str(e)}")


def actualizar_base_de_datos(base_datos, ruta_nuevos_datos):
    try:
        datos_nuevos = cargar_datos_desde_ruta(*ruta_nuevos_datos.split('/'))
        base_datos.actualizar_base(datos_nuevos)
        print(f"Base de datos '{ruta_nuevos_datos}' actualizada con éxito.")
    except FileNotFoundError as e:
        print(e)

def ejecutar_proyecto():
    ruta_datos = 'C:\\Users\\MATEO\\Documents\\python\\app_z_data\\data'
    nombre_archivo_base = 'archivo.csv'
    nombre_nuevos_datos_1 = 'nuevos_datos_1.csv'
    nombre_nuevos_datos_2 = 'nuevos_datos_2.csv'

    bases_de_datos = [
        BaseDeDatos(nombre_archivo_base, ruta_datos),
        BaseDeDatos(nombre_nuevos_datos_1, ruta_datos),
        BaseDeDatos(nombre_nuevos_datos_2, ruta_datos)
    ]

    nuevos_datos_rutas = [
        os.path.join(ruta_datos, nombre_nuevos_datos_1),
        os.path.join(ruta_datos, nombre_nuevos_datos_2),
        os.path.join(ruta_datos, nombre_nuevos_datos_2)
    ]

    for base_datos, nuevos_datos_ruta in zip(bases_de_datos[1:], nuevos_datos_rutas[1:]):
        actualizar_base_de_datos(base_datos, nuevos_datos_ruta)

    fecha_especifica = pd.Timestamp('21-11-20221 00:00:00')

    # Crear una sola figura para ambas visualizaciones
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    # Obtener y graficar datos repetidos
    for i in range(1, 3):
        datos_comparados = bases_de_datos[0].comparar_bases(bases_de_datos[0], bases_de_datos[i], fecha_especifica)

        flujo_integracion = FlujoIntegracion()
        flujo_integracion.validar_y_verificar_estado(datos_comparados)
        flujo_integracion.enviar_registro_datos_posteriores(datos_comparados)

        datos_repetidos = bases_de_datos[0].obtener_datos_repetidos(bases_de_datos[i], fecha_especifica)
        if not datos_repetidos.empty:
            ax1.scatter(datos_repetidos['id'], datos_repetidos['historia'], label=f'Datos Repetidos ({bases_de_datos[0].nombre} vs {bases_de_datos[i].nombre})')
            ax1.set_xlabel('ID')
            ax1.set_ylabel('Historia')
            ax1.set_title(f'Datos Repetidos ({bases_de_datos[0].nombre} vs {bases_de_datos[i].nombre})')
            ax1.legend()

    # Obtener y graficar datos de cada base
    for i in range(3):
        datos = bases_de_datos[i].obtener_datos(fecha_especifica)
        ax2.hist(datos['historia'], bins=50, alpha=0.5, label=bases_de_datos[i].nombre)
        ax2.set_xlabel('Historia')
        ax2.set_ylabel('Frecuencia')
        ax2.set_title('Histograma de Historia')
        ax2.legend()

    # Ajustar el espacio entre los dos subplots
    plt.subplots_adjust(hspace=0.5)

    # Mostrar la figura
    plt.show()

    app.run_server(debug=True)

def obtener_datos(self, fecha_especifica):
    return self.datos[self.datos['fecha'] >= fecha_especifica]

# Llamada a la función ejecutar_proyecto
ejecutar_proyecto()
