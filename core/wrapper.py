import subprocess
from pathlib import Path

class QuadtreeWrapper:
    def __init__(self):
        self.binary_path = Path(__file__).parent / "quadtree" / "build" / "mesher_roi"
        if not self.binary_path.exists():
            raise FileNotFoundError(
                "Ejecutable no encontrado. Ejecuta './setup.sh' primero."
            )

    def generate_mesh(self, input_file, output_file="/core/outputs/output", refinement_level=5):
        """Genera una malla y devuelve la ruta del archivo VTK."""
        subprocess.run([
            str(self.binary_path),
            "-p", str(input_file),
            "-s", str(refinement_level),
            "-v", "-u", str(output_file)
        ], check=True)
        return Path(output_file)