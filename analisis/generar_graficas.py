# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# generar_graficas.py
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Script de simulación estadistica y generación de graficas de respaldo para el reporte del Laboratorio 2.
#
#              Reutiliza las implementaciones del receptor para ejecutar experimentos de Monte Carlo variando la longitud de los
#              mensajes, la probabilidad de error del canal y el algoritmo empleado. Clasifica cada ejecución en entrega correcta,
#              error detectado y aceptación erronea, calcula el overhead de cada esquema y exporta las figuras al directorio
#              figures, ademas de imprimir en consola un resumen tabular de los resultados obtenidos.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

import random
import sys
from pathlib import Path

import matplotlib

# El backend Agg permite generar imagenes sin necesidad de un entorno grafico
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Rutas base del proyecto calculadas a partir de la ubicación de este archivo
RAIZ = Path(__file__).resolve().parent.parent
DIR_RECEPTOR = RAIZ / "receptor"
DIR_FIGURAS = RAIZ / "figures"

# Se agrega el receptor al path para reutilizar los algoritmos ya implementados
sys.path.insert(0, str(DIR_RECEPTOR))

from algoritmos import fletcher, hamming

# Longitudes de mensaje utilizadas en los experimentos, en bits
LONGITUDES = [8, 32, 64, 128, 256]

# Probabilidades de error por bit evaluadas en el canal simulado
PROBABILIDADES = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10]

# Cantidad de repeticiones por combinación de parametros
REPETICIONES = 400

# Longitud fija utilizada en los experimentos que varian la probabilidad de error
LONGITUD_REFERENCIA = 64

# Semilla fija para que los resultados del reporte sean reproducibles
SEMILLA = 20260802


def linea_mayor():
    """Imprime una linea divisoria de 120 caracteres de guion."""
    print("-" * 120)


def franja_mayor(titulo):
    """Imprime un titulo centrado entre dos lineas divisorias de 120 caracteres."""
    linea_mayor()
    print(titulo.center(120).rstrip())
    linea_mayor()


def mostrar_encabezado():
    """Muestra el encabezado institucional que identifica al script al iniciar."""
    franja_mayor("UNIVERSIDAD DEL VALLE DE GUATEMALA")
    print("Facultad de Ingeniería")
    print("Departamento de Computación")
    print("Redes")
    print("Laboratorio #2")
    print("Simulación y Generación de Gráficas")
    print("André Emilio Pivaral López - 23574")
    linea_mayor()
    print()


def mensaje_aleatorio(longitud, generador):
    """Genera una cadena binaria aleatoria de la longitud indicada."""
    return "".join(generador.choice("01") for _ in range(longitud))


def aplicar_ruido(trama, probabilidad, generador):
    """Invierte cada bit de la trama de forma independiente segun la probabilidad indicada."""
    bits = list(trama)

    for i in range(len(bits)):
        # Cada bit se evalua por separado, incluidos los bits de redundancia
        if generador.random() < probabilidad:
            bits[i] = "1" if bits[i] == "0" else "0"

    return "".join(bits)


def alterar_bits(trama, cantidad, generador):
    """Invierte una cantidad exacta de bits en posiciones distintas escogidas al azar."""
    bits = list(trama)

    # sample garantiza posiciones distintas, evitando que dos inversiones se anulen entre si
    for posicion in generador.sample(range(len(bits)), cantidad):
        bits[posicion] = "1" if bits[posicion] == "0" else "0"

    return "".join(bits)


def evaluar_hamming(mensaje, trama_recibida):
    """Clasifica el resultado de una recepción bajo el Código de Hamming."""
    resultado = hamming.verificar(trama_recibida)

    if resultado["estado"] == "ERROR_NO_CORREGIBLE":
        return "detectado"

    # La entrega es correcta unicamente si el mensaje recuperado coincide con el original
    if resultado["mensaje"] == mensaje:
        return "correcto"

    # Si el mensaje difiere, el receptor acepto una trama erronea sin advertirlo
    return "aceptacion_erronea"


