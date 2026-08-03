/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * utilidades.hpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Declaraciones de las funciones de presentación en consola y de validación de cadenas binarias del emisor.
 *
 *              Centraliza el formato visual del programa mediante franjas divisorias de 120 caracteres con el titulo centrado y
 *              etiquetas alineadas en columna. Todas las rutinas de medida y centrado interpretan la cadena como UTF-8, de modo
 *              que las tildes y los signos de apertura no desalineen el texto. Incluye ademas la configuración de la consola de
 *              Windows y la lectura de datos del usuario con espaciado automatico.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#ifndef UTILIDADES_HPP
#define UTILIDADES_HPP

#include <string>

// Ancho de todas las lineas divisorias del programa
const int ANCHO_MAYOR = 120;

// Ajusta la consola para que interprete correctamente los caracteres acentuados en Windows
void configurarConsola();

// Imprime una linea divisoria de 120 caracteres de guion
void lineaMayor();

// Imprime un titulo centrado entre dos lineas divisorias de 120 caracteres
void franjaMayor(const std::string &titulo);

// Imprime un par etiqueta valor con la etiqueta alineada a un ancho fijo
void etiqueta(const std::string &nombre, const std::string &valor);

// Cuenta los caracteres reales de una cadena UTF-8, ignorando los bytes de continuación
int longitudUtf8(const std::string &cadena);

// Elimina espacios, tabulaciones y saltos de linea de una cadena
std::string limpiarCadena(const std::string &cadena);

// Indica si la cadena contiene al menos un caracter y solamente los simbolos 0 y 1
bool esBinaria(const std::string &cadena);

// Muestra un rotulo, lee una linea completa y deja un espacio en blanco despues de la respuesta
std::string leerDato(const std::string &rotulo);

// Divide una cadena binaria en grupos separados por espacio para facilitar su lectura
std::string agruparBits(const std::string &bits, int tamanioGrupo);

#endif
