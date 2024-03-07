import matplotlib.pyplot as plt
from data_base import BaseDeDatos

# Crea una instancia de la clase BaseDeDatos
base_de_datos = BaseDeDatos('archivo.csv')

# Actualiza la base de datos
base_de_datos.actualizar_base('nuevos_datos.csv')

# Comparar las bases de datos
otra_base_de_datos = BaseDeDatos('otra_base.csv')
resultados_comparacion = base_de_datos.comparar_bases(base_de_datos, otra_base_de_datos, '2022-01-01')

# Visualizar los datos
# Por ejemplo, crear un gráfico de barras para mostrar el número de filas en cada base de datos
datos_base = base_de_datos.obtener_datos()
datos_otra_base = otra_base_de_datos.obtener_datos()

# Agrupar los datos por base de datos y contar el número de filas
datos_agrupados = datos_base.append(datos_otra_base).groupby(datos_base.index // len(datos_base)).size().reset_index(name='counts')
datos_agrupados.columns = ['base_de_datos', 'counts']

# Crear un gráfico de barras
plt.bar(datos_agrupados['base_de_datos'], datos_agrupados['counts'])
plt.xlabel('Base de Datos')
plt.ylabel('Número de Filas')
plt.title('Número de Filas en Cada Base de Datos')
plt.show()
'''import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from base_de_datos.base_de_datos import BaseDeDatos
from flujo_integracion.flujo_integracion import FlujoIntegracion

app = dash.Dash(__name__)

base_de_datos = BaseDeDatos('datos/archivo.csv')  # Asegúrate de tener el archivo de datos en la carpeta "datos"
otra_base_de_datos = BaseDeDatos('datos/otro_archivo.csv')  # Cambia a la ruta de tu segunda base de datos
flujo_integracion = FlujoIntegracion()

app.layout = html.Div([
    html.H1("Dashboard de Mi Proyecto"),

    dcc.Graph(
        id='grafico-comparacion',
        figure={
            'data': [],
            'layout': {
                'title': 'Comparación de Datos',
            }
        }
    ),

    html.H3("Inventario"),
    html.Table(id='tabla-inventario'),

    # Otros componentes según necesidades adicionales
])

@app.callback(
    Output('grafico-comparacion', 'figure'),
    [Input('actualizar-boton', 'n_clicks')]  # Puedes agregar más entradas según sea necesario
)
def actualizar_grafico_comparacion(n_clicks):
    datos_comparacion = flujo_integracion.comparar_bases(base_de_datos, otra_base_de_datos, 'fecha')
    # Puedes personalizar la lógica según los datos de comparación actualizados

    return {
        'data': [ ... ],  # Personaliza según los datos de comparación actualizados
        'layout': {
            'title': 'Comparación de Datos Actualizada',
        }
    }

@app.callback(
    Output('tabla-inventario', 'children'),
    [Input('actualizar-boton', 'n_clicks')]  # Puedes agregar más entradas según sea necesario
)
def actualizar_tabla_inventario(n_clicks):
    inventario_actual = base_de_datos.obtener_inventario()
    # Puedes personalizar la lógica según el inventario actualizado

    filas = [html.Tr([html.Td(col) for col in inventario_actual.columns])] + \
            [html.Tr([html.Td(dato) for dato in fila]) for fila in inventario_actual.values]

    return filas

if __name__ == '__main__':
    app.run_server(debug=True)
'''