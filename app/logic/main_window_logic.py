import os
import re
import glob
import shutil
# --- CAMBIO: Importar QApplication ---
from PyQt5.QtWidgets import QMenu, QListWidgetItem, QMessageBox, QDialog, QApplication
from PyQt5.QtCore import Qt
from app.interface.manual_dialog import ManualDialog
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from app.logic.mesh_generator import MeshGeneratorController
from app.interface.options_dialog import OpcionesDialog

# --- Definimos un nombre de contexto para este archivo ---
# (pylupdate5 lo leerá como un string literal)
CONTEXTO = "MainWindowLogic"

def accion_b(main_window):
    if main_window.refinement_viewer.switcher:
        main_window.refinement_viewer.switcher.clear_extra_models()

def accion_r(main_window):
    if main_window.refinement_viewer.switcher:
        print("🔁 Reseteando cámara y modelo")
        main_window.refinement_viewer.switcher.actor.SetOrientation(0, 0, 0)
        main_window.refinement_viewer.switcher.actor.SetPosition(0, 0, 0)
        main_window.refinement_viewer.switcher.actor.SetScale(1, 1, 1)
        main_window.refinement_viewer.renderer.ResetCamera()
        if isinstance(main_window.refinement_viewer.interactor.GetInteractorStyle(), CustomInteractorStyle):
            main_window.refinement_viewer.interactor.GetInteractorStyle().reset_camera_and_rotation()
        main_window.refinement_viewer.renderer.GetRenderWindow().Render()

def accion_w(main_window):
    if main_window.refinement_viewer.switcher:
        main_window.refinement_viewer.switcher.actor.GetProperty().SetRepresentationToWireframe()
        main_window.refinement_viewer.renderer.GetRenderWindow().Render()

def accion_s(main_window):
    if main_window.refinement_viewer.switcher:
        main_window.refinement_viewer.switcher.actor.GetProperty().SetRepresentationToSurface()
        main_window.refinement_viewer.renderer.GetRenderWindow().Render()

def dragEnterEvent(main_window, event):
    if event.mimeData().hasUrls():
        urls = event.mimeData().urls()
        if all(url.toLocalFile().endswith('.poly') for url in urls):
            event.acceptProposedAction()

def dropEvent(main_window, event):
    archivos = [url.toLocalFile() for url in event.mimeData().urls()]
    for archivo in archivos:
        procesar_archivo_arrastrado(main_window, archivo)

def procesar_archivo_arrastrado(main_window, ruta_archivo):
    dialogo = MeshGeneratorController(main_window)
    dialogo.archivos_seleccionados = [ruta_archivo]
    dialogo.ruta_archivos.setText(ruta_archivo)

    if not ruta_archivo.endswith('.poly'):
        # --- CAMBIO: Usar QApplication.translate ---
        QMessageBox.critical(main_window, 
                             QApplication.translate(CONTEXTO, "Error"), 
                             QApplication.translate(CONTEXTO, "El archivo no es un archivo .poly válido."))
        return

    if dialogo.exec_() == QDialog.Accepted:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            nombre = os.path.basename(ruta_archivo)
            if nombre not in main_window.rutas_archivos:
                main_window.rutas_archivos[nombre] = ruta_archivo
                main_window.lista_archivos.addItem(nombre)
            # main_window.vista_texto.setPlainText(contenido) # Asumo que vista_texto ya no existe
        except Exception as e:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.critical(main_window, QApplication.translate(CONTEXTO, "Error al leer archivo"), str(e))

def _encontrar_serie_completa(main_window, base_name, extension):
    patterns = [
        f"{base_name}_*.{extension}",
        f"{base_name}-*.{extension}",
        f"{os.path.basename(base_name)}_*.{extension}",
        f"{os.path.basename(base_name)}-*.{extension}"
    ]
    search_dir = os.path.dirname(base_name) if os.path.dirname(base_name) else "."
    all_files = []
    for pattern in patterns:
        full_pattern = os.path.join(search_dir, pattern)
        all_files.extend(glob.glob(full_pattern))
    unique_files = list(set(all_files))
    def extract_number(filepath):
        filename = os.path.basename(filepath)
        match = re.search(r'(\d+)\.'+extension+'$', filename)
        return int(match.group(1)) if match else 0
    try:
        unique_files.sort(key=extract_number)
        return unique_files
    except:
        return []

