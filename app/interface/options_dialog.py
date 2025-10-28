from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QCheckBox, QPushButton, 
                             QApplication, QComboBox, QLabel, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import QTranslator, QEvent
from app.logic.export_utils import ExportManager

class OpcionesDialog(QDialog):
    def __init__(self, parent=None, poly_name=None, refinement_level=None):
        super().__init__(parent)
        
        # Guardamos la app y la ventana principal (parent)
        self.app = QApplication.instance()
        self.main_window = parent 

        self.setWindowTitle("Opciones avanzadas") # Se traducirá en retranslateUi
        self.setFixedSize(300, 200) # Un poco más alto para el nuevo widget

        # --- Widgets existentes ---
        self.checkbox = QCheckBox("") # Texto en retranslateUi
        if self.main_window:
            self.checkbox.setChecked(self.main_window.ignorar_limite_hardware)
        else:
            self.checkbox.setChecked(False)

        self.btn_exportar = QPushButton("") # Texto en retranslateUi
        self.btn_exportar.clicked.connect(self.exportar_historial)
        
        self.btn_ok = QPushButton("") # Texto en retranslateUi
        self.btn_ok.clicked.connect(self.accept)

        # Lógica de exportación existente
        self.export_manager = ExportManager(self)
        self.poly_name = poly_name
        self.refinement_level = refinement_level

        # --- NUEVO: Selector de Idioma ---
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("") # Texto en retranslateUi
        self.lang_combo = QComboBox()
        
        # Añadimos los idiomas (Texto visible, código-del-idioma)
        self.lang_combo.addItem("Español", userData="es")
        self.lang_combo.addItem("English", userData="en")

        # Seleccionar el idioma actual en el combo
        self.update_combo_selection()

        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        
        # Conexión del combo
        self.lang_combo.currentIndexChanged.connect(self.switch_language)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.btn_exportar)
        layout.addLayout(lang_layout) # Añadimos el layout del idioma
        layout.addStretch(1) # Espaciador
        layout.addWidget(self.btn_ok)
        self.setLayout(layout)

        # Carga inicial de texto
        self.retranslateUi()

    def switch_language(self, index):
        """
        Se llama cuando el QComboBox cambia.
        """
        # 1. Obtenemos el código de idioma ("es" o "en") del item seleccionado
        lang_code = self.lang_combo.itemData(index)
        
        # Evitar recarga si ya es el idioma actual
        current_lang = self.app.translator.language().split('_')[0]
        if current_lang == lang_code:
            return

        # 2. Quitamos el traductor viejo
        self.app.removeTranslator(self.app.translator)

        # 3. Creamos, cargamos e instalamos el nuevo traductor
        translator = QTranslator()
        
        path = f"translations/meshstep_{lang_code}.qm"
        alt_path = f"../translations/meshstep_{lang_code}.qm"
        
        if translator.load(path) or translator.load(alt_path):
            self.app.translator = translator # Guardamos el nuevo como el "actual"
            self.app.installTranslator(self.app.translator)
        else:
            print(f"Error: No se pudo cargar la traducción para {lang_code}")
            # Si falla, reinstalamos el viejo
            self.app.installTranslator(self.app.translator)

    def retranslateUi(self):
        """
        Traduce el texto de este diálogo
        """
        self.setWindowTitle(self.tr("Opciones avanzadas"))
        self.checkbox.setText(self.tr("Ignorar límite de hardware"))
        self.btn_ok.setText(self.tr("Aceptar"))
        self.btn_exportar.setText(self.tr("Exportar historial de mallado"))
        self.lang_label.setText(self.tr("Idioma:"))

    def changeEvent(self, event):
        """
        Escucha el evento de cambio de idioma para traducir este diálogo
        """
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
            self.update_combo_selection() # Sincroniza el combo
        else:
            super().changeEvent(event)

    def update_combo_selection(self):
        """ Sincroniza el QComboBox con el idioma actual de la app """
        current_lang = self.app.translator.language().split('_')[0]
        if current_lang == "en":
            self.lang_combo.setCurrentIndex(1)
        else:
            self.lang_combo.setCurrentIndex(0)

    def accept(self):
        """
        Al aceptar, guardamos el estado del checkbox en la ventana principal
        """
        if self.main_window:
            self.main_window.ignorar_limite_hardware = self.checkbox.isChecked()
        super().accept()

    def exportar_historial(self):
        """
        Lógica de exportación existente, con mensaje de error traducible.
        """
        success, message = self.export_manager.export_log_file(self.poly_name, self.refinement_level)
        if not success and message == "no_log_file":
            # Usamos self.tr() para que el error también se traduzca
            QMessageBox.critical(self, self.tr("Error"), 
                                 self.tr("No se encontró ningún archivo de historial para exportar."))