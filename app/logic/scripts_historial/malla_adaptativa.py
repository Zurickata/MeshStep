import vtk
import os
import numpy as np

# -----------------------------
# Utilidades VTK
# -----------------------------
def leer_vtk(filename):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def guardar_vtk(ugrid, filename):
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(ugrid)
    writer.Write()

# -----------------------------
# Geometría
# -----------------------------
def subdividir_quad(quad):
    """Divide un quad [p0, p1, p2, p3] en 4 hijos"""
    p0, p1, p2, p3 = quad
    m01 = 0.5 * (p0 + p1)
    m12 = 0.5 * (p1 + p2)
    m23 = 0.5 * (p2 + p3)
    m30 = 0.5 * (p3 + p0)
    c   = 0.25 * (p0 + p1 + p2 + p3)
    return [
        [p0, m01, c, m30],
        [m01, p1, m12, c],
        [c, m12, p2, m23],
        [m30, c, m23, p3]
    ]

def punto_en_lista(p, puntos, tol=1e-6):
    """Chequea si p está en la nube de puntos (con tolerancia)"""
    return any(np.linalg.norm(p - q) < tol for q in puntos)

def quad_en_squad(quad, squad_points, tol=1e-6):
    """Un quad es válido si sus 4 vértices están en squad_points"""
    return all(punto_en_lista(p, squad_points, tol) for p in quad)

# -----------------------------
# Recursivo con backtracking
# -----------------------------
def refinar_quad(quad, squad_points, nivel, nivel_max, caras_congeladas, path="root"):
    if nivel == nivel_max:
        caras_congeladas.append(quad)
        print(f"[{path}] Nivel max alcanzado, congelo quad.")
        return [quad]

    if quad_en_squad(quad, squad_points):
        hijos = subdividir_quad(quad)
        hijos_resultado = []
        hijos_congelados = []
        valido = True
        for i, h in enumerate(hijos):
            child_path = f"{path}.{i}"
            if quad_en_squad(h, squad_points):
                res = refinar_quad(h, squad_points, nivel+1, nivel_max, hijos_congelados, child_path)
                hijos_resultado.extend(res)
            else:
                valido = False
                print(f"[{child_path}] ❌ hijo no cumple, invalido subdivisión.")
                break

        if valido:
            print(f"[{path}] ✅ todos los hijos válidos, sustituyo por hijos.")
            caras_congeladas.extend(hijos_congelados)
            return hijos_resultado
        else:
            caras_congeladas.append(quad)
            print(f"[{path}] 🔒 fallback: hijos inválidos, conservo padre.")
            return [quad]

    else:
        hijos = subdividir_quad(quad)
        out = []
        for i, h in enumerate(hijos):
            child_path = f"{path}.{i}"
            out.extend(refinar_quad(h, squad_points, nivel+1, nivel_max, caras_congeladas, child_path))
        return out

# -----------------------------
# Refinamiento adaptativo
# -----------------------------
def refinamiento_adaptativo(malla_file, squad_file, nivel_max=2, output_file="caras_congeladas.vtk"):
    malla = leer_vtk(malla_file)
    squad = leer_vtk(squad_file)

    squad_points = [np.array(squad.GetPoint(i)) for i in range(squad.GetNumberOfPoints())]
    caras_congeladas = []

    for i in range(malla.GetNumberOfCells()):
        cell = malla.GetCell(i)
        if cell.GetNumberOfPoints() != 4:
            continue
        quad = [np.array(malla.GetPoint(cell.GetPointId(k))) for k in range(4)]
        refinar_quad(quad, squad_points, 0, nivel_max, caras_congeladas, path=f"cell{i}")

    # Exportar VTK
    points = vtk.vtkPoints()
    quads_vtk = vtk.vtkCellArray()
    point_map = {}

    for quad in caras_congeladas:
        ids = []
        for p in quad:
            pt = tuple(np.round(p, 6))  # clave con redondeo
            if pt not in point_map:
                pid = points.InsertNextPoint(p.tolist())
                point_map[pt] = pid
            ids.append(point_map[pt])
        vtk_quad = vtk.vtkQuad()
        for j, pid in enumerate(ids):
            vtk_quad.GetPointIds().SetId(j, pid)
        quads_vtk.InsertNextCell(vtk_quad)

    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.SetCells(vtk.VTK_QUAD, quads_vtk)

    guardar_vtk(ugrid, output_file)
    print(f"\n✅ Archivo exportado: {output_file}")

# -----------------------------
# MAIN
# -----------------------------

# def malla_adaptativa_completa(name,nivel_refinamiento):
#     for x in range(nivel_refinamiento):
#         refinamiento_adaptativo(
#         f"{name}_grid.vtk",  #Malla base (grid)
#         f"{name}_quads.vtk", #Malla quads del nivel
#         nivel_max=x,
#         output_file=f"{name}_{x+1}_borde_caras.vtk"
#     )

def malla_adaptativa_completa(name, nivel_refinamiento, input_dir="."):
    # Construimos las rutas completas de los archivos de entrada
    grid_file = os.path.join(input_dir, f"{name}_grid.vtk")
    quads_file = os.path.join(input_dir, f"{name}_quads.vtk")

    for x in range(nivel_refinamiento):
        refinamiento_adaptativo(
            grid_file,
            quads_file,
            nivel_max=x,
            output_file=f"{name}_{x+1}_borde_caras.vtk"
        )

# malla_adaptativa_completa("a_debug_5", 5, "../outputs")
