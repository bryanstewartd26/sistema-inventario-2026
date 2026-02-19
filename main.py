from db  import obtener_conexion
from seguridad import hash_password
from auth import (login)
from menu import (mostrar_menu, procesar_opcion)



def ver_tabla(nombre_tabla):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {nombre_tabla}")
    filas = cursor.fetchall()

    if not filas:
        print("No hay informacion en la Tabla")

    conn.close()
    for fila in filas:
        print(fila)


def ver_tablas():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tablas = cursor.fetchall()
    conn.close()

    if not tablas:
        print("No hay tablas en la base de datos")
        return

    print("\nTABLAS EN LA BASE DE DATOS")
    print("-" * 30)

    for tabla in tablas:
        print(f"- {tabla[0]}")



def main():
    print("=== LOGIN ===")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")
    password_hash = hash_password(password)

    resultado = login(usuario, password_hash)

    if not resultado["ok"]:
        print(resultado["mensaje"])
        return  # corta el programa

    usuario_actual = {
        "usuario": resultado["usuario"],
        "rol": resultado["rol"]
    }

    while True:
        mostrar_menu(usuario_actual["rol"])
        opcion = input("Elige una opción: ")

        continuar = procesar_opcion(opcion, usuario_actual)
        if not continuar:
            break

if __name__ == "__main__":
    main()
    #agregar_stock_interactivo()
    #ver_tabla("ventas")
    #ver_tabla("usuarios")
    #crear_usuario("stewart", "123", "vendedor)

