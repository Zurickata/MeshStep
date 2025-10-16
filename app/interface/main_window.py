from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
                             QSplitter, QStyle, QTabWidget,
                             QMenuBar, QAction, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from app.visualization.RefinementViewer import RefinementViewer
from app.interface.panel_derecho import PanelDerecho
from app.visualization.vtkplayer import VTKPlayer
from app.logic.main_window_logic import (
    dragEnterEvent, dropEvent,
    abrir_dialogo_carga, mostrar_contenido, mostrar_menu_contextual,
    abrir_opciones_dialog, cambiar_visualizador, closeEvent, abrir_manual
)

from .panel_derecho import PanelDerecho

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        self.ignorar_limite_hardware = False

        logo_label = QLabel()
        icono_svg = QPixmap("meshsteppng.svg")
        logo_label.setPixmap(icono_svg.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.menubar = QMenuBar(self)
        self.file_menu = self.menubar.addMenu("Archivo")
        self.edit_menu = self.menubar.addMenu("Editar")
        self.help_menu = self.menubar.addMenu("Ayuda")

        # Iconos estándar
        icon_cargar = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        icon_opciones = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)

        # Botones en barra horizontal
        self.boton_cargar = QPushButton(icon_cargar, "Cargar archivos", self)
        self.boton_cargar.clicked.connect(lambda: abrir_dialogo_carga(self))

        self.boton_opciones = QPushButton(icon_opciones, "Opciones", self)
        self.boton_opciones.clicked.connect(lambda: abrir_opciones_dialog(self))

        # Barra horizontal de botones
        barra_botones = QHBoxLayout()
        barra_botones.addWidget(self.boton_cargar)
        barra_botones.addWidget(self.boton_opciones)
        barra_botones.addStretch(1)  # Para que los botones queden a la izquierda

        # Acciones del menú
        self.action_cargar = QAction("Cargar archivos", self)
        self.action_cargar.triggered.connect(lambda: abrir_dialogo_carga(self))
        self.file_menu.addAction(self.action_cargar)

        self.action_opciones = QAction("Opciones", self)
        self.action_opciones.triggered.connect(lambda: abrir_opciones_dialog(self))
        self.edit_menu.addAction(self.action_opciones)

        self.action_help = QAction("Manual", self)
        self.action_help.triggered.connect(lambda: abrir_manual(self))
        self.help_menu.addAction(self.action_help)

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(lambda item: mostrar_contenido(self, item))
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(lambda pos: mostrar_menu_contextual(self, pos))

        self.refinement_viewer = RefinementViewer(self)
        self.panel_derecho = PanelDerecho(parent=self)
        self.refinement_viewer.panel_derecho = self.panel_derecho
        self.panel_derecho.refinement_viewer = self.refinement_viewer

        self.rutas_archivos = {}
        self.rutas_octree = {}

        self.vtk_player = VTKPlayer(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.refinement_viewer, "Niveles de refinación")
        self.tab_widget.addTab(self.vtk_player, "Paso a paso")
        self.tab_widget.currentChanged.connect(lambda idx: cambiar_visualizador(self, idx))

        self.panel_central = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.tab_widget)
        self.panel_central.setLayout(central_layout)

        splitter = QSplitter(Qt.Horizontal)
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        layout_izquierdo.addWidget(self.lista_archivos)
        layout_izquierdo.addWidget(logo_label)
        panel_izquierdo.setLayout(layout_izquierdo)

<<<<<<< HEAD
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
        self.panel_derecho = PanelDerecho(self)
        
        # Conectar señales del panel derecho
        self._conectar_señales_panel_derecho()
        
        """ panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        self.label_derecho = QLabel("Métricas de ángulos críticos")
        self.label_derecho.setAlignment(Qt.AlignCenter)
        self.label_derecho.setWordWrap(True) 
        layout_derecho.addWidget(self.label_derecho)
            
        # AGREGAR LOS NUEVOS BOTONES
        layout_derecho.addWidget(self.boton_n)
        layout_derecho.addWidget(self.boton_a)
        # layout_derecho.addWidget(self.boton_b)
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
        #    btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred) """

        # Configurar el splitter con el nuevo panel
        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_central)
        splitter.addWidget(self.panel_derecho)  # Nuevo panel derecho
