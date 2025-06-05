#!/bin/bash

# Compilar el algoritmo Quadtree 
mkdir -p core/quadtree/build
cd core/quadtree/build
cmake ../src
make
cd ../../..
echo "¡Algoritmo Compilado!"

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# source venv/Scripts/activate  # Windows (Git Bash)

echo "¡Entorno Virtual Listo!"

# Instalar dependencias
pip install -r requirements.txt

echo "¡Configuración completada! Ejecuta: python -m app.main"