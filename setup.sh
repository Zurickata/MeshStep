#!/bin/bash

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# source venv/Scripts/activate  # Windows (Git Bash)

# Instalar dependencias
pip install -r requirements.txt

# Compilar el algoritmo Quadtree (solo si no existe el binario)
mkdir -p core/quadtree/build
cd core/quadtree/build
cmake ../src
make
cd ../../..

echo "¡Configuración completada! Ejecuta: python -m app.main"