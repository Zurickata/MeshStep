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


        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(self.panel_central)
        splitter.addWidget(self.panel_derecho)
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

    # Eventos de drag & drop
    def dragEnterEvent(self, event):
        dragEnterEvent(self, event)

    def dropEvent(self, event):
        dropEvent(self, event)

    def closeEvent(self, event):
        closeEvent(self, event)