# MeshStep

## PreRequisito
- Ejecutar en Terminal Linux
- Tener instalado Python 3.1 <, junto con el pip y el python3.12-venv (Para crear los entornos virtuales)
    - Si no tiene ninguna de estas 2 últimas:
    - Instalar pip:
        ```bash
        sudo apt install python3-pip
    - Instalar python3.12-venv:
        ```bash
        sudo apt install python3.12-venv

- Tener instalado Cmake 3.22.1 
    - Si no se tiene instalado Cmake ejecutar "sudo apt install cmake # version 3.22.1-1ubuntu1.22.04.2"

## Instalación

1. Clona el repositorio:
    ```bash
   git clone https://github.com/Zurickata/MeshStep.git
   cd MeshStep

2. Ejecutar el script de configuración:
    ```bash
   ./setup.sh
    
- En caso de que no se pueda correr por permisos, ejecutar:
    ```bash
    chmod +x setup.sh && ./setup.sh

- Si necesita recompilar, elimina la carpeta build y compila nuevamente:
    ```bash
    rm -rf core/quadtree/build
    ./setup.sh

3. Volver a levantar el entorno virtual
    ```bash
    source venv/bin/activate

4. Ahora puedes ejecutar la aplicación:
    ```bash
    python -m app.main



En Caso de error con libreria QT, algo como esto:
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: xcb.

error: exception occurred: Subprocess aborted


Intente lo siguiente:
    ```bash
        sudo apt update
        sudo apt install libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxkbcommon-x11-0 libxcb-xkb1

    ```bash
            sudo apt install libx11-xcb1 libxcb1 libxcb-glx0 libxcb-keysyms1 libxcb-image0 \
            libxcb-shm0 libxcb-icccm4 libxcb-sync1 libxcb-xfixes0 libxcb-shape0 libxcb-randr0 \
            libxcb-render-util0 libxcb-xinerama0 libxcb-util1 libxcb-cursor0 libxkbcommon-x11-0 \
            libxrender1 libxi6

y si sigue fallando:

    ```bash
        sudo apt install libxcb-xinput0