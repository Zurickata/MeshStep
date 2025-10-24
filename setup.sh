#!/bin/bash

# Compilar el algoritmo Quadtree 
rm -rf core/quadtree/build
mkdir -p core/quadtree/build
cd core/quadtree/build
cmake ../src
make
cd ../../..
echo "¡Quadtree Compilado!"

# Compilar el algoritmo Octree 
rm -rf core/octree/build
mkdir -p core/octree/build
cd core/octree/build
cmake ../src
make
cd ../../..
cd core/octree
git checkout master
git pull origin master
cd ../..
echo "¡Octree Compilado!"

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# source venv/Scripts/activate  # Windows (Git Bash)

echo "¡El entorno Virtual Listo!"

# Instalar dependencias
pip install -r requirements.txt

echo "¡Configuración completada! Ejecuta: python -m app.main"