# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Makefile
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Redes
#
# Descripción: Archivo de construcción del programa emisor del Laboratorio 2, escrito en C++ bajo el estandar C++17.
#
#              Compila de forma separada cada capa de la arquitectura y los dos algoritmos de integridad, generando los objetos
#              dentro del directorio build y enlazandolos en el ejecutable emisor. Detecta el sistema operativo para enlazar la
#              biblioteca ws2_32 de Winsock en Windows y para utilizar los comandos de creación y borrado de directorios que
#              correspondan. Incluye los objetivos all, run y clean.
#
# Autor:        André Emilio Pivaral López - 23574
# Fecha:        2 de Agosto de 2026
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Compilador utilizado para todo el proyecto
CXX = g++

# Banderas de compilación; se habilitan advertencias y el estandar C++17
CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -Iinclude

# Directorios de codigo fuente y de objetos intermedios
DIR_SRC = src
DIR_BUILD = build

# La variable OS solo esta definida como Windows_NT en sistemas Windows
ifeq ($(OS),Windows_NT)

# En Windows el ejecutable lleva extension exe y se enlaza la biblioteca de Winsock
OBJETIVO = emisor.exe
LIBS = -lws2_32

# Comandos nativos de la consola de Windows para crear y eliminar directorios
CREAR_DIR = if not exist "$(DIR_BUILD)" mkdir "$(DIR_BUILD)"
LIMPIAR = if exist "$(DIR_BUILD)" rmdir /s /q "$(DIR_BUILD)" & if exist "$(OBJETIVO)" del /q "$(OBJETIVO)"
EJECUTAR = $(OBJETIVO)

else

# En Linux y macOS los sockets forman parte de la biblioteca estandar del sistema
OBJETIVO = emisor
LIBS =

CREAR_DIR = mkdir -p $(DIR_BUILD)
LIMPIAR = rm -rf $(DIR_BUILD) $(OBJETIVO)
EJECUTAR = ./$(OBJETIVO)

endif

# Lista de archivos fuente que componen el emisor
FUENTES = $(DIR_SRC)/emisor.cpp \
          $(DIR_SRC)/utilidades.cpp \
          $(DIR_SRC)/capa_presentacion.cpp \
          $(DIR_SRC)/capa_enlace.cpp \
          $(DIR_SRC)/capa_ruido.cpp \
          $(DIR_SRC)/capa_transmision.cpp \
          $(DIR_SRC)/hamming.cpp \
          $(DIR_SRC)/fletcher.cpp

# Traduce cada archivo fuente a su archivo objeto correspondiente
OBJETOS = $(FUENTES:$(DIR_SRC)/%.cpp=$(DIR_BUILD)/%.o)

# Objetivo por defecto que construye el ejecutable
all: $(OBJETIVO)

# Enlaza todos los objetos para producir el ejecutable final
$(OBJETIVO): $(OBJETOS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LIBS)

# Regla generica que compila cada archivo fuente a objeto
$(DIR_BUILD)/%.o: $(DIR_SRC)/%.cpp | $(DIR_BUILD)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Crea el directorio de objetos cuando aun no existe
$(DIR_BUILD):
	$(CREAR_DIR)

# Compila y ejecuta el emisor en una sola instrucción
run: $(OBJETIVO)
	$(EJECUTAR)

# Elimina los objetos intermedios y el ejecutable generado
clean:
	$(LIMPIAR)

.PHONY: all run clean
