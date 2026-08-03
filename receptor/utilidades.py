# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# utilidades.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Funciones de presentación en consola y de validación de cadenas binarias del receptor.
#
#              Replica en Python el estilo visual del emisor mediante franjas divisorias de 120 caracteres con el titulo centrado
#              y etiquetas alineadas en columna. Encapsula ademas la lectura
#              de datos del usuario agregando de forma automatica el espacio en blanco posterior a cada respuesta, y provee la
#              verificación de que una trama contenga unicamente los simbolos del alfabeto binario.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Ancho de todas las lineas divisorias del programa
ANCHO_MAYOR = 120

# Ancho reservado para los rotulos de modo que todos los valores queden alineados en columna
ANCHO_ETIQUETA = 30


def linea_mayor():
    """Imprime una linea divisoria de 120 caracteres de guion."""
    print("-" * ANCHO_MAYOR)


def franja_mayor(titulo):
    """Imprime un titulo centrado entre dos lineas divisorias de 120 caracteres."""
    linea_mayor()

    # center opera sobre caracteres, por lo que las tildes no descuadran el centrado
    print(titulo.center(ANCHO_MAYOR).rstrip())
    linea_mayor()


def etiqueta(nombre, valor):
    """Imprime un par etiqueta valor con la etiqueta alineada a un ancho fijo."""
    # ljust completa con espacios hasta alcanzar el ancho reservado para el rotulo
    print(f"{(nombre + ':').ljust(ANCHO_ETIQUETA)}{valor}")


def leer_dato(rotulo):
    """Muestra un rotulo, lee la respuesta y deja un espacio en blanco despues de ella."""
    entrada = input(rotulo)

    # El espacio en blanco posterior separa visualmente la respuesta del siguiente bloque
    print()

    return entrada


def limpiar_cadena(cadena):
    """Elimina espacios, tabulaciones y saltos de linea de una cadena."""
    # El usuario suele copiar la trama con espacios de agrupamiento que deben descartarse
    return "".join(caracter for caracter in cadena if caracter not in " \t\n\r")


def es_binaria(cadena):
    """Indica si la cadena contiene al menos un caracter y solamente los simbolos 0 y 1."""
    # set permite verificar en una sola operación que no existan simbolos ajenos al alfabeto binario
    return len(cadena) > 0 and set(cadena).issubset({"0", "1"})


def agrupar_bits(bits, tamanio_grupo):
    """Divide una cadena binaria en grupos separados por espacio para facilitar su lectura."""
    # Un tamaño no positivo indica que no se desea agrupar la cadena
    if tamanio_grupo <= 0:
        return bits

    return " ".join(bits[i:i + tamanio_grupo] for i in range(0, len(bits), tamanio_grupo))
