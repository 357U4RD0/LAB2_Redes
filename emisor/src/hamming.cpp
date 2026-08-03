/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * hamming.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Implementación del algoritmo de corrección de errores Código de Hamming para el lado emisor.
 *
 *              Determina la cantidad minima de bits de redundancia mediante la desigualdad m + r + 1 <= 2^r, coloca los bits de
 *              datos en las posiciones que no son potencia de dos y calcula cada bit de paridad con paridad par sobre el conjunto
 *              de posiciones que le corresponde. El resultado es una trama sistematica que el receptor puede verificar y corregir.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#include "hamming.hpp"

int calcularBitsRedundancia(int bitsMensaje) {
    int r = 1;

    // Incrementa r hasta que se cumpla la condición de capacidad m + r + 1 <= 2^r
    while ((bitsMensaje + r + 1) > (1 << r)) {
        r++;
    }

    return r;
}

ResultadoHamming codificarHamming(const std::string &mensajeBinario) {
    ResultadoHamming resultado;

    int m = static_cast<int>(mensajeBinario.size());
    int r = calcularBitsRedundancia(m);
    int n = m + r;

    // Vector de trabajo con indice uno para respetar la numeración clasica de posiciones de Hamming
    std::vector<int> trama(n + 1, 0);

    int indiceMensaje = 0;

    for (int posicion = 1; posicion <= n; posicion++) {
        // Una posición es de paridad cuando es potencia de dos, es decir cuando solo tiene un bit encendido
        bool esPotenciaDeDos = (posicion & (posicion - 1)) == 0;

        if (esPotenciaDeDos) {
            resultado.posicionesParidad.push_back(posicion);
        } else {
            // Las posiciones restantes reciben los bits de datos en el mismo orden en que fueron ingresados
            trama[posicion] = mensajeBinario[indiceMensaje] - '0';
            indiceMensaje++;
        }
    }

    for (int posicionParidad : resultado.posicionesParidad) {
        int paridad = 0;

        for (int posicion = 1; posicion <= n; posicion++) {
            // Un bit de paridad cubre las posiciones cuyo indice contiene encendido el mismo bit que dicha paridad
            if (posicion != posicionParidad && (posicion & posicionParidad) != 0) {
                paridad ^= trama[posicion];
            }
        }

        // Se utiliza paridad par, por lo que el bit de control iguala la suma modulo dos de las posiciones cubiertas
        trama[posicionParidad] = paridad;
    }

    // Convierte el vector de enteros a la cadena binaria que viajara por la red
    for (int posicion = 1; posicion <= n; posicion++) {
        resultado.trama += static_cast<char>('0' + trama[posicion]);
    }

    resultado.bitsDatos = m;
    resultado.bitsRedundancia = r;

    return resultado;
}
