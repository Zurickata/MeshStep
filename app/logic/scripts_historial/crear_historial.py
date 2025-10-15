import os
import app.logic.scripts_historial.quad2closeto as quad2closeto
import app.logic.scripts_historial.closeto2remsu as closeto2remsu
import app.logic.scripts_historial.remsu2shrink as remsu2shrink
import app.logic.scripts_historial.subdivider as subdivider
import app.logic.scripts_historial.malla_adaptativa as malla_adaptativa
import app.logic.scripts_historial.reordenarV2 as reordenar

def escribir_del_faces(outfile, caras_no_b):
    # Elegir el tamaño del bloque según el rango
    if caras_no_b > 100:
        bloque = 10
    elif caras_no_b > 50:
        bloque = 5
    else:
        bloque = 1

    # Cuántas veces cabe el bloque completo
    cantidad = caras_no_b // bloque
    for _ in range(cantidad):
        outfile.write(f"del_face_cid {bloque}\n")

    # Si queda un sobrante, lo agregamos
    residuo = caras_no_b % bloque
    if residuo > 0:
        outfile.write(f"del_face_cid {residuo}\n")

def combine_historial(name,LR,output_file,vtkq,vtkc,vtkr,vtks):
    # output_file = "historial_completo_new.txt"
    input_files = [
        "movimientos1_new.txt",
        "movimientos2_new.txt",
        "movimientos3_new.txt"
    ]

    changes_files = [
        f"change {name}_grid.vtk",
    ]

    for x in range(LR):
        changes_files.append(f"change {name}_{x+1}_subdividida.vtk")
    ## changes_files  agregar nombres finales!
     
    changes_files.append(f"change {name}_ordenado.vtk") 

    # changes_files.append(f"change {name}_quads.vtk")

    caras_no_b = reordenar.reordenar_ugrid_total(f"{name}_{LR}_subdividida.vtk",f"{name}_quads.vtk",f"{name}_ordenado.vtk")

    with open(output_file, 'w') as outfile:
        for x in changes_files:
            outfile.write(x + "\n\n")
        escribir_del_faces(outfile, caras_no_b)
        outfile.write(f"change {name}_quads.vtk" + "\n")
        for fname in input_files:
            if os.path.exists(fname):
                with open(fname) as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Add a newline for separation

def combine_historial_borde(name,LR,output_file,vtkq,vtkc,vtkr,vtks):

    changes_files = []

    for x in range(LR):
        changes_files.append(f"change {name}_{x+1}_borde_caras.vtk")
    ## changes_files  agregar nombres finales!
    changes_files.append(f"change {name}_quads.vtk")
    changes_files.append(f"change {name}_closeto.vtk")
    changes_files.append(f"change {name}_remsur.vtk")
    changes_files.append(f"change {name}_shrink.vtk")
    with open(output_file, 'w') as outfile:
        for x in changes_files:
            outfile.write(x + "\n\n")

def crear_historial(name,nivel_refinamiento,tipo="completo", input_dir="."):
    if tipo == "borde":
        malla_adaptativa.malla_adaptativa_completa(name, nivel_refinamiento, input_dir)
        combine_historial_borde(name,nivel_refinamiento,f"{name}_historial.txt",f"{name}_quads.vtk",f"{name}_closeto.vtk",f"{name}_remSur.vtk",f"{name}_shrimk.vtk")
    else:
        subdivider.subdividir_completo(name, nivel_refinamiento, input_dir)
        quad2closeto.generar_movimientos_numpy(f"{name}_quads.vtk", f"{name}_closeto.vtk", "movimientos1_new.txt")
        closeto2remsu.generar_historial_caras_numpy(f"{name}_closeto.vtk", f"{name}_remSur.vtk", "movimientos2_new.txt")
        remsu2shrink.generar_movimientos_numpy(f"{name}_remSur.vtk", f"{name}_shrink.vtk", "movimientos3_new.txt")
        combine_historial(name,nivel_refinamiento,f"{name}_historial.txt",f"{name}_quads.vtk",f"{name}_closeto.vtk",f"{name}_remSur.vtk",f"{name}_shrimk.vtk")