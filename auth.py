from logger import log_event, log_error
from db import obtener_conexion
from seguridad import hash_password
import sqlite3


def crear_tabla_usuarios():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            password TEXT,
            rol TEXT
        )
    """)

    conn.commit()
    conn.close()


def crear_usuario(usuario, password, rol):
    password_hash = hash_password(password)
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
            (usuario, password_hash, rol)
        )
        conn.commit()
        return {"ok": True, "mensaje": "Usuario creado correctamente"}
    except Exception:
        return {"ok": False, "mensaje": "El usuario ya existe"}
    finally:
        conn.close()


def login(usuario, password_hash):
    conn = obtener_conexion()
    if conn is None:
        return {"ok": False, "mensaje":"Error de conexión"}
    
    try:

        cursor = conn.cursor()
        cursor.execute(
            "SELECT rol FROM usuarios WHERE usuario = ? AND password = ?",
            (usuario, password_hash)
        )

        fila = cursor.fetchone()
        
        conn.close()

        if fila is None:
            log_error(f"Intento fallido de login: {usuario}")
            return {"ok": False, "mensaje": "Credenciales inválidas"}
            

        log_event(f"Login exitoso: {usuario}")

        return {
            "ok": True,
            "usuario": usuario,
            "rol": fila[0]
        }
    
    except sqlite3.Error as e:
        log_error(f"Error en login - Usuario: {usuario} - {e}")
        return {"ok": False, "mensaje": "Error interno en login"}

    finally:
        conn.close()
        


def ver_usuarios():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT usuario, rol FROM usuarios")
    filas = cursor.fetchall()
    conn.close()

    return filas


def borrar_usuarios():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()
