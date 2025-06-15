import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QDialog, QSpinBox, QMessageBox, QTextEdit, QListWidget, QSplitter, QListWidgetItem,
    QMenu
)
from PyQt5.QtCore import Qt


# el popup pa cargar los archivos
class CargarArchivoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargar archivos")
        self.resize(400, 300) #ahora si es resize no es na fixed size tiene mas sentido

        # variables para refinacion rutas labels y cosas
        self.archivos_seleccionados = []
        self.nivel_refinamiento = 1 #placeholder

        self.ruta_archivos = QLabel("Ningún archivo seleccionado")

        #definir y conectar el boton pa abrir el exporador
        self.boton_seleccionar = QPushButton("Seleccionar archivos")
        self.boton_seleccionar.clicked.connect(self.abrir_explorador)

        self.label_refinamiento = QLabel("Nivel de refinamiento:")
        self.spin_refinamiento = QSpinBox()
        self.spin_refinamiento.setRange(1, 100)
        self.spin_refinamiento.setValue(1)
        self.spin_refinamiento.valueChanged.connect(self.verificar_refinamiento)

        self.boton_confirmar = QPushButton("Confirmar")
        self.boton_confirmar.clicked.connect(self.confirmar_datos)


        # Layout del pupup onda ordenar la cuestion
        layout = QVBoxLayout()
        layout.addWidget(self.boton_seleccionar)
        layout.addWidget(self.ruta_archivos)
        layout.addWidget(self.label_refinamiento)
        layout.addWidget(self.spin_refinamiento)
        layout.addWidget(self.boton_confirmar)
        self.setLayout(layout)


    # pa abrir el explorador de archivos
    def abrir_explorador(self):
        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecciona archivos",
            "",
            "Archivos .poly (*.poly)"
        )
        if archivos:
            self.archivos_seleccionados = archivos
            self.ruta_archivos.setText(f"{len(archivos)} archivo(s) seleccionados")

    # que tire el warning si el nivel de refinamiento es muy alto
    def verificar_refinamiento(self):
        valor = self.spin_refinamiento.value()
        if valor > 10:
            QMessageBox.warning(
                self,
                "Advertencia",
                "Los niveles altos de refinamiento (>10) pueden requerir mucha memoria RAM."
            )

    # una peque;ña confirmacion pa ver que se esta cargando
    def confirmar_datos(self):
        if not self.archivos_seleccionados:
            QMessageBox.critical(self, "Error", "Debes seleccionar al menos un archivo .poly antes de confirmar.")
            return

        self.nivel_refinamiento = self.spin_refinamiento.value()

        QMessageBox.information(
            self,
            "Confirmación",
            f"Se cargaron {len(self.archivos_seleccionados)} archivo(s) con nivel de refinamiento: {self.nivel_refinamiento}"
        )
        self.accept()



# ya esta si es la app principal onda lo que se abre primero
class AppPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        #defino primero los widgets y cosas que quiero usar
        self.boton_cargar = QPushButton("Cargar archivos", self)
        self.boton_cargar.clicked.connect(self.abrir_dialogo_carga)

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(self.mostrar_contenido)
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)


        self.vista_texto = QTextEdit(self)
        self.vista_texto.setReadOnly(True)

        self.rutas_archivos = {}

        splitter = QSplitter(Qt.Horizontal)

        # Panel izquierdo
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        layout_izquierdo.addWidget(self.boton_cargar)
        layout_izquierdo.addWidget(self.lista_archivos)
        panel_izquierdo.setLayout(layout_izquierdo)

        # Panel central: vista del archivo
        panel_central = self.vista_texto

        # Panel derecho: solo muestra un texto por ahora
        panel_derecho = QLabel("Soy el panel derecho onda\naqui van las metricas y eso :p\n\npero mira intenta arrastrar los bordes\nes bacan igual")
        panel_derecho.setAlignment(Qt.AlignCenter)

        # Añadir widgets al splitter
        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_central)
        splitter.addWidget(panel_derecho)

        # Control de proporciones
        splitter.setStretchFactor(0, 1)  # Izquierda
        splitter.setStretchFactor(1, 3)  # Centro
        splitter.setStretchFactor(2, 1)  # Derecha

        # Usar el splitter como layout principal
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setAcceptDrops(True)


    #para que el boton ese abra el dialogo de popup de cargar archivos
    def abrir_dialogo_carga(self):
        dialogo = CargarArchivoDialog(self)
        if dialogo.exec_() == QDialog.Accepted:
            for ruta in dialogo.archivos_seleccionados:
                nombre = os.path.basename(ruta)
                if nombre not in self.rutas_archivos:
                    self.rutas_archivos[nombre] = ruta
                    self.lista_archivos.addItem(nombre)

    # cuando se seleccione un poly por al lado que se cargue en el centro
    def mostrar_contenido(self, item):
        nombre = item.text()
        ruta = self.rutas_archivos.get(nombre)
        if ruta:
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.vista_texto.setPlainText(contenido)
            except Exception as e:
                QMessageBox.critical(self, "Error al leer archivo", str(e))
    
    # me fui en la vola le puse pa arrastrar y soltar archivos .poly
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Acepta solo si todos los archivos son .poly
            if all(url.toLocalFile().endswith('.poly') for url in urls):
                event.acceptProposedAction()

    def dropEvent(self, event):
        archivos = [url.toLocalFile() for url in event.mimeData().urls()]
        for archivo in archivos:
            self.procesar_archivo_arrastrado(archivo)
    
    def procesar_archivo_arrastrado(self, ruta_archivo):
        dialogo = CargarArchivoDialog(self)
        dialogo.archivos_seleccionados = [ruta_archivo]
        dialogo.ruta_archivos.setText(ruta_archivo)

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
    
    def mostrar_menu_contextual(self, posicion):
        item = self.lista_archivos.itemAt(posicion)
        if item:
            menu = QMenu()
            accion_eliminar = menu.addAction("Eliminar archivo de la lista")

            accion = menu.exec_(self.lista_archivos.mapToGlobal(posicion))
            if accion == accion_eliminar:
                nombre = item.text()
                # Eliminar del diccionario y de la lista
                if nombre in self.rutas_archivos:
                    del self.rutas_archivos[nombre]
                self.lista_archivos.takeItem(self.lista_archivos.row(item))
                
                # Limpiar el panel central si estaba mostrando el archivo eliminado
                if self.vista_texto.toPlainText():
                    self.vista_texto.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AppPrincipal()
    ventana.show()
    sys.exit(app.exec_())
