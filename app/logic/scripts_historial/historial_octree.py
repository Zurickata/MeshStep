import os
import math
import numpy as np
import vtk
from collections import defaultdict
import app.logic.scripts_historial.quad2closeto as quad2closeto
import app.logic.scripts_historial.remsu2shrink as remsu2shrink
import app.logic.scripts_historial.subdivider3d_octree as sub3d

def leer_celdas_vtk(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    celdas_raw = []
    start = False
    num_celdas = 0
    for line in lines:
        if line.strip().startswith("CELLS"):
            parts = line.strip().split()
            if len(parts) > 1:
                num_celdas = int(parts[1])
            start = True
            continue
        if start:
            if not line.strip() or line.strip().startswith("CELL_TYPES"):
                break
            celdas_raw.extend([int(v) for v in line.strip().split()])
    celdas = [] 
    i = 0
    while len(celdas) < num_celdas and i < len(celdas_raw):
        num_puntos = celdas_raw[i]
        i += 1
        if i + num_puntos <= len(celdas_raw):
            celda_indices = celdas_raw[i : i + num_puntos]
            celdas.append(set(celda_indices))
            i += num_puntos
        else:
            break 
            
    return celdas

def comparar_pts(pts_before, pts_after):
    del_ids = []
    del_pts = []
    pts_after_set = set(map(tuple, pts_after))
    for i, pt in enumerate(pts_before):
        if tuple(pt) not in pts_after_set:
            del_pts.append(pt)
            del_ids.append(i)
    return del_ids, del_pts

def punto_mas_cercano(pt, pts):
    x0, y0, z0 = pt
    min_dist = float("inf")
    closest = None
    for p in pts:
        x, y, z = p
        dist = math.sqrt((x - x0)**2 + (y - y0)**2 + (z - z0)**2)
        if dist < min_dist:
            min_dist = dist
            closest = p
    return closest

def mapear_puntos(pts_antes, pts_despues):
    pt_dict = {}
    id_antes = {tuple(pt): i for i, pt in enumerate(pts_antes)}

    for j, pt in enumerate(pts_despues):
        t = tuple(pt)
        if t in id_antes:
            pt_dict[j] = id_antes[t]
    return pt_dict

def comparar_celdas(celdas_old, celdas_new, del_pts, mapeo):
    del_pts_set = set(del_pts)
    old_cells_processed = set()
    new_cells_processed = set()
    
    celdas_new_traducidas = []
    for raw_cell_set in celdas_new:
        translated_set = set()
        is_valid = True
        for id_r in raw_cell_set:
            if id_r in mapeo:
                translated_set.add(mapeo[id_r])
            else:
                print(f"Error: No se encontró mapeo para el índice {id_r} de remSur.")
                is_valid = False
                break
        if is_valid:
            celdas_new_traducidas.append(translated_set)

    celdas_eliminadas = [] 

    for i, old_set in enumerate(celdas_old):
        if old_set.intersection(del_pts_set):
            continue
            
        for j, new_set in enumerate(celdas_new_traducidas):
            if j in new_cells_processed:
                continue
            
            if old_set == new_set:
                old_cells_processed.add(i)
                new_cells_processed.add(j)
                break

    vert_to_old_cell_map = defaultdict(list)
    for i, old_set in enumerate(celdas_old):
        if i in old_cells_processed:
            continue

        surviving_verts = old_set.difference(del_pts_set)
        for v in surviving_verts:
            vert_to_old_cell_map[v].append(i)

    new_cell_parent_scores = defaultdict(lambda: defaultdict(int))
    
    for j, new_set in enumerate(celdas_new_traducidas):
        if j in new_cells_processed:
            continue
            
        for v in new_set:
            if v in vert_to_old_cell_map:
                parent_cells = vert_to_old_cell_map[v]
                for old_idx in parent_cells:
                    new_cell_parent_scores[j][old_idx] += 1


    for j, scores in new_cell_parent_scores.items():
        if not scores:
            continue

        best_parent_old_idx = max(scores, key=scores.get)
        
        new_cells_processed.add(j)
        old_cells_processed.add(best_parent_old_idx) 

    for i in range(len(celdas_old)):
        if i not in old_cells_processed:
            celdas_eliminadas.append(i)

    return celdas_eliminadas

def cargar_ugrid(filename):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.DeepCopy(reader.GetOutput())
    return ugrid

def guardar_ugrid(ugrid, filepath):
    out = []
    out.append("# vtk DataFile Version 3.0\n")
    out.append("VTK file formatted in classic ASCII\n")
    out.append("ASCII\n")
    out.append("DATASET UNSTRUCTURED_GRID\n")

    npoints = ugrid.GetNumberOfPoints()
    out.append(f"POINTS {npoints} float\n")
    for i in range(0, npoints, 2):
        line_coords = []
        for j in range(2):
            idx = i + j
            if idx >= npoints:
                break
            x, y, z = ugrid.GetPoint(idx)
            line_coords.extend([f"{c:+.{8}E}" for c in (x, y, z)])
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

    with open(filepath, "w") as f:
        f.writelines(out)

def mover_vertice(ugrid, vid, new_pos):
    pts = ugrid.GetPoints()
    if vid < 0 or vid >= pts.GetNumberOfPoints():
        print(f"[WARN] mov: vid {vid} fuera de rango.")
        return ugrid
    pts.SetPoint(vid, new_pos)
    pts.Modified()
    ugrid.Modified()
    return ugrid

def borrar_caras(ugrid, caras_a_borrar_ids):
    """
    Elimina celdas por sus IDs (índices).
    """
    caras_a_borrar_set = set(caras_a_borrar_ids)
    nuevas_celdas = vtk.vtkCellArray()
    tipos = vtk.vtkUnsignedCharArray()
    tipos.SetName("types")
    for i in range(ugrid.GetNumberOfCells()):
        if i in caras_a_borrar_set:
            continue
        cell = ugrid.GetCell(i)
        tipos.InsertNextValue(ugrid.GetCellType(i))
        nuevas_celdas.InsertNextCell(cell)
    nuevo_grid = vtk.vtkUnstructuredGrid()
    nuevo_grid.SetPoints(ugrid.GetPoints())
    nuevo_grid.SetCells(tipos, nuevas_celdas)
    return nuevo_grid

def historial_patrones(vtkc, vtkr, vtks, output_path):
    pts_before = quad2closeto.leer_puntos_vtk_numpy(vtkc)
    pts_after = quad2closeto.leer_puntos_vtk_numpy(vtkr)
    i, del_pts = comparar_pts(pts_before, pts_after)
    _, add_pts = comparar_pts(pts_after, pts_before)
    celdas_before = leer_celdas_vtk(vtkc)
    celdas_after = leer_celdas_vtk(vtkr)
    ugrid = cargar_ugrid(vtkc)
    with open(output_path, "w") as f:
        # agregar/mover los puntos
        # todavía estoy revisando si es más fácil mover o agregar el punto
        # porque no queda exactamente bien la comparación :(
        for pt in add_pts:
            pto_cercano = punto_mas_cercano(pt, del_pts)
            idx = next(j for j, x in enumerate(del_pts) if np.array_equal(x, pto_cercano))
            
            # me está generando problemas :(
            # f.write(f"mov {i[idx]} {pt[0]:+0.8E} {pt[1]:+0.8E} {pt[2]:+0.8E}\n")
            # ugrid = mover_vertice(ugrid, i[idx], pt)
            pts_before[i[idx]] = pt
            del i[idx]
            del del_pts[idx]
            
            # si decidimos agregar el punto extra
            # f.write(f"add_pt {pt[0]:+0.8E} {pt[1]:+0.8E} {pt[2]:+0.8E}\n")
        
        mapeo = mapear_puntos(pts_before, pts_after)
        del_cells = comparar_celdas(celdas_before, celdas_after, i, mapeo)
        # borrar celdas
        for j in reversed(del_cells):
            f.write(f"del_face {j} {' '.join(map(str, celdas_before[j]))}\n")
            ugrid = borrar_caras(ugrid, [j])

        intermedio = vtkc[:-4]
        guardar_ugrid(ugrid, f"{intermedio}_step.vtk")
        # eliminar los puntos
        # for pt in reversed(i):
            # f.write(f"del_pt {pt}\n")
        
        f.write(f"change {vtks}\n")
        

def combinar_historial_octree(name,nivel_refinamiento, output_file):
    input_files = [
        "movimientos1_new.txt",
        "movimientos2_new.txt",
        "movimientos3_new.txt"
    ]

    changes_files = [
        f"change {name}_grid.vtk",
    ]
    for x in range(nivel_refinamiento):
        changes_files.append(f"change {name}_{x+1}_subdividida.vtk")
    with open(output_file, 'w') as outfile:
        for x in changes_files:
            outfile.write(x + "\n\n")
        outfile.write(f"change {name}_quads.vtk" + "\n")
        for fname in input_files:
            if os.path.exists(fname):
                with open(fname) as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")

def crear_historial_octree(name,nivel_refinamiento,tipo="completo", input_dir="."):
    sub3d.subdividir_completo(name, nivel_refinamiento, input_dir, f"{name}_quads.vtk")
    quad2closeto.generar_movimientos_numpy(f"{name}_quads.vtk", f"{name}_closeto.vtk", "movimientos1_new.txt")
    historial_patrones(f"{name}_closeto.vtk", f"{name}_remSur.vtk", f"{name}_shrink.vtk", "movimientos2_new.txt")
    remsu2shrink.generar_movimientos_numpy(f"{name}_remSur.vtk", f"{name}_shrink.vtk", "movimientos3_new.txt")

    combinar_historial_octree(name, nivel_refinamiento,f"{name}_historial.txt")