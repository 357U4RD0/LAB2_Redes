# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# transmision.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Servicio recibir_informacion correspondiente a la capa de Transmisión del receptor.
#
#              Levanta un servidor TCP que permanece escuchando de forma indefinida en el puerto elegido y atiende una conexión a
#              la vez. Acumula los bytes recibidos hasta encontrar el salto de linea que delimita el mensaje y separa la carga util
#              en los campos algoritmo, parametro y trama acordados con el emisor.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

import socket

# Puerto por defecto utilizado durante las pruebas del laboratorio
PUERTO_POR_DEFECTO = 50007


def crear_servidor(host, puerto):
    """Crea y deja escuchando un socket TCP en el host y puerto indicados."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SO_REUSEADDR permite reiniciar el receptor sin esperar la liberación del puerto
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((host, puerto))

    # La cola admite una conexión pendiente porque el emisor transmite una trama por vez
    servidor.listen(1)

    return servidor


def recibir_informacion(servidor):
    """Espera una conexión entrante y devuelve la carga util recibida junto con la dirección del emisor."""
    conexion, direccion = servidor.accept()

    datos = b""

    with conexion:
        while True:
            fragmento = conexion.recv(4096)

            # Un fragmento vacio indica que el emisor cerro la conexión
            if not fragmento:
                break

            datos += fragmento

            # El salto de linea delimita el final de la trama enviada
            if b"\n" in datos:
                break

    return datos.decode("utf-8", errors="ignore").strip(), direccion


def separar_carga(carga):
    """Separa la carga util en los campos algoritmo, parametro y trama."""
    partes = carga.split(";")

    # El formato acordado con el emisor contiene exactamente tres campos
    if len(partes) != 3:
        return None

    algoritmo = partes[0].strip().upper()

    try:
        parametro = int(partes[1].strip())
    except ValueError:
        parametro = 0

    trama = partes[2].strip()

    return algoritmo, parametro, trama