=======
        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(self.panel_central)
        splitter.addWidget(self.panel_derecho)
>>>>>>> 0e18fd0544ffd6977e098ebd3592d57a4e8f298d
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)

        layout = QVBoxLayout()
        layout.setMenuBar(self.menubar)
        layout.addLayout(barra_botones)
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setAcceptDrops(True)

<<<<<<< HEAD
    def _conectar_señales_panel_derecho(self):
        """Conecta las señales del panel derecho con las funciones existentes"""
       
        # Conectar botones de acciones
        self.panel_derecho.boton_wireframe.clicked.connect(self.accion_w)
        self.panel_derecho.boton_solido.clicked.connect(self.accion_s)
        self.panel_derecho.boton_puntos_criticos.clicked.connect(self.accion_a)
        self.panel_derecho.boton_limpiar.clicked.connect(self.accion_b)
        self.panel_derecho.boton_reset_camara.clicked.connect(self.accion_r)
       
        
        
        # Conectar slider de velocidad
        self.panel_derecho.slider_velocidad.valueChanged.connect(self.ajustar_velocidad)

    def ajustar_velocidad(self, valor):
        """Ajusta la velocidad de la animación"""
        segundos = valor / 1000.0
        self.timer_animacion.setInterval(valor)
        self.panel_derecho.label_velocidad_valor.setText(f"{segundos:.1f}s")

    # Este método se encarga de leer el archivo _histo.txt y actualizar el panel derecho con los ángulos
    """ def actualizar_panel_derecho(self, ruta_archivo):
        try:
            # Cambiar extensión del archivo de .vtk a _histo.txt
            base, _ = os.path.splitext(ruta_archivo)
            ruta_modificada = f"{base}_histo.txt"
            numero = base.split('_')[-1]

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
                contenido_html = "<b>Nivel de Refinamiento: " + numero + "</b><br><br><br>"
                contenido_html += "<b>Ángulos Críticos:</b><br><br>"
                if angulo_triangulo:
                    contenido_html += formatear_angulo("Triángulos", angulo_triangulo)
                if angulo_cuadrado:
                    contenido_html += formatear_angulo("Cuadriláteros", angulo_cuadrado)
            else:
                contenido_html = "<b>No se encontraron líneas de ángulos para triángulos ni cuadriláteros.</b>"

            self.label_derecho.setText(contenido_html)

        except Exception as e:
            self.label_derecho.setText(f"<b>Error al leer el archivo:</b><br>{e}") """

    # Métodos para cada acción

    # Moverse entre los poly
    def accion_n(self):
        if not self.switcher:
            return
        polys_cargados = list(self.switcher.file_dict.keys())
        if not polys_cargados:
            return
        
        try:
            i = polys_cargados.index(self.switcher.current_poly)
            next_index = (i + 1) % len(polys_cargados)
            next_poly = polys_cargados[next_index]
        except ValueError:
            next_poly = polys_cargados[0]
        
        archivos = self.switcher.file_dict.get(next_poly, [])
        if archivos:
            self.switcher.current_poly = next_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.actualizar_panel_derecho(archivos[0])

            items = self.lista_archivos.findItems(next_poly, Qt.MatchExactly)
            if items:
                self.lista_archivos.setCurrentItem(items[0])
            
            # Eliminar los puntos críticos si están
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()

        # if self.switcher:
        #     self.switcher.current_index = (self.switcher.current_index + 1) % len(self.switcher.file_list)
        #     self.switcher.load_model(self.switcher.file_list[self.switcher.current_index])
        #     self.switcher.clear_extra_models()
        #     self.switcher.toggle_load = False

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
        dialogo = MeshGeneratorController(self)

        if dialogo.exec_() == QDialog.Accepted:
            ruta_poly = dialogo.archivos_seleccionados[0]
            nombre_poly = os.path.basename(ruta_poly)

            if nombre_poly not in self.rutas_archivos:
                self.rutas_archivos[nombre_poly] = dialogo.generated_files
                self.lista_archivos.addItem(nombre_poly)

            items = self.lista_archivos.findItems(nombre_poly, Qt.MatchExactly)
            if items:
                self.lista_archivos.setCurrentItem(items[0]) 

            if not self.switcher:
                self.switcher = ModelSwitcher(self.renderer, self.interactor, {nombre_poly: dialogo.generated_files})
            else:
                self.switcher.file_dict[nombre_poly] = dialogo.generated_files

            self.switcher.current_poly = nombre_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            # self.actualizar_panel_derecho(dialogo.generated_files[0])

        elif dialogo.exec_() == QDialog.Rejected:
            return
        
        print("Rutas_Archivo:", self.rutas_archivos)
        print("Lista_Archivos:", self.lista_archivos)
        print("Generated_Files:", dialogo.generated_files)

    def mostrar_contenido(self, item):
        nombre_poly = item.text()
        archivos_vtk = self.rutas_archivos.get(nombre_poly)

        if archivos_vtk and self.switcher:
            self.switcher.current_poly = nombre_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.actualizar_panel_derecho(archivos_vtk[0])

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
                
