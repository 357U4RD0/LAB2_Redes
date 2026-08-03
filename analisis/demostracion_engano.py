# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# demostracion_engano.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Script que construye y documenta casos en los que el receptor acepta como intacta una trama alterada.
#
#              Reproduce tres debilidades estructurales concretas; el patron de tres bits cuyo sindrome de Hamming se anula, la
#              corrección incorrecta de Hamming ante dos bits invertidos y la equivalencia de un bloque nulo con un bloque de unos
#              en el Fletcher checksum debida a la aritmetica modulo 2^k - 1. Cada caso se ejecuta contra las implementaciones
#              reales del receptor y se imprime como evidencia verificable para la sección de discusión del reporte.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

import sys
from pathlib import Path

# Rutas base del proyecto calculadas a partir de la ubicación de este archivo
RAIZ = Path(__file__).resolve().parent.parent
DIR_RECEPTOR = RAIZ / "receptor"

# Se agrega el receptor al path para reutilizar los algoritmos ya implementados
sys.path.insert(0, str(DIR_RECEPTOR))

from algoritmos import fletcher, hamming


def linea_mayor():
    """Imprime una linea divisoria de 120 caracteres de guion."""
    print("-" * 120)


def franja_mayor(titulo):
    """Imprime un titulo centrado entre dos lineas divisorias de 120 caracteres."""
    linea_mayor()
    print(titulo.center(120).rstrip())
    linea_mayor()


def etiqueta(nombre, valor):
    """Imprime un par etiqueta valor con la etiqueta alineada a un ancho fijo."""
    print(f"{(nombre + ':').ljust(30)}{valor}")


def mostrar_encabezado():
    """Muestra el encabezado institucional que identifica al script al iniciar."""
    franja_mayor("UNIVERSIDAD DEL VALLE DE GUATEMALA")
    print("Facultad de Ingeniería")
    print("Departamento de Computación")
    print("Redes")
    print("Laboratorio #2")
    print("Demostración de Engaño a los Algoritmos")
    print("André Emilio Pivaral López - 23574")
    linea_mayor()
    print()


def traducir_estado(estado):
    """Traduce el estado interno del algoritmo a una descripción legible."""
    equivalencias = {
        "SIN_ERRORES": "Sin Errores",
        "ERROR_CORREGIDO": "Error Detectado y Corregido",
        "ERROR_NO_CORREGIBLE": "Error Detectado No Corregible",
        "ERROR_DETECTADO": "Error Detectado: Trama Descartada",
        "TRAMA_INVALIDA": "Trama Inválida",
    }

    return equivalencias.get(estado, estado)


def invertir(trama, posiciones):
    """Invierte los bits de la trama en las posiciones indicadas, numeradas desde uno."""
    bits = list(trama)

    for posicion in posiciones:
        bits[posicion - 1] = "1" if bits[posicion - 1] == "0" else "0"

    return "".join(bits)


def caso_hamming_sindrome_nulo():
    """Demuestra un patron de tres bits que anula el sindrome del Código de Hamming."""
    franja_mayor("CASO 1: HAMMING CON SÍNDROME NULO")

    mensaje = "10110011"
    trama = hamming.codificar(mensaje)

    # Las posiciones 3, 5 y 6 cumplen 3 XOR 5 XOR 6 igual a cero, por lo que el sindrome se cancela
    posiciones = [3, 5, 6]
    alterada = invertir(trama, posiciones)

    resultado = hamming.verificar(alterada)

    etiqueta("Mensaje Original", mensaje)
    etiqueta("Trama Emitida", trama)
    etiqueta("Bits Invertidos", ", ".join(str(posicion) for posicion in posiciones))
    etiqueta("Trama Alterada", alterada)
    etiqueta("Síndrome Calculado", str(resultado["sindrome"]))
    etiqueta("Diagnóstico del Receptor", traducir_estado(resultado["estado"]))
    etiqueta("Mensaje Entregado", resultado["mensaje"])
    print()

    # El engaño se confirma cuando el receptor no reporta error pero el mensaje entregado difiere del original
    enganio = resultado["estado"] == "SIN_ERRORES" and resultado["mensaje"] != mensaje

    franja_mayor("¡ENGAÑO LOGRADO!" if enganio else "ENGAÑO NO LOGRADO")
    print("El síndrome es la suma XOR de las posiciones alteradas. Cuando ese")
    print("valor se anula, todas las paridades vuelven a cumplirse y el receptor")
    print("concluye que la trama está intacta pese a contener tres errores.")
    print()


