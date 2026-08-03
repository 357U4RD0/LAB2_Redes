@echo off
REM ----------------------------------------------------------------------------------------------------------------------------------------------------------------
REM compilar.bat
REM ----------------------------------------------------------------------------------------------------------------------------------------------------------------
REM UNIVERSIDAD DEL VALLE DE GUATEMALA
REM Redes
REM
REM Descripcion: Script de compilacion del emisor.
REM
REM              Compila en una sola invocacion todos los archivos fuente del emisor y enlaza la biblioteca ws2_32 requerida por
REM              la interfaz de sockets, produciendo el ejecutable emisor.exe en este mismo directorio. Ajusta la pagina de
REM              codigos de la consola a UTF-8 para que los mensajes con tilde se muestren correctamente y reporta el resultado
REM              con el mismo estilo visual del resto del proyecto.
REM
REM Autor:        Andre Emilio Pivaral Lopez - 23574
REM Fecha:        2 de Agosto de 2026
REM ----------------------------------------------------------------------------------------------------------------------------------------------------------------

setlocal

REM La pagina de codigos 65001 corresponde a UTF-8 y permite mostrar los caracteres acentuados
chcp 65001 >nul

echo ------------------------------------------------------------------------------------------------------------------------
echo                                                   COMPILACIÓN - EMISOR
echo ------------------------------------------------------------------------------------------------------------------------
echo.

REM Verifica que el compilador este disponible en la variable PATH antes de continuar
where g++ >nul 2>nul
if errorlevel 1 (
    echo ------------------------------------------------------------------------------------------------------------------------
    echo                                                   ERROR DE COMPILACIÓN
    echo ------------------------------------------------------------------------------------------------------------------------
    echo Motivo: no se encontró el compilador en el PATH del sistema.
    echo.
    exit /b 1
)

REM Compila y enlaza todos los archivos fuente en una sola instruccion
g++ -std=c++17 -Wall -Wextra -O2 -Iinclude ^
    src/emisor.cpp ^
    src/utilidades.cpp ^
    src/capa_presentacion.cpp ^
    src/capa_enlace.cpp ^
    src/capa_ruido.cpp ^
    src/capa_transmision.cpp ^
    src/hamming.cpp ^
    src/fletcher.cpp ^
    -o emisor.exe -lws2_32

if errorlevel 1 (
    echo.
    echo ------------------------------------------------------------------------------------------------------------------------
    echo                                                   ERROR DE COMPILACIÓN
    echo ------------------------------------------------------------------------------------------------------------------------
    echo Motivo: revisa los mensajes del compilador mostrados arriba.
    echo.
    exit /b 1
)

echo ------------------------------------------------------------------------------------------------------------------------
echo                                                  ¡COMPILACIÓN EXITOSA!
echo ------------------------------------------------------------------------------------------------------------------------
echo Ejecutable: emisor.exe
echo.

endlocal
