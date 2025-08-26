import numpy as np

def leer_puntos_vtk(path):
    puntos = []
    with open(path,'r') as f:
        lines = f.readlines()
    start = False
    for line in lines:
        if line.strip().startswith("POINTS"):
            start = True
            continue
        if start:
            if line.strip() == "" or line.strip().startswith("CELLS"):
                break
            puntos.extend([float(v) for v in line.strip().split()])
    return np.array(puntos).reshape(-1,3)

def leer_celdas_vtk(path):
    celdas = []
    with open(path,'r') as f:
        lines = f.readlines()
    start = False
    for line in lines:
        if line.strip().startswith("CELLS"):
            start = True
            continue
        if start:
            if line.strip() == "" or line.strip().startswith("CELL_TYPES"):
                break
            vals = [int(v) for v in line.strip().split()]
            if len(vals) > 1:
                nverts = vals[0]
                celdas.append(vals[1:1+nverts])
    return celdas   # <<< cambio aquí


def generar_historial(vtk_old, vtk_new, salida_txt, tol=1e-12):
    pts_old = leer_puntos_vtk(vtk_old)
    pts_new = leer_puntos_vtk(vtk_new)
    
    celdas_old = leer_celdas_vtk(vtk_old)
    celdas_new = leer_celdas_vtk(vtk_new)
    
    set_new_pts = set(map(tuple, pts_new))
    historial = []

    # Historial de caras eliminadas
    set_new_faces = set(tuple(sorted(c)) for c in celdas_new)
    for i, c in enumerate(celdas_old):
        if tuple(sorted(c)) not in set_new_faces:
            historial.append(f"del_face {i} {' '.join(map(str,c))}")
    
    # Historial de puntos eliminados
    for i, pt in enumerate(pts_old):
        if not any(np.allclose(pt, p, atol=tol) for p in pts_new):
            historial.append(f"del_pt {i}")
        else:
            # Puntos que cambiaron
            idx_new = [j for j,p in enumerate(pts_new) if np.allclose(pt,p,atol=tol)][0]
            if not np.allclose(pt, pts_new[idx_new], atol=tol):
                x,y,z = pts_new[idx_new]
                historial.append(f"mov {i} {x:+0.8E} {y:+0.8E} {z:+0.8E}")

    with open(salida_txt,'w') as f:
        for line in historial:
            f.write(line+'\n')

# Uso
vtk_old = "a_output_3_shrink.vtk"
vtk_new = "a_output_3.vtk"
salida = "historial_completo.txt"

generar_historial(vtk_old, vtk_new, salida)
print(f"Archivo de historial generado: {salida}")
