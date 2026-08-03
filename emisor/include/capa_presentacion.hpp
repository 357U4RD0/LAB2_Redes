/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_presentacion.hpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Declaración del servicio codificar_mensaje correspondiente a la capa de Presentación del emisor.
 *
 *              Traduce cada caracter del mensaje entregado por la capa de Aplicación a su representación ASCII binaria de ocho
 *              bits, tal como lo exige la arquitectura completa del laboratorio. El resultado es la cadena binaria que recibe la
 *              capa de Enlace para el calculo de la información de integridad.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#ifndef CAPA_PRESENTACION_HPP
#define CAPA_PRESENTACION_HPP

#include <string>

// Convierte un texto en su representación ASCII binaria de ocho bits por caracter
std::string codificarMensaje(const std::string &texto);

#endif
