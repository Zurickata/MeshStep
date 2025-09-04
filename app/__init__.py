# Importaciones para facilitar el acceso
from app.interface.main_window import MainWindow
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from app.logic.mesh_generator import MeshGeneratorController
from app.visualization.mesh_metrics import calcular_angulo, calcular_metricas_calidad
__all__ = ['MainWindow', 'ModelSwitcher', 'CustomInteractorStyle', 'MeshGeneratorController', 'calcular_angulo', 'calcular_metricas_calidad']