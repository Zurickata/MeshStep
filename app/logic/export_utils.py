import os
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths

class ExportManager:
    def __init__(self, parent_window=None):
        self.parent = parent_window

    def get_log_file_path(self, poly_name=None, refinement_level=None):
        """
        Obtiene la ruta del archivo de log del mallado según el nombre del input y nivel de refinamiento.
        Si no se especifica, busca el historial genérico.
        """
        outputs_dir = Path("outputs")
        if poly_name and refinement_level is not None:
            # Ejemplo: a_output_5_historial.txt
            base_name = Path(poly_name).stem
            log_name = f"{base_name}_output_{refinement_level}_historial.txt"
            log_path = outputs_dir / log_name
            if log_path.exists():
                return str(log_path)
        elif poly_name:
            # Buscar cualquier historial que empiece con el nombre base
            base_name = Path(poly_name).stem
            files = list(outputs_dir.glob(f"{base_name}_output*_historial.txt"))
            if files:
                return str(files[-1])  # El último por defecto
        # Fallback: buscar cualquier historial
        files = list(outputs_dir.glob("*_output*_historial.txt"))
        if files:
            return str(files[-1])
        return None

    def validate_log_file(self, poly_name=None, refinement_level=None):
        log_path = self.get_log_file_path(poly_name, refinement_level)
        if not log_path or not os.path.exists(log_path):
            return False, "No se encontró ningún archivo de registro del mallado"
        if os.path.getsize(log_path) == 0:
            return False, "El archivo de registro está vacío"
        return True, log_path

    def read_log_content(self, log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error al leer el archivo: {str(e)}"

    def export_log_file(self, poly_name=None, refinement_level=None):
        is_valid, message = self.validate_log_file(poly_name, refinement_level)
        if not is_valid:
            return False, "no_log_file"
        log_path = message
        default_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Exportar registro de mallado",
            os.path.join(default_dir, os.path.basename(log_path)),
            "Archivos de texto (*.txt);;Todos los archivos (*)"
        )
        if not file_path:
            return False, "export_cancelled"
        try:
            content = self.read_log_content(log_path)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            success_msg = f"Registro exportado exitosamente a:\n{file_path}"
            if self.parent:
                QMessageBox.information(self.parent, "Éxito", success_msg)
            return True, success_msg
        except Exception as e:
            error_msg = f"Error al exportar el registro: {str(e)}"
            if self.parent:
                QMessageBox.critical(self.parent, "Error", error_msg)
            return False, error_msg
