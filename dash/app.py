from dash import Dash, html, dcc, Input, Output, dash
import pandas as pd
from data_base.base_de_datos import BaseDeDatos
import webbrowser

# Crear una instancia de la clase Dash
app = Dash(__name__)

# Definir el diseño de la página de bienvenida
pagina_bienvenida_layout = html.Div([
    html.H1("¡Bienvenido a la Aplicación de Análisis de Datos!"),
    html.Button("Ingresar", id="ingresar-button", n_clicks=0)
])

# Definir el diseño de la página principal
pagina_principal_layout = html.Div([
    html.H1("Análisis de datos"),

    # Botón de actualización de datos
    html.Button("Cargar Datos", id="actualizar-button"),

    # Selección de fecha
    html.H1("Buscar por fecha"),
    dcc.DatePickerSingle(
        id='fecha-picker',
        min_date_allowed=pd.to_datetime('2021-11-20'),
        max_date_allowed=pd.to_datetime('today'),
        initial_visible_month=pd.to_datetime('2022-02-10'),
        date=pd.to_datetime('today')
    ),

    # Filtros por categorías
    html.H1("Filtro por categoria"),
    dcc.Dropdown(
        id='categorias-dropdown',
        options=[
            {'label': 'Más repetidos', 'value': 'categoria1'},
            {'label': 'Categoría 2', 'value': 'categoria2'},
            {'label': 'Categoría 3', 'value': 'categoria3'}
        ],
        value=['categoria1', 'categoria2'],
        multi=True
    ),

    # Botón de exportación
    html.Button("Exportar CSV", id="exportar-csv-button"),

    # Selección de variables
    dcc.Dropdown(
        id='variables-dropdown',
        options=[
            {'label': 'Variable 1', 'value': 'variable1'},
            {'label': 'Variable 2', 'value': 'variable2'},
            {'label': 'Variable 3', 'value': 'variable3'}
        ],
        value='variable1'
    ),

    # Botón reinicio
    html.Button("Reiniciar", id="reiniciar-button"),

    # Controles de zoom y pan
    dcc.Graph(id="grafico-numero-filas"),
    html.Hr(),
    dcc.Graph(id="grafico-datos-repetidos")
])

# Callback para redirigir al usuario a la página principal al hacer clic en "Ingresar"
@app.callback(
    Output('url', 'pathname'),
    [Input('ingresar-button', 'n_clicks')]
)
def redireccionar_a_pagina_principal(n_clicks):
    if n_clicks > 0:
        return '/pagina-principal'
    return '/'

# Agregar la ruta para la página principal
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback para mostrar la página correspondiente según la URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def mostrar_pagina(pathname):
    if pathname == '/pagina-principal':
        return pagina_principal_layout
    else:
        return pagina_bienvenida_layout

# Función para cargar los datos
def cargar_datos(fecha):
    try:
        # Crea instancias de la clase BaseDeDatos para cada archivo
        base_de_datos_1 = BaseDeDatos('archivo.csv')
        base_de_datos_2 = BaseDeDatos('otra_base.csv')

        # Actualiza las bases de datos si es necesario
        base_de_datos_1.actualizar_base('nuevos_datos_1.csv')
        base_de_datos_2.actualizar_base('nuevos_datos_2.csv')

        # Comparar las bases de datos si es necesario
        resultados_comparacion = base_de_datos_1.comparar_bases(base_de_datos_2, fecha)

        # Crear una sola figura para ambas visualizaciones
        fig_numero_filas = {
            "data": [
                {"x": ['Power bi', 'Azure'], "y": [len(base_de_datos_1.datos), len(base_de_datos_2.datos)], "type": "bar", "name": "Número de Filas"}
            ],
            "layout": {
                "title": "Cantidad de Datos",
                "xaxis": {"title": "Base de Datos"},
                "yaxis": {"title": "Filas"}
            }
        }

        # Obtener y graficar datos repetidos
        datos_repetidos = base_de_datos_1.obtener_datos_repetidos(base_de_datos_2, fecha)
        fig_datos_repetidos = {
            "data": [
                {"x": datos_repetidos['id'], "y": datos_repetidos['historia'], "type": "scatter", "mode": "markers", "name": "Datos Repetidos"}
            ],
            "layout": {
                "title": "Datos Repetidos",
                "xaxis": {"title": "ID"},
                "yaxis": {"title": "Historia"}
            }
        }

        return fig_numero_filas, fig_datos_repetidos

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None

