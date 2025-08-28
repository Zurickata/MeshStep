import numpy as np

def leer_celdas_vtk_numpy(path):
    """
    Lee las celdas (caras) de un VTK ASCII y devuelve un array de arrays
    donde cada sub-array contiene los IDs de los puntos de la celda.
    """
    with open(path, 'r') as f:
        lines = f.readlines()

    cells = []
    start = False
    for line in lines:
        if line.strip().startswith("CELLS"):
            start = True
            continue
        if start:
            if line.strip() == "":
                break
            vals = [int(v) for v in line.strip().split()]
            if len(vals) > 1:
                nverts = vals[0]
                cells.append(vals[1:1+nverts])
    return np.array(cells, dtype=int)

def generar_historial_caras_numpy(vtk_old, vtk_new, salida_txt):
    # Leer celdas
    celdas_old = leer_celdas_vtk_numpy(vtk_old)
    celdas_new = leer_celdas_vtk_numpy(vtk_new)

    # Convertir a sets de tuplas ordenadas para comparar rápido
    set_old = set(tuple(sorted(c)) for c in celdas_old)
    set_new = set(tuple(sorted(c)) for c in celdas_new)

    # Caras borradas
    borradas = set_old - set_new

    with open(salida_txt, 'w') as f:
        for i, c in enumerate(borradas, start=1):
            f.write(f"del {i} {' '.join(map(str, c))}\n")

# ---------------------
# Ejemplo de uso
# ---------------------
vtk1 = "a_output_3_closeto.vtk"
vtk2 = "a_output_3_remSur.vtk"
salida = "historial_caras.txt"

generar_historial_caras_numpy(vtk1, vtk2, salida)
print(f"Archivo de historial de caras generado: {salida}")
