/*
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * emisor.cpp
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * UNIVERSIDAD DEL VALLE DE GUATEMALA
 * Redes
 *
 * Descripción: Programa emisor del Laboratorio 2, implementado en C++, que aplica esquemas de detección y corrección de errores.
 *
 *              Implementa la capa de Aplicación y coordina el descenso del mensaje por las capas de Presentación, Enlace, el modulo
 *              de Ruido y la capa de Transmisión. Permite ingresar el mensaje como cadena binaria directa o como texto convertido a
 *              ASCII binario, seleccionar entre el Código de Hamming y el Fletcher checksum, aplicar una tasa de error configurable
 *              y entregar la trama resultante mediante traslado manual en pantalla o mediante sockets sobre el puerto elegido.
 *              Cada menu conserva una opción de retorno que devuelve el control al paso inmediatamente anterior.
 *
 * Autor:        André Emilio Pivaral López - 23574
 * Fecha:        2 de Agosto de 2026
 * ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

#include "capa_enlace.hpp"
#include "capa_presentacion.hpp"
#include "capa_ruido.hpp"
#include "capa_transmision.hpp"
#include "fletcher.hpp"
#include "utilidades.hpp"

// Codigos de retorno utilizados por los menus para indicar continuar, retroceder o repetir
const int RESULTADO_CONTINUAR = 0;
const int RESULTADO_VOLVER = 1;
const int RESULTADO_REPETIR = 2;

// Muestra el encabezado institucional que identifica al programa al iniciar
static void mostrarEncabezado() {
    franjaMayor("UNIVERSIDAD DEL VALLE DE GUATEMALA");
    std::cout << "Facultad de Ingeniería" << std::endl;
    std::cout << "Departamento de Computación" << std::endl;
    std::cout << "Redes" << std::endl;
    std::cout << "Laboratorio #2" << std::endl;
    std::cout << "Emisor de Tramas con Detección y Corrección de Errores" << std::endl;
    std::cout << "André Emilio Pivaral López - 23574" << std::endl;
    lineaMayor();
    std::cout << "Emisor en C++" << std::endl;
    std::cout << "Algoritmos: Hamming y Fletcher Checksum" << std::endl;
    lineaMayor();
    std::cout << std::endl;
}

// Presenta el menu principal y devuelve la opción elegida por el usuario
static std::string mostrarMenuPrincipal() {
    franjaMayor("MENÚ PRINCIPAL");
    std::cout << "1. Modo Manual: mostrar la trama en la pantalla" << std::endl;
    std::cout << "2. Modo Socket: enviar la trama al receptor" << std::endl;
    std::cout << "3. Salir" << std::endl;

    return limpiarCadena(leerDato("Selecciona una Opción: "));
}

// Solicita el mensaje binario, ya sea de forma directa o a traves de la codificación ASCII
static int solicitarMensaje(std::string &mensajeBinario, std::string &textoOriginal, bool &usoTexto) {
    franjaMayor("CAPA DE APLICACIÓN");
    std::cout << "1. Ingresar un Mensaje como Binario" << std::endl;
    std::cout << "2. Ingresar un Mensaje como Texto y Convertirlo a Binario" << std::endl;
    std::cout << "3. Volver" << std::endl;

    std::string opcion = limpiarCadena(leerDato("Selecciona una Opción: "));

    // La tercera opción devuelve el control al menu principal sin procesar ningun mensaje
    if (opcion == "3") return RESULTADO_VOLVER;

    if (opcion == "1") {
        usoTexto = false;

        std::string entrada = limpiarCadena(leerDato("Ingresa el Mensaje: "));

        // Rechaza cualquier entrada que contenga simbolos distintos de cero y uno
        if (!esBinaria(entrada)) {
            std::cout << "El mensaje debe contener únicamente los símbolos 0 y 1." << std::endl;
            std::cout << std::endl;
            return RESULTADO_REPETIR;
        }

        mensajeBinario = entrada;
        textoOriginal = "";

        return RESULTADO_CONTINUAR;
    }

    if (opcion == "2") {
        usoTexto = true;

        textoOriginal = leerDato("Ingresa el Mensaje: ");

        if (textoOriginal.empty()) {
            std::cout << "El mensaje no puede estar vacío." << std::endl;
            std::cout << std::endl;
            return RESULTADO_REPETIR;
        }

        // La capa de Presentación traduce el texto a su representación ASCII binaria
        mensajeBinario = codificarMensaje(textoOriginal);

        return RESULTADO_CONTINUAR;
    }

    std::cout << "La opción seleccionada no es válida." << std::endl;
    std::cout << std::endl;

    return RESULTADO_REPETIR;
}

// Solicita el tamaño de bloque que utilizara el Fletcher checksum
static int solicitarTamanioBloque(int &tamanioBloque) {
    franjaMayor("TAMAÑO DE BLOQUE");
    std::cout << "1. 8 Bits" << std::endl;
    std::cout << "2. 16 Bits" << std::endl;
    std::cout << "3. 32 Bits" << std::endl;
    std::cout << "4. Volver" << std::endl;

    std::string opcion = limpiarCadena(leerDato("Selecciona una Opción: "));

    // La cuarta opción regresa a la selección de algoritmo
    if (opcion == "4") return RESULTADO_VOLVER;

    if (opcion == "1") tamanioBloque = 8;
    else if (opcion == "2") tamanioBloque = 16;
    else if (opcion == "3") tamanioBloque = 32;
    else {
        std::cout << "La opción seleccionada no es válida." << std::endl;
        std::cout << std::endl;
        return RESULTADO_REPETIR;
    }

    return RESULTADO_CONTINUAR;
}

// Solicita el algoritmo de integridad y, cuando corresponde, el tamaño de bloque de Fletcher
static int solicitarAlgoritmo(Algoritmo &algoritmo, int &tamanioBloque) {
    franjaMayor("SELECCIÓN DE ALGORITMO");
    std::cout << "1. Hamming: corrección de errores" << std::endl;
    std::cout << "2. Fletcher Checksum: detección de errores" << std::endl;
    std::cout << "3. Volver" << std::endl;

    std::string opcion = limpiarCadena(leerDato("Selecciona una Opción: "));

    // La tercera opción regresa a la captura del mensaje
    if (opcion == "3") return RESULTADO_VOLVER;

    if (opcion == "1") {
        algoritmo = Algoritmo::HAMMING;

        // Hamming no utiliza tamaño de bloque, por lo que el parametro se anula
        tamanioBloque = 0;

        return RESULTADO_CONTINUAR;
    }

    if (opcion == "2") {
        algoritmo = Algoritmo::FLETCHER;

        while (true) {
            int resultado = solicitarTamanioBloque(tamanioBloque);

            // El retorno desde el tamaño de bloque reabre la selección de algoritmo
            if (resultado == RESULTADO_VOLVER) return RESULTADO_REPETIR;
            if (resultado == RESULTADO_CONTINUAR) return RESULTADO_CONTINUAR;
        }
    }

    std::cout << "La opción seleccionada no es válida." << std::endl;
    std::cout << std::endl;

    return RESULTADO_REPETIR;
}

// Solicita la tasa de error del canal expresada como un error por cada N bits transmitidos
static double solicitarTasaError(std::string &descripcion) {
    franjaMayor("MÓDULO DE RUIDO");
    std::cout << "La tasa se expresa como un error por cada N bits transmitidos." << std::endl;
    std::cout << "Ingresa 0 para desactivar el ruido y conservar la trama intacta." << std::endl;

    std::string entrada = limpiarCadena(leerDato("Ingresa el Valor de N: "));

    std::istringstream flujo(entrada);
    double denominador = 0.0;
    flujo >> denominador;

    // Un denominador no positivo se interpreta como un canal ideal sin ruido
    if (denominador <= 0.0) {
        descripcion = "Ninguna: canal ideal";
        return 0.0;
    }

    std::ostringstream texto;
    texto << "1/" << static_cast<long long>(denominador);
    descripcion = texto.str();

    return 1.0 / denominador;
}

// Ejecuta el descenso completo del mensaje por las capas del emisor
static void ejecutarTransmision(bool modoSocket) {
    std::string mensajeBinario;
    std::string textoOriginal;
    bool usoTexto = false;

    Algoritmo algoritmo = Algoritmo::HAMMING;
    int tamanioBloque = 0;

    bool listo = false;

    while (!listo) {
        int resultadoMensaje = solicitarMensaje(mensajeBinario, textoOriginal, usoTexto);

        // El retorno desde la capa de Aplicación cancela por completo la transmisión
        if (resultadoMensaje == RESULTADO_VOLVER) return;
        if (resultadoMensaje == RESULTADO_REPETIR) continue;

        while (true) {
            int resultadoAlgoritmo = solicitarAlgoritmo(algoritmo, tamanioBloque);

            if (resultadoAlgoritmo == RESULTADO_CONTINUAR) {
                listo = true;
                break;
            }

            // El retorno desde la selección de algoritmo reabre la captura del mensaje
            if (resultadoAlgoritmo == RESULTADO_VOLVER) break;
        }
    }

    franjaMayor("CAPA DE PRESENTACIÓN");

    if (usoTexto) {
        etiqueta("Texto Original", textoOriginal);
        etiqueta("Caracteres", std::to_string(textoOriginal.size()));
        etiqueta("Mensaje en ASCII Binario", agruparBits(mensajeBinario, 8));
    } else {
        etiqueta("Tipo de Entrada", "Binaria Directa");
        etiqueta("Mensaje Binario", mensajeBinario);
    }

    etiqueta("Bits del Mensaje", std::to_string(mensajeBinario.size()));
    std::cout << std::endl;

    // La capa de Enlace calcula la información de integridad y la concatena al mensaje
    ResultadoEnlace enlace = calcularIntegridad(mensajeBinario, algoritmo, tamanioBloque);

    franjaMayor("CAPA DE ENLACE");
    etiqueta("Algoritmo", nombreAlgoritmo(algoritmo));
    etiqueta("Detalle", enlace.detalle);
    etiqueta("Bits de Redundancia", std::to_string(enlace.bitsRedundancia));
    etiqueta("Longitud de la Trama", std::to_string(enlace.trama.size()));
    etiqueta("Trama Calculada", enlace.trama);
    std::cout << std::endl;

    std::string descripcionTasa;
    double probabilidad = solicitarTasaError(descripcionTasa);

    // Toda la trama queda expuesta al ruido, incluida la información de redundancia
    ResultadoRuido ruido = aplicarRuido(enlace.trama, probabilidad);

    etiqueta("Tasa Aplicada", descripcionTasa);
    etiqueta("Bits Alterados", std::to_string(ruido.posicionesAlteradas.size()));

    if (!ruido.posicionesAlteradas.empty()) {
        std::string posiciones;

        for (size_t i = 0; i < ruido.posicionesAlteradas.size(); i++) {
            // Concatena las posiciones alteradas separadas por coma para contrastarlas con el receptor
            if (i > 0) posiciones += ", ";
            posiciones += std::to_string(ruido.posicionesAlteradas[i]);
        }

        etiqueta("Posiciones Alteradas", posiciones);
    }

    std::cout << std::endl;

    franjaMayor("CAPA DE TRANSMISIÓN");

    // Etiqueta que el receptor utiliza para saber que algoritmo debe aplicar
    std::string clave = (algoritmo == Algoritmo::HAMMING) ? "HAMMING" : "FLETCHER";

    if (modoSocket) {
        std::string host = limpiarCadena(leerDato("Ingresa el Host del Receptor [127.0.0.1]: "));

        // Valor por defecto que apunta al mismo equipo cuando el usuario no escribe nada
        if (host.empty()) host = "127.0.0.1";

        std::string puertoTexto = limpiarCadena(leerDato("Ingresa el Puerto del Receptor [50007]: "));

        int puerto = 50007;

        if (!puertoTexto.empty()) {
            std::istringstream flujo(puertoTexto);
            flujo >> puerto;
        }

        // La carga util incluye los metadatos y la trama separados por punto y coma
        std::string carga = clave + ";" + std::to_string(tamanioBloque) + ";" + ruido.trama;

        std::string error;

        if (enviarInformacion(host, puerto, carga, error)) {
            franjaMayor("¡TRAMA ENVIADA CORRECTAMENTE!");
            etiqueta("Destino", host + ":" + std::to_string(puerto));
        } else {
            franjaMayor("FALLO EN EL ENVÍO");
            etiqueta("Motivo", error);
        }

        std::cout << std::endl;
    } else {
        etiqueta("Modo", "Traslado Manual");
        etiqueta("Algoritmo de Destino", nombreAlgoritmo(algoritmo));

        if (algoritmo == Algoritmo::FLETCHER) {
            etiqueta("Bloque de Destino", std::to_string(tamanioBloque) + " Bits");
        }

        std::cout << std::endl;
        std::cout << "Copia la siguiente trama y pégala en el receptor:" << std::endl;
        lineaMayor();
        std::cout << ruido.trama << std::endl;
        lineaMayor();
        std::cout << std::endl;
    }

    // El overhead se calcula como la proporción de bits adicionales respecto del mensaje original
    double overhead = (enlace.bitsMensaje > 0)
                          ? (100.0 * static_cast<double>(enlace.bitsRedundancia) / static_cast<double>(enlace.bitsMensaje))
                          : 0.0;

    std::ostringstream overheadTexto;
    overheadTexto << std::fixed << std::setprecision(2) << overhead << "%";

    franjaMayor("RESUMEN DE LA TRANSMISIÓN");
    etiqueta("Bits de Datos", std::to_string(enlace.bitsMensaje));
    etiqueta("Bits de Redundancia", std::to_string(enlace.bitsRedundancia));
    etiqueta("Overhead", overheadTexto.str());
    etiqueta("Trama Final", ruido.trama);
    std::cout << std::endl;
}

int main() {
    // La consola de Windows debe configurarse antes de imprimir cualquier caracter acentuado
    configurarConsola();

    mostrarEncabezado();

    while (true) {
        std::string opcion = mostrarMenuPrincipal();

        if (opcion == "1") {
            ejecutarTransmision(false);
        } else if (opcion == "2") {
            ejecutarTransmision(true);
        } else if (opcion == "3") {
            franjaMayor("FIN DEL PROGRAMA EMISOR");
            std::cout << std::endl;
            break;
        } else {
            std::cout << "La opción seleccionada no es válida." << std::endl;
            std::cout << std::endl;
        }
    }

    return 0;
}
