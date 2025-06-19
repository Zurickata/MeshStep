#!/bin/bash

# Ruta donde están los archivos output
TARGET_DIR="./outputs/"

# Eliminar todos los archivos output_* en esa ruta
find "$TARGET_DIR" -type f \( -name '*_output_*' -o -name 'output_*.*' \) -delete

echo "Archivos eliminados en: $TARGET_DIR"