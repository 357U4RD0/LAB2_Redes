/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * utilidades.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Implementación de las funciones de presentación en consola y de validación de cadenas binarias del emisor.
 *
 *              Define el estilo uniforme de salida del programa y resuelve el centrado contando caracteres UTF-8 en lugar de
 *              bytes, condición necesaria para que los titulos acentuados queden alineados. Configura ademas la pagina de codigos
 *              de la consola de Windows y encapsula la lectura de datos del usuario agregando de forma automatica el espacio en
 *              blanco posterior a cada respuesta.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

// La configuración de la consola solo aplica en Windows y requiere la cabecera del sistema
#ifdef _WIN32
#include <windows.h>
#endif

#include "utilidades.hpp"

#include <iostream>

void configurarConsola() {
#ifdef _WIN32
    // La pagina de codigos 65001 corresponde a UTF-8 y permite mostrar tildes y signos de apertura
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
#endif
}

void lineaMayor() {
    std::cout << std::string(ANCHO_MAYOR, '-') << std::endl;
}

// Centra un texto dentro del ancho indicado utilizando su longitud real en caracteres
static void imprimirCentrado(const std::string &texto, int ancho) {
    int relleno = (ancho - longitudUtf8(texto)) / 2;

    // Evita rellenos negativos cuando el texto es mas largo que la linea divisoria
    if (relleno < 0) relleno = 0;

    std::cout << std::string(relleno, ' ') << texto << std::endl;
}

void franjaMayor(const std::string &titulo) {
    lineaMayor();
    imprimirCentrado(titulo, ANCHO_MAYOR);
    lineaMayor();
}

void etiqueta(const std::string &nombre, const std::string &valor) {
    // Ancho reservado para el rotulo de modo que todos los valores queden alineados en columna
    const int anchoNombre = 30;

    std::string texto = nombre + ":";

    // El relleno se calcula sobre la longitud real para no descuadrar los rotulos con tilde
    int faltante = anchoNombre - longitudUtf8(texto);

    if (faltante < 0) faltante = 0;

    std::cout << texto << std::string(faltante, ' ') << valor << std::endl;
}

int longitudUtf8(const std::string &cadena) {
    int total = 0;

    for (unsigned char byte : cadena) {
        // Los bytes de continuación de UTF-8 inician con el patron 10xxxxxx y no cuentan como caracter nuevo
        if ((byte & 0xC0) != 0x80) total++;
    }

    return total;
}

std::string limpiarCadena(const std::string &cadena) {
    std::string resultado;

    for (char caracter : cadena) {
        // Descarta cualquier caracter de espaciado que el usuario haya copiado junto con la trama
        if (caracter != ' ' && caracter != '\t' && caracter != '\n' && caracter != '\r') {
            resultado += caracter;
        }
    }

    return resultado;
}

bool esBinaria(const std::string &cadena) {
    // Una cadena vacia no se considera una trama valida
    if (cadena.empty()) return false;

    for (char caracter : cadena) {
        // Cualquier simbolo distinto de 0 o 1 invalida la trama completa
        if (caracter != '0' && caracter != '1') return false;
    }

    return true;
}

std::string leerDato(const std::string &rotulo) {
    std::string entrada;

    std::cout << rotulo;

    // Se utiliza getline para admitir cadenas con espacios intermedios
    std::getline(std::cin, entrada);

    // El espacio en blanco posterior separa visualmente la respuesta del siguiente bloque
    std::cout << std::endl;

    return entrada;
}

std::string agruparBits(const std::string &bits, int tamanioGrupo) {
    // Si el agrupamiento no aplica se devuelve la cadena original sin modificar
    if (tamanioGrupo <= 0) return bits;

    std::string resultado;

    for (size_t i = 0; i < bits.size(); i++) {
        // Inserta un espacio cada tamanioGrupo bits, excepto al inicio de la cadena
        if (i > 0 && i % static_cast<size_t>(tamanioGrupo) == 0) resultado += " ";
        resultado += bits[i];
    }

    return resultado;
}
