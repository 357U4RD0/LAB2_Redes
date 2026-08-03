# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# presentacion.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Servicio decodificar_mensaje correspondiente a la capa de Presentación del receptor.
#
#              Traduce la cadena ASCII binaria entregada por la capa de Enlace a los caracteres correspondientes cuando la trama
#              resulta valida. Si la longitud no es multiplo de ocho o si aparecen codigos no imprimibles, informa la condición a
#              la capa de Aplicación en lugar de mostrar un texto que podria inducir a una interpretación erronea del resultado.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


def decodificar_mensaje(mensaje_binario):
    """Convierte una cadena ASCII binaria en texto y devuelve el estado de la conversión."""
    # Sin una longitud multiplo de ocho la cadena no representa caracteres ASCII completos
    if len(mensaje_binario) == 0 or len(mensaje_binario) % 8 != 0:
        return False, "La longitud del mensaje no es múltiplo de 8: no aplica decodificación ASCII"

    texto = ""

    for inicio in range(0, len(mensaje_binario), 8):
        # Cada grupo de ocho bits corresponde al codigo ASCII de un caracter
        codigo = int(mensaje_binario[inicio:inicio + 8], 2)

        # Se aceptan unicamente los codigos imprimibles del rango ASCII estandar
        if codigo < 32 or codigo > 126:
            return False, "El mensaje contiene códigos ASCII no imprimibles"

        texto += chr(codigo)

    return True, texto
