import sys
import os
import re
import glob
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QDialog, QSpinBox, QMessageBox, QListWidget, QSplitter, QListWidgetItem, QMenu, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from FeriaVTK import ModelSwitcher, CustomInteractorStyle


class CargarArchivoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargar archivos")
        self.resize(400, 300)

        self.archivos_seleccionados = []
        self.nivel_refinamiento = 1

        self.ruta_archivos = QLabel("Ningún archivo seleccionado")

        self.boton_seleccionar = QPushButton("Seleccionar archivos")
        self.boton_seleccionar.clicked.connect(self.abrir_explorador)

        self.label_refinamiento = QLabel("Nivel de refinamiento:")
        self.spin_refinamiento = QSpinBox()
        self.spin_refinamiento.setRange(1, 100)
        self.spin_refinamiento.setValue(1)
        self.spin_refinamiento.valueChanged.connect(self.verificar_refinamiento)

        self.boton_confirmar = QPushButton("Confirmar")
        self.boton_confirmar.clicked.connect(self.confirmar_datos)

        layout = QVBoxLayout()
        layout.addWidget(self.boton_seleccionar)
        layout.addWidget(self.ruta_archivos)
        layout.addWidget(self.label_refinamiento)
        layout.addWidget(self.spin_refinamiento)
        layout.addWidget(self.boton_confirmar)
        self.setLayout(layout)

    def abrir_explorador(self):
        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecciona archivos",
            "",
            "Archivos .vtk (*.vtk)"
        )
        if archivos:
            self.archivos_seleccionados = archivos
            self.ruta_archivos.setText(f"{len(archivos)} archivo(s) seleccionados")

    def verificar_refinamiento(self):
        valor = self.spin_refinamiento.value()
        if valor > 10:
            QMessageBox.warning(
                self,
                "Advertencia",
                "Los niveles altos de refinamiento (>10) pueden requerir mucha memoria RAM."
            )

    def confirmar_datos(self):
        if not self.archivos_seleccionados:
            QMessageBox.critical(self, "Error", "Debes seleccionar al menos un archivo .vtk antes de confirmar.")
            return

        self.nivel_refinamiento = self.spin_refinamiento.value()

        QMessageBox.information(
            self,
            "Confirmación",
            f"Se cargaron {len(self.archivos_seleccionados)} archivo(s) con nivel de refinamiento: {self.nivel_refinamiento}"
        )
        self.accept()


class AppPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        self.boton_cargar = QPushButton("Cargar archivos", self)
        self.boton_cargar.clicked.connect(self.abrir_dialogo_carga)

        # NUEVOS BOTONES PARA ACCIONES
        self.boton_n = QPushButton("Siguiente modelo (n)", self)
        self.boton_n.clicked.connect(self.accion_n)

        self.boton_a = QPushButton("Toggle puntos críticos (a)", self)
        self.boton_a.clicked.connect(self.accion_a)

        self.boton_b = QPushButton("Borrar extras (b)", self)
        self.boton_b.clicked.connect(self.accion_b)

        self.boton_r = QPushButton("Reset cámara/modelo (r)", self)
        self.boton_r.clicked.connect(self.accion_r)

        self.boton_w = QPushButton("Wireframe (w)", self)
        self.boton_w.clicked.connect(self.accion_w)

        self.boton_s = QPushButton("Sólido (s)", self)
        self.boton_s.clicked.connect(self.accion_s)

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(self.mostrar_contenido)
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        self.rutas_archivos = {}

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(CustomInteractorStyle(self.renderer))
        self.interactor.Initialize()

         # Crear botones de navegación
        self.boton_anterior = QPushButton("◀ Anterior")
        self.boton_siguiente = QPushButton("Siguiente ▶")

        # Conectar botones a funciones
        self.boton_anterior.clicked.connect(self.navegar_anterior)
        self.boton_siguiente.clicked.connect(self.navegar_siguiente)

        # Estilo para los botones de navegación
        self.boton_anterior.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """)
        
        self.boton_siguiente.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """)

        # Crear layout para los botones de navegación
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.boton_anterior)
        nav_layout.addWidget(self.boton_siguiente)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(5)
        
        # Widget contenedor para los botones de navegación
        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        nav_widget.setFixedHeight(40)

        self.switcher = None

        splitter = QSplitter(Qt.Horizontal)

        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        layout_izquierdo.addWidget(self.boton_cargar)

        layout_izquierdo.addWidget(self.lista_archivos)
        panel_izquierdo.setLayout(layout_izquierdo)

        # Layout principal del panel central
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.vtk_widget, 1)  # El widget VTK ocupa la mayor parte
        central_layout.addWidget(nav_widget)          # Los botones de navegación abajo
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        
        # Widget contenedor del panel central
        panel_central = QWidget()
        panel_central.setLayout(central_layout)

        # Panel derecho
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        self.label_derecho = QLabel("Métricas de ángulos críticos")
        self.label_derecho.setAlignment(Qt.AlignCenter)
        self.label_derecho.setWordWrap(True) 
        layout_derecho.addWidget(self.label_derecho)
                # AGREGAR LOS NUEVOS BOTONES
        layout_derecho.addWidget(self.boton_n)
        layout_derecho.addWidget(self.boton_a)
        layout_derecho.addWidget(self.boton_b)
        layout_derecho.addWidget(self.boton_r)
        layout_derecho.addWidget(self.boton_w)
        layout_derecho.addWidget(self.boton_s)
        panel_derecho.setLayout(layout_derecho)

        # Configurar el tamaño mínimo de los paneles
        panel_derecho.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        panel_derecho.setMinimumWidth(100)  # You can adjust this value

        # Configurar el tamaño de los botones
        self.label_derecho.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        #for btn in [self.boton_n, self.boton_a, self.boton_b, self.boton_r, self.boton_w, self.boton_s]:
        #    btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)

        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_central)
        splitter.addWidget(panel_derecho)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setAcceptDrops(True)


    # Este método se encarga de leer el archivo _histo.txt y actualizar el panel derecho con los ángulos
    def actualizar_panel_derecho(self, ruta_archivo):
        try:
            # Cambiar extensión del archivo de .vtk a _histo.txt
            base, _ = os.path.splitext(ruta_archivo)
            ruta_modificada = f"{base}_histo.txt"

            # Leer el archivo línea por línea
            with open(ruta_modificada, 'r') as f:
                lineas = f.readlines()

            angulo_triangulo = None
            angulo_cuadrado = None

            for i, linea in enumerate(lineas):
                if "For Triangles:" in linea and i + 1 < len(lineas):
                    angulo_triangulo = lineas[i + 1].strip()
                if "For Quads:" in linea and i + 1 < len(lineas):
                    angulo_cuadrado = lineas[i + 1].strip()

            def formatear_angulo(label, linea):
                partes = linea.split('|')
                min_ang = partes[0].strip()
                max_ang = partes[1].strip() if len(partes) > 1 else ''
                return f"<b>- {label}:</b><br>{min_ang}<br>{max_ang}<br><br>"

            if angulo_triangulo or angulo_cuadrado:
                contenido_html = "<b>Ángulos Críticos:</b><br><br>"
                if angulo_triangulo:
                    contenido_html += formatear_angulo("Triángulos", angulo_triangulo)
                if angulo_cuadrado:
                    contenido_html += formatear_angulo("Cuadriláteros", angulo_cuadrado)
            else:
                contenido_html = "<b>No se encontraron líneas de ángulos para triángulos ni cuadriláteros.</b>"

            self.label_derecho.setText(contenido_html)

        except Exception as e:
            self.label_derecho.setText(f"<b>Error al leer el archivo:</b><br>{e}")

    # Métodos para cada acción
    def accion_n(self):
        if self.switcher:
            self.switcher.current_index = (self.switcher.current_index + 1) % len(self.switcher.file_list)
            self.switcher.load_model(self.switcher.file_list[self.switcher.current_index])
            self.switcher.clear_extra_models()
            self.switcher.toggle_load = False

    #Toggle puntos críticos
    def accion_a(self):
        if self.switcher:
            self.switcher.toggle_load = not self.switcher.toggle_load
            if self.switcher.toggle_load:
                print("Cargando puntos criticos...")
                self.switcher.marcar_angulos_extremos()
                self.renderer.GetRenderWindow().Render()
            else:
                print("Toggle desactivado puntos criticos.")
                self.switcher.clear_extra_models()
                self.renderer.GetRenderWindow().Render()

    def accion_b(self):
        if self.switcher:
            self.switcher.clear_extra_models()

    def accion_r(self):
        if self.switcher:
            print("🔁 Reseteando cámara y modelo")
            self.switcher.actor.SetOrientation(0, 0, 0)
            self.switcher.actor.SetPosition(0, 0, 0)
            self.switcher.actor.SetScale(1, 1, 1)
            self.renderer.ResetCamera()
            if isinstance(self.interactor.GetInteractorStyle(), CustomInteractorStyle):
                self.interactor.GetInteractorStyle().reset_camera_and_rotation()
            self.renderer.GetRenderWindow().Render()

    def accion_w(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToWireframe()
            self.renderer.GetRenderWindow().Render()

    def accion_s(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToSurface()
            self.renderer.GetRenderWindow().Render()

    def abrir_dialogo_carga(self):
        dialogo = CargarArchivoDialog(self)
        if dialogo.exec_() == QDialog.Accepted:
            if not self.switcher:
                self.switcher = ModelSwitcher(self.renderer, self.interactor, dialogo.archivos_seleccionados)
            else:
                for ruta in dialogo.archivos_seleccionados:
                    self.switcher.add_model(ruta)

            for ruta in dialogo.archivos_seleccionados:
                nombre = os.path.basename(ruta)
                if nombre not in self.rutas_archivos:
                    self.rutas_archivos[nombre] = ruta
                    self.lista_archivos.addItem(nombre)

    def mostrar_contenido(self, item):
        nombre = item.text()
        ruta = self.rutas_archivos.get(nombre)
        if ruta and self.switcher:
            self.switcher.load_model(ruta)
            self.actualizar_panel_derecho(ruta)

    def mostrar_menu_contextual(self, posicion):
        item = self.lista_archivos.itemAt(posicion)
        if item:
            menu = QMenu()
            accion_eliminar = menu.addAction("Eliminar archivo de la lista")
            accion = menu.exec_(self.lista_archivos.mapToGlobal(posicion))
            if accion == accion_eliminar:
                nombre = item.text()
                if nombre in self.rutas_archivos:
                    del self.rutas_archivos[nombre]
                self.lista_archivos.takeItem(self.lista_archivos.row(item))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if all(url.toLocalFile().endswith('.vtk') for url in urls):
                event.acceptProposedAction()

    def dropEvent(self, event):
        archivos = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile().endswith('.vtk')]
        for ruta_archivo in archivos:
            self.procesar_archivo_arrastrado(ruta_archivo)

    def procesar_archivo_arrastrado(self, ruta_archivo):
        dialogo = CargarArchivoDialog(self)
        dialogo.archivos_seleccionados = [ruta_archivo]
        dialogo.ruta_archivos.setText(ruta_archivo)

        if not ruta_archivo.endswith('.vtk'):
            QMessageBox.critical(self, "Error", "El archivo no es un archivo .vtk válido.")
            return

        if dialogo.exec_() == QDialog.Accepted:
            nombre = os.path.basename(ruta_archivo)
            if nombre not in self.rutas_archivos:
                self.rutas_archivos[nombre] = ruta_archivo
                self.lista_archivos.addItem(nombre)

            if not self.switcher:
                self.switcher = ModelSwitcher(self.renderer, self.interactor, [ruta_archivo])
            else:
                self.switcher.add_model(ruta_archivo)

    def navegar_anterior(self):
        """Función para navegar al modelo anterior numéricamente"""
        if not self.switcher or not self.switcher.file_list:
            return
            
        current_file = self.switcher.file_list[self.switcher.current_index]
        base_name, number, extension = self._descomponer_nombre_archivo(current_file)
        
        if number is not None:
            # Buscar el archivo con número anterior
            prev_number = number - 1
            prev_file = self._encontrar_archivo_numerado(base_name, prev_number, extension)
            
            if prev_file:
                self._cargar_archivo_numerado(prev_file)
            else:
                QMessageBox.information(self, "Información", "No se encontró el archivo anterior en la secuencia.")

    def navegar_siguiente(self):
        """Función para navegar al siguiente modelo numéricamente"""
        print("\n=== INICIANDO NAVEGACIÓN SIGUIENTE ===")
        
        if not self.switcher or not self.switcher.file_list:
            print("DEBUG: No hay switcher o lista de archivos vacía")
            QMessageBox.warning(self, "Advertencia", "No hay archivos cargados.")
            return
            
        current_file = self.switcher.file_list[self.switcher.current_index]
        print(f"DEBUG: Archivo actual: {current_file}")
        print(f"DEBUG: Índice actual: {self.switcher.current_index}")
        print(f"DEBUG: Lista completa: {self.switcher.file_list}")
        
        # Descomponer el nombre del archivo
        base_name, number, extension = self._descomponer_nombre_archivo(current_file)
        print(f"DEBUG: Base: '{base_name}', Número: {number}, Ext: '{extension}'")
        
        if number is None:
            print("DEBUG: El archivo no sigue el patrón numerado")
            QMessageBox.warning(self, "Advertencia", "El archivo actual no sigue el patrón de numeración esperado (nombre_1.vtk).")
            return
        
        # Buscar TODOS los archivos numerados en la misma serie
        serie_archivos = self._encontrar_serie_completa(base_name, extension)
        print(f"DEBUG: Serie completa encontrada: {serie_archivos}")
        
        if not serie_archivos:
            print("DEBUG: No se encontró serie completa")
            QMessageBox.warning(self, "Advertencia", "No se encontraron archivos en esta serie numérica.")
            return
        
        # Encontrar la posición del archivo actual en la serie ordenada
        try:
            current_pos = serie_archivos.index(current_file)
            print(f"DEBUG: Posición actual en serie: {current_pos}")
        except ValueError:
            print("DEBUG: Archivo actual no está en la serie encontrada")
            QMessageBox.warning(self, "Error", "Inconsistencia en la serie de archivos.")
            return
        
        # Determinar siguiente archivo
        if current_pos + 1 < len(serie_archivos):
            next_file = serie_archivos[current_pos + 1]
            print(f"DEBUG: Siguiente archivo en serie: {next_file}")
            self._cargar_archivo_numerado(next_file)
        else:
            print("DEBUG: No hay más archivos en esta serie")
            QMessageBox.information(self, "Información", "Has llegado al final de la serie.")

    def _encontrar_serie_completa(self, base_name, extension):
        """Encuentra todos los archivos de la misma serie numérica"""
        print(f"DEBUG: Buscando serie completa para: {base_name}_*.{extension}")
        
        # Patrones a buscar
        patterns = [
            f"{base_name}_*.{extension}",
            f"{base_name}-*.{extension}",
            f"{os.path.basename(base_name)}_*.{extension}",
            f"{os.path.basename(base_name)}-*.{extension}"
        ]
        
        # Directorio donde buscar
        search_dir = os.path.dirname(base_name) if os.path.dirname(base_name) else "."
        print(f"DEBUG: Buscando en directorio: {search_dir}")
        
        # Encontrar todos los archivos que coincidan
        all_files = []
        for pattern in patterns:
            full_pattern = os.path.join(search_dir, pattern)
            print(f"DEBUG: Buscando con patrón: {full_pattern}")
            all_files.extend(glob.glob(full_pattern))
        
        # Eliminar duplicados
        unique_files = list(set(all_files))
        print(f"DEBUG: Archivos encontrados: {unique_files}")
        
        # Ordenar numéricamente
        def extract_number(filepath):
            filename = os.path.basename(filepath)
            match = re.search(r'(\d+)\.'+extension+'$', filename)
            return int(match.group(1)) if match else 0
        
        try:
            unique_files.sort(key=extract_number)
            print(f"DEBUG: Archivos ordenados: {unique_files}")
            return unique_files
        except:
            print("DEBUG: Error al ordenar archivos")
            return []

    def _descomponer_nombre_archivo(self, filepath):
        """Extrae las partes del nombre del archivo para detectar números"""
        filename = os.path.basename(filepath)
        base_dir = os.path.dirname(filepath)
        
        # Busca patrones como: nombre_X.ext o nombre-X.ext (X es el número)
        match = re.match(r'^(.*?)[-_](\d+)\.([^.]+)$', filename)
        if match:
            base_name = match.group(1)
            number = int(match.group(2))
            extension = match.group(3)
            return (os.path.join(base_dir, base_name), number, extension)
        
        # Si no encuentra el patrón, devuelve None para el número
        base, ext = os.path.splitext(filename)
        return (os.path.join(base_dir, base), None, ext[1:] if ext else '')

    def _encontrar_archivo_numerado(self, base_name, number, extension):
        """Busca un archivo con el número especificado"""
        possible_paths = [
            f"{base_name}_{number}.{extension}",
            f"{base_name}-{number}.{extension}",
            f"{base_name}{number}.{extension}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def _cargar_archivo_numerado(self, filepath):
        """Carga un archivo y actualiza la interfaz"""
        # Verificar si el archivo ya está en la lista
        filename = os.path.basename(filepath)
        
        if filename not in self.rutas_archivos:
            # Si no está en la lista, agregarlo
            self.rutas_archivos[filename] = filepath
            self.lista_archivos.addItem(filename)
            if self.switcher:
                self.switcher.add_model(filepath)
        
        # Cargar el archivo
        if self.switcher:
            try:
                self.switcher.load_model(filepath)
                self.actualizar_panel_derecho(filepath)
                # Actualizar el índice actual al nuevo archivo
                if filepath in self.switcher.file_list:
                    self.switcher.current_index = self.switcher.file_list.index(filepath)
                self.renderer.GetRenderWindow().Render()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AppPrincipal()
    ventana.show()
    sys.exit(app.exec_())
