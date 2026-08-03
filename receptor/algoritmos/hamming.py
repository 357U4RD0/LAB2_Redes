# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# hamming.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Algoritmo de corrección de errores Código de Hamming para el lado receptor.
#
#              Recalcula la paridad par de cada bit de control y construye el sindrome como la suma de las posiciones de los bits
#              de paridad que fallan. Un sindrome igual a cero indica ausencia de errores detectables, un sindrome dentro del rango
#              de la trama identifica y corrige el bit invertido, y un sindrome fuera de rango revela un error no corregible.
#              Se incluye tambien el codificador, utilizado unicamente por el script de simulación que genera las graficas.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


def calcular_bits_redundancia(bits_mensaje):
    """Calcula la cantidad minima de bits de redundancia r tal que m + r + 1 <= 2^r."""
    r = 1

    # Incrementa r hasta que la desigualdad de capacidad del codigo se satisface
    while (bits_mensaje + r + 1) > (2 ** r):
        r += 1

    return r


def es_potencia_de_dos(numero):
    """Indica si un numero positivo es potencia de dos."""
    # Un numero potencia de dos posee un unico bit encendido en su representación binaria
    return numero > 0 and (numero & (numero - 1)) == 0


def codificar(mensaje_binario):
    """Construye la trama de Hamming con paridad par a partir de un mensaje binario."""
    m = len(mensaje_binario)
    r = calcular_bits_redundancia(m)
    n = m + r

    # Se utiliza indice uno para respetar la numeración clasica de posiciones de Hamming
    trama = [0] * (n + 1)

    indice_mensaje = 0

    for posicion in range(1, n + 1):
        # Las posiciones que no son potencia de dos reciben los bits de datos en orden
        if not es_potencia_de_dos(posicion):
            trama[posicion] = int(mensaje_binario[indice_mensaje])
            indice_mensaje += 1

    for posicion_paridad in [2 ** i for i in range(r)]:
        paridad = 0

        for posicion in range(1, n + 1):
            # Un bit de paridad cubre las posiciones cuyo indice comparte el bit encendido con dicha paridad
            if posicion != posicion_paridad and (posicion & posicion_paridad) != 0:
                paridad ^= trama[posicion]

        trama[posicion_paridad] = paridad

    return "".join(str(bit) for bit in trama[1:])


def verificar(trama_recibida):
    """Verifica la trama, corrige un error simple cuando es posible y extrae el mensaje original."""
    n = len(trama_recibida)

    # Cantidad de bits de paridad presentes en una trama de longitud n
    r = 0
    while (2 ** r) <= n:
        r += 1

    bits = [0] + [int(bit) for bit in trama_recibida]

    sindrome = 0

    for posicion_paridad in [2 ** i for i in range(r)]:
        paridad = 0

        for posicion in range(1, n + 1):
            # Suma modulo dos de todas las posiciones cubiertas por el bit de paridad, incluido el propio bit
            if (posicion & posicion_paridad) != 0:
                paridad ^= bits[posicion]

        # Cuando la paridad par no se cumple, la posición del bit de control se acumula en el sindrome
        if paridad != 0:
            sindrome += posicion_paridad

    resultado = {
        "sindrome": sindrome,
        "longitud": n,
        "bits_redundancia": r,
        "bits_datos": n - r,
        "posicion_corregida": None,
        "trama_corregida": trama_recibida,
        "mensaje": "",
        "estado": "",
    }

    if sindrome == 0:
        # Sindrome nulo significa que todas las paridades se cumplen y no se detecta error
        resultado["estado"] = "SIN_ERRORES"
    elif sindrome <= n:
        lista = list(trama_recibida)

        # El sindrome corresponde directamente a la posición del bit invertido
        lista[sindrome - 1] = "1" if lista[sindrome - 1] == "0" else "0"

        resultado["trama_corregida"] = "".join(lista)
        resultado["posicion_corregida"] = sindrome
        resultado["estado"] = "ERROR_CORREGIDO"
    else:
        # Un sindrome que apunta fuera de la trama evidencia un patron de error no corregible
        resultado["estado"] = "ERROR_NO_CORREGIBLE"

    if resultado["estado"] != "ERROR_NO_CORREGIBLE":
        # Extrae los bits de datos descartando las posiciones potencia de dos
        resultado["mensaje"] = "".join(
            resultado["trama_corregida"][posicion - 1]
            for posicion in range(1, n + 1)
            if not es_potencia_de_dos(posicion)
        )

    return resultado
