/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * capa_transmision.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Implementación del servicio enviar_informacion correspondiente a la capa de Transmisión del emisor.
 *
 *              Crea un socket TCP, resuelve la dirección del receptor y transmite la carga util completa controlando los envios
 *              parciales que puede reportar el sistema operativo. El codigo es portable; utiliza Winsock en Windows y sockets
 *              POSIX en Linux y macOS, seleccionando la implementación mediante compilación condicional. El formato acordado con
 *              el receptor es algoritmo, parametro y trama separados por punto y coma, terminando con un salto de linea.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

// Windows expone la interfaz de sockets a traves de Winsock, que requiere cabeceras e inicialización propias
#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>

// Alias que unifican los nombres de tipo y de funciones entre ambas plataformas
typedef SOCKET DescriptorSocket;
#define SOCKET_INVALIDO INVALID_SOCKET
#define cerrarSocket closesocket

#else
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

// En sistemas POSIX el descriptor es un entero y se libera con close
typedef int DescriptorSocket;
#define SOCKET_INVALIDO (-1)
#define cerrarSocket close

#endif

#include "capa_transmision.hpp"

#include <cstring>

// Convierte una dirección IPv4 en notación decimal punteada a su forma binaria dentro de la estructura sockaddr_in
static bool convertirDireccion(const std::string &host, sockaddr_in &direccion) {
    // inet_addr esta disponible en todas las versiones de Winsock y en POSIX, lo que evita depender de inet_pton
    unsigned long valor = inet_addr(host.c_str());

    // INADDR_NONE indica que la cadena no representa una dirección IPv4 valida
    if (valor == INADDR_NONE) return false;

    direccion.sin_addr.s_addr = static_cast<unsigned int>(valor);

    return true;
}

bool enviarInformacion(const std::string &host, int puerto, const std::string &carga, std::string &mensajeError) {
#ifdef _WIN32
    WSADATA datosWinsock;

    // Winsock exige inicializar la biblioteca antes de utilizar cualquier función de sockets
    if (WSAStartup(MAKEWORD(2, 2), &datosWinsock) != 0) {
        mensajeError = "No fue posible inicializar Winsock";
        return false;
    }
#endif

    // Crea un socket de flujo sobre IPv4, equivalente a una conexión TCP
    DescriptorSocket descriptor = socket(AF_INET, SOCK_STREAM, 0);

    if (descriptor == SOCKET_INVALIDO) {
        mensajeError = "No fue posible crear el socket";

#ifdef _WIN32
        WSACleanup();
#endif
        return false;
    }

    sockaddr_in direccion;

    // memset garantiza que la estructura quede sin datos residuales antes de completarla
    std::memset(&direccion, 0, sizeof(direccion));

    direccion.sin_family = AF_INET;

    // htons convierte el puerto al orden de bytes de red exigido por la interfaz de sockets
    direccion.sin_port = htons(static_cast<unsigned short>(puerto));

    // Traduce la dirección en notación decimal punteada a su forma binaria
    if (!convertirDireccion(host, direccion)) {
        mensajeError = "Dirección de host inválida";
        cerrarSocket(descriptor);

#ifdef _WIN32
        WSACleanup();
#endif
        return false;
    }

    if (connect(descriptor, reinterpret_cast<sockaddr *>(&direccion), sizeof(direccion)) < 0) {
        mensajeError = "No fue posible conectar con el receptor: verifica que esté escuchando";
        cerrarSocket(descriptor);

#ifdef _WIN32
        WSACleanup();
#endif
        return false;
    }

    // El salto de linea final delimita el mensaje para que el receptor sepa cuando termino la trama
    std::string mensaje = carga + "\n";

    size_t enviados = 0;

    while (enviados < mensaje.size()) {
        // send puede transmitir menos bytes de los solicitados, por lo que se repite hasta completar la carga
        int bytes = static_cast<int>(send(descriptor, mensaje.c_str() + enviados,
                                          static_cast<int>(mensaje.size() - enviados), 0));

        if (bytes <= 0) {
            mensajeError = "Fallo durante el envío de la trama";
            cerrarSocket(descriptor);

#ifdef _WIN32
            WSACleanup();
#endif
            return false;
        }

        enviados += static_cast<size_t>(bytes);
    }

    // Libera el descriptor para no dejar conexiones abiertas entre envios sucesivos
    cerrarSocket(descriptor);

#ifdef _WIN32
    // Libera los recursos reservados por Winsock al finalizar el envio
    WSACleanup();
#endif

    return true;
}
