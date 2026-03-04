from datetime import datetime


LOG_FILE = "sistema.log"


def log_event(mensaje):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[INFO] {fecha} - {mensaje}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(linea)


def log_error(mensaje):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[ERROR] {fecha} - {mensaje}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(linea)