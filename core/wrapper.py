import subprocess
from pathlib import Path

class QuadtreeWrapper:
    def __init__(self):
        self.binary_path = self._compile_quadtree()

    def _compile_quadtree(self):
        """Compila el algoritmo al primer uso."""
        quadtree_dir = Path(__file__).parent / "quadtree"
        build_dir = quadtree_dir / "build"
        
        if not (build_dir / "mesher_roi").exists():
            subprocess.run(["cmake", "../src"], cwd=build_dir, check=True)
            subprocess.run(["make"], cwd=build_dir, check=True)
        
        return build_dir / "mesher_roi"

    def generate_mesh(self, input_file, output_file="output.vtk", refinement_level=5):
        """Genera una malla y devuelve la ruta del archivo VTK."""
        subprocess.run([
            str(self.binary_path),
            "-p", str(input_file),
            "-s", str(refinement_level),
            "-v", "-u", str(output_file[:-4])  # Remove .vtk extension
        ], check=True)
        return Path(output_file).absolute()