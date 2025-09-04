import vtk
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

def poly_to_vtk(filepath):
    import vtk

    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    with open(filepath, 'r') as f:
        lines_raw = f.readlines()

    # Buscar la línea con el número de puntos
    i = 0
    while i < len(lines_raw):
        line = lines_raw[i].strip()
        if line and not line.startswith('#'):
            if line.split()[0].isdigit():
                num_points = int(line.split()[0])
                i += 1
                break
        i += 1

    # Leer los puntos
    for _ in range(num_points):
        while i < len(lines_raw) and (not lines_raw[i].strip() or lines_raw[i].strip().startswith('#')):
            i += 1
        parts = lines_raw[i].strip().split()
        if len(parts) >= 3:
            x, y = float(parts[1]), float(parts[2])
            points.InsertNextPoint(x, y, 0)
        i += 1

    # Buscar la línea con el número de segmentos
    while i < len(lines_raw):
        line = lines_raw[i].strip()
        if line and not line.startswith('#'):
            if line.split()[0].isdigit():
                num_segments = int(line.split()[0])
                i += 1
                break
        i += 1

    # Leer los segmentos
    for _ in range(num_segments):
        while i < len(lines_raw) and (not lines_raw[i].strip() or lines_raw[i].strip().startswith('#')):
            i += 1
        parts = lines_raw[i].strip().split()
        if len(parts) >= 3:
            start_id = int(parts[1]) - 1
            end_id = int(parts[2]) - 1
            vtk_line = vtk.vtkLine()
            vtk_line.GetPointIds().SetId(0, start_id)
            vtk_line.GetPointIds().SetId(1, end_id)
            lines.InsertNextCell(vtk_line)
        i += 1

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)
    return polydata

class BaseViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        self.setLayout(layout)
        self.actor = None

    def load_poly_or_mdl(self, filepath):
        self.renderer.RemoveAllViewProps()
        if filepath.endswith('.vtk'):
            reader = vtk.vtkUnstructuredGridReader()
            reader.SetFileName(filepath)
            reader.Update()
            polydata = reader.GetOutput()
            mapper = vtk.vtkDataSetMapper()
        elif filepath.endswith('.poly'):
            polydata = poly_to_vtk(filepath)
            mapper = vtk.vtkPolyDataMapper()
        else:
            QMessageBox.critical(self, "Formato no soportado", "Solo se pueden visualizar archivos .vtk o .poly en 'Paso a paso'.")
            return

        mapper.SetInputData(polydata)
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.renderer.AddActor(self.actor)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()