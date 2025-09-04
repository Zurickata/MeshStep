import vtk
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../outputs")

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

def borrar_carascid(ugrid, cantidad):
    """
    Elimina 'cantidad' de caras/celdas desde la posición 0 de un vtkUnstructuredGrid.
    """
    n = ugrid.GetNumberOfCells()
    cantidad = min(cantidad, n)  # seguridad, no pasarse del total

    ids = vtk.vtkIdTypeArray()
    for cid in range(cantidad):
        ids.InsertNextValue(cid)

    selectionNode = vtk.vtkSelectionNode()
    selectionNode.SetFieldType(vtk.vtkSelectionNode.CELL)
    selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
    selectionNode.SetSelectionList(ids)
    selectionNode.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)

    selection = vtk.vtkSelection()
    selection.AddNode(selectionNode)

    extract = vtk.vtkExtractSelection()
    extract.SetInputData(0, ugrid)
    extract.SetInputData(1, selection)
    extract.Update()

    ugrid_out = vtk.vtkUnstructuredGrid.SafeDownCast(extract.GetOutput())
    return ugrid_out

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


def change_model(name, outputs_dir=OUTPUTS_DIR):
    # Caso 2: archivo .vtk
    if not os.path.isfile(name):
        alt_path = os.path.join(outputs_dir, name)
        if os.path.isfile(alt_path):
            name = alt_path

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

        elif op == "del_face_cid":
            # del_face_cid <cantidad>
            if len(tokens) != 2:
                print(f"[WARN] del_face_cid: formato inválido → {' '.join(tokens)}")
                return ugrid
            cantidad = int(tokens[1])
            print(f"del_face_cid: borrando {cantidad} celdas desde la posición 0")
            ugrid = borrar_carascid(ugrid, cantidad)
        
        
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
def visualizar_con_script(ugrid, script_file, renderer, render_window, interactor):
    with open(script_file, "r") as f:
        lineas = [ln for ln in f if ln.strip()]

    comandos = [parse_line(ln) for ln in lineas]
    comandos = [t for t in comandos if t is not None]

    estado = {"i": 0}

    renderer.RemoveAllViewProps()

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(ugrid)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetEdgeVisibility(1)
    actor.GetProperty().SetColor(0.8, 0.8, 1.0)

    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)
    render_window.Render()

    def keypress(obj, _):
        key = obj.GetKeySym()
        nonlocal ugrid

        if key == "n":  # siguiente comando
            if estado["i"] < len(comandos):
                tokens = comandos[estado["i"]]
                print(f"[{estado['i']+1}/{len(comandos)}] Ejecutando:", " ".join(tokens))
                ugrid = ejecutar_comando(ugrid, tokens)
                renderer.RemoveAllViewProps()
                mapper = vtk.vtkDataSetMapper()
                mapper.SetInputData(ugrid)
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                actor.GetProperty().SetEdgeVisibility(1)
                actor.GetProperty().SetColor(0.8, 0.8, 1.0)
                renderer.AddActor(actor)
                render_window.Render()
                estado["i"] += 1
                print(f"→ Puntos: {ugrid.GetNumberOfPoints()} | Celdas: {ugrid.GetNumberOfCells()}")
            else:
                print("No quedan más comandos.")

        elif key == "s":
            print("Guardando a salida.vtk ...")
            guardar_ugrid(ugrid, "salida.vtk")

        elif key == "r":  # reinicio
            print("Reiniciando modelo y script...")
            ugrid = cargar_ugrid("a_output_3_quads.vtk")
            estado["i"] = 0
            mapper.SetInputData(ugrid)
            actor.GetProperty().SetColor(0.8, 0.8, 1.0)
            render_window.Render()
            print(f"→ Reiniciado: Puntos {ugrid.GetNumberOfPoints()} | Celdas {ugrid.GetNumberOfCells()}")

    interactor.AddObserver("KeyPressEvent", keypress)

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


class VTKPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.actor = None

        # Botones de control
        self.boton_siguiente = QPushButton("Siguiente paso (n)")
        self.boton_reiniciar = QPushButton("Reiniciar (r)")
        self.boton_guardar = QPushButton("Guardar (s)")

        self.boton_siguiente.clicked.connect(self.siguiente_paso)
        self.boton_reiniciar.clicked.connect(self.reiniciar)
        self.boton_guardar.clicked.connect(self.guardar)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.boton_siguiente)
        botones_layout.addWidget(self.boton_reiniciar)
        botones_layout.addWidget(self.boton_guardar)

        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        layout.addLayout(botones_layout)
        self.setLayout(layout)

        # Estado del script
        self.comandos = []
        self.estado = {"i": 0}
        self.ugrid = None
        self.script_file = None
        self.vtk_file = None

    def run_script(self, vtk_file, script_file, outputs_dir=OUTPUTS_DIR):
        alt_path_vtk = os.path.join(outputs_dir, vtk_file)
        alt_path_script = os.path.join(outputs_dir, script_file)

        self.renderer.RemoveAllViewProps()
        self.vtk_file = alt_path_vtk
        self.script_file = alt_path_script
        self.ugrid = cargar_ugrid(alt_path_vtk)
        self.comandos = []
        self.estado = {"i": 0}

        # Leer comandos
        with open(alt_path_script, "r") as f:
            lineas = [ln for ln in f if ln.strip()]
        self.comandos = [parse_line(ln) for ln in lineas if parse_line(ln) is not None]

        self._mostrar_ugrid(self.ugrid)

        # Conectar eventos de teclado
        interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        interactor.RemoveObservers("KeyPressEvent")  # Evita duplicados
        interactor.AddObserver("KeyPressEvent", self.keypress)

    def _mostrar_ugrid(self, ugrid):
        self.renderer.RemoveAllViewProps()
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(ugrid)
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetEdgeVisibility(1)
        self.actor.GetProperty().SetColor(0.8, 0.8, 1.0)
        self.renderer.AddActor(self.actor)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def siguiente_paso(self):
        self._ejecutar_comando("n")

    def reiniciar(self):
        self._ejecutar_comando("r")

    def guardar(self):
        self._ejecutar_comando("s")

    def keypress(self, obj, _):
        key = obj.GetKeySym()
        if key == "n":
            self.siguiente_paso()
        elif key == "r":
            self.reiniciar()
        elif key == "s":
            self.guardar()

    def _ejecutar_comando(self, comando):
        if comando == "n":
            if self.estado["i"] < len(self.comandos):
                tokens = self.comandos[self.estado["i"]]
                print(f"[{self.estado['i']+1}/{len(self.comandos)}] Ejecutando:", " ".join(tokens))
                self.ugrid = ejecutar_comando(self.ugrid, tokens)
                self._mostrar_ugrid(self.ugrid)
                self.estado["i"] += 1
                print(f"→ Puntos: {self.ugrid.GetNumberOfPoints()} | Celdas: {self.ugrid.GetNumberOfCells()}")
            else:
                print("No quedan más comandos.")
                QMessageBox.information(self, "Fin", "Ya estás en el último paso.")
        elif comando == "r":
            print("Reiniciando modelo y script...")
            self.ugrid = cargar_ugrid(self.vtk_file)
            self.estado["i"] = 0
            self._mostrar_ugrid(self.ugrid)
            print(f"→ Reiniciado: Puntos {self.ugrid.GetNumberOfPoints()} | Celdas {self.ugrid.GetNumberOfCells()}")
        elif comando == "s":
            print("Guardando a salida.vtk ...")
            guardar_ugrid(self.ugrid, "salida.vtk")