#!/bin/bash

# =========================================================
# 🧩 MeshStep Setup Script
# Descripción:
#   Este script prepara el entorno de desarrollo de MeshStep:
#   - Verifica dependencias del sistema
#   - Compila los algoritmos Quadtree y Octree (C++)
#   - Crea entorno virtual y instala dependencias Python
# =========================================================

# --- Colores para mensajes ---
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # Sin color

echo -e "${GREEN}🚀 Iniciando configuración de MeshStep...${NC}"

# --- Verificar dependencias del sistema ---
echo -e "${YELLOW}🔍 Verificando dependencias del sistema...${NC}"

# Lista de dependencias y cómo probarlas
declare -A DEPENDENCIAS
DEPENDENCIAS=(
  ["python3"]="python3 --version"
  ["pip3"]="pip3 --version"
  ["python3-venv"]="python3 -m venv --help"
  ["cmake"]="cmake --version"
  ["git"]="git --version"
  ["make"]="make --version"
)

FALTAN=0

for dep in "${!DEPENDENCIAS[@]}"; do
    cmd=${DEPENDENCIAS[$dep]}
    if eval "$cmd" &>/dev/null; then
        echo -e "${GREEN}✅ $dep está instalado.${NC}"
    else
        echo -e "${RED}❌ $dep no está instalado o no se encontró su comando.${NC}"
        FALTAN=$((FALTAN + 1))
    fi
done

if [ $FALTAN -ne 0 ]; then
    echo -e "\n${RED}⚠️ Faltan $FALTAN dependencias. Por favor instálalas antes de continuar.${NC}"
    exit 1
else
    echo -e "\n${GREEN}✅ Todas las dependencias están correctamente instaladas.${NC}\n"
fi

# --- Inicializar submódulos ---
echo -e "${YELLOW}🔄 Actualizando submódulos del repositorio...${NC}"
git submodule init
git submodule update
echo -e "${GREEN}✅ Submódulos actualizados correctamente.${NC}\n"

# --- Función para compilar algoritmos ---
compilar_algoritmo() {
    local modulo=$1
    echo -e "${YELLOW}⚙️  Compilando algoritmo ${modulo}...${NC}"

    cd core/${modulo} || { echo -e "${RED}No se encontró core/${modulo}${NC}"; exit 1; }

    git checkout master &>/dev/null
    git pull origin master &>/dev/null

    # Reconstruir build
    rm -rf build
    mkdir -p build && cd build || exit 1
    
    # ⚙️ Detectar estructura del módulo (algunos usan src/, otros no)
    if [ -d "../src" ]; then
        cmake ../src
    else
        cmake ..
    fi

    make -j$(nproc)

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ ${modulo} compilado correctamente.${NC}\n"
    else
        echo -e "${RED}❌ Error al compilar ${modulo}.${NC}"
        exit 1
    fi

    cd ../../..
}

# --- Compilar Quadtree y Octree ---
compilar_algoritmo "quadtree"
compilar_algoritmo "octree"
compilar_algoritmo "jeans"

# --- Crear entorno virtual ---
echo -e "${YELLOW}🐍 Creando entorno virtual de Python...${NC}"
python3 -m venv venv

# Activar entorno
# shellcheck disable=SC1091
source venv/bin/activate || { echo -e "${RED}No se pudo activar el entorno virtual.${NC}"; exit 1; }

echo -e "${GREEN}✅ Entorno virtual activado.${NC}"

# --- Instalar dependencias de Python ---
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📦 Instalando dependencias Python...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencias instaladas correctamente.${NC}\n"
else
    echo -e "${RED}⚠️ No se encontró el archivo requirements.txt${NC}"
fi

# --- Mensaje final ---
echo -e "${GREEN}🎉 Configuración completada exitosamente.${NC}"
echo -e "Para ejecutar MeshStep:\n"
echo -e "${YELLOW}source venv/bin/activate${NC}"
echo -e "${YELLOW}python -m app.main${NC}\n"