def _descomponer_nombre_archivo(main_window, filepath):
    filename = os.path.basename(filepath)
    base_dir = os.path.dirname(filepath)
    match = re.match(r'^(.*?)[-_](\d+)\.([^.]+)$', filename)
    if match:
        base_name = match.group(1)
        number = int(match.group(2))
        extension = match.group(3)
        return (os.path.join(base_dir, base_name), number, extension)
    base, ext = os.path.splitext(filename)
    return (os.path.join(base_dir, base), None, ext[1:] if ext else '')

def _encontrar_archivo_numerado(main_window, base_name, number, extension):
    possible_paths = [
        f"{base_name}_{number}.{extension}",
        f"{base_name}-{number}.{extension}",
        f"{base_name}{number}.{extension}"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def _cargar_archivo_numerado(main_window, filepath):
    filename = os.path.basename(filepath)
    if filename not in main_window.rutas_archivos:
        main_window.rutas_archivos[filename] = filepath
        main_window.lista_archivos.addItem(filename)
        if main_window.switcher:
            main_window.switcher.add_model(filepath)
    if main_window.switcher:
        try:
            main_window.switcher.load_model(filepath)
            main_window.refinement_viewer.panel_derecho.actualizar_panel_derecho(filepath)
            if hasattr(main_window.switcher, 'metricas_actuales') and main_window.switcher.metricas_actuales:
                main_window.refinement_viewer.panel_derecho.actualizar_estadisticas(main_window.switcher.metricas_actuales)
            if filepath in main_window.switcher.file_list:
                main_window.switcher.current_index = main_window.switcher.file_list.index(filepath)
            main_window.refinement_viewer.renderer.GetRenderWindow().Render()
        except Exception as e:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.critical(main_window, 
                                 QApplication.translate(CONTEXTO, "Error"), 
                                 f"{QApplication.translate(CONTEXTO, 'No se pudo cargar el archivo')}:\n{str(e)}")

def abrir_dialogo_carga(main_window):
    dialogo = MeshGeneratorController(main_window, ignorar_limite=main_window.ignorar_limite_hardware)
    main_window.mesh_generator_controller = dialogo

    if dialogo.exec_() == QDialog.Accepted:
        if dialogo.cargar_sin_generar:
            archivo = dialogo.archivos_seleccionados[0]
            main_window.tab_widget.setCurrentIndex(1)
            main_window.base_viewer.load_poly_or_mdl(archivo)
            return

        ruta_poly = dialogo.archivos_seleccionados[0]
        nombre_poly = os.path.basename(ruta_poly)
        if dialogo.quadtree.isChecked():
            diccionario = main_window.rutas_archivos
            tipo = "2D"
        elif dialogo.octree.isChecked():
            diccionario = main_window.rutas_octree
            tipo = "3D"
        else:
            diccionario = main_window.rutas_archivos
            tipo = "2D"

        item_text = f"{nombre_poly} ({tipo})"
        if nombre_poly not in diccionario:
            diccionario[nombre_poly] = dialogo.generated_files
            #  GUARDAR LA RUTA DEL POLY TAMBIÉN
            diccionario[nombre_poly + "_path"] = ruta_poly
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, tipo)
            main_window.lista_archivos.addItem(item)

        if not main_window.switcher:
            main_window.switcher = ModelSwitcher(
                main_window.refinement_viewer.renderer,
                main_window.refinement_viewer.interactor,
                {nombre_poly: dialogo.generated_files}
            )
            main_window.refinement_viewer.set_switcher(main_window.switcher, poly_path=ruta_poly)
        else:
            main_window.switcher.file_dict[nombre_poly] = dialogo.generated_files
            main_window.refinement_viewer.poly_path = ruta_poly
            #update overlay
            main_window.refinement_viewer.update_overlay_poly(ruta_poly)

        main_window.switcher.current_poly = nombre_poly
        main_window.switcher.current_index = 0
        main_window.switcher._load_current()
        #Intento asegurar el update
        main_window.refinement_viewer.update_overlay_poly(ruta_poly)
        main_window.panel_derecho.actualizar_panel_derecho(dialogo.generated_files[0])
        if main_window.refinement_viewer.switcher:
            main_window.panel_derecho.actualizar_estadisticas(main_window.refinement_viewer.switcher.metricas_actuales)


