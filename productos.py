from db import obtener_conexion
from datetime import datetime


def crear_tabla_productos():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT,
            talla TEXT,
            precio INTEGER,
            stock INTEGER
        )
    """)

    conn.commit()
    conn.close()


def insertar_producto(codigo, nombre, talla, precio, stock):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO productos (codigo, nombre, talla, precio, stock)
        VALUES (?, ?, ?, ?, ?)
    """, (codigo, nombre, talla, precio, stock))

    conn.commit()
    conn.close()


def cargar_productos_desde_bd():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT codigo, nombre, talla, precio, stock FROM productos")
    filas = cursor.fetchall()
    conn.close()

    productos = []
    for fila in filas:
        productos.append({
            "codigo": fila[0],
            "nombre": fila[1],
            "talla": fila[2],
            "precio": fila[3],
            "stock": fila[4]
        })

    return productos


def agregar_stock(codigo, cantidad):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT stock FROM productos WHERE codigo = ?",
        (codigo,)
    )
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return {"ok": False, "mensaje": "Producto no encontrado"}

    cursor.execute(
        "UPDATE productos SET stock = stock + ? WHERE codigo = ?",
        (cantidad, codigo)
    )

    conn.commit()
    conn.close()

    return {"ok": True, "mensaje": f"Stock aumentado en {cantidad} unidades"}


def agregar_stock_interactivo():
    codigo = input("Código del producto: ")
    try:
        cantidad = int(input("Cantidad a agregar: "))
    except ValueError:
        print("Cantidad inválida")
        return

    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero")
        return

    resultado = agregar_stock(codigo, cantidad)
    print(resultado["mensaje"])



def calcular_valor_total(inventario):
    total = 0
    for producto in inventario:
        total += producto["precio"] * producto["stock"]
    return total


def mostrar_valor_total(inventario):
    total = calcular_valor_total(inventario)
    print(f"Valor total del inventario: ${total}")
