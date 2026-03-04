import sqlite3
from db import obtener_conexion
from datetime import datetime
from logger import log_error, log_event


def crear_tabla_ventas():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            codigo_producto TEXT,
            cantidad INTEGER,
            fecha TEXT
        )
    """)

    conn.commit()
    conn.close()


def vender_producto_por_codigo_bd(codigo, usuario):
    conn = obtener_conexion()
    if conn is None:
        return {"ok": False, "mensaje":"Error de conexión"}
    

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT stock FROM productos WHERE codigo = ?",
            (codigo,)
        )
        resultado = cursor.fetchone()

        if not resultado:
            return {"ok": False, "mensaje": "Producto no encontrado"}

        if resultado[0] <= 0:
            return {"ok": False, "mensaje": "No hay stock disponible"}

        # Descontar stock
        cursor.execute(
            "UPDATE productos SET stock = stock - 1 WHERE codigo = ?",
            (codigo,)
        )
        log_event(f"Venta realizada por {usuario} - Código: {codigo}")

        # Registrar venta
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            INSERT INTO ventas (usuario, codigo_producto, cantidad, fecha)
            VALUES (?, ?, ?, ?)
            """,
            (usuario, codigo, 1, fecha)
        )

        conn.commit()
        return {"ok": True, "mensaje": "Producto vendido y venta registrada"}
    
        

    except sqlite3.Error as e:
        conn.rollback()
        log_error(f"Error en venta - Usuario: {usuario} - Código: {codigo} - {e}")
        print("❌ Error durante la venta:", e)
        return {"ok": False, "mensaje": "Error interno en la venta"}

    finally:
        conn.close()
