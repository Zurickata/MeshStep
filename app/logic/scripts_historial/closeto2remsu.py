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
    return cells

def generar_historial_caras_numpy(vtk_old, vtk_new, salida_txt):
    # Leer celdas
    celdas_old = leer_celdas_vtk_numpy(vtk_old)
    celdas_new = leer_celdas_vtk_numpy(vtk_new)

    set_new = set(tuple(face) for face in celdas_new)
    indices_del = [i for i, face in enumerate(celdas_old) if tuple(face) not in set_new][::-1]

    with open(salida_txt, 'w') as f:
        if indices_del:
            lines = [
                f"del_face {i} {' '.join(map(str, celdas_old[i]))}"
                for i in indices_del
            ]
            f.write('\n'.join(lines) + '\n')
        else:
            f.write('')
