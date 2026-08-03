# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# fletcher.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Algoritmo de detección de errores Fletcher checksum para el lado receptor.
#
#              Separa los ultimos 2k bits de la trama como checksum recibido, recalcula sum1 y sum2 sobre el resto del mensaje en
#              aritmetica modulo 2^k - 1 y compara ambos valores. Al tratarse de un esquema exclusivamente de detección, la trama
#              se descarta cuando los checksums difieren, sin intentar ninguna reconstrucción del contenido original.
#              Se incluye tambien el codificador, utilizado unicamente por el script de simulación que genera las graficas.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Tamaños de bloque admitidos por el laboratorio
TAMANIOS_VALIDOS = (8, 16, 32)


def tamanio_bloque_valido(tamanio_bloque):
    """Verifica que el tamaño de bloque solicitado sea uno de los tres valores permitidos."""
    return tamanio_bloque in TAMANIOS_VALIDOS


def calcular_sumas(mensaje_binario, tamanio_bloque):
    """Calcula las sumas parciales sum1 y sum2 sobre un mensaje cuya longitud es multiplo del bloque."""
    # El modulo del algoritmo es 2^k - 1, lo que evita que un bloque nulo pase inadvertido en sum1
    modulo = (2 ** tamanio_bloque) - 1

    suma1 = 0
    suma2 = 0
    bloques = 0

    for inicio in range(0, len(mensaje_binario), tamanio_bloque):
        # Interpreta cada bloque como un entero sin signo en notación big endian
        valor = int(mensaje_binario[inicio:inicio + tamanio_bloque], 2)

        # sum1 acumula el valor de los bloques en aritmetica modular
        suma1 = (suma1 + valor) % modulo

        # sum2 acumula los valores sucesivos de sum1, haciendo al checksum sensible al orden
        suma2 = (suma2 + suma1) % modulo

        bloques += 1

    return suma1, suma2, bloques


def codificar(mensaje_binario, tamanio_bloque):
    """Aplica relleno de ceros, calcula el checksum y devuelve la trama concatenada."""
    sobrante = len(mensaje_binario) % tamanio_bloque

    # El relleno se agrega a la derecha para no alterar el orden de los bits originales
    relleno = 0 if sobrante == 0 else tamanio_bloque - sobrante

    mensaje_con_relleno = mensaje_binario + ("0" * relleno)

    suma1, suma2, _ = calcular_sumas(mensaje_con_relleno, tamanio_bloque)

    # El checksum se forma con sum2 en la parte alta y sum1 en la parte baja, ocupando 2k bits
    checksum = format(suma2, f"0{tamanio_bloque}b") + format(suma1, f"0{tamanio_bloque}b")

    return mensaje_con_relleno + checksum


def verificar(trama_recibida, tamanio_bloque):
    """Separa el checksum recibido, lo recalcula sobre el mensaje y compara ambos valores."""
    longitud_checksum = 2 * tamanio_bloque

    resultado = {
        "estado": "",
        "mensaje": "",
        "checksum_recibido": "",
        "checksum_calculado": "",
        "suma1": 0,
        "suma2": 0,
        "bloques": 0,
        "tamanio_bloque": tamanio_bloque,
    }

    # La trama debe contener al menos un bloque de datos ademas del checksum
    if len(trama_recibida) < longitud_checksum + tamanio_bloque:
        resultado["estado"] = "TRAMA_INVALIDA"
        return resultado

    cuerpo = trama_recibida[:-longitud_checksum]

    # La longitud del cuerpo debe ser multiplo del bloque porque el emisor aplico relleno
    if len(cuerpo) % tamanio_bloque != 0:
        resultado["estado"] = "TRAMA_INVALIDA"
        return resultado

    checksum_recibido = trama_recibida[-longitud_checksum:]

    suma1, suma2, bloques = calcular_sumas(cuerpo, tamanio_bloque)

    checksum_calculado = format(suma2, f"0{tamanio_bloque}b") + format(suma1, f"0{tamanio_bloque}b")

    resultado["mensaje"] = cuerpo
    resultado["checksum_recibido"] = checksum_recibido
    resultado["checksum_calculado"] = checksum_calculado
    resultado["suma1"] = suma1
    resultado["suma2"] = suma2
    resultado["bloques"] = bloques

    # La igualdad de ambos checksums es la unica evidencia de integridad que ofrece el algoritmo
    resultado["estado"] = "SIN_ERRORES" if checksum_recibido == checksum_calculado else "ERROR_DETECTADO"

    return resultado
