import os
from data_base import BaseDeDatos

# Set the path to the directory containing the csv files
path = 'C:/Users/MATEO/Documents'

# List of CSV files
csv_files = [
    os.path.join(path, 'dataa_1.csv'),
    os.path.join(path, 'dataa_2.csv')
]

# Create instances of the BaseDeDatos class for each CSV file
dbs = [BaseDeDatos(csv_file) for csv_file in csv_files]

# Access the data from each CSV file
for csv_file, db in zip(csv_files, dbs):
    print(f"Data from file {csv_file}:")
    print(db.obtener_datos())
    print()