def evaluar_fletcher(mensaje_con_relleno, trama_recibida, tamanio_bloque):
    """Clasifica el resultado de una recepción bajo el Fletcher checksum."""
    resultado = fletcher.verificar(trama_recibida, tamanio_bloque)

    if resultado["estado"] != "SIN_ERRORES":
        return "detectado"

    if resultado["mensaje"] == mensaje_con_relleno:
        return "correcto"

    return "aceptacion_erronea"


def simular_probabilidades(generador):
    """Ejecuta el experimento que varia la probabilidad de error del canal."""
    datos = {
        "HAMMING": {"correcto": [], "detectado": [], "aceptacion_erronea": []},
        "FLETCHER-8": {"correcto": [], "detectado": [], "aceptacion_erronea": []},
        "FLETCHER-16": {"correcto": [], "detectado": [], "aceptacion_erronea": []},
    }

    for probabilidad in PROBABILIDADES:
        conteos = {clave: {"correcto": 0, "detectado": 0, "aceptacion_erronea": 0} for clave in datos}

        for _ in range(REPETICIONES):
            mensaje = mensaje_aleatorio(LONGITUD_REFERENCIA, generador)

            trama = hamming.codificar(mensaje)
            recibida = aplicar_ruido(trama, probabilidad, generador)
            conteos["HAMMING"][evaluar_hamming(mensaje, recibida)] += 1

            for bloque, clave in ((8, "FLETCHER-8"), (16, "FLETCHER-16")):
                trama = fletcher.codificar(mensaje, bloque)

                # El cuerpo esperado excluye los 2k bits de checksum agregados al final
                cuerpo = trama[: len(trama) - 2 * bloque]

                recibida = aplicar_ruido(trama, probabilidad, generador)
                conteos[clave][evaluar_fletcher(cuerpo, recibida, bloque)] += 1

        for clave in datos:
            for categoria in datos[clave]:
                # Los conteos se convierten a porcentaje sobre el total de repeticiones
                datos[clave][categoria].append(100.0 * conteos[clave][categoria] / REPETICIONES)

    return datos


def simular_cantidad_errores(generador):
    """Ejecuta el experimento que altera una cantidad exacta de bits por trama."""
    cantidades = [0, 1, 2, 3]

    datos = {
        "HAMMING": {"correcto": [], "detectado": [], "aceptacion_erronea": []},
        "FLETCHER-8": {"correcto": [], "detectado": [], "aceptacion_erronea": []},
    }

    for cantidad in cantidades:
        conteos = {clave: {"correcto": 0, "detectado": 0, "aceptacion_erronea": 0} for clave in datos}

        for _ in range(REPETICIONES):
            mensaje = mensaje_aleatorio(LONGITUD_REFERENCIA, generador)

            trama = hamming.codificar(mensaje)
            recibida = alterar_bits(trama, cantidad, generador) if cantidad else trama
            conteos["HAMMING"][evaluar_hamming(mensaje, recibida)] += 1

            trama = fletcher.codificar(mensaje, 8)
            cuerpo = trama[: len(trama) - 16]
            recibida = alterar_bits(trama, cantidad, generador) if cantidad else trama
            conteos["FLETCHER-8"][evaluar_fletcher(cuerpo, recibida, 8)] += 1

        for clave in datos:
            for categoria in datos[clave]:
                datos[clave][categoria].append(100.0 * conteos[clave][categoria] / REPETICIONES)

    return cantidades, datos


