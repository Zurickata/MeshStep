import os
import app.logic.scripts_historial.quad2closeto as quad2closeto
import app.logic.scripts_historial.remsu2shrink as remsu2shrink

def comparar_pts(pts_before, pts_after):
    del_ids = []
    del_pts = []
    for i, pt in enumerate(pts_before):
        flag = False
        x, y, z = pt
        for pt2 in pts_after:
            if x == pt2[0] and y == pt2[1] and z == pt2[2]:
                flag = True
        if not flag:
            del_pts.append(pt)
            del_ids.append(i)
    return del_ids, del_pts

def historial_patrones(vtkc, vtkr, output_path):
    pts_before = quad2closeto.leer_puntos_vtk_numpy(vtkc)
    pts_after = quad2closeto.leer_puntos_vtk_numpy(vtkr)
    i, _ = comparar_pts(pts_before, pts_after)
    _, add_pts = comparar_pts(pts_after, pts_before)
    with open(output_path, "w") as f:
        for pt in reversed(i):
            f.write(f"del {pt}\n")
        for pt in add_pts:
            f.write(f"add_pt {pt[0]:+0.8E} {pt[1]:+0.8E} {pt[2]:+0.8E}\n")
        # comparar las caras diferentes :c

def combinar_historial_octree(name, output_file):
    input_files = [
        "movimientos1_new.txt",
        "movimientos2_new.txt",
        "movimientos3_new.txt"
    ]

    changes_files = [
        f"change {name}_grid.vtk",
    ]

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
    quad2closeto.generar_movimientos_numpy(f"{name}_quads.vtk", f"{name}_closeto.vtk", "movimientos1_new.txt")
    historial_patrones(f"{name}_closeto.vtk", f"{name}_remsur.vtk", "movimientos2_new.txt")
    remsu2shrink.generar_movimientos_numpy(f"{name}_remsur.vtk", f"{name}_shrink.vtk", "movimientos3_new.txt")

    combinar_historial_octree(name, f"{name}_historial.txt")