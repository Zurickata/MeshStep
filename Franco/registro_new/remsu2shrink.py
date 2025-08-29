import numpy as np

def leer_puntos_vtk_numpy(path):
    """
    Lee los puntos de un archivo VTK ASCII y devuelve un array Nx3 con float64
    """
    with open(path, 'r') as f:
        lines = f.readlines()

    puntos = []
    start = False
    for line in lines:
        if line.strip().startswith("POINTS"):
            start = True
            continue
        if start:
            if line.strip() == "":
                break
            puntos.extend([float(v) for v in line.strip().split()])

    puntos = np.array(puntos).reshape(-1, 3)
    return puntos

def generar_movimientos_numpy(vtk_old, vtk_new, salida_txt, tol=1e-12):
    puntos_old = leer_puntos_vtk_numpy(vtk_old)
    puntos_new = leer_puntos_vtk_numpy(vtk_new)

    if puntos_old.shape != puntos_new.shape:
        raise ValueError("Los archivos VTK no tienen la misma cantidad de puntos")

    # Detectar puntos que cambiaron
    diff = np.abs(puntos_old - puntos_new)
    cambios = np.any(diff > tol, axis=1)

    with open(salida_txt, 'w') as f:
        for i, moved in enumerate(cambios):
            if moved:
                x, y, z = puntos_new[i]
                f.write(f"mov {i} {x:+0.8E} {y:+0.8E} {z:+0.8E}\n")

# Ejemplo de uso
vtk1 = "a_output_3_remSur.vtk"
vtk2 = "a_output_3_shrink.vtk"
salida = "movimientos3_new.txt"

generar_movimientos_numpy(vtk1, vtk2, salida)
print(f"Archivo de movimientos generado: {salida}")