# Callback para actualizar los datos al hacer clic en el botón
@app.callback(
    [Output("grafico-numero-filas", "figure"),
     Output("grafico-datos-repetidos", "figure")],
    [Input("actualizar-button", "n_clicks"),
     Input("fecha-picker", "date")]
)
def actualizar_datos(n_clicks, fecha):
    if n_clicks is None:
        return dash.no_update, dash.no_update

    # Llamar a la función para cargar los datos
    fig_numero_filas, fig_datos_repetidos = cargar_datos(pd.to_datetime(fecha))

    # Retornar las figuras actualizadas
    return fig_numero_filas, fig_datos_repetidos

# Callback para exportar los datos a CSV
@app.callback(
    Output("exportar-csv-button", "children"),
    [Input("exportar-csv-button", "n_clicks")]
)
def exportar_csv(n_clicks):
    if n_clicks is None:
        return "Exportar CSV"

    # Lógica para exportar los datos a CSV
    # Agregar aquí la lógica para exportar los datos a CSV
    # Por ahora, simplemente retornamos el texto del botón
    return "Exportar CSV"

# Callback para reiniciar la visualización
@app.callback(
    [Output("fecha-picker", "date"),
     Output("variables-dropdown", "value")],
    [Input("reiniciar-button", "n_clicks")]
)
def reiniciar_visualizacion(n_clicks):
    if n_clicks is None:
        return dash.no_update, dash.no_update

    # Lógica para reiniciar la visualización
    # Por ahora, simplemente restablecemos la fecha seleccionada y el valor del dropdown
    return pd.to_datetime('2021-11-20'), 'variable1'

# Ejecutar la aplicación si este script es el principal
if __name__ == "__main__":
    app.run_server(debug=True)

'''from dash import Dash, html, dcc, Input, Output, dash
import pandas as pd
from data_base.base_de_datos import BaseDeDatos

# Crear una instancia de la clase Dash
app = Dash(__name__)

# Definir la estructura de la aplicación
app.layout = html.Div([
    html.H1("Análisis de datos"),

    # Botón de actualización de datos
    html.Button("Cargar Datos", id="actualizar-button"),

    # Selección de fecha
html.H1("Buscar por fecha"),
    dcc.DatePickerSingle(
        id='fecha-picker',
        min_date_allowed=pd.to_datetime('2021-11-20'),
        max_date_allowed=pd.to_datetime('today'),
        initial_visible_month=pd.to_datetime('2022-02-10'),
        date=pd.to_datetime('today')
    ),

    # Filtros por categorías
    html.H1("Filtro por categoria"),
    dcc.Dropdown(
        id='categorias-dropdown',
        options=[
            {'label': 'Más repetidos', 'value': 'categoria1'},
            {'label': 'Categoría 2', 'value': 'categoria2'},
            {'label': 'Categoría 3', 'value': 'categoria3'}
        ],
        value=['categoria1', 'categoria2'],
        multi=True
    ),

    # Botón de exportación
    html.Button("Exportar CSV", id="exportar-csv-button"),

    # Selección de variables
    dcc.Dropdown(
        id='variables-dropdown',
        options=[
            {'label': 'Variable 1', 'value': 'variable1'},
            {'label': 'Variable 2', 'value': 'variable2'},
            {'label': 'Variable 3', 'value': 'variable3'}
        ],
        value='variable1'
    ),

    # Botón reinicio
    html.Button("Reiniciar", id="reiniciar-button"),

    # Controles de zoom y pan
    dcc.Graph(id="grafico-numero-filas"),
    html.Hr(),
    dcc.Graph(id="grafico-datos-repetidos")
])


# Función para cargar los datos
def cargar_datos(fecha):
    try:
        # Crea instancias de la clase BaseDeDatos para cada archivo
        base_de_datos_1 = BaseDeDatos('archivo.csv')
        base_de_datos_2 = BaseDeDatos('otra_base.csv')

        # Actualiza las bases de datos si es necesario
        base_de_datos_1.actualizar_base('nuevos_datos_1.csv')
        base_de_datos_2.actualizar_base('nuevos_datos_2.csv')

        # Comparar las bases de datos si es necesario 
        resultados_comparacion = base_de_datos_1.comparar_bases(base_de_datos_2, fecha)

        # Crear una sola figura para ambas visualizaciones
        fig_numero_filas = {
            "data": [
                {"x": ['Power bi', 'Azure'], "y": [len(base_de_datos_1.datos), len(base_de_datos_2.datos)], "type": "bar", "name": "Número de Filas"}
            ],
            "layout": {
                "title": "Cantidad de Datos",
                "xaxis": {"title": "Base de Datos"},
                "yaxis": {"title": "Filas"}
            }
        }

        # Obtener y graficar datos repetidos
        datos_repetidos = base_de_datos_1.obtener_datos_repetidos(base_de_datos_2, fecha)
        fig_datos_repetidos = {
            "data": [
                {"x": datos_repetidos['id'], "y": datos_repetidos['historia'], "type": "scatter", "mode": "markers", "name": "Datos Repetidos"}
            ],
            "layout": {
                "title": "Datos Repetidos",
                "xaxis": {"title": "ID"},
                "yaxis": {"title": "Historia"}
            }
        }

        return fig_numero_filas, fig_datos_repetidos

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None


# Callback para actualizar los datos al hacer clic en el botón
@app.callback(
    [Output("grafico-numero-filas", "figure"),
     Output("grafico-datos-repetidos", "figure")],
    [Input("actualizar-button", "n_clicks"),
     Input("fecha-picker", "date")]
)
def actualizar_datos(n_clicks, fecha):
    if n_clicks is None:
        return dash.no_update, dash.no_update

    # Llamar a la función para cargar los datos
    fig_numero_filas, fig_datos_repetidos = cargar_datos(pd.to_datetime(fecha))

    # Retornar las figuras actualizadas
    return fig_numero_filas, fig_datos_repetidos


# Callback para exportar los datos a CSV
@app.callback(
    Output("exportar-csv-button", "children"),
    [Input("exportar-csv-button", "n_clicks")]
)
def exportar_csv(n_clicks):
    if n_clicks is None:
        return "Exportar CSV"

    # Lógica para exportar los datos a CSV
    # Agregar aquí la lógica para exportar los datos a CSV
    # Por ahora, simplemente retornamos el texto del botón
    return "Exportar CSV"


# Callback para reiniciar la visualización
@app.callback(
    [Output("fecha-picker", "date"),
     Output("variables-dropdown", "value")],
    [Input("reiniciar-button", "n_clicks")]
)
def reiniciar_visualizacion(n_clicks):
    if n_clicks is None:
        return dash.no_update, dash.no_update

    # Lógica para reiniciar la visualización
    # Por ahora, simplemente restablecemos la fecha seleccionada y el valor del dropdown
    return pd.to_datetime('2021-11-20'), 'variable1'


# Ejecutar la aplicación si este script es el principal
if __name__ == "__main__":
    app.run_server(debug=True) '''

