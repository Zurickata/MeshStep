#!/usr/bin/env python3
import sys
import os
import vtk
import numpy as np

# -----------------------------
# Leer un archivo VTK
# -----------------------------
def read_vtk(filename):
    print(f"\n📂 Leyendo VTK: {filename}")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No existe el archivo: {filename}")

    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    ugrid = reader.GetOutput()

    npts = ugrid.GetNumberOfPoints()
    ncells = ugrid.GetNumberOfCells()
    print(f" - {npts} puntos, {ncells} celdas leídas")

    pts = np.array([ugrid.GetPoint(i) for i in range(npts)])

    cells = []
    for i in range(ncells):
        cell = ugrid.GetCell(i)
        if cell and cell.GetCellType() == vtk.VTK_HEXAHEDRON:
            cells.append([cell.GetPointId(j) for j in range(8)])

    print(f" - {len(cells)} hexahedros detectados")
    return pts, cells

# -----------------------------
# Guardar un archivo VTK
# -----------------------------
def save_vtk(filename, points, cells):
    print(f"💾 Guardando archivo: {filename}")
    os.makedirs(os.path.dirname(os.path.abspath(filename)) or ".", exist_ok=True)

    pts_vtk = vtk.vtkPoints()
    for p in points:
        pts_vtk.InsertNextPoint(*p)

    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(pts_vtk)

    for cell in cells:
        hex_cell = vtk.vtkHexahedron()
        for i, v in enumerate(cell):
            hex_cell.GetPointIds().SetId(i, v)
        ugrid.InsertNextCell(hex_cell.GetCellType(), hex_cell.GetPointIds())

    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(ugrid)
    writer.SetFileTypeToASCII()
    writer.Write()
    print("✅ Guardado exitoso\n")

# -----------------------------
# Subdivisión de una celda hexaédrica
# -----------------------------
def subdivide_hexa(points, cell):
    p = points[cell]
    v = [p[i] for i in range(8)]
    c = p.mean(axis=0)

    edge_pairs = [(0,1),(1,2),(2,3),(3,0),
                  (4,5),(5,6),(6,7),(7,4),
                  (0,4),(1,5),(2,6),(3,7)]
    e = [(p[i]+p[j])/2 for i,j in edge_pairs]

    face_quads = [(0,1,2,3),(4,5,6,7),
                  (0,1,5,4),(1,2,6,5),
                  (2,3,7,6),(0,3,7,4)]
    f = [p[list(ids)].mean(axis=0) for ids in face_quads]

    all_pts = np.vstack([v, e, f, c])

    V = list(range(0,8))
    E = list(range(8,20))
    F = list(range(20,26))
    C = 26

    sub_cells = [
        [V[0], E[0], F[0], E[3], E[8], F[2], C, F[5]],
        [E[0], V[1], E[1], F[0], F[2], E[9], F[3], C],
        [F[0], E[1], V[2], E[2], C, F[3], E[10], F[4]],
        [E[3], F[0], E[2], V[3], F[5], C, F[4], E[11]],
        [E[8], F[2], C, F[5], V[4], E[4], F[1], E[7]],
        [F[2], E[9], F[3], C, E[4], V[5], E[5], F[1]],
        [C, F[3], E[10], F[4], F[1], E[5], V[6], E[6]],
        [F[5], C, F[4], E[11], E[7], F[1], E[6], V[7]],
    ]
    return all_pts, sub_cells

# -----------------------------
# Refinamiento octree recursivo (una sola pasada)
# -----------------------------
def octree_refine(points, cells):
    new_pts_list = []
    new_cells_list = []
    pt_map = {}
    pt_count = 0

    for cell in cells:
        all_pts, sub_cells = subdivide_hexa(points, cell)
        idx_map = []
        for pt in all_pts:
            key = tuple(np.round(pt, 8))
            if key in pt_map:
                idx_map.append(pt_map[key])
            else:
                idx_map.append(pt_count)
                pt_map[key] = pt_count
                new_pts_list.append(pt)
                pt_count += 1

        for sc in sub_cells:
            new_cells_list.append([idx_map[i] for i in sc])

    new_points = np.array(new_pts_list)
    print(f" - Refinado -> {len(new_points)} puntos, {len(new_cells_list)} celdas")
    return new_points, new_cells_list