def calcular_overhead():
    """Calcula el overhead porcentual de cada esquema para las longitudes evaluadas."""
    datos = {"HAMMING": [], "FLETCHER-8": [], "FLETCHER-16": [], "FLETCHER-32": []}

    for longitud in LONGITUDES:
        # El overhead de Hamming corresponde unicamente a sus bits de paridad
        redundancia = hamming.calcular_bits_redundancia(longitud)
        datos["HAMMING"].append(100.0 * redundancia / longitud)

        for bloque in (8, 16, 32):
            sobrante = longitud % bloque
            relleno = 0 if sobrante == 0 else bloque - sobrante

            # El overhead de Fletcher incluye el checksum de 2k bits y el relleno agregado
            redundancia = 2 * bloque + relleno
            datos[f"FLETCHER-{bloque}"].append(100.0 * redundancia / longitud)

    return datos


def graficar_entrega_correcta(datos):
    """Genera la grafica de tasa de entrega correcta contra la probabilidad de error."""
    figura, ejes = plt.subplots(figsize=(8, 5))

    for clave, marcador in (("HAMMING", "o"), ("FLETCHER-8", "s"), ("FLETCHER-16", "^")):
        ejes.plot(PROBABILIDADES, datos[clave]["correcto"], marker=marcador, label=clave)

    ejes.set_xlabel("Probabilidad de error por bit")
    ejes.set_ylabel("Mensajes entregados correctamente (por ciento)")
    ejes.set_title(f"Entrega correcta contra probabilidad de error, mensaje de {LONGITUD_REFERENCIA} bits")
    ejes.grid(True, linestyle="--", alpha=0.5)
    ejes.legend()

    figura.tight_layout()
    figura.savefig(DIR_FIGURAS / "figura1_entrega_correcta.png", dpi=200)
    plt.close(figura)


def graficar_aceptacion_erronea(datos):
    """Genera la grafica de aceptación erronea, es decir de fallas silenciosas del algoritmo."""
    figura, ejes = plt.subplots(figsize=(8, 5))

    for clave, marcador in (("HAMMING", "o"), ("FLETCHER-8", "s"), ("FLETCHER-16", "^")):
        ejes.plot(PROBABILIDADES, datos[clave]["aceptacion_erronea"], marker=marcador, label=clave)

    ejes.set_xlabel("Probabilidad de error por bit")
    ejes.set_ylabel("Tramas aceptadas con contenido erroneo (por ciento)")
    ejes.set_title("Fallas silenciosas contra probabilidad de error")
    ejes.grid(True, linestyle="--", alpha=0.5)
    ejes.legend()

    figura.tight_layout()
    figura.savefig(DIR_FIGURAS / "figura2_aceptacion_erronea.png", dpi=200)
    plt.close(figura)


def graficar_overhead(datos):
    """Genera la grafica de overhead porcentual contra la longitud del mensaje."""
    figura, ejes = plt.subplots(figsize=(8, 5))

    for clave, marcador in (("HAMMING", "o"), ("FLETCHER-8", "s"), ("FLETCHER-16", "^"), ("FLETCHER-32", "d")):
        ejes.plot(LONGITUDES, datos[clave], marker=marcador, label=clave)

    ejes.set_xlabel("Longitud del mensaje (bits)")
    ejes.set_ylabel("Overhead (por ciento del mensaje)")
    ejes.set_title("Overhead de redundancia contra longitud del mensaje")
    ejes.set_xscale("log", base=2)
    ejes.grid(True, linestyle="--", alpha=0.5)
    ejes.legend()

    figura.tight_layout()
    figura.savefig(DIR_FIGURAS / "figura3_overhead.png", dpi=200)
    plt.close(figura)


