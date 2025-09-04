import os
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths

class ExportManager:
    def __init__(self, parent_window=None):
        self.parent = parent_window
        self.default_log_path = Path("historial_completo_new.txt")
    
    def get_log_file_path(self):
        """Obtiene la ruta del archivo de log del mallado"""
        # Primero verifica si existe en la ruta por defecto
        if self.default_log_path.exists():
            return str(self.default_log_path)
        
        # Si no existe, busca en otras ubicaciones comunes
        possible_paths = [
            Path("core/quadtree/build/historial_completo_new.txt"),
            Path("historial_completo_new.txt"),
            Path("outputs/logs/historial_completo_new.txt"),
            Path("outputs/historial_completo_new.txt")
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        return None
    
    def validate_log_file(self):
        """Valida que el archivo de log exista y sea válido"""
        log_path = self.get_log_file_path()
        
        if not log_path:
            return False, "No se encontró ningún archivo de registro del mallado"
        
        if not os.path.exists(log_path):
            return False, f"El archivo de registro no existe en: {log_path}"
        
        # Verificar que el archivo no esté vacío
        if os.path.getsize(log_path) == 0:
            return False, "El archivo de registro está vacío"
        
        return True, log_path
    
    def read_log_content(self, log_path):
        """Lee el contenido del archivo de log"""
        try:
            with open(log_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error al leer el archivo: {str(e)}"
    
    def export_log_file(self):
        """Exporta el archivo de log a una ubicación seleccionada por el usuario"""
        # Validar que exista el archivo
        is_valid, message = self.validate_log_file()
        
        if not is_valid:
            return False, "no_log_file"
        
        log_path = message
        
        # Obtener la ubicación para guardar
        default_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Exportar registro de mallado",
            os.path.join(default_dir, "quadtree_log.txt"),
            "Archivos de texto (*.txt);;Todos los archivos (*)"
        )
        
        if not file_path:
            return False, "export_cancelled"
        
        try:
            # Leer y escribir el contenido
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
