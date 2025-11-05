from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
                             QSplitter, QStyle, QTabWidget,
                             QMenuBar, QAction, QLabel, QMessageBox, QToolButton, QFrame, QFileDialog, QActionGroup)
from PyQt5.QtCore import Qt, QEvent, QSize
from PyQt5.QtGui import QPixmap
from app.visualization.RefinementViewer import RefinementViewer
from app.interface.panel_derecho import PanelDerecho
from app.interface.panel_pap import PanelPAP
from app.visualization.vtkplayer import VTKPlayer
from app.logic.main_window_logic import (
    dragEnterEvent, dropEvent,
    abrir_dialogo_carga, mostrar_contenido, mostrar_menu_contextual,
    abrir_opciones_dialog, cambiar_visualizador, closeEvent, abrir_manual,
    accion_w, accion_s, abrir_dialogo_vtk_externo
)
from app.logic.export_utils import ExportManager

from .panel_derecho import PanelDerecho

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        self.perfil_actual = "principiante" 
        self.widgets_expertos = []

        self.ignorar_limite_hardware = False

        logo_label = QLabel()
        icono_svg = QPixmap("meshsteppng.svg")
        logo_label.setPixmap(icono_svg.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.menubar = QMenuBar(self)
        self.file_menu = self.menubar.addMenu("")
        self.edit_menu = self.menubar.addMenu("")
        self.help_menu = self.menubar.addMenu("")
        self.view_menu = self.menubar.addMenu("")
        self.color_menu = self.menubar.addMenu("")
        self.reload_menu = self.menubar.addMenu("")

        #Perfiles
        self.perfil_menu = self.menubar.addMenu("") 
        grupo_perfil = QActionGroup(self)
        grupo_perfil.setExclusive(True)

        grupo_perfil.setExclusive(True)

        self.accion_principiante = QAction("", self, checkable=True)
        self.accion_principiante.setChecked(True)
        self.accion_principiante.triggered.connect(lambda: self.cambiar_perfil("principiante"))
        self.perfil_menu.addAction(self.accion_principiante)
        grupo_perfil.addAction(self.accion_principiante)

        self.accion_experto = QAction("", self, checkable=True)
        self.accion_experto.triggered.connect(lambda: self.cambiar_perfil("experto"))
        self.perfil_menu.addAction(self.accion_experto)
        grupo_perfil.addAction(self.accion_experto)

        self.widgets_expertos.append(self.edit_menu.menuAction()) # Menú "Editar" (Opciones) es experto
        self.widgets_expertos.append(self.color_menu.menuAction()) # Menú "Coloreos" es experto
        self.widgets_expertos.append(self.reload_menu.menuAction()) # Menú "Reestablecer" es experto

        # Iconos estándar
        icon_cargar = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        icon_opciones = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)

        # Botones en barra horizontal
        #self.boton_cargar = QPushButton(icon_cargar, "", self)
        #self.boton_cargar.clicked.connect(lambda: abrir_dialogo_carga(self))

        #self.boton_opciones = QPushButton(icon_opciones, "", self)
        #self.boton_opciones.clicked.connect(lambda: abrir_opciones_dialog(self))

        #self.boton_wireframe = QPushButton("", self)
        #self.boton_wireframe.clicked.connect(lambda: accion_w(self))

        #self.boton_solido = QPushButton("", self)
        #self.boton_solido.clicked.connect(lambda: accion_s(self))

        #self.boton_color_area = QPushButton("", self)
        #self.boton_color_area.clicked.connect(lambda: self.refinement_viewer.accion_area() if getattr(self, "refinement_viewer", None) else None)

        #self.boton_color_angulo_minimo = QPushButton("", self)
        #self.boton_color_angulo_minimo.clicked.connect(lambda: self.refinement_viewer.accion_angulo_minimo() if getattr(self, "refinement_viewer", None) else None)

        #self.boton_color_relacion_aspecto = QPushButton("", self)
        #self.boton_color_relacion_aspecto.clicked.connect(lambda: self.refinement_viewer.accion_relacion_aspecto() if getattr(self, "refinement_viewer", None) else None)

        # Barra: usar QToolButton para un aspecto más profesional
        icon_size = QSize(22, 22)

        self.boton_cargar = QToolButton(self)
        self.boton_cargar.setIcon(icon_cargar)
        self.boton_cargar.setIconSize(icon_size)
        self.boton_cargar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.boton_cargar.clicked.connect(lambda: abrir_dialogo_carga(self))

        self.boton_opciones = QToolButton(self)
        self.boton_opciones.setIcon(icon_opciones)
        self.boton_opciones.setIconSize(icon_size)
        self.boton_opciones.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.boton_opciones.clicked.connect(lambda: abrir_opciones_dialog(self))
        self.widgets_expertos.append(self.boton_opciones) #Perfil: Widget experto

        self.boton_wireframe = QToolButton(self)
        self.boton_wireframe.setIconSize(icon_size)
        self.boton_wireframe.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.boton_wireframe.clicked.connect(lambda: accion_w(self))

        self.boton_solido = QToolButton(self)
        self.boton_solido.setIconSize(icon_size)
        self.boton_solido.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.boton_solido.clicked.connect(lambda: accion_s(self))

        self.boton_color_area = QToolButton(self)
        self.boton_color_area.setIconSize(icon_size)
        self.boton_color_area.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.boton_color_area.clicked.connect(lambda: self.refinement_viewer.accion_area() if getattr(self, "refinement_viewer", None) else None)
        self.widgets_expertos.append(self.boton_color_area) #Perfil: Widget experto

        self.boton_color_angulo_minimo = QToolButton(self)
        self.boton_color_angulo_minimo.setIconSize(icon_size)
        self.boton_color_angulo_minimo.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.boton_color_angulo_minimo.clicked.connect(lambda: self.refinement_viewer.accion_angulo_minimo() if getattr(self, "refinement_viewer", None) else None)
        
        self.widgets_expertos.append(self.boton_color_angulo_minimo) #Perfil: Widget experto

        self.boton_color_relacion_aspecto = QToolButton(self)
        self.boton_color_relacion_aspecto.setIconSize(icon_size)
        self.boton_color_relacion_aspecto.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.boton_color_relacion_aspecto.clicked.connect(lambda: self.refinement_viewer.accion_relacion_aspecto() if getattr(self, "refinement_viewer", None) else None)
        
        self.widgets_expertos.append(self.boton_color_relacion_aspecto) #Perfil: Widget experto

        # Labels compactos entre grupos
        self.vista_label = QLabel("")
        self.vista_label.setAlignment(Qt.AlignCenter)
        self.vista_label.setStyleSheet("padding:4px; font-weight:600;")

        self.colores_label = QLabel("")
        self.colores_label.setAlignment(Qt.AlignCenter)
        self.colores_label.setStyleSheet("padding:4px; font-weight:600;")
        self.widgets_expertos.append(self.colores_label) #Perfil: Widget experto


        # Barra horizontal de botones con separadores
        # Barra horizontal de botones con separadores
        barra_botones = QHBoxLayout()
        barra_botones.setSpacing(8)
        
        # --- WIDGETS DE LA BARRA ---
        barra_botones.addWidget(self.boton_cargar)
        barra_botones.addWidget(self.boton_opciones) 
        sep1 = QFrame(self); sep1.setFrameShape(QFrame.VLine); sep1.setFrameShadow(QFrame.Sunken); sep1.setFixedHeight(28)
        barra_botones.addWidget(sep1)
        self.widgets_expertos.append(sep1) #Perfil: Widget experto
        barra_botones.addWidget(self.vista_label)
        barra_botones.addWidget(self.boton_wireframe)
        barra_botones.addWidget(self.boton_solido)
        sep2 = QFrame(self); sep2.setFrameShape(QFrame.VLine); sep2.setFrameShadow(QFrame.Sunken); sep2.setFixedHeight(28)
        barra_botones.addWidget(sep2)
        self.widgets_expertos.append(sep2) #Perfil: Widget experto
        barra_botones.addWidget(self.colores_label)
        barra_botones.addWidget(self.boton_color_area)
        barra_botones.addWidget(self.boton_color_angulo_minimo)
        barra_botones.addWidget(self.boton_color_relacion_aspecto)
        
        # ---------------------------
        
        barra_botones.addStretch(1)  # Para que los botones queden a la izquierda

        # Acciones del menú
        self.action_cargar = QAction("", self)
        self.action_cargar.triggered.connect(lambda: abrir_dialogo_carga(self))
        self.file_menu.addAction(self.action_cargar)
        self.action_cargar_vtk = QAction("", self)
        self.action_cargar_vtk.triggered.connect(lambda: abrir_dialogo_vtk_externo(self))
        self.file_menu.addAction(self.action_cargar_vtk)
        self.widgets_expertos.append(self.action_cargar_vtk) #Perfil: Widget experto

        self.action_opciones = QAction("", self)
        self.action_opciones.triggered.connect(lambda: abrir_opciones_dialog(self))
        self.edit_menu.addAction(self.action_opciones)

        self.action_help = QAction("", self)
        self.action_help.triggered.connect(lambda: abrir_manual(self))
        self.help_menu.addAction(self.action_help)

        self.action_exportar = QAction("", self)
        self.action_exportar.triggered.connect(lambda: self.exportar_historial())
        self.file_menu.addAction(self.action_exportar)
        self.widgets_expertos.append(self.action_exportar) #Perfil: Widget experto

        self.action_visual = QAction("", self)
        #self.action_visual.triggered.connect(lambda: cambiar_visualizador(self))

        # Acciones de vista: Wireframe / Sólido dentro del menú 'Vista'
        self.action_wireframe = QAction("", self)
        self.action_wireframe.triggered.connect(lambda: accion_w(self))
        self.view_menu.addAction(self.action_wireframe)

        self.action_solido = QAction("", self)
        self.action_solido.triggered.connect(lambda: accion_s(self))
        self.view_menu.addAction(self.action_solido)

        # Menú de colores

        self.action_area = QAction("", self)
        self.action_area.triggered.connect(
            lambda: self.refinement_viewer.accion_area() if getattr(self, "refinement_viewer", None) else None
        )
        self.color_menu.addAction(self.action_area)

        self.action_angulo_minimo = QAction("", self)
        self.action_angulo_minimo.triggered.connect(lambda: self.refinement_viewer.accion_angulo_minimo() if getattr(self, "refinement_viewer", None) else None)
        self.color_menu.addAction(self.action_angulo_minimo)

        self.action_relacion_aspecto = QAction("", self)
        self.action_relacion_aspecto.triggered.connect(lambda: self.refinement_viewer.accion_relacion_aspecto() if getattr(self, "refinement_viewer", None) else None)
        self.color_menu.addAction(self.action_relacion_aspecto)

        #angulo critico
        self.view_menu.addSeparator()

        self.action_puntos_criticos = QAction("", self)
        self.action_puntos_criticos.setShortcut("A")
        self.action_puntos_criticos.triggered.connect(
            lambda: self.panel_derecho.toggle_puntos_criticos() if getattr(self, "panel_derecho", None) else None
        )
        self.view_menu.addAction(self.action_puntos_criticos)
        self.widgets_expertos.append(self.action_puntos_criticos)

        # Acción para mostrar/ocultar una malla de referencia VTK
        self.action_referencia = QAction("", self)
        self.action_referencia.triggered.connect(lambda: self.toggle_reference_action())
        self.view_menu.addAction(self.action_referencia)
        self.widgets_expertos.append(self.action_referencia) #Perfil: Widget experto

        # Acción para togglear visibilidad del preview ya cargado (no carga archivos)
        self.action_toggle_preview = QAction("", self)
        self.action_toggle_preview.triggered.connect(lambda: self.toggle_preview_action())
        self.view_menu.addAction(self.action_toggle_preview)
        self.widgets_expertos.append(self.action_toggle_preview) #Perfil: Widget experto

        #agrego resets

        self.action_reset_camara = QAction("", self)
        self.action_reset_camara.setShortcut("R")
        self.action_reset_camara.triggered.connect(
            lambda: self.panel_derecho.resetear_camara() if getattr(self, "panel_derecho", None) else None
        )
        self.reload_menu.addAction(self.action_reset_camara)

        self.action_recargar = QAction("", self)
        self.action_recargar.setShortcut("L")
        self.action_recargar.triggered.connect(
            lambda: self.panel_derecho.reload_modelo() if getattr(self, "panel_derecho", None) else None
        )
        self.reload_menu.addAction(self.action_recargar)


        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(lambda item: mostrar_contenido(self, item))
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(lambda pos: mostrar_menu_contextual(self, pos))

        self.refinement_viewer = RefinementViewer(self)
        self.panel_derecho = PanelDerecho(parent=self)
        self.panel_pap = PanelPAP(parent=self)

        self.widgets_expertos.append(self.panel_derecho) #Perfil: Widget experto
        

        # Integrar los panels derecho en un contenedor para poder alternarlos
        self.refinement_viewer.panel_derecho = self.panel_derecho
        self.panel_derecho.refinement_viewer = self.refinement_viewer
        # panel_pap quedará oculto hasta que se entre en Paso a Paso
        self.panel_pap.hide()

        self.rutas_archivos = {}
        self.rutas_octree = {}

        self.vtk_player = VTKPlayer(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.refinement_viewer, "")
        self.tab_widget.addTab(self.vtk_player, "")
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

        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(self.panel_central)
        # Añadimos ambos panels al splitter dentro de un contenedor derecho
        self.right_container = QWidget() #right_container = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_layout.addWidget(self.panel_derecho)
        right_layout.addWidget(self.panel_pap)
        self.right_container.setLayout(right_layout)
        splitter.addWidget(self.right_container)


        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)

        layout = QVBoxLayout()
        layout.setMenuBar(self.menubar)
        layout.addLayout(barra_botones)
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setAcceptDrops(True)

        self.switcher = None
        self.retranslateUi()

        self.actualizar_visibilidad_ui()

    def retranslateUi(self):
        self.setWindowTitle(self.tr("MeshStep"))
        self.file_menu.setTitle(self.tr("Archivo"))
        self.edit_menu.setTitle(self.tr("Editar"))
        self.help_menu.setTitle(self.tr("Ayuda"))
        self.boton_cargar.setText(self.tr("Cargar archivos"))
        self.boton_opciones.setText(self.tr("Opciones"))
        self.boton_wireframe.setText(self.tr("Wireframe"))
        self.boton_solido.setText(self.tr("Solido"))
        self.boton_color_area.setText(self.tr("Área"))
        self.boton_color_angulo_minimo.setText(self.tr("Ángulo Mínimo"))
        self.boton_color_relacion_aspecto.setText(self.tr("Relación de Aspecto"))
        self.vista_label.setText(self.tr("Vista:"))
        self.colores_label.setText(self.tr("Coloreos:"))
        # Textos traducibles para el menú 'Vista' y sus acciones
        self.view_menu.setTitle(self.tr("Vista"))
        self.action_wireframe.setText(self.tr("Wireframe"))
        self.action_wireframe.setToolTip(self.tr("Alternar al modo wireframe (W)"))
        self.action_solido.setText(self.tr("Sólido"))
        self.action_solido.setToolTip(self.tr("Alternar al modo sólido (S)"))
        self.action_cargar.setText(self.tr("Cargar archivos"))
        self.action_cargar_vtk.setText(self.tr("Cargar malla VTK"))
        self.color_menu.setTitle(self.tr("Coloreos"))
        self.action_area.setText(self.tr("Área"))
        self.action_angulo_minimo.setText(self.tr("Ángulo Mínimo"))
        self.action_relacion_aspecto.setText(self.tr("Relación de Aspecto"))
        self.reload_menu.setTitle(self.tr("Reestablecer"))
        self.action_reset_camara.setText(self.tr("Restablecer Cámara"))
        self.action_reset_camara.setToolTip(self.tr("Restablecer la cámara (R)"))
        self.action_recargar.setText(self.tr("Recargar Modelo"))
        self.action_recargar.setToolTip(self.tr("Recargar modelo (L)"))
        self.action_puntos_criticos.setText(self.tr("Puntos Críticos"))
        self.action_puntos_criticos.setToolTip(self.tr("Alternar puntos críticos (P)"))
        self.action_referencia.setText(self.tr("Referencia"))
        self.action_referencia.setToolTip(self.tr("Mostrar/ocultar malla de referencia (VTK)"))
        self.action_toggle_preview.setText(self.tr("Mostrar/Ocultar referencia"))
        self.action_toggle_preview.setToolTip(self.tr("Alternar visibilidad del preview de referencia (no carga archivos)"))
        self.action_opciones.setText(self.tr("Opciones"))
        self.action_help.setText(self.tr("Manual"))
        self.action_exportar.setText(self.tr("Exportar historial de mallado"))
        self.tab_widget.setTabText(0, self.tr("Niveles de refinación"))
        self.tab_widget.setTabText(1, self.tr("Paso a paso"))

        # --- INICIO: LÓGICA DE PERFILES (Traducciones) ---
        self.perfil_menu.setTitle(self.tr("Perfil"))
        self.accion_principiante.setText(self.tr("Principiante"))
        self.accion_principiante.setToolTip(self.tr("Ocultar herramientas avanzadas"))
        self.accion_experto.setText(self.tr("Experto"))
        self.accion_experto.setToolTip(self.tr("Mostrar todas las herramientas"))
        # --- FIN: LÓGICA DE PERFILES (Traducciones) ---

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        else:
            super().changeEvent(event)

    def toggle_reference_action(self):
        """Load a VTK reference from the selected list item or open a file dialog, then toggle visibility.

        Behavior:
        - If a list item is selected and it maps to one or more files, try to find a .vtk file and load it.
        - Otherwise, fallback to opening the file dialog from the refinement viewer.
        - Ensure the Refinement tab is active.
        """
        # Decide which viewer to use depending on active tab
        viewer = None
        if getattr(self, 'tab_widget', None) and self.tab_widget.currentIndex() == 1:
            viewer = getattr(self, 'vtk_player', None)
        else:
            viewer = getattr(self, 'refinement_viewer', None)

        if not viewer:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Viewer no disponible."))
            return

        current_item = self.lista_archivos.currentItem()
        filepath = None

        if current_item:
            nombre = current_item.text().split(" ")[0]
            archivos = None
            if nombre in self.rutas_archivos:
                archivos = self.rutas_archivos.get(nombre)
            elif nombre in self.rutas_octree:
                archivos = self.rutas_octree.get(nombre)

            # archivos puede ser lista o dict; buscar un .vtk
            if isinstance(archivos, list):
                for a in archivos:
                    if isinstance(a, str) and a.lower().endswith('.vtk'):
                        filepath = a
                        break
            elif isinstance(archivos, dict):
                for v in archivos.values():
                    if isinstance(v, list):
                        for a in v:
                            if isinstance(a, str) and a.lower().endswith('.vtk'):
                                filepath = a
                                break
                        if filepath:
                            break

        if filepath:
            try:
                # viewer can be refinement_viewer or vtk_player
                if hasattr(viewer, 'load_vtk_reference'):
                    viewer.load_vtk_reference(filepath)
                # ensure visible
                if hasattr(viewer, 'toggle_reference'):
                    viewer.toggle_reference()
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), str(e))
        else:
            # Fallback: ask user to pick a vtk file via the viewer method if available
            if hasattr(viewer, 'seleccionar_y_cargar_referencia'):
                viewer.seleccionar_y_cargar_referencia()
            elif hasattr(viewer, 'load_vtk_reference'):
                # open dialog here if viewer doesn't provide it
                filepath, _ = QFileDialog.getOpenFileName(self, self.tr("Seleccionar archivo VTK"), "", "Archivos VTK (*.vtk)")
                if filepath:
                    viewer.load_vtk_reference(filepath)

    def toggle_preview_action(self):
        """Toggle visibility of the already-loaded reference preview without loading a file.

        If no reference is loaded, show an informational message.
        """
        # Target the active viewer (refinement or vtk_player)
        viewer = None
        if getattr(self, 'tab_widget', None) and self.tab_widget.currentIndex() == 1:
            viewer = getattr(self, 'vtk_player', None)
        else:
            viewer = getattr(self, 'refinement_viewer', None)

        if not viewer:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Viewer no disponible."))
            return

        # If a reference widget exists on the chosen viewer, toggle it. Otherwise inform the user.
        if hasattr(viewer, 'reference_widget'):
            try:
                if hasattr(viewer, 'toggle_reference'):
                    viewer.toggle_reference()
                else:
                    QMessageBox.information(self, self.tr("Sin acción"), self.tr("El viewer no soporta toggle_reference."))
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), str(e))
        else:
            QMessageBox.information(
                self,
                self.tr("Sin referencia cargada"),
                self.tr("No hay una malla de referencia cargada. Usa 'Referencia' para cargar una.")
            )

    #LÓGICA DE PERFILES

    def cambiar_perfil(self, perfil):
        """Actualiza el estado y llama a la función que actualiza la UI."""
        if self.perfil_actual != perfil:
            self.perfil_actual = perfil
            print(f"Cambiando a perfil: {self.perfil_actual}")
            self.actualizar_visibilidad_ui()

    def actualizar_visibilidad_ui(self):
        """Recorre la lista de widgets expertos y los muestra o oculta."""
        
        # Determina si deben ser visibles
        es_experto = (self.perfil_actual == "experto")

        # Itera sobre todos los widgets guardados
        for widget in self.widgets_expertos:
            widget.setVisible(es_experto)
    #FIN: LÓGICA DE PERFILES 

    # Eventos de drag & drop
    def dragEnterEvent(self, event):
        dragEnterEvent(self, event)

    def dropEvent(self, event):
        dropEvent(self, event)

    def closeEvent(self, event):
        closeEvent(self, event)

    def exportar_historial(self):
        """
        Exporta el historial usando ExportManager.
        Intenta usar el archivo seleccionado en la lista; si no hay ninguno, pasa None.
        Muestra mensaje de error traducible si no existe archivo de historial.
        """
        current_item = self.lista_archivos.currentItem()
        poly_name = current_item.text() if current_item else None
        refinement_level = None

        export_manager = ExportManager(self)
        success, message = export_manager.export_log_file(poly_name, refinement_level)
        if not success and message == "no_log_file":
            QMessageBox.critical(self, self.tr("Error"),
                                    self.tr("No se encontró ningún archivo de historial para exportar."))
        elif success:
            QMessageBox.information(self, self.tr("Éxito"),
                                    self.tr("Historial exportado correctamente."))
