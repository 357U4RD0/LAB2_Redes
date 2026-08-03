/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_ruido.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Implementación del servicio aplicar_ruido correspondiente al modulo de Ruido del emisor.
 *
 *              Utiliza un generador Mersenne Twister sembrado con el reloj del sistema y una distribución uniforme continua para
 *              decidir, bit por bit, si ocurre una inversión. Registra las posiciones alteradas con el fin de contrastarlas contra
 *              el diagnostico emitido por el receptor durante las pruebas experimentales.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#include "capa_ruido.hpp"

#include <chrono>
#include <random>

ResultadoRuido aplicarRuido(const std::string &trama, double probabilidadError) {
    ResultadoRuido resultado;

    resultado.trama = trama;

    // Una probabilidad no positiva equivale a un canal ideal, por lo que la trama se devuelve intacta
    if (probabilidadError <= 0.0) return resultado;

    // La semilla proviene del reloj de alta resolución para que cada ejecución produzca una secuencia distinta
    unsigned int semilla = static_cast<unsigned int>(std::chrono::high_resolution_clock::now().time_since_epoch().count());

    std::mt19937 generador(semilla);
    std::uniform_real_distribution<double> distribucion(0.0, 1.0);

    for (size_t i = 0; i < resultado.trama.size(); i++) {
        // Cada bit se evalua de forma independiente contra la probabilidad de error del canal
        if (distribucion(generador) < probabilidadError) {
            // La inversión se realiza intercambiando el simbolo por su complemento
            resultado.trama[i] = (resultado.trama[i] == '0') ? '1' : '0';

            // Las posiciones se reportan iniciando en uno para coincidir con la numeración del receptor
            resultado.posicionesAlteradas.push_back(static_cast<int>(i) + 1);
        }
    }

    return resultado;
}