def caso_hamming_correccion_incorrecta():
    """Demuestra la corrección equivocada del Código de Hamming ante dos bits invertidos."""
    franja_mayor("CASO 2: HAMMING CON DOS ERRORES")

    mensaje = "10110011"
    trama = hamming.codificar(mensaje)

    # Dos inversiones producen un sindrome igual al XOR de ambas posiciones, que apunta a un tercer bit
    posiciones = [5, 9]
    alterada = invertir(trama, posiciones)

    resultado = hamming.verificar(alterada)

    etiqueta("Mensaje Original", mensaje)
    etiqueta("Trama Emitida", trama)
    etiqueta("Bits Invertidos", ", ".join(str(posicion) for posicion in posiciones))
    etiqueta("Trama Alterada", alterada)
    etiqueta("Síndrome Calculado", str(resultado["sindrome"]))
    etiqueta("Diagnóstico del Receptor", traducir_estado(resultado["estado"]))
    etiqueta("Posición Corregida", f"Bit número {resultado['posicion_corregida']}")
    etiqueta("Mensaje Entregado", resultado["mensaje"])
    print()

    # El fallo silencioso ocurre cuando el receptor cree haber corregido pero el mensaje sigue siendo incorrecto
    enganio = resultado["mensaje"] != mensaje

    franja_mayor("¡ENGAÑO LOGRADO!" if enganio else "ENGAÑO NO LOGRADO")
    print("La distancia mínima del código de Hamming básico es tres, lo que")
    print("permite corregir un solo bit. Con dos errores el síndrome apunta a una")
    print("tercera posición y el receptor introduce un error adicional al corregir.")
    print()


def caso_fletcher_bloque_equivalente():
    """Demuestra la equivalencia entre un bloque nulo y un bloque de unos en Fletcher checksum."""
    franja_mayor("CASO 3: FLETCHER CON BLOQUE EQUIVALENTE")

    tamanio_bloque = 8

    # El primer bloque es completamente nulo, condición necesaria para aplicar el patron
    mensaje = "00000000" + "01001101"

    trama = fletcher.codificar(mensaje, tamanio_bloque)

    # Invertir el bloque nulo completo lo transforma en el valor 2^k - 1, congruente con cero en el modulo usado
    posiciones = list(range(1, tamanio_bloque + 1))
    alterada = invertir(trama, posiciones)

    resultado = fletcher.verificar(alterada, tamanio_bloque)

    etiqueta("Mensaje Original", mensaje)
    etiqueta("Trama Emitida", trama)
    etiqueta("Bits Invertidos", f"Los {tamanio_bloque} bits del primer bloque")
    etiqueta("Trama Alterada", alterada)
    etiqueta("Checksum Recibido", resultado["checksum_recibido"])
    etiqueta("Checksum Calculado", resultado["checksum_calculado"])
    etiqueta("Diagnóstico del Receptor", traducir_estado(resultado["estado"]))
    print()

    cuerpo_original = trama[: len(trama) - 2 * tamanio_bloque]

    # El engaño se confirma cuando el receptor valida la trama aunque el cuerpo difiera del emitido
    enganio = resultado["estado"] == "SIN_ERRORES" and resultado["mensaje"] != cuerpo_original

    franja_mayor("¡ENGAÑO LOGRADO!" if enganio else "ENGAÑO NO LOGRADO")
    print("El algoritmo trabaja en módulo 2^k menos uno, por lo que el valor cero")
    print("y el valor 2^k menos uno son congruentes. Sustituir un bloque nulo por")
    print("un bloque de unos deja sum1 y sum2 sin cambio y el checksum coincide.")
    print()


def main():
    """Ejecuta los tres casos de engaño y muestra la conclusión del experimento."""
    mostrar_encabezado()

    caso_hamming_sindrome_nulo()
    caso_hamming_correccion_incorrecta()
    caso_fletcher_bloque_equivalente()

    franja_mayor("CONCLUSIÓN DEL EXPERIMENTO")
    print("Los tres casos fueron construidos de forma deliberada y se verifican de")
    print("manera automática en cada ejecución. No implican que los algoritmos fallen")
    print("con frecuencia ante ruido aleatorio, sino que existen patrones específicos")
    print("de alteración que ambos esquemas no pueden distinguir de una trama intacta.")
    print()


# Punto de entrada estandar del script
if __name__ == "__main__":
    main()
