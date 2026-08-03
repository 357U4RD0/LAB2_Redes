/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * fletcher.hpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Declaraciones del algoritmo de detección de errores Fletcher checksum para el lado emisor.
 *
 *              Permite configurar bloques de 8, 16 o 32 bits y aplica relleno de ceros cuando la longitud del mensaje no es
 *              multiplo del tamaño de bloque seleccionado. Calcula las sumas parciales sum1 y sum2 en aritmetica modulo 2^k - 1
 *              y concatena el checksum resultante de 2k bits al final del mensaje, produciendo la trama que entrega la capa de Enlace.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#ifndef FLETCHER_HPP
#define FLETCHER_HPP

#include <cstdint>
#include <string>

// Estructura que agrupa el resultado del calculo de Fletcher checksum
struct ResultadoFletcher {
    // Trama completa formada por el mensaje con relleno y el checksum concatenado
    std::string trama;

    // Mensaje original luego de aplicar el relleno de ceros
    std::string mensajeConRelleno;

    // Representación binaria del checksum con longitud de 2k bits
    std::string checksum;

    // Tamaño de bloque utilizado, en bits
    int tamanioBloque;

    // Cantidad de ceros agregados como relleno
    int bitsRelleno;

    // Cantidad de bloques procesados
    int cantidadBloques;

    // Sumas parciales del algoritmo, conservadas para mostrarlas como evidencia
    uint64_t suma1;
    uint64_t suma2;
};

// Verifica que el tamaño de bloque solicitado sea uno de los tres valores permitidos
bool tamanioBloqueValido(int tamanioBloque);

// Calcula el Fletcher checksum de un mensaje binario y devuelve la trama concatenada
ResultadoFletcher codificarFletcher(const std::string &mensajeBinario, int tamanioBloque);

#endif
