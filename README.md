# MeshStep  
**Visualización Educativa de Algoritmos de Mallado (Quadtree y Octree)**  

MeshStep es una herramienta interactiva para visualizar el proceso de generación de mallas 2D y 3D paso a paso, facilitando el aprendizaje y análisis de los algoritmos de mallado.

---

## Requisitos del sistema  

**Sistema operativo:** Linux (Ubuntu/Debian o WSL)  
**Versión mínima recomendada:** Ubuntu 22.04 o superior  

### Dependencias necesarias
Asegúrate de tener instalados los siguientes paquetes:
- `python3` (≥ 3.10)
- `pip3`
- `python3-venv`
- `cmake` (≥ 3.22)
- `git`
- `make`

Para instalarlos:
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv cmake git make
```

---

## Instalación

### 1. Clonar el repositorio  
```bash
git clone https://github.com/Zurickata/MeshStep.git
cd MeshStep
```

> Esto descargará el proyecto y sus submódulos internos.

---

### 2. Configurar el entorno y compilar  
Ejecuta el script de configuración (asegúrate de tener permisos de ejecución):
```bash
chmod +x setup.sh
./setup.sh
```

Este script realizará automáticamente:
- La verificación de dependencias del sistema.  
- La compilación de los algoritmos **Quadtree** y **Octree**.  
- La creación del entorno virtual Python (`venv`).  
- La instalación de todas las librerías necesarias desde `requirements.txt`.

---

### 3. Activar el entorno virtual  
Cada vez que abras una nueva sesión de terminal:
```bash
source venv/bin/activate
```

---

### 4. Ejecutar MeshStep  
Una vez dentro del entorno virtual:
```bash
python -m app.main
```

---

## Recompilación manual (si es necesario)
Si modificas los algoritmos o deseas recompilar desde cero:
```bash
./setup.sh
```

---

## Solución a errores comunes

### Error Qt: `Could not load the Qt platform plugin "xcb"`
Instala las librerías requeridas:
```bash
sudo apt install -y libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxkbcommon-x11-0 libxcb-xkb1 libxcb-xinput0
```

Si el error persiste, asegúrate de tener también:
```bash
sudo apt install -y libx11-xcb1 libxcb-glx0 libxcb-shm0 libxcb-sync1 libxcb-xfixes0 libxcb-shape0 libxcb-randr0 libxcb-util1 libxrender1 libxi6
```

---

## Ejecución rápida (resumen)

```bash
git clone https://github.com/Zurickata/MeshStep.git
cd MeshStep
chmod +x setup.sh && ./setup.sh
source venv/bin/activate
python -m app.main
```

---

## Equipo de desarrollo
Proyecto desarrollado en el marco de la **Feria de Software USM 2025**  
por estudiantes de la **Universidad Técnica Federico Santa María**.
