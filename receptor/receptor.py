# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# receptor.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Programa receptor del Laboratorio 2, implementado en Python, que verifica y corrige tramas recibidas.
#
#              Implementa la capa de Aplicación y coordina el ascenso de la trama por las capas de Transmisión, Enlace y
#              Presentación. Admite el traslado manual, en el cual el usuario pega la salida del emisor, y tambien la recepción por
#              sockets con escucha permanente en el puerto elegido. Distingue de forma explicita entre trama correcta, error
#              detectado con descarte de la trama y error corregido con indicación de la posición afectada. Cada menu conserva una
#              opción de retorno que devuelve el control al paso inmediatamente anterior.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

import sys
from pathlib import Path

# Agrega el directorio del receptor al path para permitir la ejecución desde cualquier ubicación
sys.path.insert(0, str(Path(__file__).resolve().parent))

from algoritmos import fletcher
from capas import enlace, transmision
from capas.presentacion import decodificar_mensaje
from utilidades import (
    agrupar_bits,
    es_binaria,
    etiqueta,
    franja_mayor,
    leer_dato,
    limpiar_cadena,
    linea_mayor,
)

# Codigos de retorno utilizados por los menus para indicar continuar, retroceder o repetir
RESULTADO_CONTINUAR = 0
RESULTADO_VOLVER = 1
RESULTADO_REPETIR = 2


def mostrar_encabezado():
    """Muestra el encabezado institucional que identifica al programa al iniciar."""
    franja_mayor("UNIVERSIDAD DEL VALLE DE GUATEMALA")
    print("Facultad de Ingeniería")
    print("Departamento de Computación")
    print("Redes")
    print("Laboratorio #2")
    print("Receptor de Tramas con Detección y Corrección de Errores")
    print("André Emilio Pivaral López - 23574")
    linea_mayor()
    print("Receptor en Python")
    print("Algoritmos: Hamming y Fletcher Checksum")
    linea_mayor()
    print()


def mostrar_menu_principal():
    """Presenta el menu principal y devuelve la opción elegida por el usuario."""
    franja_mayor("MENÚ PRINCIPAL")
    print("1. Modo Manual: verificar una trama ingresada")
    print("2. Modo Socket: escuchar tramas en un puerto")
    print("3. Salir")

    return limpiar_cadena(leer_dato("Selecciona una Opción: "))


def solicitar_tamanio_bloque():
    """Solicita el tamaño de bloque que utilizara el Fletcher checksum."""
    franja_mayor("TAMAÑO DE BLOQUE")
    print("1. 8 Bits")
    print("2. 16 Bits")
    print("3. 32 Bits")
    print("4. Volver")

    opcion = limpiar_cadena(leer_dato("Selecciona una Opción: "))

    # La cuarta opción regresa a la selección de algoritmo
    if opcion == "4":
        return RESULTADO_VOLVER, 0

    equivalencias = {"1": 8, "2": 16, "3": 32}

    if opcion in equivalencias:
        return RESULTADO_CONTINUAR, equivalencias[opcion]

    print("La opción seleccionada no es válida.")
    print()

    return RESULTADO_REPETIR, 0


def solicitar_algoritmo():
    """Solicita el algoritmo de verificación y, cuando corresponde, el tamaño de bloque."""
    franja_mayor("CAPA DE APLICACIÓN")
    print("1. Hamming: corrección de errores")
    print("2. Fletcher Checksum: detección de errores")
    print("3. Volver")

    opcion = limpiar_cadena(leer_dato("Selecciona una Opción: "))

    # La tercera opción devuelve el control al menu principal
    if opcion == "3":
        return RESULTADO_VOLVER, None, 0

    if opcion == "1":
        # Hamming no utiliza tamaño de bloque, por lo que el parametro se anula
        return RESULTADO_CONTINUAR, enlace.HAMMING, 0

    if opcion == "2":
        while True:
            resultado, tamanio = solicitar_tamanio_bloque()

            # El retorno desde el tamaño de bloque reabre la selección de algoritmo
            if resultado == RESULTADO_VOLVER:
                return RESULTADO_REPETIR, None, 0

            if resultado == RESULTADO_CONTINUAR:
                return RESULTADO_CONTINUAR, enlace.FLETCHER, tamanio

    print("La opción seleccionada no es válida.")
    print()

    return RESULTADO_REPETIR, None, 0


