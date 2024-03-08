import matplotlib.pyplot as plt
from data_base.base_de_datos import BaseDeDatos

try:
    # Crea instancias de la clase BaseDeDatos para cada archivo
    base_de_datos_1 = BaseDeDatos('archivo.csv')
    base_de_datos_2 = BaseDeDatos('otra_base.csv')

    # Actualiza las bases de datos si es necesario
    base_de_datos_1.actualizar_base('nuevos_datos_1.csv')
    base_de_datos_2.actualizar_base('nuevos_datos_2.csv')

    # Comparar las bases de datos si es necesario
    resultados_comparacion = base_de_datos_1.comparar_bases(base_de_datos_2, '2022-01-01')

    # Crear una sola figura para ambas visualizaciones
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 8))

    # Crear un gráfico de barras
    ax1.bar(['Base de Datos 1', 'Base de Datos 2'], [len(base_de_datos_1.datos), len(base_de_datos_2.datos)])
    ax1.set_xlabel('Base de Datos')
    ax1.set_ylabel('Número de Filas')
    ax1.set_title('Número de Filas en Cada Base de Datos')

    # Obtener y graficar datos repetidos
    datos_repetidos = base_de_datos_1.obtener_datos_repetidos(base_de_datos_1, '2022-01-01')
    if not datos_repetidos.empty:
        # Personaliza la visualización de los datos repetidos según tu necesidad
        ax2.scatter(datos_repetidos['id'], datos_repetidos['historia'], label='Datos Repetidos')
        ax2.set_xlabel('ID')
        ax2.set_ylabel('Historia')
        ax2.set_title('Datos Repetidos')
        ax2.legend()

    # Mostrar la figura
    plt.tight_layout()
    plt.show()

except FileNotFoundError as e:
    print(f"Error: {e}")


def app():
    return None