import subprocess
import os
from pathlib import Path

class QuadtreeWrapper:
    def __init__(self):
        self.quadtree_dir = Path(__file__).parent / "quadtree"
        self.binary_path = self.quadtree_dir / "build" / "mesher_roi"
        self.outputs_dir = Path(__file__).parent.parent / "outputs"

        # Crear directorio outputs si no existe
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

        if not self.binary_path.exists():
            raise FileNotFoundError(
                "Ejecutable no encontrado. Ejecuta './setup.sh' primero."
            )

    def generate_mesh(self, input_file, output_file="output", refinement_level=5, show_quality_metrics=False):
        """
        Genera una malla y devuelve la ruta del archivo VTK.
        
        Args:
            input_file: Nombre del archivo de entrada (debe estar en core/quadtree/data)
            output_file: Nombre base del archivo de salida (sin extensión)
            refinement_level: Nivel de refinamiento (1-10)
            show_quality_metrics: Si True, muestra métricas de calidad (-q)
        """
        try:
            # Convertimos a rutas absolutas
            abs_input = str((self.quadtree_dir / "data" / Path(input_file).name).resolve())
            abs_output = str((self.outputs_dir / output_file).resolve())
            
            # Creamos el comando base
            command = [
                str(self.binary_path),
                "-p", abs_input,
                "-s", str(refinement_level),
                "-v",
                "-u", abs_output
            ]
            
            # Añadimos -q si show_quality_metrics es True
            if show_quality_metrics:
                command.insert(5, "-q")  
            
            # Creamos el entorno de ejecución
            env = os.environ.copy()
            env["LD_LIBRARY_PATH"] = f"/usr/lib/x86_64-linux-gnu:{env.get('LD_LIBRARY_PATH', '')}"
            
            # Ejecutamos desde el directorio build
            result = subprocess.run(
                command,
                cwd=str(self.quadtree_dir / "build"),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            
            print(result.stdout)
            return abs_output + ".vtk"
            
        except subprocess.CalledProcessError as e:
            error_msg = f"""
            Error al ejecutar el mesher:
            Comando: {' '.join(e.cmd)}
            Código: {e.returncode}
            Salida: {e.stdout}
            Error: {e.stderr}
            """
            print(error_msg)
            
            if e.returncode == -11:
                print("⚠️ Error de segmentación - Verifica:")
                print("1. Permisos del ejecutable: ls -la", self.binary_path)
                print("2. Dependencias: ldd", self.binary_path)
            
            raise RuntimeError("Falló la generación de malla") from e