import subprocess
import os
import re
from pathlib import Path

class BaseWrapper:
    def __init__(self, algo_name: str, input_flag: str):
        """
        Inicializa el wrapper para un algoritmo de mallado.
        
        Args:
            algo_name: "quadtree" o "octree"
            input_flag: el flag a usar para el input ("-p" o "-d")
        """
        self.algo_name = algo_name
        self.input_flag = input_flag
        self.algo_dir = Path(__file__).parent / algo_name
        self.binary_path = self.algo_dir / "build" / "mesher_roi"
        self.outputs_dir = Path(__file__).parent.parent / "outputs"

        # Crear directorio outputs si no existe
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

        if not self.binary_path.exists():
            raise FileNotFoundError(
                f"Ejecutable de {algo_name} no encontrado. Ejecuta './setup.sh' primero."
            )

    def generate_mesh(self, input_file, output_file="output",
                      refinement_level=5, refinement_type="-s",
                      show_quality_metrics=False):
        """
        Genera una malla y devuelve la ruta del archivo VTK.
        """
        try:
            abs_input = str(Path(input_file).resolve())
            abs_output = str((self.outputs_dir / f"{self.algo_name}_{output_file}").resolve())

            # 🚩 Aquí usamos el flag dinámico (puede ser -p o -d)
            command = [
                str(self.binary_path),
                self.input_flag, abs_input,
                refinement_type, str(refinement_level),
                "-v",
                "-u", abs_output
            ]

            if show_quality_metrics:
                command.insert(5, "-q")

            env = os.environ.copy()
            env["LD_LIBRARY_PATH"] = f"/usr/lib/x86_64-linux-gnu:{env.get('LD_LIBRARY_PATH', '')}"

            result = subprocess.run(
                command,
                cwd=str(self.algo_dir / "build"),
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
            Error al ejecutar el mesher ({self.algo_name}):
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

            raise RuntimeError(f"Falló la generación de malla con {self.algo_name}") from e


# Wrappers específicos
class QuadtreeWrapper(BaseWrapper):
    def __init__(self):
        super().__init__("quadtree", "-p")


class OctreeWrapper(BaseWrapper):
    def __init__(self):
        super().__init__("octree", "-d")

# --- Jeans Wrapper (Métricas de calidad 3D) ---
class JeansWrapper:
    """
    Ejecuta el binario 'jeans' para obtener métricas de calidad 3D.
    Soporta flags -s (estadísticas) y -j (lista de Jens por elemento).
    """

    def __init__(self):
        self.algo_name = "jeans"
        self.algo_dir = Path(__file__).parent / self.algo_name
        self.binary_path = self.algo_dir / "build" / "jens"
        self.outputs_dir = Path(__file__).parent.parent / "outputs"
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

        if not self.binary_path.exists():
            raise FileNotFoundError(
                f"Ejecutable de {self.algo_name} no encontrado. Ejecuta './setup.sh' primero."
            )

    def run(self, input_file: str, flag: str = "-s", save_output: bool = True) -> str:
        """
        Ejecuta el binario Jeans con el flag indicado (-s o -j).

        Args:
            input_file: ruta al archivo .m3d a analizar
            flag: '-s' para estadísticas o '-j' para valores por elemento
            save_output: si True, guarda el resultado en outputs/

        Returns:
            stdout completo como string
        """
        abs_input = str(Path(input_file).resolve())

        if not Path(abs_input).exists():
            raise FileNotFoundError(f"No se encontró el archivo de entrada: {abs_input}")

        if flag not in ["-s", "-j"]:
            raise ValueError(f"Flag '{flag}' no soportado. Usa '-s' o '-j'.")

        command = [str(self.binary_path), flag, abs_input]

        try:
            result = subprocess.run(
                command,
                cwd=str(self.algo_dir / "build"),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            output = result.stdout

            if save_output:
                out_name = f"{Path(abs_input).stem}_jeans{flag}.txt".replace("-", "")
                out_path = self.outputs_dir / out_name
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(output)
                print(f"📄 Resultado guardado en {out_path}")

            return output

        except subprocess.CalledProcessError as e:
            print(f"❌ Error al ejecutar Jeans con {flag}")
            print("Comando:", " ".join(e.cmd))
            print("Salida:", e.stdout)
            print("Error:", e.stderr)
            raise RuntimeError("Falló la ejecución de Jeans") from e

def parse_jeans_output(output: str) -> dict:
    """
    Parsea la salida de Jeans (-s o -j) y devuelve un diccionario estructurado.
    """
    data = {"histogram": [], "by_type": {}, "values": []}

    # Patrón de pares TikZ
    tikz_re = re.compile(r"\(([-\d\.]+),\s*([-\d\.]+)\)")
    # Patrón por tipo de elemento
    type_re = re.compile(
        r"\[\s*([-\d\.]+),([-\d\.]+)\]\s+average:\s*([-\d\.]+)\s+\((\d+)\)"
    )

    # General
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("negative:"):
            data["negative"] = int(line.split(":")[1].strip())
        elif line.startswith("total:"):
            data["total"] = int(line.split(":")[1].strip())
        elif line.startswith("worst quality"):
            data["worst_quality"] = float(line.split()[-1])
        elif line.startswith("average quality"):
            data["average_quality"] = float(line.split()[-1])

        # Histogram (tikz format)
        elif tikz_re.match(line):
            m = tikz_re.match(line)
            data["histogram"].append((float(m.group(1)), float(m.group(2))))

        # Quality per element type
        elif type_re.match(line):
            tnames = ["Hex", "Pri", "Pyr", "Tet"]
            if "by_type" not in data:
                data["by_type"] = {}
            matches = type_re.match(line)
            idx = len(data["by_type"])
            if idx < len(tnames):
                data["by_type"][tnames[idx]] = {
                    "min": float(matches.group(1)),
                    "max": float(matches.group(2)),
                    "avg": float(matches.group(3)),
                    "count": int(matches.group(4)),
                }

        # Valores por elemento (flag -j)
        elif re.fullmatch(r"[0-9eE\.\+\-]+", line):
            try:
                val = float(line)
                data["values"].append(val)
            except ValueError:
                pass

    return data