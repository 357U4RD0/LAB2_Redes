/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * hamming.hpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Declaraciones del algoritmo de corrección de errores Código de Hamming para el lado emisor.
 *
 *              Expone el calculo de la cantidad minima de bits de redundancia que satisface la desigualdad m + r + 1 <= 2^r y la
 *              construcción de la trama codificada. Los bits de paridad se ubican en las posiciones potencia de dos y se calculan
 *              con paridad par sobre los conjuntos de posiciones que cada uno cubre, quedando la trama lista para la capa de Enlace.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#ifndef HAMMING_HPP
#define HAMMING_HPP

#include <string>
#include <vector>

// Estructura que agrupa el resultado de la codificación de Hamming
struct ResultadoHamming {
    // Trama completa formada por los bits de datos y los bits de paridad intercalados
    std::string trama;

    // Cantidad de bits de datos del mensaje original
    int bitsDatos;

    // Cantidad de bits de redundancia agregados
    int bitsRedundancia;

    // Posiciones, iniciando en uno, donde quedaron ubicados los bits de paridad
    std::vector<int> posicionesParidad;
};

// Calcula la cantidad minima de bits de redundancia r tal que m + r + 1 <= 2^r
int calcularBitsRedundancia(int bitsMensaje);

// Construye la trama de Hamming con paridad par a partir de un mensaje binario
ResultadoHamming codificarHamming(const std::string &mensajeBinario);

#endif
