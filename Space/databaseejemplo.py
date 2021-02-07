import sqlite3

conexion = sqlite3.connect('basededatos.db')
cursor = conexion.cursor()

def close():
    conexion.commit()
    cursor.close()
########### Tipos de sentencias ###########

# Crear tabla

'''CREATE TABLE nombretabla(nombrecolumna tipocolumna...nombrecolumna2 tipocolumna2...)'''

# Insertar datos predefinidos en tabla

'''INSERT INTO nombretabla (nombrecolumna, nombrecolumna2) VALUES(valorcolumna, valorcolumna2)'''

# Insertar datos desde variable

# x = [valor, valor2]

'''INSERT INTO nombretabla (nombrecolumna, nombrecolumna2) VALUES(?, ?)''' #, x

# Seleccionar datos de tabla de columnas

'''SELECT nombrecolumna, nombreolumna FROM nombretabla'''

# Seleccionar datos con condiciones

'''SELECT nombrecolumna FROM nombretabla WHERE nombrecolumna < x'''

# Seleccionar todos los datos de la tabla

'''SELECT * FROM nombretabla'''

# Borrar datos de la tabla

'''DELETE FROM nombretabla WHERE nombrecolumna = x'''

# Borrar todos los datos de la tabla (CUIDADO)

'''DELETE FROM nombretabla'''

########### Ejecutando sentencias ###########

# Creación de tabla

## 1. Saber la sentencia SQL que realizar. Para crear tabla sabemos que es CREATE TABLE...

# cursor.execute(
#     '''
#     CREATE TABLE IF NOT EXISTS records(
#     puntuacion INTEGER,
#     nombre TEXT)
#     '''
# )

## 2. En este momento nos creará la base de datos con la tabla

# x = [(3200, 'Tirso'), (2400, 'Fernando'), (4000, 'Paulita')]
# cursor.executemany(
#     "INSERT INTO records(puntuacion, nombre) VALUES(?, ?)", x
# )
# conexion.commit()
# cursor.close()

# Seleccionar datos

# cursor.execute(
#     '''SELECT * FROM records ORDER BY puntuacion DESC WHERE puntuacion > 3000'''
# )

# records = cursor.fetchall()

# close()

# print(records)

# Borrar datos

# cursor.execute(
#     '''DELETE FROM records WHERE puntuacion < 4000'''
# )

# close()


# cursor.execute(
#     '''SELECT * FROM records WHERE puntuacion > 3000'''
# )

# records_actuales = cursor.fetchall()

# close()

# print(records_actuales)

# cursor.execute(
#     '''DELETE FROM records'''
# )

# close()