def graficar_cantidad_errores(cantidades, datos):
    """Genera la grafica de barras del comportamiento ante cero, uno, dos y tres errores."""
    figura, ejes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)

    for indice, clave in enumerate(("HAMMING", "FLETCHER-8")):
        base = [0.0] * len(cantidades)

        for categoria, etiqueta in (
            ("correcto", "Entrega correcta"),
            ("detectado", "Error detectado"),
            ("aceptacion_erronea", "Aceptacion erronea"),
        ):
            valores = datos[clave][categoria]

            # Las barras se apilan acumulando la altura de las categorias previas
            ejes[indice].bar(range(len(cantidades)), valores, bottom=base, label=etiqueta)
            base = [base[i] + valores[i] for i in range(len(valores))]

        ejes[indice].set_title(clave)
        ejes[indice].set_xticks(range(len(cantidades)))
        ejes[indice].set_xticklabels([str(cantidad) for cantidad in cantidades])
        ejes[indice].set_xlabel("Bits alterados por trama")

    ejes[0].set_ylabel("Porcentaje de tramas")

    # La leyenda se coloca al pie de la figura para no encimarse sobre las barras
    manejadores, etiquetas = ejes[0].get_legend_handles_labels()
    figura.legend(manejadores, etiquetas, loc="lower center", ncol=3)

    figura.suptitle("Comportamiento ante cero, uno, dos y tres errores")
    figura.tight_layout(rect=(0, 0.08, 1, 1))
    figura.savefig(DIR_FIGURAS / "figura4_cantidad_errores.png", dpi=200)
    plt.close(figura)


def main():
    """Ejecuta todos los experimentos, exporta las figuras y muestra el resumen en consola."""
    mostrar_encabezado()

    # El directorio de figuras se crea cuando aun no existe
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)

    generador = random.Random(SEMILLA)

    franja_mayor("EXPERIMENTO 1: PROBABILIDAD DE ERROR DEL CANAL")
    datos_probabilidad = simular_probabilidades(generador)

    for clave in datos_probabilidad:
        print(f"{clave}")

        for i, probabilidad in enumerate(PROBABILIDADES):
            correcto = datos_probabilidad[clave]["correcto"][i]
            detectado = datos_probabilidad[clave]["detectado"][i]
            erroneo = datos_probabilidad[clave]["aceptacion_erronea"][i]

            print(f"   Probabilidad {probabilidad}")
            print(f"      Entrega Correcta: {correcto:.2f}%")
            print(f"      Error Detectado: {detectado:.2f}%")
            print(f"      Aceptación Errónea: {erroneo:.2f}%")

        print()

    franja_mayor("EXPERIMENTO 2: CANTIDAD EXACTA DE ERRORES")
    cantidades, datos_cantidad = simular_cantidad_errores(generador)

    for clave in datos_cantidad:
        print(f"{clave}")

        for i, cantidad in enumerate(cantidades):
            correcto = datos_cantidad[clave]["correcto"][i]
            detectado = datos_cantidad[clave]["detectado"][i]
            erroneo = datos_cantidad[clave]["aceptacion_erronea"][i]

            print(f"   Bits Alterados: {cantidad}")
            print(f"      Entrega Correcta: {correcto:.2f}%")
            print(f"      Error Detectado: {detectado:.2f}%")
            print(f"      Aceptación Errónea: {erroneo:.2f}%")

        print()

    franja_mayor("EXPERIMENTO 3: OVERHEAD DE REDUNDANCIA")
    datos_overhead = calcular_overhead()

    for clave in datos_overhead:
        print(f"{clave}")

        for i, valor in enumerate(datos_overhead[clave]):
            print(f"   Mensaje de {LONGITUDES[i]} Bits: {valor:.2f}%")

        print()

    graficar_entrega_correcta(datos_probabilidad)
    graficar_aceptacion_erronea(datos_probabilidad)
    graficar_overhead(datos_overhead)
    graficar_cantidad_errores(cantidades, datos_cantidad)

    franja_mayor("FIGURAS EXPORTADAS")
    print(f"Directorio: {DIR_FIGURAS}")
    print()
    print("1. figura1_entrega_correcta.png")
    print("2. figura2_aceptacion_erronea.png")
    print("3. figura3_overhead.png")
    print("4. figura4_cantidad_errores.png")
    print()


# Punto de entrada estandar del script
if __name__ == "__main__":
    main()
