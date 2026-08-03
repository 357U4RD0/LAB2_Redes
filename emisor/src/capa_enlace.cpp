/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_enlace.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Implementación del servicio calcular_integridad correspondiente a la capa de Enlace del emisor.
 *
 *              Encapsula la invocación de los algoritmos de integridad y homogeneiza su salida en una unica estructura, de modo
 *              que las capas superiores no necesiten conocer los detalles internos de cada esquema. Registra la cantidad de bits
 *              de redundancia agregados, dato que se emplea posteriormente para el analisis de overhead solicitado en el reporte.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#include "capa_enlace.hpp"

#include "fletcher.hpp"
#include "hamming.hpp"

std::string nombreAlgoritmo(Algoritmo algoritmo) {
    // Traduce el identificador interno a una etiqueta legible para la salida en pantalla
    if (algoritmo == Algoritmo::HAMMING) return "Hamming: corrección de errores";
    return "Fletcher Checksum: detección de errores";
}

ResultadoEnlace calcularIntegridad(const std::string &mensajeBinario, Algoritmo algoritmo, int tamanioBloque) {
    ResultadoEnlace salida;

    salida.bitsMensaje = static_cast<int>(mensajeBinario.size());

    if (algoritmo == Algoritmo::HAMMING) {
        ResultadoHamming resultado = codificarHamming(mensajeBinario);

        salida.trama = resultado.trama;
        salida.bitsRedundancia = resultado.bitsRedundancia;

        // Documenta el codigo (n, m) obtenido para dejar constancia de la relación entre datos y redundancia
        salida.detalle = "Código (" + std::to_string(resultado.bitsDatos + resultado.bitsRedundancia) + ", " +
                         std::to_string(resultado.bitsDatos) + ") con " + std::to_string(resultado.bitsRedundancia) +
                         " bits de paridad";
    } else {
        ResultadoFletcher resultado = codificarFletcher(mensajeBinario, tamanioBloque);

        salida.trama = resultado.trama;

        // La redundancia de Fletcher incluye el checksum de 2k bits y los ceros de relleno agregados
        salida.bitsRedundancia = 2 * tamanioBloque + resultado.bitsRelleno;

        salida.detalle = std::to_string(resultado.cantidadBloques) + " bloques de " + std::to_string(tamanioBloque) +
                         " bits, relleno de " + std::to_string(resultado.bitsRelleno) + " bits, sum1 = " +
                         std::to_string(resultado.suma1) + ", sum2 = " + std::to_string(resultado.suma2);
    }

    return salida;
}