# -----------------------------
# Filtro por superficie
# -----------------------------
def load_ref_surface(ref_file):
    print(f"🌐 Cargando superficie de referencia: {ref_file}")
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(ref_file)
    reader.Update()
    ugrid = reader.GetOutput()

    surface = vtk.vtkGeometryFilter()
    surface.SetInputData(ugrid)
    surface.Update()
    poly = surface.GetOutput()
    print(f" - Superficie: {poly.GetNumberOfPoints()} puntos, {poly.GetNumberOfCells()} celdas")
    return poly

def filter_hexes(points, cells, ref_poly):
    print("🧩 Filtrando celdas dentro de la superficie...")
    select = vtk.vtkSelectEnclosedPoints()
    pts = vtk.vtkPoints()
    for p in points:
        pts.InsertNextPoint(*p)
    poly_pts = vtk.vtkPolyData()
    poly_pts.SetPoints(pts)

    select.SetInputData(poly_pts)
    select.SetSurfaceData(ref_poly)
    select.Update()

    kept_cells = []
    for cell in cells:
        centroid = np.mean(points[cell], axis=0)
        if select.IsInsideSurface(*centroid):
            kept_cells.append(cell)

    print(f" - {len(kept_cells)} celdas conservadas de {len(cells)}")
    return kept_cells

# -----------------------------
# Subdividir con filtrado en cada nivel
# -----------------------------
def subdividir_completo(name, nivel_refinamiento, input_dir=".", ref_vtk=None):
    base_grid = os.path.join(input_dir, f"{name}_grid.vtk")
    print(f"\n🚀 Iniciando subdivisión completa para '{name}'")
    print(f"📁 Directorio de entrada: {input_dir}")
    print(f"🔹 Archivo base: {base_grid}")

    if not os.path.exists(base_grid):
        raise FileNotFoundError(f"No existe el archivo base: {base_grid}")

    pts, cells = read_vtk(base_grid)

    # Cargar referencia si existe
    ref_poly = None
    if ref_vtk is not None:
        ref_path = os.path.join(input_dir, ref_vtk) if not os.path.isabs(ref_vtk) else ref_vtk
        if os.path.exists(ref_path):
            ref_poly = load_ref_surface(ref_path)
        else:
            print(f"⚠️ No se encontró la referencia {ref_vtk}, se omite filtrado")

    # Subdividir + filtrar en cada paso
    for lvl in range(1, nivel_refinamiento + 1):
        print(f"\n🔸 Nivel {lvl} de {nivel_refinamiento}")
        pts, cells = octree_refine(pts, cells)

        if ref_poly is not None:
            cells = filter_hexes(pts, cells, ref_poly)

        out_file = os.path.join(input_dir, f"{name}_{lvl}_subdividida.vtk")
        save_vtk(out_file, pts, cells)

    print("🏁 Subdivisión completa terminada\n")

# -----------------------------
# Main CLI
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--completo":
        if len(sys.argv) < 4:
            print("Uso: python subdivider_hex_simple.py --completo name nivel [input_dir] [quads_ref.vtk]")
            sys.exit(1)

        name = sys.argv[2]
        nivel = int(sys.argv[3])
        input_dir = sys.argv[4] if len(sys.argv) > 4 else "."
        ref_vtk = sys.argv[5] if len(sys.argv) > 5 else None

        subdividir_completo(name, nivel, input_dir, ref_vtk)
        sys.exit(0)

    print("Uso directo: python subdivider_hex_simple.py --completo name nivel [input_dir] [quads_ref.vtk]")
