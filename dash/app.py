# app.py
from dash import Dash, html

# Crear una instancia de la clase Dash
app = Dash(__name__)

# Configurar el diseño de la aplicación
app.layout = html.Div("¡Hola, Dash!")

# Ejecutar la aplicación si este script es el principal
if __name__ == "__main__":
    app.run_server(debug=True)