def mostrar_contenido(main_window, item):
    nombre_poly = item.text().split(" ")[0]
    archivos_vtk = main_window.rutas_archivos.get(nombre_poly) or main_window.rutas_octree.get(nombre_poly)
    poly_path = None
    if nombre_poly in main_window.rutas_archivos:
        poly_path = main_window.rutas_archivos.get(nombre_poly + "_path", None)
        if not poly_path:
            posibles = [os.path.join("data", nombre_poly), os.path.join("data", nombre_poly.replace(" ", ""))]
            for p in posibles:
                if os.path.exists(p):
                    poly_path = p
                    break
    elif nombre_poly in main_window.rutas_octree:
        poly_path = main_window.rutas_octree.get(nombre_poly + "_path", None)
    if poly_path:
        main_window.refinement_viewer.update_overlay_poly(poly_path)
    if archivos_vtk and main_window.switcher:
        main_window.switcher.current_poly = nombre_poly
        main_window.switcher.current_index = 0
        main_window.switcher._load_current()
        #prueba con overlay
        if poly_path:
            main_window.refinement_viewer.update_overlay_poly(poly_path)

        main_window.panel_derecho.actualizar_panel_derecho(archivos_vtk[0])
        if main_window.refinement_viewer.switcher:
            main_window.panel_derecho.actualizar_estadisticas(main_window.refinement_viewer.switcher.metricas_actuales)

def mostrar_menu_contextual(main_window, posicion):
    item = main_window.lista_archivos.itemAt(posicion)
    if item:
        menu = QMenu()
        # --- CAMBIO: Usar QApplication.translate ---
        accion_eliminar = menu.addAction(QApplication.translate(CONTEXTO, "Eliminar archivo de la lista"))
        accion = menu.exec_(main_window.lista_archivos.mapToGlobal(posicion))
        if accion == accion_eliminar:
            nombre = item.text().split(" ")[0]
            if nombre in main_window.rutas_archivos:
                del main_window.rutas_archivos[nombre]
            main_window.lista_archivos.takeItem(main_window.lista_archivos.row(item))

def abrir_opciones_dialog(main_window):
    # Obtener el nombre del poly y nivel de refinamiento actual
    poly_name = None
    refinement_level = None
    if main_window.switcher and main_window.switcher.current_poly:
        poly_name = main_window.switcher.current_poly
        # Intentar extraer el nivel de refinamiento del nombre del archivo
        archivos = main_window.switcher.file_dict.get(poly_name, [])
        if archivos:
            # Ejemplo: a_output_5.vtk -> 5
            import re
            m = re.search(r'_output_(\d+)', archivos[-1])
            if m:
                refinement_level = int(m.group(1))
    dialog = OpcionesDialog(main_window, poly_name=poly_name, refinement_level=refinement_level)
    # dialog.checkbox.setChecked(main_window.ignorar_limite_hardware) # OpcionesDialog ya hace esto
    if dialog.exec_() == QDialog.Accepted:
        main_window.ignorar_limite_hardware = dialog.checkbox.isChecked()

