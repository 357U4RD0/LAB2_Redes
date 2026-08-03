/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_presentacion.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Implementación del servicio codificar_mensaje correspondiente a la capa de Presentación del emisor.
 *
 *              Recorre el texto caracter por caracter y genera su codigo ASCII expresado en ocho bits, concatenando los grupos en
 *              una unica cadena binaria. Esta capa desconoce por completo el algoritmo de integridad utilizado, lo que mantiene la
 *              independencia entre capas descrita en el modelo de referencia.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#include "capa_presentacion.hpp"

std::string codificarMensaje(const std::string &texto) {
    std::string binario;

    for (unsigned char caracter : texto) {
        for (int bit = 7; bit >= 0; bit--) {
            // Extrae cada bit del codigo ASCII desde el mas significativo hasta el menos significativo
            binario += static_cast<char>('0' + ((caracter >> bit) & 1));
        }
    }

    return binario;
}
