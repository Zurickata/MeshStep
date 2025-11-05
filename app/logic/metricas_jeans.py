import os
import re
import subprocess
import vtk


def convertir_vtk_a_m3d(vtk_path: str, m3d_path: str):
    """
    Convierte un archivo .vtk a .m3d con el formato esperado por el binario Jeans.

    Formato de salida:
    [Nodes, ARRAY1<STRING>]
    <n_nodos>
    1 x y z
    ...
    [Elements, ARRAY1<STRING>]
    <n_elementos>
    <Tipo> n1 n2 ... nN 1000.0 0.45 1.0
    """

    print(f"[CONVERT] Iniciando conversión de {os.path.basename(vtk_path)} → {os.path.basename(m3d_path)}")

    if not os.path.exists(vtk_path):
        print(f"[CONVERT] ❌ No se encontró el archivo {vtk_path}")
        return False

    try:
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(vtk_path)
        reader.Update()

        grid = reader.GetOutput()
        num_points = grid.GetNumberOfPoints()
        num_cells = grid.GetNumberOfCells()

        if num_points == 0 or num_cells == 0:
            print(f"[CONVERT] ❌ El archivo {vtk_path} no contiene puntos o celdas válidas.")
            return False

        with open(m3d_path, "w") as f:
            # --- Encabezado de nodos ---
            f.write("[Nodes, ARRAY1<STRING>]\n")
            f.write(f"{num_points}\n\n")

            for i in range(num_points):
                x, y, z = grid.GetPoint(i)
                f.write(f"1 {x:+.8E} {y:+.8E} {z:+.8E}\n")

            f.write("\n[Elements, ARRAY1<STRING>]\n")
            f.write(f"{num_cells}\n\n")

            tipo_m3d = {
                10: "T",  # Tetrahedron
                12: "H",  # Hexahedron
                13: "R",  # Wedge (Prisma)
                14: "P",  # Pyramid
            }

            skip_count = 0

            for i in range(num_cells):
                cell = grid.GetCell(i)
                cell_type = grid.GetCellType(i)

                if cell_type not in tipo_m3d:
                    skip_count += 1
                    continue

                letra = tipo_m3d[cell_type]
                ids = cell.GetPointIds()
                npts = ids.GetNumberOfIds()
                indices = [str(ids.GetId(j)) for j in range(npts)]  # ✅ iteración correcta
                f.write(f"{letra} {' '.join(indices)} 1000.0 0.45 1.0\n")

            if skip_count > 0:
                print(f"[CONVERT] ⚠️ Se omitieron {skip_count} celdas de tipo no soportado.")

        print(f"[CONVERT] ✅ Conversión completada → {os.path.basename(m3d_path)}")
        return True

    except Exception as e:
        print(f"[CONVERT] ❌ Error durante la conversión: {e}")
        return False


def ejecutar_jeans(m3d_path: str, jeans_bin_path: str, modo: str = "-s"):
    """
    Ejecuta el binario jeans con el modo especificado (-s o -j).
    Devuelve la salida de la ejecución o None si hay error.
    """
    if not os.path.exists(m3d_path):
        print(f"[JEANS] ❌ No existe {m3d_path}, no se puede ejecutar Jeans.")
        return None

    if not os.path.exists(jeans_bin_path):
        print(f"[JEANS] ❌ No se encontró el binario Jeans en {jeans_bin_path}")
        return None

    cmd = [jeans_bin_path, modo, m3d_path]
    print(f"[JEANS] Ejecutando métricas globales ({modo})...")

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        salida = result.stdout.strip()
        if salida:
            print(f"[JEANS] ✅ Métricas obtenidas correctamente.")
        else:
            print(f"[JEANS] ⚠️ No se recibió salida del binario Jeans.")

        return salida

    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar Jeans con {modo}")
        print(f"Comando: {' '.join(e.cmd)}")
        print(f"Salida:\n{e.stdout}")
        print(f"Error:\n{e.stderr}")
        return None

    except Exception as e:
        print(f"[JEANS] ❌ Error inesperado al generar métricas: {e}")
        return None


def generar_metricas_jeans(vtk_file: str, jeans_bin_path: str, output_dir: str):
    """
    Convierte un archivo .vtk a .m3d (si es necesario) y ejecuta las métricas Jeans.
    Genera archivos .txt con las salidas -s y -j.
    """
    base_name = os.path.splitext(os.path.basename(vtk_file))[0]
    m3d_file = os.path.join(output_dir, f"{base_name}.m3d")
    jeans_s_output = os.path.join(output_dir, f"{base_name}_jeanss.txt")
    jeans_j_output = os.path.join(output_dir, f"{base_name}_jeansj.txt")

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(m3d_file):
        print(f"[JEANS] ⚙️ No existe {base_name}.m3d, intentando generar desde {base_name}.vtk...")
        ok = convertir_vtk_a_m3d(vtk_file, m3d_file)
        if not ok:
            print("[JEANS] ❌ No se pudo generar el archivo .m3d, se omiten métricas.")
            return False

    for modo, salida in [("-s", jeans_s_output), ("-j", jeans_j_output)]:
        resultado = ejecutar_jeans(m3d_file, jeans_bin_path, modo)
        if resultado is not None:
            with open(salida, "w") as f:
                f.write(resultado)
            print(f"📄 Resultado guardado en {salida}")
        else:
            print(f"[JEANS] ⚠️ No se pudo generar métricas para modo {modo}")

    return True

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