def mostrar_verificacion(trama, algoritmo, tamanio_bloque, resultado):
    """Muestra el detalle del calculo realizado por la capa de Enlace."""
    detalle = resultado["detalle"]

    franja_mayor("CAPA DE ENLACE")
    etiqueta("Algoritmo", enlace.nombre_algoritmo(algoritmo))
    etiqueta("Longitud de la Trama", str(len(trama)))
    etiqueta("Trama Recibida", trama)

    if algoritmo == enlace.HAMMING:
        etiqueta("Bits de Datos", str(detalle["bits_datos"]))
        etiqueta("Bits de Paridad", str(detalle["bits_redundancia"]))
        etiqueta("Síndrome Calculado", str(detalle["sindrome"]))
    else:
        etiqueta("Tamaño de Bloque", f"{tamanio_bloque} Bits")
        etiqueta("Bloques Procesados", str(detalle["bloques"]))
        etiqueta("Checksum Recibido", detalle["checksum_recibido"])
        etiqueta("Checksum Calculado", detalle["checksum_calculado"])

    print()


def mostrar_diagnostico(resultado):
    """Muestra el veredicto de la verificación y la información asociada."""
    detalle = resultado["detalle"]
    estado = resultado["estado"]

    if estado == "TRAMA_INVALIDA":
        franja_mayor("TRAMA INVÁLIDA")
        etiqueta("Motivo", "La longitud no corresponde al algoritmo indicado")
        etiqueta("Acción", "Trama Descartada")
    elif estado == "SIN_ERRORES":
        franja_mayor("¡TRAMA RECIBIDA SIN ERRORES!")
        etiqueta("Diagnóstico", "Integridad Verificada")
        etiqueta("Mensaje Recuperado", agrupar_bits(resultado["mensaje"], 8))
    elif estado == "ERROR_CORREGIDO":
        franja_mayor("ERROR DETECTADO Y CORREGIDO")
        etiqueta("Diagnóstico", "Error Simple Corregido")
        etiqueta("Posición Corregida", f"Bit número {detalle['posicion_corregida']}")
        etiqueta("Trama Corregida", detalle["trama_corregida"])
        etiqueta("Mensaje Recuperado", agrupar_bits(resultado["mensaje"], 8))
        print()
        print("El código de Hamming básico corrige un único bit invertido.")
        print("Ante dos o más errores la corrección aplicada puede ser incorrecta.")
    elif estado == "ERROR_NO_CORREGIBLE":
        franja_mayor("ERROR DETECTADO NO CORREGIBLE")
        etiqueta("Diagnóstico", "Síndrome Fuera de Rango")
        etiqueta("Acción", "Trama Descartada")
        print()
        print("El síndrome apunta a una posición inexistente en la trama.")
        print("Esto evidencia un patrón de error superior a la capacidad del código.")
    else:
        franja_mayor("ERROR DETECTADO")
        etiqueta("Diagnóstico", "Los Checksums No Coinciden")
        etiqueta("Acción", "Trama Descartada")
        print()
        print("Fletcher Checksum es un algoritmo de detección, no de corrección.")
        print("La trama se descarta sin intentar reconstruir el mensaje original.")

    print()


def procesar_trama(trama, algoritmo, tamanio_bloque):
    """Ejecuta la verificación de integridad y muestra el diagnostico completo de la trama."""
    resultado = enlace.verificar_integridad(trama, algoritmo, tamanio_bloque)

    mostrar_verificacion(trama, algoritmo, tamanio_bloque, resultado)
    mostrar_diagnostico(resultado)

    # La capa de Presentación solo interviene cuando existe un mensaje recuperado
    if resultado["mensaje"]:
        franja_mayor("CAPA DE PRESENTACIÓN")

        exito, texto = decodificar_mensaje(resultado["mensaje"])

        if exito:
            etiqueta("Decodificación ASCII", "Aplicada")
            etiqueta("Texto Recuperado", texto)
        else:
            etiqueta("Decodificación ASCII", "No Aplicada")
            etiqueta("Motivo", texto)

        print()

    franja_mayor("CAPA DE APLICACIÓN")

    if resultado["estado"] == "SIN_ERRORES":
        print("Mensaje entregado a la aplicación: la trama llegó íntegra.")
    elif resultado["estado"] == "ERROR_CORREGIDO":
        print("Mensaje entregado a la aplicación luego de aplicar la corrección.")
    else:
        print("No se entrega mensaje: se notifica el error a la aplicación.")

    print()


