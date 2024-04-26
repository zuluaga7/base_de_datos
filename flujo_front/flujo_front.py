import data_base


def validar_informacion(informacion_esperada=None):
    # Obtener la información del módulo base_de_datos.py
    informacion_db = data_base.obtener_informacion()

    # Comparar la información obtenida con la información esperada
    if informacion_db == informacion_esperada:
        return True

    return False


def verificar_informacion(fecha_cierre=None):

    # Obtener la información del módulo base_de_datos.py
    informacion_db = data_base.obtener_informacion()

    # Filtrar la información por fecha de cierre
    informacion_filtrada = []
    for dato in informacion_db:
        if dato["fecha_cierre"] > fecha_cierre:
            informacion_filtrada.append(dato)

    # Encontrar los datos que se repiten en la información filtrada
    datos_repetidos = []
    for dato in informacion_filtrada:
        if dato in datos_repetidos:
            continue
        else:
            datos_repetidos.append(dato)

    # Mostrar los datos que se repiten
    for dato in datos_repetidos:
        print(dato)


class FlujoFront:

    def obtener_datos_repetidos(informacion, fecha_cierre):

        # Filtrar la información por fecha de cierre
        informacion_filtrada = []
        for dato in informacion:
            if dato["fecha_cierre"] > fecha_cierre:
                informacion_filtrada.append(dato)

        # Encontrar los datos que se repiten en la información filtrada
        datos_repetidos = []
        conjunto_datos = set()
        for dato in informacion_filtrada:
            if dato in conjunto_datos:
                datos_repetidos.append(dato)
            else:
                conjunto_datos.add(dato)

        return datos_repetidos

    # Ejemplo de uso
    informacion = [
        {"fecha_cierre": "2023-01-01"},
        {"fecha_cierre": "2023-02-01"},
        {"fecha_cierre": "2023-03-01"},
        {"fecha_cierre": "2023-04-01"},
        {"fecha_cierre": "2023-05-01"},
        {"fecha_cierre": "2023-06-01"},
        {"fecha_cierre": "2023-07-01"},
        {"fecha_cierre": "2023-08-01"},
        {"fecha_cierre": "2023-09-01"},
        {"fecha_cierre": "2023-10-01"},
        {"fecha_cierre": "2023-11-01"},
        {"fecha_cierre": "2023-12-01"},
    ]

    fecha_cierre = "2023-06-01"

    datos_repetidos = obtener_datos_repetidos(informacion, fecha_cierre)

    for dato in datos_repetidos:
        print(dato)



