import os
import app.logic.scripts_historial.quad2closeto as quad2closeto
import app.logic.scripts_historial.closeto2remsu as closeto2remsu
import app.logic.scripts_historial.remsu2shrink as remsu2shrink
import app.logic.scripts_historial.subdivider as subdivider
import app.logic.scripts_historial.malla_adaptativa as malla_adaptativa

def combine_historial(name,LR,output_file,vtkq,vtkc,vtkr,vtks):
    # output_file = "historial_completo_new.txt"
    input_files = [
        "movimientos1_new.txt",
        "movimientos2_new.txt",
        "movimientos3_new.txt"
    ]

    changes_files = [
        f"change {name}_gird.vtk",
    ]

    for x in range(LR):
        changes_files.append(f"change {name}_{x+1}_subdividida.vtk")
    ## changes_files  agregar nombres finales!
    changes_files.append(f"change {name}_quads.vtk")
     

    with open(output_file, 'w') as outfile:
        for x in changes_files:
            outfile.write(x + "\n\n")
        for fname in input_files:
            if os.path.exists(fname):
                with open(fname) as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Add a newline for separation

def combine_historial_borde(name,LR,output_file,vtkq,vtkc,vtkr,vtks):
    # output_file = "historial_completo_new.txt"
    input_files = [
        "movimientos1_new.txt",
        "movimientos2_new.txt",
        "movimientos3_new.txt"
    ]

    changes_files = [
        f"change {name}_gird.vtk",
    ]

    for x in range(LR):
        changes_files.append(f"change {name}_{x+1}_borde_caras.vtk")
    ## changes_files  agregar nombres finales!
    changes_files.append(f"change {name}_quads.vtk")
     
    with open(output_file, 'w') as outfile:
        for x in changes_files:
            outfile.write(x + "\n\n")
        for fname in input_files:
            if os.path.exists(fname):
                with open(fname) as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Add a newline for separation

def crear_historial(name,nivel_refinamiento,tipo="completo", input_dir="."):
    if tipo == "borde":
        malla_adaptativa.malla_adaptativa_completa(name, nivel_refinamiento, input_dir)
    else:
        subdivider.subdividir_completo(name, nivel_refinamiento, input_dir)

    quad2closeto.generar_movimientos_numpy(f"{name}_quads.vtk", f"{name}_closeto.vtk", "movimientos1_new.txt")
    closeto2remsu.generar_historial_caras_numpy(f"{name}_closeto.vtk", f"{name}_remSur.vtk", "movimientos2_new.txt")
    remsu2shrink.generar_movimientos_numpy(f"{name}_remSur.vtk", f"{name}_shrink.vtk", "movimientos3_new.txt")

    if tipo == "borde":
        combine_historial_borde(name,nivel_refinamiento,f"{name}_historial.txt",f"{name}_quads.vtk",f"{name}_closeto.vtk",f"{name}_remSur.vtk",f"{name}_shrimk.vtk")
    else:
        combine_historial(name,nivel_refinamiento,f"{name}_historial.txt",f"{name}_quads.vtk",f"{name}_closeto.vtk",f"{name}_remSur.vtk",f"{name}_shrimk.vtk")

# if __name__ == "__main__":
#     crear_historial("a_output_3", 3, "borde")