import os
import quad2closeto
import closeto2remsu
import remsu2shrink
import shrink2vtk


def combine_historial():
    output_file = "historial_completo_new.txt"
    input_files = [
        "movimientos1_new.txt",
        "movimientos2_new.txt",
        "movimientos3_new.txt"
        #"movimientos4.txt"
    ]

    with open(output_file, 'w') as outfile:
        for fname in input_files:
            if os.path.exists(fname):
                with open(fname) as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Add a newline for separation

if __name__ == "__main__":
    combine_historial()
    print("Historial completo generado en 'historial_completo_new.txt'.")