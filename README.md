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
