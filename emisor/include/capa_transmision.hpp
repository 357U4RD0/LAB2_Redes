/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_transmision.hpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Declaración del servicio enviar_informacion correspondiente a la capa de Transmisión del emisor.
 *
 *              Establece una conexión TCP contra el receptor mediante sockets sobre el puerto elegido y envia la trama junto con
 *              los metadatos minimos que el receptor necesita para reconstruir el proceso de verificación. Esta capa complementa
 *              el traslado manual exigido por la guia resumida y habilita la arquitectura completa descrita en las instrucciones.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#ifndef CAPA_TRANSMISION_HPP
#define CAPA_TRANSMISION_HPP

#include <string>

// Envia una carga util por sockets y devuelve verdadero si la operación fue exitosa
bool enviarInformacion(const std::string &host, int puerto, const std::string &carga, std::string &mensajeError);

#endif