def modo_manual():
    """Solicita la trama pegada por el usuario y ejecuta su verificación."""
    algoritmo = None
    tamanio_bloque = 0

    while True:
        resultado, algoritmo, tamanio_bloque = solicitar_algoritmo()

        # El retorno desde la capa de Aplicación cancela la verificación
        if resultado == RESULTADO_VOLVER:
            return

        if resultado == RESULTADO_CONTINUAR:
            break

    franja_mayor("CAPA DE TRANSMISIÓN")
    print("Pega la trama binaria generada por el emisor.")
    print("Puedes alterar manualmente uno o más bits antes de pegarla.")

    trama = limpiar_cadena(leer_dato("Ingresa la Trama Recibida: "))

    if not es_binaria(trama):
        print("La trama debe contener únicamente los símbolos 0 y 1.")
        print()
        return

    procesar_trama(trama, algoritmo, tamanio_bloque)


def modo_socket():
    """Levanta el servidor de sockets y procesa de forma continua las tramas recibidas."""
    franja_mayor("CAPA DE TRANSMISIÓN")
    print("El receptor quedará a la espera de las tramas enviadas por el emisor.")
    print("Presiona Ctrl+C para detener la escucha y volver al menú principal.")

    entrada = limpiar_cadena(leer_dato(f"Ingresa el Puerto de Escucha [{transmision.PUERTO_POR_DEFECTO}]: "))

    # Se conserva el puerto por defecto cuando el usuario no escribe un valor
    puerto = int(entrada) if entrada.isdigit() else transmision.PUERTO_POR_DEFECTO

    try:
        servidor = transmision.crear_servidor("0.0.0.0", puerto)
    except OSError as error:
        franja_mayor("ERROR DE ESCUCHA")
        etiqueta("Motivo", str(error))
        print()
        return

    franja_mayor("¡RECEPTOR EN ESCUCHA!")
    etiqueta("Puerto", str(puerto))
    print()

    try:
        while True:
            carga, direccion = transmision.recibir_informacion(servidor)

            campos = transmision.separar_carga(carga)

            if campos is None:
                franja_mayor("CARGA NO VÁLIDA")
                etiqueta("Motivo", "El formato recibido no es el acordado")
                print()
                continue

            algoritmo, parametro, trama = campos

            franja_mayor("TRAMA ENTRANTE")
            etiqueta("Origen", f"{direccion[0]}:{direccion[1]}")
            etiqueta("Algoritmo Declarado", algoritmo)
            print()

            if not es_binaria(trama):
                franja_mayor("CARGA NO VÁLIDA")
                etiqueta("Motivo", "La trama recibida no es binaria")
                print()
                continue

            procesar_trama(trama, algoritmo, parametro)
    except KeyboardInterrupt:
        print()
        franja_mayor("ESCUCHA FINALIZADA POR EL USUARIO")
        print()
    finally:
        # Libera el socket para que el puerto quede disponible en la siguiente ejecución
        servidor.close()


def main():
    """Controla el ciclo principal del receptor."""
    mostrar_encabezado()

    while True:
        opcion = mostrar_menu_principal()

        if opcion == "1":
            modo_manual()
        elif opcion == "2":
            modo_socket()
        elif opcion == "3":
            franja_mayor("FIN DEL PROGRAMA RECEPTOR")
            print()
            break
        else:
            print("La opción seleccionada no es válida.")
            print()


# Punto de entrada estandar del script
if __name__ == "__main__":
    main()
