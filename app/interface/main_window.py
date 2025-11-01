from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
                             QSplitter, QStyle, QTabWidget,
                             QMenuBar, QAction, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap
from app.visualization.RefinementViewer import RefinementViewer
from app.interface.panel_derecho import PanelDerecho
from app.interface.panel_pap import PanelPAP
from app.visualization.vtkplayer import VTKPlayer
from app.logic.main_window_logic import (
    dragEnterEvent, dropEvent,
    abrir_dialogo_carga, mostrar_contenido, mostrar_menu_contextual,
    abrir_opciones_dialog, cambiar_visualizador, closeEvent, abrir_manual,
    accion_w, accion_s
)
#from app.logic.export_utils import ExportManager

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
        self.file_menu = self.menubar.addMenu("")
        self.edit_menu = self.menubar.addMenu("")
        self.help_menu = self.menubar.addMenu("")
        self.view_menu = self.menubar.addMenu("")
        self.color_menu = self.menubar.addMenu("")

        # Iconos estándar
        icon_cargar = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        icon_opciones = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)

        # Botones en barra horizontal
        self.boton_cargar = QPushButton(icon_cargar, "", self)
        self.boton_cargar.clicked.connect(lambda: abrir_dialogo_carga(self))

        self.boton_opciones = QPushButton(icon_opciones, "", self)
        self.boton_opciones.clicked.connect(lambda: abrir_opciones_dialog(self))

        self.boton_wireframe = QPushButton("", self)
        self.boton_wireframe.clicked.connect(lambda: accion_w(self))

        self.boton_solido = QPushButton("", self)
        self.boton_solido.clicked.connect(lambda: accion_s(self))

        # Barra horizontal de botones
        barra_botones = QHBoxLayout()
        barra_botones.addWidget(self.boton_cargar)
        barra_botones.addWidget(self.boton_opciones)
        barra_botones.addWidget(self.boton_wireframe)
        barra_botones.addWidget(self.boton_solido)
        barra_botones.addStretch(1)  # Para que los botones queden a la izquierda

        # Acciones del menú
        self.action_cargar = QAction("", self)
        self.action_cargar.triggered.connect(lambda: abrir_dialogo_carga(self))
        self.file_menu.addAction(self.action_cargar)

        self.action_opciones = QAction("", self)
        self.action_opciones.triggered.connect(lambda: abrir_opciones_dialog(self))
        self.edit_menu.addAction(self.action_opciones)

        self.action_help = QAction("", self)
        self.action_help.triggered.connect(lambda: abrir_manual(self))
        self.help_menu.addAction(self.action_help)

        #self.action_exportar = QAction("", self)
        #self.action_exportar.triggered.connect(lambda: self.exportar_historial())
        #self.file_menu.addAction(self.action_exportar)

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

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(lambda item: mostrar_contenido(self, item))
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(lambda pos: mostrar_menu_contextual(self, pos))

        self.refinement_viewer = RefinementViewer(self)
        self.panel_derecho = PanelDerecho(parent=self)
        self.panel_pap = PanelPAP(parent=self)

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
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_layout.addWidget(self.panel_derecho)
        right_layout.addWidget(self.panel_pap)
        right_container.setLayout(right_layout)
        splitter.addWidget(right_container)
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

    def retranslateUi(self):
        self.setWindowTitle(self.tr("MeshStep"))
        self.file_menu.setTitle(self.tr("Archivo"))
        self.edit_menu.setTitle(self.tr("Editar"))
        self.help_menu.setTitle(self.tr("Ayuda"))
        self.boton_cargar.setText(self.tr("Cargar archivos"))
        self.boton_opciones.setText(self.tr("Opciones"))
        self.boton_wireframe.setText(self.tr("Wireframe"))
        self.boton_solido.setText(self.tr("Solido"))
        # Textos traducibles para el menú 'Vista' y sus acciones
        self.view_menu.setTitle(self.tr("Vista"))
        self.action_wireframe.setText(self.tr("Wireframe"))
        self.action_wireframe.setToolTip(self.tr("Alternar al modo wireframe (W)"))
        self.action_solido.setText(self.tr("Sólido"))
        self.action_solido.setToolTip(self.tr("Alternar al modo sólido (S)"))
        self.action_cargar.setText(self.tr("Cargar archivos"))
        self.color_menu.setTitle(self.tr("Coloreos"))
        self.action_area.setText(self.tr("Área"))
        self.action_angulo_minimo.setText(self.tr("Ángulo Mínimo"))
        self.action_relacion_aspecto.setText(self.tr("Relación de Aspecto"))
        self.action_opciones.setText(self.tr("Opciones"))
        self.action_help.setText(self.tr("Manual"))
        #self.action_exportar.setText(self.tr("Exportar historial de mallado"))
        self.tab_widget.setTabText(0, self.tr("Niveles de refinación"))
        self.tab_widget.setTabText(1, self.tr("Paso a paso"))

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        else:
            super().changeEvent(event)

    # Eventos de drag & drop
    def dragEnterEvent(self, event):
        dragEnterEvent(self, event)

    def dropEvent(self, event):
        dropEvent(self, event)

    def closeEvent(self, event):
        closeEvent(self, event)

#    def exportar_historial(self):
#        """
#        Exporta el historial usando ExportManager.
#        Intenta usar el archivo seleccionado en la lista; si no hay ninguno, pasa None.
#        Muestra mensaje de error traducible si no existe archivo de historial.
#        """
#        current_item = self.lista_archivos.currentItem()
#        poly_name = current_item.text() if current_item else None
#        refinement_level = None  # ajustar si tienes forma de obtener el nivel actual
#
#        export_manager = ExportManager(self)
#        success, message = export_manager.export_log_file(poly_name, refinement_level)
#        if not success and message == "no_log_file":
#            QMessageBox.critical(self, self.tr("Error"),
#                                 self.tr("No se encontró ningún archivo de historial para exportar."))
#        elif success:
#            QMessageBox.information(self, self.tr("Éxito"),
#                                    self.tr("Historial exportado correctamente."))
