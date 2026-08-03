# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# enlace.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Servicios verificar_integridad y corregir_mensaje correspondientes a la capa de Enlace del receptor.
#
#              Selecciona el algoritmo indicado por la capa de Aplicación, delega en el la verificación de la trama y traduce su
#              salida a un diagnostico uniforme de tres estados; trama correcta, error detectado sin posibilidad de corrección y
#              error corregido con indicación de la posición afectada. Es el punto de integración de los algoritmos implementados.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

from algoritmos import fletcher, hamming

# Identificadores de los algoritmos disponibles en la capa de Enlace
HAMMING = "HAMMING"
FLETCHER = "FLETCHER"


def nombre_algoritmo(algoritmo):
    """Devuelve el nombre legible del algoritmo seleccionado."""
    if algoritmo == HAMMING:
        return "Hamming: corrección de errores"

    return "Fletcher Checksum: detección de errores"


def verificar_integridad(trama, algoritmo, tamanio_bloque=0):
    """Verifica la integridad de la trama y, cuando el algoritmo lo permite, corrige el error encontrado."""
    if algoritmo == HAMMING:
        detalle = hamming.verificar(trama)

        # El resultado del algoritmo se traduce a la estructura comun que consume la capa de Aplicación
        return {
            "algoritmo": algoritmo,
            "estado": detalle["estado"],
            "mensaje": detalle["mensaje"],
            "detalle": detalle,
        }

    detalle = fletcher.verificar(trama, tamanio_bloque)

    return {
        "algoritmo": algoritmo,
        "estado": detalle["estado"],
        "mensaje": detalle["mensaje"] if detalle["estado"] == "SIN_ERRORES" else "",
        "detalle": detalle,
    }
