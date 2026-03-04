import sqlite3

DB_NAME = "inventario.db"

def obtener_conexion():
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print("❌ Error al conectar con la base de datos")
        print(e)
        return None
