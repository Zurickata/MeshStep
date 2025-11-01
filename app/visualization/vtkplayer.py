import vtk
import numpy as np
import os
import sys
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QFileDialog, QProgressDialog
from PyQt5.QtCore import QStandardPaths, pyqtSignal, Qt, QTimer
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

def eliminar_colores(ugrid):
    """
    Elimina cualquier array de colores (scalars) de un vtkUnstructuredGrid.
    Esto quita los colores tanto de puntos como de celdas.
    """
    # Borrar arrays asociados a puntos
    point_data = ugrid.GetPointData()
    if point_data:
        for i in reversed(range(point_data.GetNumberOfArrays())):
            name = point_data.GetArrayName(i)
            if name and ("color" in name.lower() or "scalars" in name.lower()):
                print(f"[INFO] Eliminando array de puntos: {name}")
                point_data.RemoveArray(name)
        point_data.SetScalars(None)

    # Borrar arrays asociados a celdas
    cell_data = ugrid.GetCellData()
    if cell_data:
        for i in reversed(range(cell_data.GetNumberOfArrays())):
            name = cell_data.GetArrayName(i)
            if name and ("color" in name.lower() or "scalars" in name.lower()):
                print(f"[INFO] Eliminando array de celdas: {name}")
                cell_data.RemoveArray(name)
        cell_data.SetScalars(None)

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
        return eliminar_colores(ugrid)

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
def guardar_ugrid(ugrid, filename=None, parent=None, precision=8, puntos_por_linea=2):
    default_name = filename or "salida.vtk"
    # Determinar si es necesario pedir ruta al usuario
    need_dialog = True
    if filename:
        # Si filename contiene un directorio o es ruta absoluta, no pedir diálogo
        if os.path.isabs(filename) or os.path.dirname(filename):
            need_dialog = False

    if need_dialog:
        default_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        suggested = os.path.join(default_dir, default_name)
        file_path, _ = QFileDialog.getSaveFileName(parent, "Guardar VTK", suggested, "VTK files (*.vtk);;Todos los archivos (*)")
        if not file_path:
            print("[INFO] Guardado cancelado por el usuario.")
            return False, "cancelled"
        filename = file_path

    try:
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

        msg = f"Archivo guardado en: {filename}"
        print(f"[INFO] {msg}")
        if parent:
            QMessageBox.information(parent, "Guardado", msg)
        return True, filename

    except Exception as e:
        err = f"Error al guardar VTK: {e}"
        print(f"[ERROR] {err}")
        if parent:
            QMessageBox.critical(parent, "Error al guardar", err)
        return False, str(e)

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
def fit_camera_to_actor(renderer, actor, padding=1, dolly=1.5, min_distance=1e-6):
    """
    Ajusta la cámara del renderer para encuadrar el actor.
    padding: margen sobre la caja delimitadora (1.0 = sin margen).
    dolly: factor adicional para acercar la cámara ( >1 = más cerca).
    """
    if actor is None or renderer is None:
        return
    bounds = actor.GetBounds()
    if not bounds:
        return
    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    dx = xmax - xmin
    dy = ymax - ymin
    dz = zmax - zmin

    # Si la caja es prácticamente nula, no hacemos nada
    if dx <= 0 and dy <= 0 and dz <= 0:
        return

    # Centro y "diagonal" de la caja
    cx = (xmin + xmax) / 2.0
    cy = (ymin + ymax) / 2.0
    cz = (zmin + zmax) / 2.0
    diag = math.sqrt(max(dx*dx + dy*dy + dz*dz, 1e-12))

    cam = renderer.GetActiveCamera()
    if cam is None:
        return

    # Usamos el ángulo de vista vertical para calcular distancia necesaria
    fov = max(1.0, cam.GetViewAngle())
    fov_rad = math.radians(fov)
    # Distancia para que la diagonal quepa en el fov vertical (aprox)
    distance = (diag * padding) / (2.0 * math.sin(fov_rad / 2.0))
    if distance < min_distance:
        distance = min_distance

    # Dirección de proyección (normalizada). Vector desde cámara hacia el focal point.
    dirp = list(cam.GetDirectionOfProjection())
    norm = math.sqrt(dirp[0]**2 + dirp[1]**2 + dirp[2]**2)
    if norm == 0:
        dirn = [0.0, 0.0, -1.0]
    else:
        dirn = [d / norm for d in dirp]

    # Posicionar la cámara en center - dir * distance
    px = cx - dirn[0] * distance
    py = cy - dirn[1] * distance
    pz = cz - dirn[2] * distance

    cam.SetFocalPoint(cx, cy, cz)
    cam.SetPosition(px, py, pz)
    renderer.ResetCameraClippingRange()

    # Reset para asegurar buen framing, luego aplicar dolly (acercamiento adicional)
    try:
        renderer.ResetCamera()
    except Exception:
        pass

    # aplicar dolly si se pide (1.0 = sin cambio, >1 = más cerca)
    try:
        if dolly != 1.0:
            cam.Dolly(dolly)
            renderer.ResetCameraClippingRange()
    except Exception:
        pass

    try:
        cam.Modified()
    except Exception:
        pass

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

    # Ajustar cámara para que el modelo quepa bien
    fit_camera_to_actor(renderer, actor, padding=1.1)
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
                # Ajustar cámara tras cambiar la malla
                fit_camera_to_actor(renderer, actor, padding=1.1)
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

