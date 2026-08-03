# Laboratorio 2 - Esquemas de Detección y Corrección de Errores

Implementación de un emisor y un receptor escritos en lenguajes distintos que aplican esquemas de detección y corrección de errores sobre tramas binarias, con arquitectura por capas, módulo de ruido probabilístico, traslado manual de la trama y transmisión real mediante sockets, acompañada del análisis experimental del comportamiento de cada algoritmo frente a cero, uno y múltiples errores.

## Integrantes

• André Emilio Pivaral López - 23574

**Universidad del Valle de Guatemala**  
Facultad de Ingeniería  
Departamento de Computación  
Redes  
  
**Catedrático:** Kevin Antonio Velásquez Aguilar  
**Sección:** 10

## Descripción

El proyecto simula la manera en que la capa de Enlace protege la integridad de los datos cuando el medio de transmisión no es confiable. El emisor recibe un mensaje, calcula la información de redundancia correspondiente al algoritmo seleccionado, expone la trama completa a un canal ruidoso y la entrega al receptor. El receptor recalcula esa información, determina si la trama llegó íntegra y, cuando el algoritmo lo permite, corrige el error e informa la posición afectada.

Se implementaron dos algoritmos, uno de cada categoría exigida. El Código de Hamming cumple la función de corrección: emplea cualquier código de la forma (n, m) que satisfaga la desigualdad m más r más uno menor o igual que dos elevado a r, ubica los bits de paridad en las posiciones potencia de dos y utiliza paridad par, de modo que el síndrome calculado por el receptor señala directamente la posición del bit invertido. El Fletcher checksum cumple la función de detección: admite tramas de cualquier longitud, opera con bloques configurables de ocho, dieciséis o treinta y dos bits, aplica relleno de ceros cuando la longitud del mensaje no es múltiplo del bloque y acumula las sumas parciales en aritmética módulo dos elevado a k menos uno.

El emisor está escrito en C++ y el receptor en Python, cumpliendo la condición de utilizar lenguajes distintos a cada lado de la comunicación. Ambos programas replican la misma arquitectura por capas: Aplicación solicita el mensaje y el algoritmo, Presentación traduce entre texto y ASCII binario, Enlace calcula y verifica la integridad, el módulo de Ruido altera bits con una probabilidad configurable y Transmisión traslada la trama. Los dos modos de operación conviven en el mismo programa: el modo manual muestra la trama en pantalla para copiarla al receptor, tal como pide la guía resumida, y el modo socket la envía por TCP hacia un receptor que permanece escuchando en el puerto elegido, tal como describen las instrucciones completas.

El módulo de ruido actúa sobre la totalidad de la trama, incluidos los bits de redundancia, de manera que la propia información de control también puede corromperse. El receptor distingue de forma explícita entre tres desenlaces: trama recibida sin errores, error detectado y corregido con indicación de la posición, y error detectado que obliga a descartar la trama.

El análisis experimental, las capturas de los tres escenarios de prueba, las gráficas de respaldo y la discusión completa se encuentran en el informe en PDF incluido como entregable.

## Estructura del proyecto

    Laboratorio2/
    ├── analisis/
    │   ├── demostracion_engano.py                          construye y verifica los casos que engañan a cada algoritmo
    │   └── generar_graficas.py                             simulación de Monte Carlo y exportación de las gráficas
    ├── emisor/
    │   ├── include/
    │   │   ├── capa_enlace.hpp                             servicio calcular_integridad
    │   │   ├── capa_presentacion.hpp                       servicio codificar_mensaje
    │   │   ├── capa_ruido.hpp                              servicio aplicar_ruido
    │   │   ├── capa_transmision.hpp                        servicio enviar_informacion
    │   │   ├── fletcher.hpp                                algoritmo de detección
    │   │   ├── hamming.hpp                                 algoritmo de corrección
    │   │   └── utilidades.hpp                              presentación en consola y validación de entradas
    │   ├── src/
    │   │   ├── capa_enlace.cpp
    │   │   ├── capa_presentacion.cpp
    │   │   ├── capa_ruido.cpp
    │   │   ├── capa_transmision.cpp
    │   │   ├── emisor.cpp                                  capa de aplicación y menú principal
    │   │   ├── fletcher.cpp
    │   │   ├── hamming.cpp
    │   │   └── utilidades.cpp
    │   ├── compilar.bat                                    construcción en Windows sin make
    │   └── Makefile                                        construcción en Windows, Linux y macOS
    ├── figures/
    │   ├── figura1_entrega_correcta.png                    entrega correcta contra probabilidad de error
    │   ├── figura2_aceptacion_erronea.png                  fallas silenciosas contra probabilidad de error
    │   ├── figura3_overhead.png                            overhead contra longitud del mensaje
    │   └── figura4_cantidad_errores.png                    comportamiento ante cero, uno, dos y tres errores
    ├── receptor/
    │   ├── algoritmos/
    │   │   ├── fletcher.py                                 verificación del checksum
    │   │   └── hamming.py                                  cálculo del síndrome y corrección
    │   ├── capas/
    │   │   ├── enlace.py                                   servicio verificar_integridad
    │   │   ├── presentacion.py                             servicio decodificar_mensaje
    │   │   └── transmision.py                              servicio recibir_informacion
    │   ├── receptor.py                                     capa de aplicación y menú principal
    │   └── utilidades.py                                   presentación en consola y validación de entradas
    ├── .gitignore
    ├── Informe.pdf
    └── README.md

## Requisitos

- Compilador de C++ compatible con el estándar C++17. Se utilizó g++ 8.1.0 de MinGW-w64 en Windows.
- Python; se utilizó la versión 3.12. El receptor funciona con la biblioteca estándar y no requiere paquetes adicionales.
- Paquete matplotlib, necesario únicamente para el script que genera las gráficas.

## Compilación y ejecución

Construcción del emisor en Windows, desde el directorio `emisor`:

    .\compilar.bat

Ejecución del emisor:

    .\emisor.exe

Ejecución del receptor, desde el directorio `receptor`:

    python receptor.py

Generación de las gráficas, desde la raíz del proyecto:

    python analisis/generar_graficas.py

Demostración de los casos que engañan a cada algoritmo, desde la raíz del proyecto:

    python analisis/demostracion_engano.py

## Contenido del análisis

- Prueba de los tres escenarios exigidos sobre tres mensajes de longitud distinta, de cuatro, ocho y sesenta y cuatro bits, con cada uno de los dos algoritmos. Los escenarios corresponden a trama intacta, trama con un bit alterado y trama con dos o más bits alterados.
- Comportamiento diferenciado del receptor en cada desenlace, incluyendo la posición corregida cuando el algoritmo lo permite y el descarte de la trama cuando solo puede detectar.
- Simulación de Monte Carlo que varía la longitud del mensaje, la probabilidad de error del canal, el algoritmo empleado y el tamaño de bloque del checksum, con clasificación de cada ejecución en entrega correcta, error detectado y aceptación errónea.
- Medición del overhead de cada esquema, entendido como la proporción de bits adicionales respecto del mensaje original, y su relación con la efectividad observada.
- Construcción deliberada de tres casos que llevan al receptor a aceptar una trama alterada como intacta: el patrón de tres bits cuyo síndrome de Hamming se anula, la corrección equivocada de Hamming ante dos bits invertidos y la equivalencia entre un bloque nulo y un bloque de unos en Fletcher, consecuencia de la aritmética módulo dos elevado a k menos uno. Los tres se verifican de forma automática en cada ejecución contra las implementaciones reales del receptor.
