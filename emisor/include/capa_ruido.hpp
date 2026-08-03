/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_ruido.hpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Declaración del servicio aplicar_ruido correspondiente al modulo de Ruido del emisor.
 *
 *              Simula el canal no confiable evaluando cada bit de la trama de forma independiente contra una probabilidad de error
 *              expresada como errores por bits transmitidos. La totalidad de la trama queda expuesta al ruido, incluida la
 *              información de redundancia, de modo que los bits de paridad y el checksum tambien pueden resultar alterados.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#ifndef CAPA_RUIDO_HPP
#define CAPA_RUIDO_HPP

#include <string>
#include <vector>

// Estructura devuelta por el servicio aplicar_ruido
struct ResultadoRuido {
    // Trama luego de la posible inversión de bits
    std::string trama;

    // Posiciones, iniciando en uno, de los bits que sufrieron inversión
    std::vector<int> posicionesAlteradas;
};

// Invierte cada bit de la trama con la probabilidad indicada, expresada como valor entre cero y uno
ResultadoRuido aplicarRuido(const std::string &trama, double probabilidadError);

#endif
