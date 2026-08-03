/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_enlace.hpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Declaración del servicio calcular_integridad correspondiente a la capa de Enlace del emisor.
 *
 *              Actua como punto de integración de los algoritmos implementados; selecciona entre el Código de Hamming para
 *              corrección de errores y el Fletcher checksum para detección de errores. Devuelve la trama con la información de
 *              redundancia concatenada junto con los datos descriptivos que se muestran como evidencia en pantalla.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#ifndef CAPA_ENLACE_HPP
#define CAPA_ENLACE_HPP

#include <string>

// Identificadores de los algoritmos disponibles en la capa de Enlace
enum class Algoritmo {
    HAMMING,
    FLETCHER
};

// Estructura devuelta por el servicio calcular_integridad
struct ResultadoEnlace {
    // Trama lista para ser expuesta al ruido y transmitida
    std::string trama;

    // Cantidad de bits del mensaje que ingreso a la capa
    int bitsMensaje;

    // Cantidad de bits agregados como redundancia, incluyendo el relleno cuando aplica
    int bitsRedundancia;

    // Detalle textual del calculo realizado, utilizado unicamente para la impresión de evidencia
    std::string detalle;
};

// Calcula la información de integridad y la concatena al mensaje binario recibido
ResultadoEnlace calcularIntegridad(const std::string &mensajeBinario, Algoritmo algoritmo, int tamanioBloque);

// Devuelve el nombre legible del algoritmo seleccionado
std::string nombreAlgoritmo(Algoritmo algoritmo);

#endif