'''import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash
from data_base.base_de_datos import BaseDeDatos

# Crear una instancia de la clase Dash
app = Dash(__name__)

# Definir la estructura de la aplicación
app.layout = html.Div([
    html.H1("Visualización de Datos"),

    # Botón de actualización de datos
    html.Button("Actualizar Datos", id="actualizar-button"),

    # Gráfico de barras para visualizar el número de filas en cada base de datos
    dcc.Graph(id="grafico-numero-filas"),
    html.Hr(),
    # Gráfico para visualizar los datos repetidos
    dcc.Graph(id="grafico-datos-repetidos")
])


# Función para cargar los datos
def cargar_datos():
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
        fig_numero_filas = {
            "data": [
                {"x": ['Base de Datos 1', 'Base de Datos 2'], "y": [len(base_de_datos_1.datos), len(base_de_datos_2.datos)], "type": "bar", "name": "Número de Filas"}
            ],
            "layout": {
                "title": "Número de Filas en Cada Base de Datos",
                "xaxis": {"title": "Base de Datos"},
                "yaxis": {"title": "Número de Filas"}
            }
        }

        # Obtener y graficar datos repetidos
        datos_repetidos = base_de_datos_1.obtener_datos_repetidos(base_de_datos_2, '2022-01-01')
        fig_datos_repetidos = {
            "data": [
                {"x": datos_repetidos['id'], "y": datos_repetidos['historia'], "type": "scatter", "mode": "markers", "name": "Datos Repetidos"}
            ],
            "layout": {
                "title": "Datos Repetidos",
                "xaxis": {"title": "ID"},
                "yaxis": {"title": "Historia"}
            }
        }

        return fig_numero_filas, fig_datos_repetidos

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None


# Callback para actualizar los datos al hacer clic en el botón
@app.callback(
    [Output("grafico-numero-filas", "figure"),
     Output("grafico-datos-repetidos", "figure")],
    [Input("actualizar-button", "n_clicks")]
)
def actualizar_datos(n_clicks):
    if n_clicks is None:
        return dash.no_update, dash.no_update

    # Llamar a la función para cargar los datos
    fig_numero_filas, fig_datos_repetidos = cargar_datos()

    # Retornar las figuras actualizadas
    return fig_numero_filas, fig_datos_repetidos


# Ejecutar la aplicación si este script es el principal
if __name__ == "__main__":
    app.run_server(debug=True)'''
