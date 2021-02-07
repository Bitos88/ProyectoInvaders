import sqlite3

conexion = sqlite3.connect('basededatos.db')
cursor = conexion.cursor()

#Creacion de la tabla
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS records(
    puntuacion INTEGER,
    nombre TEXT)'''
)

#inserción datos en la tabla creada
def datosDB(puntuacion, nombre):
    x = (puntuacion, f"{nombre}")

    cursor.execute("INSERT INTO records(puntuacion, nombre) VALUES(?, ?)", x)

    conexion.commit()
    #cursor.close()

def elegirDatos():
    cursor.execute('''SELECT * FROM records ORDER BY puntuacion DESC''')
    records = []
    for x in range(3):
        records.append(cursor.fetchone())
    conexion.commit()
    #cursor.close()

    return records

'''
for element in r:
    print(element[0])
    print(element[1])
'''