=======
        self.switcher = None
>>>>>>> 0e18fd0544ffd6977e098ebd3592d57a4e8f298d

    # Eventos de drag & drop
    def dragEnterEvent(self, event):
        dragEnterEvent(self, event)

    def dropEvent(self, event):
        dropEvent(self, event)

<<<<<<< HEAD
        if not ruta_archivo.endswith('.poly'):
            QMessageBox.critical(self, "Error", "El archivo no es un archivo .poly válido.")
            return

        if dialogo.exec_() == QDialog.Accepted:
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                # Agregar a lista lateral
                nombre = os.path.basename(ruta_archivo)
                if nombre not in self.rutas_archivos:
                    self.rutas_archivos[nombre] = ruta_archivo
                    self.lista_archivos.addItem(nombre)
                # Mostrar en el panel central directamente (opcional)
                self.vista_texto.setPlainText(contenido)
            except Exception as e:
                QMessageBox.critical(self, "Error al leer archivo", str(e))
    
    def navegar_anterior(self):
        """Función para navegar al modelo anterior numéricamente"""
        if not self.switcher:
            return

        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            return

        if self.switcher.current_index > 0:
            self.switcher.anterior_modelo()
            self.actualizar_panel_derecho(archivos[self.switcher.current_index])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
        else:
            QMessageBox.information(self, "Inicio", "Ya estás en el primer modelo.")

    def navegar_siguiente(self):
        """Función para navegar al siguiente modelo numéricamente"""
        if not self.switcher:
            return

        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            return

        if self.switcher.current_index + 1 < len(archivos):
            self.switcher.siguiente_modelo()
            # self.actualizar_panel_derecho(archivos[self.switcher.current_index])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
        else:
            QMessageBox.information(self, "Fin", "Ya estás en el último modelo.")

    def iniciar_animacion(self):
        """Inicia el avance automático de modelos"""
        if self.switcher and self.switcher.file_dict:
            self.boton_play.setEnabled(False)
            self.boton_pausa.setEnabled(True)
            self.timer_animacion.start()
            
    def detener_animacion(self):
        """Detiene el avance automático"""
        self.timer_animacion.stop()
        self.boton_play.setEnabled(True)
        self.boton_pausa.setEnabled(False)
        
    def avance_automatico(self):
        """Función que se ejecuta automáticamente cada intervalo de tiempo"""
        if not self.switcher:
            self.detener_animacion()
            return
            
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            self.detener_animacion()
            return
            
        # Si estamos en el último modelo, volver al primero
        if self.switcher.current_index + 1 >= len(archivos):
            self.reiniciar_secuencia()
        else:
            self.navegar_siguiente()
            
    def reiniciar_secuencia(self):
        """Vuelve al primer modelo de la secuencia actual"""
        if not self.switcher:
            return
            
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if archivos:
            self.switcher.current_index = 0
            self.switcher._load_current()
            # self.actualizar_panel_derecho(archivos[0])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
            
            # Resaltar el elemento correspondiente en la lista
            items = self.lista_archivos.findItems(self.switcher.current_poly, Qt.MatchExactly)
            if items:
                self.lista_archivos.setCurrentItem(items[0])

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
=======
    def closeEvent(self, event):
        closeEvent(self, event)
>>>>>>> 0e18fd0544ffd6977e098ebd3592d57a4e8f298d