class CustomVTKPlayerStyle(vtk.vtkInteractorStyleTrackballCamera):
    """InteractorStyle personalizado con controles como FeriaVTK"""
    
    def __init__(self, vtk_player):
        super().__init__()
        self.vtk_player = vtk_player
        self.AddObserver("KeyPressEvent", self.on_key_press)
        self.AddObserver("LeftButtonPressEvent", self._left_down, 1.0)
        self.AddObserver("LeftButtonReleaseEvent", self._left_up, 1.0)
        self.AddObserver("MiddleButtonPressEvent", self._middle_down, 1.0)
        self.AddObserver("MiddleButtonReleaseEvent", self._middle_up, 1.0)

    # Click izquierdo => PAN (equivalente a botón medio por defecto)
    def _left_down(self, obj, evt):
        print("[VTKPlayerStyle] LeftButtonDown -> PAN")
        if hasattr(obj, "AbortFlagOn"):
            obj.AbortFlagOn()  # aborta el evento original
        vtk.vtkInteractorStyleTrackballCamera.OnMiddleButtonDown(self)

    def _left_up(self, obj, evt):
        if hasattr(obj, "AbortFlagOn"):
            obj.AbortFlagOn()
        vtk.vtkInteractorStyleTrackballCamera.OnMiddleButtonUp(self)

    # Botón medio => ROTACIÓN (equivalente a botón izquierdo por defecto)
    def _middle_down(self, obj, evt):
        print("[VTKPlayerStyle] MiddleButtonDown -> ROTATE")
        if hasattr(obj, "AbortFlagOn"):
            obj.AbortFlagOn()
        vtk.vtkInteractorStyleTrackballCamera.OnLeftButtonDown(self)

    def _middle_up(self, obj, evt):
        if hasattr(obj, "AbortFlagOn"):
            obj.AbortFlagOn()
        vtk.vtkInteractorStyleTrackballCamera.OnLeftButtonUp(self)

    def OnRightButtonDown(self):
        vtk.vtkInteractorStyleTrackballCamera.OnRightButtonDown(self)

    def OnRightButtonUp(self):
        vtk.vtkInteractorStyleTrackballCamera.OnRightButtonUp(self)

    def on_key_press(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key == "n":
            self.vtk_player.siguiente_paso()
        elif key == "r" and self.GetInteractor().GetControlKey():
            self.vtk_player.reiniciar()
        elif key == "r":
            print("🔁 Reseteando cámara")
            self.vtk_player.reset_camera()
        elif key == "s":
            self.vtk_player.guardar()
        else:
            self.OnKeyPress()


class VTKPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.actor = None
        self._custom_style = None

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

    # Helpers públicos para consultar estado
    def current_step(self) -> int:
        """Devuelve el índice actual del estado (i)."""
        return int(self.estado.get("i", 0))

    def total_steps(self) -> int:
        """Devuelve el total de comandos/pasos cargados."""
        return len(self.comandos) if self.comandos is not None else 0

    def apply_custom_style(self):
        """Reaplica el estilo personalizado y mantiene referencia para evitar GC."""
        interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        # Crear y guardar referencia
        self._custom_style = CustomVTKPlayerStyle(self)
        self._custom_style.SetDefaultRenderer(self.renderer)
        interactor.SetInteractorStyle(self._custom_style)
        # Debug para confirmar
        print("[VTKPlayer] Style aplicado:", type(interactor.GetInteractorStyle()).__name__)

    def run_script(self, vtk_file, script_file, outputs_dir=OUTPUTS_DIR):
        # Obtener referencia a ventana principal para verificar estado del historial
        main_window = self.window()
        mesh_generator = None

        try:
            # Buscar instancia de MeshGeneratorController en la jerarquía (si existe)
            if hasattr(main_window, 'mesh_generator_controller'):
                mesh_generator = main_window.mesh_generator_controller
            elif hasattr(main_window, 'mesh_generator'):
                mesh_generator = main_window.mesh_generator
        except Exception:
            mesh_generator = None

        # Construir rutas completas
        alt_path_vtk = os.path.join(outputs_dir, vtk_file)
        alt_path_script = os.path.join(outputs_dir, script_file)

        # 🧩 Validar existencia o generación del historial
        def intentar_cargar_historial():
            """Intenta cargar el historial, si ya existe o terminó de generarse."""
            if os.path.exists(alt_path_script):
                print(f"[VTKPlayer] Historial encontrado: {alt_path_script}")
                progress.close()
                QTimer.singleShot(300, lambda: self._run_script_core(alt_path_vtk, alt_path_script))
                return True
            if mesh_generator and not mesh_generator.historial_generandose:
                # Ya no se está generando y el archivo no existe → error
                progress.close()
                QMessageBox.critical(self, "Error", "No existe historial disponible para este modelo.")
                return True
            return False
        
        # Si el historial se está generando → mostrar spinner
        if mesh_generator and getattr(mesh_generator, "historial_generandose", False):
            print("[VTKPlayer] Historial aún generándose, mostrando spinner...")
            progress = QProgressDialog("Generando historial...", None, 0, 0, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.setWindowTitle("Creando historial")
            progress.setAutoClose(False)
            progress.setAutoReset(False)
            progress.setMinimumWidth(400)
            progress.show()

            # Variable de guardia para evitar ejecuciones múltiples
            self._historial_cargado = False

            # Reintentar cada 2 segundos
            self._historial_timer = QTimer(self)

            def revisar_historial():
                # Evitar llamadas repetidas
                if getattr(self, "_historial_cargado", False):
                    return

                # 🧠 Si ya existe el archivo del historial
                if os.path.exists(alt_path_script):
                    print(f"[VTKPlayer] ✅ Historial encontrado: {alt_path_script}")
                    self._historial_cargado = True  # marcar como cargado

                    # Detener timer de forma segura
                    if hasattr(self, "_historial_timer") and self._historial_timer.isActive():
                        self._historial_timer.stop()
                        try:
                            self._historial_timer.timeout.disconnect(revisar_historial)
                        except TypeError:
                            pass

                    progress.close()
                    # Ejecutar la carga real una sola vez
                    QTimer.singleShot(300, lambda: self._run_script_core(alt_path_vtk, alt_path_script))
                    return

                # 🧠 Si el historial ya no se está generando pero no existe el archivo → error
                if mesh_generator and not mesh_generator.historial_generandose:
                    print("[VTKPlayer] ❌ El historial no se generó correctamente.")
                    if hasattr(self, "_historial_timer") and self._historial_timer.isActive():
                        self._historial_timer.stop()
                        try:
                            self._historial_timer.timeout.disconnect(revisar_historial)
                        except TypeError:
                            pass
                    progress.close()
                    QMessageBox.critical(self, "Error", "No existe historial disponible.")
                    return

                # (si no ocurre ninguna de las dos condiciones, sigue esperando)
                print("[VTKPlayer] ⏳ Aún esperando historial...")

            self._historial_timer.timeout.connect(revisar_historial)
            self._historial_timer.start(2000)
            return

        # Si el historial ya está listo → cargar directamente
        if os.path.exists(alt_path_script):
            self._run_script_core(alt_path_vtk, alt_path_script)
        else:
            QMessageBox.critical(self, "Error", "No existe historial para este modelo.")

    def _run_script_core(self, alt_path_vtk, alt_path_script):
        """Versión interna de run_script() que realmente carga los archivos."""
        print(f"[VTKPlayer] Cargando modelo {alt_path_vtk} y script {alt_path_script}")
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

        # Mostrar modelo
        self._mostrar_ugrid(self.ugrid)

        # Inicializar interactor y estilo
        iren = self.vtk_widget.GetRenderWindow().GetInteractor()
        if not iren.GetInitialized():
            iren.Initialize()
        self.apply_custom_style()

        try:
            self._update_panel_pap()
        except Exception:
            pass

    def _mostrar_ugrid(self, ugrid):
        self.renderer.RemoveAllViewProps()
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(ugrid)
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetEdgeVisibility(1)
        self.actor.GetProperty().SetColor(0.8, 0.8, 1.0)
        self.renderer.AddActor(self.actor)
        # Ajustar cámara para que el modelo quepa bien
        fit_camera_to_actor(self.renderer, self.actor, padding=1.1)
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
                # Actualizar el panel PAP de forma robusta (buscando en ancestros y ventana)
                try:
                    self._update_panel_pap()
                except Exception:
                    pass
            else:
                print("No quedan más comandos.")
                QMessageBox.information(self, "Fin", "Ya estás en el último paso.")
        elif comando == "r":
            print("Reiniciando modelo y script...")
            self.ugrid = cargar_ugrid(self.vtk_file)
            self.estado["i"] = 0
            self._mostrar_ugrid(self.ugrid)
            print(f"→ Reiniciado: Puntos {self.ugrid.GetNumberOfPoints()} | Celdas {self.ugrid.GetNumberOfCells()}")
            try:
                self._update_panel_pap()
            except Exception:
                pass
        elif comando == "s":
            print("Guardando a salida.vtk ...")
            guardar_ugrid(self.ugrid, "salida.vtk", parent=self)

    def _update_panel_pap(self):
        """Buscar en ancestros el atributo panel_pap y, si existe, actualizar su estado.

        Esto es más robusto que depender de self.parent() porque el widget puede
        haber sido reparentado (por ejemplo dentro de un QTabWidget).
        """
        try:
            # first try window() (top-level widget)
            candidates = []
            top = None
            try:
                top = self.window()
            except Exception:
                top = None
            # include direct parent and top-level window
            candidates.append(self.parent())
            if top is not None:
                candidates.append(top)

            for start in candidates:
                anc = start
                while anc:
                    if hasattr(anc, 'panel_pap') and getattr(anc, 'panel_pap'):
                        try:
                            anc.panel_pap.actualizar_estado_pasos(self.current_step(), self.total_steps())
                        except Exception:
                            pass
                        return True
                    # subir un nivel
                    try:
                        anc = anc.parent()
                    except Exception:
                        break
            return False
        except Exception:
            return False