def exportar_registro(main_window):
    """Exporta el archivo de registro del mallado"""
    # (Asumo que export_manager no existe en main_window, sino en el panel)
    # Si esta lógica es incorrecta, la función original se mantiene
    if not hasattr(main_window, 'export_manager'):
         # Si no existe, intenta crearlo o buscarlo
         # Esto es una suposición, ajusta si es incorrecto
         from app.logic.export_utils import ExportManager
         main_window.export_manager = ExportManager(main_window)

    success, message = main_window.export_manager.export_log_file()
    
    if not success:
        if message == "no_log_file":
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.information(
                main_window,
                QApplication.translate(CONTEXTO, "Información"), 
                QApplication.translate(CONTEXTO, "No hay registro de mallado disponible.\n"
                               "Ejecute el algoritmo de mallado primero para generar un registro.")
            )
        elif message == "export_cancelled":
            pass
        else:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.warning(
                main_window,
                QApplication.translate(CONTEXTO, "Error al exportar"),
                f"{QApplication.translate(CONTEXTO, 'No se pudo exportar el registro')}:\n{message}"
            )

def cambiar_visualizador(main_window, index):
    if index == 0:  # Tab de refinamiento
        main_window.refinement_viewer.vtk_widget.show()
        main_window.refinement_viewer.vtk_widget.GetRenderWindow().Render()
        # HABILITAR panel derecho y ocultar panel_pap si existe
        if hasattr(main_window, 'panel_derecho'):
            main_window.panel_derecho.show()
        if hasattr(main_window, 'panel_pap'):
            main_window.panel_pap.hide()
    else:  # Tab de paso a paso
        # DESHABILITAR panel derecho y mostrar panel_pap
        if hasattr(main_window, 'panel_derecho'):
            main_window.panel_derecho.hide()
        # panel_pap fue creado en MainWindow; si no existe, crear uno (defensivo)
        if not hasattr(main_window, 'panel_pap'):
            try:
                from app.interface.panel_pap import PanelPAP
                main_window.panel_pap = PanelPAP(parent=main_window)
                # (Asumimos que el layout de main_window lo maneja)
            except Exception:
                main_window.panel_pap = None
        if hasattr(main_window, 'panel_pap') and main_window.panel_pap:
            main_window.panel_pap.show()
        
        # (El resto de la lógica de VTK Player)
        if hasattr(main_window, 'vtk_player'):
            main_window.vtk_player.vtk_widget.show()
            main_window.vtk_player.vtk_widget.GetRenderWindow().Render()
        else:
             print("Error: vtk_player no encontrado en main_window")
             return # Salir si no hay vtk_player


        # VALIDAR que switcher existe y tiene archivos cargados
        if not main_window.switcher:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.warning(
                main_window, 
                QApplication.translate(CONTEXTO, "Sin archivos cargados"), 
                QApplication.translate(CONTEXTO, "No hay archivos cargados.\nPrimero carga un archivo .poly para generar una malla.")
            )
            # Regresar al tab de refinamiento
            main_window.tab_widget.setCurrentIndex(0)
            return

        
        if not main_window.switcher.current_poly:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.warning(
                main_window, 
                QApplication.translate(CONTEXTO, "Sin malla seleccionada"), 
                QApplication.translate(CONTEXTO, "No hay una malla seleccionada.\nSelecciona una malla de la lista para visualizar el paso a paso.")
            )
            # Regresar al tab de refinamiento
            main_window.tab_widget.setCurrentIndex(0)
            return

        archivos = main_window.switcher.file_dict.get(main_window.switcher.current_poly, [])
        if not archivos:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.warning(
                main_window, 
                QApplication.translate(CONTEXTO, "Sin archivos generados"), 
                QApplication.translate(CONTEXTO, "No hay archivos generados para la malla seleccionada.\nGenera la malla primero.")
            )
            # Regresar al tab de refinamiento
            main_window.tab_widget.setCurrentIndex(0)
            return

        print(archivos[-1])
        item = archivos[-1]
        filename = os.path.basename(item)
        nombre_base = os.path.splitext(filename)[0]

        ruta_vtk = f"{nombre_base}.vtk"

        # Ruta base del proyecto (según ubicación de este archivo)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        outputs_dir = os.path.abspath(os.path.join(BASE_DIR, "../../outputs"))

        # Evitar duplicar prefijos
        if nombre_base.startswith("quadtree_") or nombre_base.startswith("octree_"):
            historial_quadtree = f"{nombre_base}_historial.txt"
            historial_octree = f"{nombre_base}_historial.txt"
        else:
            historial_quadtree = f"quadtree_{nombre_base}_historial.txt"
            historial_octree = f"octree_{nombre_base}_historial.txt"

        # Rutas completas
        ruta_quadtree = os.path.join(outputs_dir, historial_quadtree)
        ruta_octree = os.path.join(outputs_dir, historial_octree)

        # Verificar existencia
        historial_path = None
        historial_en_proceso = False

        # Intentar acceder al estado del generador de mallas
        mesh_generator = getattr(main_window, "mesh_generator_controller", None)
        if not mesh_generator:
            # A veces se guarda como "mesh_generator"
            mesh_generator = getattr(main_window, "mesh_generator", None)

        if mesh_generator and getattr(mesh_generator, "historial_generandose", False):
            historial_en_proceso = True

        # Construir rutas posibles
        if os.path.exists(ruta_quadtree):
            historial_path = ruta_quadtree
        elif os.path.exists(ruta_octree):
            historial_path = ruta_octree
        elif historial_en_proceso:
            # ✅ El historial aún se está generando → dejar que el VTKPlayer maneje el spinner
            print("[MainWindowLogic] El historial aún se está generando, delegando al VTKPlayer...")
            historial_path = ruta_quadtree if "quadtree" in nombre_base else ruta_octree
        else:
            # ❌ Historial inexistente y no se está generando → mensaje original
            QMessageBox.warning(
                main_window,
                "Historial no disponible",
                f"No se encontró un archivo de historial para el modelo seleccionado.\n\n"
                f"Esta funcionalidad estará disponible una vez que se genere el historial."
            )
            main_window.tab_widget.setCurrentIndex(0)
            return

        # ================================
        # 🎬 EJECUTAR EL VTKPLAYER (maneja spinner si corresponde)
        # ================================
        main_window.vtk_player.run_script(ruta_vtk, historial_path)

        try:
            interactor = main_window.vtk_player.vtk_widget.GetRenderWindow().GetInteractor()
            interactor.Initialize()
            main_window.vtk_player.apply_custom_style()
        except Exception:
            pass

