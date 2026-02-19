from productos import cargar_productos_desde_bd, mostrar_valor_total
from ventas import vender_producto_por_codigo_bd


def mostrar_menu(rol):
    print("\nSISTEMA DE INVENTARIO 2026")
    print("1. Ver inventario")
    print("2. Ver valor total")

    if rol in ("admin", "vendedor"):
        print("3. Vender producto")

    print("4. Salir")


def vender_producto_interactivo(usuario_actual):
    codigo = input("Ingresa el código del producto a vender: ")
    resultado = vender_producto_por_codigo_bd(
        codigo,
        usuario_actual["usuario"]
    )
    print(resultado["mensaje"])


def procesar_opcion(opcion, usuario_actual):
    if opcion == "1":
        print("\nInventario:")
        inventario = cargar_productos_desde_bd()
        for producto in inventario:
            print(f'{producto["nombre"]} - Stock: {producto["stock"]}')

    elif opcion == "2":
        inventario = cargar_productos_desde_bd()
        mostrar_valor_total(inventario)

    elif opcion == "3":
        if usuario_actual["rol"] not in ("admin", "vendedor"):
            print("No tienes permiso para vender productos")
            return True

        vender_producto_interactivo(usuario_actual)

    elif opcion == "4":
        print("Saliendo del sistema...")
        return False

    else:
        print("Opción no válida")

    return True
