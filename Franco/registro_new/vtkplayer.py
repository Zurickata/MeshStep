import vtk
import numpy as np
import os

# ------------------------------
# FUNCIONES DE MANIPULACIÓN
# ------------------------------
def mover_vertice(ugrid, vid, new_pos):
    pts = ugrid.GetPoints()
    if vid < 0 or vid >= pts.GetNumberOfPoints():
        print(f"[WARN] mov: vid {vid} fuera de rango.")
        return ugrid
    pts.SetPoint(vid, new_pos)
    pts.Modified()
    ugrid.Modified()
    return ugrid

def borrar_caras(ugrid, caras_a_borrar):
    """
    Elimina caras (celdas) de un vtkUnstructuredGrid sin eliminar puntos.
    
    ugrid : vtkUnstructuredGrid
        Malla original
    caras_a_borrar : list[int]
        Lista de IDs de las celdas que se deben borrar
    """
    # Crear nuevas celdas
    nuevas_celdas = vtk.vtkCellArray()
    tipos = vtk.vtkUnsignedCharArray()
    tipos.SetNumberOfComponents(1)
    tipos.SetName("types")

    # Copiar solo las caras que no están en la lista
    for i in range(ugrid.GetNumberOfCells()):
        if i in caras_a_borrar:
            continue

        cell = ugrid.GetCell(i)
        point_ids = cell.GetPointIds()

        nuevas_celdas.InsertNextCell(point_ids.GetNumberOfIds())
        for j in range(point_ids.GetNumberOfIds()):
            nuevas_celdas.InsertCellPoint(point_ids.GetId(j))

        tipos.InsertNextValue(ugrid.GetCellType(i))

    # Crear nuevo grid con mismos puntos pero celdas filtradas
    nuevo_grid = vtk.vtkUnstructuredGrid()
    nuevo_grid.SetPoints(ugrid.GetPoints())
    nuevo_grid.SetCells(tipos, nuevas_celdas)

    return nuevo_grid

def borrar_vertices(ugrid, vids_a_borrar):
    # Borra TODAS las celdas que toquen cualquiera de esos vértices
    ncells = ugrid.GetNumberOfCells()
    cids = []
    vids_set = set(vids_a_borrar)
    for cid in range(ncells):
        cell = ugrid.GetCell(cid)
        for i in range(cell.GetNumberOfPoints()):
            if cell.GetPointId(i) in vids_set:
                cids.append(cid)
                break
    return borrar_caras(ugrid, cids)


def change_model(name):
    # Caso 1: modelos predefinidos
    if name.lower() == "cube":
        cube = vtk.vtkCubeSource()
        cube.Update()
        ugrid = vtk.vtkUnstructuredGrid()
        ugrid.DeepCopy(cube.GetOutput())
        return ugrid

    elif name.lower() == "sphere":
        sphere = vtk.vtkSphereSource()
        sphere.SetThetaResolution(12)
        sphere.SetPhiResolution(12)
        sphere.Update()
        ugrid = vtk.vtkUnstructuredGrid()
        ugrid.DeepCopy(sphere.GetOutput())
        return ugrid

    # Caso 2: archivo .vtk
    if os.path.isfile(name):
        print(f"[INFO] change_model: cargando archivo '{name}'")
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(name)
        reader.Update()
        ugrid = vtk.vtkUnstructuredGrid()
        ugrid.DeepCopy(reader.GetOutput())
        return ugrid

    raise ValueError(f"[ERROR] change_model: modelo o archivo no encontrado → {name}")



# ------------------------------
# BÚSQUEDA DE CARAS POR VÉRTICES
# ------------------------------
def encontrar_celdas_por_vertices(ugrid, verts):
    """
    Devuelve los IDs de celdas cuyo conjunto de vértices coincide EXACTAMENTE
    con 'verts' (independiente del orden). Útil para quads del script.
    """
    objetivo = set(verts)
    ncells = ugrid.GetNumberOfCells()
    matches = []
    for cid in range(ncells):
        cell = ugrid.GetCell(cid)
        n = cell.GetNumberOfPoints()
        if n != len(objetivo):
            continue
        ids = {cell.GetPointId(i) for i in range(n)}
        if ids == objetivo:
            matches.append(cid)
    return matches

# ------------------------------
# GUARDADO CLÁSICO ASCII
# ------------------------------
def guardar_ugrid(ugrid, filename, precision=8, puntos_por_linea=2):
    out = []
    out.append("# vtk DataFile Version 3.0\n")
    out.append("VTK file formatted in classic ASCII\n")
    out.append("ASCII\n")
    out.append("DATASET UNSTRUCTURED_GRID\n")

    npoints = ugrid.GetNumberOfPoints()
    out.append(f"POINTS {npoints} float\n")
    for i in range(0, npoints, puntos_por_linea):
        line_coords = []
        for j in range(puntos_por_linea):
            idx = i + j
            if idx >= npoints:
                break
            x, y, z = ugrid.GetPoint(idx)
            line_coords.extend([f"{c:+.{precision}E}" for c in (x, y, z)])
        out.append(" ".join(line_coords) + "\n")

    ncells = ugrid.GetNumberOfCells()
    total_indices = sum(ugrid.GetCell(i).GetNumberOfPoints() + 1 for i in range(ncells))
    out.append(f"CELLS {ncells} {total_indices}\n")
    for i in range(ncells):
        cell = ugrid.GetCell(i)
        ids = [str(cell.GetNumberOfPoints())] + [str(cell.GetPointId(j)) for j in range(cell.GetNumberOfPoints())]
        out.append(" ".join(ids) + "\n")

    out.append(f"CELL_TYPES {ncells}\n")
    for i in range(ncells):
        out.append(str(ugrid.GetCellType(i)) + "\n")

    with open(filename, "w") as f:
        f.writelines(out)

