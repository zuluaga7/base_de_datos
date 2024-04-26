class FlujoIntegracion:
    def __init__(self):
        self.expected_columns = ['ID', 'Nombre', 'Apellido', 'Fecha', 'Valor']
        self.expected_values = {'Valor': [-1.0, 0.0, 1.0]}

    def generar_datos_despues_fecha(self, base, fecha, column_name):
        # Assuming that the 'base' argument is a pandas DataFrame
        return base[base[column_name] > fecha]

    def comparar_bases(self, base1, base2, fecha):
        # Your implementation here
        datos_base1 = self.generar_datos_despues_fecha(base1, fecha, base1.datos['Fecha'])
        datos_base2 = self.generar_datos_despues_fecha(base2, fecha, base2.datos['Fecha'])

        datos_repetidos = datos_base1.merge(datos_base2, how='inner', on='ID')

        if not datos_repetidos.empty:
            print("Datos Repetidos Después de la Fecha de Cierre:")
            print(datos_repetidos)

        return datos_repetidos

    def validar_y_verificar_estado(self, datos_comparados):
        # Check if there are any duplicate rows in the 'datos_comparados' DataFrame
        duplicates = datos_comparados[datos_comparados.duplicated()]

        if not duplicates.empty:
            raise ValueError("Duplicate rows detected in the 'datos_comparados' DataFrame.")

        # Check if the 'datos_comparados' DataFrame contains all the necessary columns
        missing_columns = set(self.expected_columns) - set(datos_comparados.columns)

        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}.")

        # Check if the 'datos_comparados' DataFrame contains any unexpected values
        unexpected_values = datos_comparados[datos_comparados.isin(self.expected_values).all(1) == False]

        if not unexpected_values.empty:
            raise ValueError("Unexpected values detected in the 'datos_comparados' DataFrame.")

        # If all the checks pass, set the 'estado' attribute to 'correcto'
        self.estado = 'correcto'

    def enviar_registro_datos_posteriores(self, datos_comparados):
        # Serialize the 'datos_comparados' DataFrame to a JSON string
        datos_json = datos_comparados.to_json(orient='records')

        # Define the URL and data for the HTTP request
        url = 'http://example.com/api/v1/data'
        data = {'datos': datos_json}

        # Make the HTTP request using the 'requests' library
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})

        # Check if the request was successful
        if response.status_code == 200:
            # Set the 'estado' attribute to 'correcto'
            self.estado = 'correcto'
        else:
            # Set the 'estado' attribute to 'error'
            self.estado = 'error'

            # Raise an exception with the error message
            raise ValueError(f"Error sending the data: {response.text}")