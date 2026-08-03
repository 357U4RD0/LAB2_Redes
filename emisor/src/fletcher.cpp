/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * fletcher.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Implementación del algoritmo de detección de errores Fletcher checksum para el lado emisor.
 *
 *              Divide el mensaje binario en bloques del tamaño configurado, aplicando relleno de ceros a la derecha cuando la
 *              longitud no es multiplo del bloque. Acumula sum1 como la suma de los bloques y sum2 como la suma de los valores
 *              sucesivos de sum1, ambas en modulo 2^k - 1, y concatena sum2 seguido de sum1 como checksum de 2k bits.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#include "fletcher.hpp"

// Convierte un valor entero sin signo a su representación binaria con una cantidad fija de bits
static std::string aBinario(uint64_t valor, int cantidadBits) {
    std::string bits(cantidadBits, '0');

    for (int i = cantidadBits - 1; i >= 0; i--) {
        // Extrae el bit menos significativo y avanza de derecha a izquierda sobre la cadena
        bits[i] = static_cast<char>('0' + (valor & 1ULL));
        valor >>= 1;
    }

    return bits;
}

bool tamanioBloqueValido(int tamanioBloque) {
    // El laboratorio exige que las tres opciones de bloque sean configurables
    return tamanioBloque == 8 || tamanioBloque == 16 || tamanioBloque == 32;
}

ResultadoFletcher codificarFletcher(const std::string &mensajeBinario, int tamanioBloque) {
    ResultadoFletcher resultado;

    resultado.tamanioBloque = tamanioBloque;
    resultado.mensajeConRelleno = mensajeBinario;

    // Determina cuantos ceros faltan para completar el ultimo bloque
    int sobrante = static_cast<int>(mensajeBinario.size()) % tamanioBloque;
    int relleno = (sobrante == 0) ? 0 : (tamanioBloque - sobrante);

    // El relleno se agrega a la derecha para no alterar el orden de los bits originales
    resultado.mensajeConRelleno.append(relleno, '0');
    resultado.bitsRelleno = relleno;

    // El modulo del algoritmo es 2^k - 1, valor que exige acumuladores de 64 bits cuando k es 32
    uint64_t modulo = (1ULL << tamanioBloque) - 1ULL;

    uint64_t suma1 = 0;
    uint64_t suma2 = 0;
    int cantidadBloques = 0;

    for (size_t inicio = 0; inicio < resultado.mensajeConRelleno.size(); inicio += tamanioBloque) {
        uint64_t valorBloque = 0;

        for (int i = 0; i < tamanioBloque; i++) {
            // Interpreta el bloque como un entero sin signo en notación big endian
            valorBloque = (valorBloque << 1) | static_cast<uint64_t>(resultado.mensajeConRelleno[inicio + i] - '0');
        }

        // sum1 acumula el valor de cada bloque en aritmetica modular
        suma1 = (suma1 + valorBloque) % modulo;

        // sum2 acumula los valores sucesivos de sum1, lo que hace al checksum sensible al orden de los bloques
        suma2 = (suma2 + suma1) % modulo;

        cantidadBloques++;
    }

    resultado.suma1 = suma1;
    resultado.suma2 = suma2;
    resultado.cantidadBloques = cantidadBloques;

    // El checksum se forma con sum2 en la parte alta y sum1 en la parte baja, ocupando 2k bits en total
    resultado.checksum = aBinario(suma2, tamanioBloque) + aBinario(suma1, tamanioBloque);

    // La trama transmitida es el mensaje con relleno seguido del checksum
    resultado.trama = resultado.mensajeConRelleno + resultado.checksum;

    return resultado;
}