# ------------------------------
# PARSE + EJECUCIÓN DE COMANDOS
# ------------------------------
def parse_line(line):
    # Ignorar comentarios y líneas vacías
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    return s.split()

def ejecutar_comando(ugrid, tokens):
    if tokens is None:
        return ugrid

    op = tokens[0]
    try:
        if op == "mov":
            # mov <vid> <x> <y> <z>
            if len(tokens) != 5:
                print(f"[WARN] mov: formato inválido → {' '.join(tokens)}")
                return ugrid
            vid = int(tokens[1])
            x, y, z = map(float, tokens[2:5])
            print(f"mov: v{vid} -> ({x:+.8e}, {y:+.8e}, {z:+.8e})")
            ugrid = mover_vertice(ugrid, vid, (x, y, z))

        elif op == "del_face":
            # del_face <idx_ignorado> v0 v1 v2 v3
            if len(tokens) < 6:
                print(f"[WARN] del_face: formato inválido → {' '.join(tokens)}")
                return ugrid
            verts = list(map(int, tokens[2:]))  # ignoramos el primer número después de del_face
            cids = encontrar_celdas_por_vertices(ugrid, verts)
            if not cids:
                print(f"[WARN] del_face: no se encontraron celdas con vértices {verts}")
                return ugrid
            print(f"del_face: borrando celdas {cids} (por vértices {verts})")
            ugrid = borrar_caras(ugrid, cids)

        elif op == "del_pt":
            # del_pt <vid>
            if len(tokens) != 2:
                print(f"[WARN] del_pt: formato inválido → {' '.join(tokens)}")
                return ugrid
            vid = int(tokens[1])
            print(f"del_pt: borrando celdas que tocan v{vid}")
            ugrid = borrar_vertices(ugrid, [vid-1])
        
        elif op == "change":
            # change <modelo>
            if len(tokens) != 2:
                print(f"[WARN] change: formato inválido → {' '.join(tokens)}")
                return ugrid
            modelo = tokens[1]
            print(f"change: cargando modelo '{modelo}'")
            ugrid = change_model(modelo)

        else:
            print(f"[WARN] Comando no reconocido: {op}")

    except Exception as e:
        print(f"[ERROR] ejecutando {' '.join(tokens)}: {e}")

    return ugrid

# ------------------------------
# VISUALIZADOR + PLAYER DE SCRIPT
# ------------------------------
def visualizar_con_script(ugrid, script_file):
    with open(script_file, "r") as f:
        lineas = [ln for ln in f if ln.strip()]

    comandos = [parse_line(ln) for ln in lineas]
    comandos = [t for t in comandos if t is not None]

    estado = {"i": 0}

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(ugrid)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetEdgeVisibility(1)
    actor.GetProperty().SetColor(0.8, 0.8, 1.0)

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(0.1, 0.1, 0.1)

    win = vtk.vtkRenderWindow()
    win.AddRenderer(ren)
    win.SetSize(900, 700)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(win)

    def keypress(obj, _):
        key = obj.GetKeySym()
        nonlocal ugrid

        if key == "n":  # siguiente comando
            if estado["i"] < len(comandos):
                tokens = comandos[estado["i"]]
                print(f"[{estado['i']+1}/{len(comandos)}] Ejecutando:", " ".join(tokens))
                ugrid = ejecutar_comando(ugrid, tokens)
                mapper.SetInputData(ugrid)
                win.Render()
                estado["i"] += 1
                print(f"→ Puntos: {ugrid.GetNumberOfPoints()} | Celdas: {ugrid.GetNumberOfCells()}")
            else:
                print("No quedan más comandos.")

        elif key == "s":
            print("Guardando a salida.vtk ...")
            guardar_ugrid(ugrid, "salida.vtk")

        elif key == "q":
            print("Saliendo...")
            iren.TerminateApp()

    iren.AddObserver("KeyPressEvent", keypress)
    win.Render()
    iren.Start()

# ------------------------------
# I/O
# ------------------------------
def cargar_ugrid(filename):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    ugrid = cargar_ugrid("a_output_3_quads.vtk")
    print("Puntos iniciales:", ugrid.GetNumberOfPoints())
    print("Celdas iniciales:", ugrid.GetNumberOfCells())
    visualizar_con_script(ugrid, "historial_completo_new.txt")