def closeEvent(main_window, event):
    # --- CAMBIO: Usar QApplication.translate ---
    reply = QMessageBox.question(
        main_window,
        QApplication.translate(CONTEXTO, "Limpiar outputs"),
        QApplication.translate(CONTEXTO, "¿Desea eliminar todos los archivos output generados?"),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.Yes
    )
    if reply == QMessageBox.Yes:
        try:
            # (Asumimos que la carpeta 'outputs' está al mismo nivel que 'app')
            current_dir = os.path.dirname(os.path.abspath(__file__))
            outputs_path = os.path.abspath(os.path.join(current_dir, "../../outputs"))
            
            if os.path.exists(outputs_path):
                # Borrar contenido, no la carpeta
                for item in os.listdir(outputs_path):
                    item_path = os.path.join(outputs_path, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                
                # --- CAMBIO: Usar QApplication.translate ---
                msg = QApplication.translate(CONTEXTO, "Contenido de 'outputs' limpiado exitosamente.")
                print(msg)
                QMessageBox.information(main_window, QApplication.translate(CONTEXTO, "Outputs limpiados"), msg)
            else:
                # --- CAMBIO: Usar QApplication.translate ---
                msg = QApplication.translate(CONTEXTO, "La carpeta 'outputs' no se encontró. No se necesita limpieza.")
                print(msg)
                QMessageBox.information(main_window, QApplication.translate(CONTEXTO, "Outputs no encontrados"), msg)
        except Exception as e:
            # --- CAMBIO: Usar QApplication.translate ---
            msg = f"{QApplication.translate(CONTEXTO, 'Error al limpiar outputs')}: {e}"
            print(msg)
            QMessageBox.critical(main_window, QApplication.translate(CONTEXTO, "Error al limpiar outputs"), msg)
    event.accept()

def abrir_manual(main_window):
    dialog = ManualDialog(main_window)
    dialog.exec_()