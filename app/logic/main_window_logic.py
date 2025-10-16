import os
import re
import glob
import shutil
from PyQt5.QtWidgets import QMenu, QListWidgetItem, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from app.interface.manual_dialog import ManualDialog
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from app.logic.mesh_generator import MeshGeneratorController
from app.interface.options_dialog import OpcionesDialog


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
        QMessageBox.critical(main_window, "Error", "El archivo no es un archivo .poly válido.")
        return

    if dialogo.exec_() == QDialog.Accepted:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            nombre = os.path.basename(ruta_archivo)
            if nombre not in main_window.rutas_archivos:
                main_window.rutas_archivos[nombre] = ruta_archivo
                main_window.lista_archivos.addItem(nombre)
            main_window.vista_texto.setPlainText(contenido)
        except Exception as e:
            QMessageBox.critical(main_window, "Error al leer archivo", str(e))

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
            QMessageBox.critical(main_window, "Error", f"No se pudo cargar el archivo:\n{str(e)}")

def abrir_dialogo_carga(main_window):
    dialogo = MeshGeneratorController(main_window, ignorar_limite=main_window.ignorar_limite_hardware)
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
        accion_eliminar = menu.addAction("Eliminar archivo de la lista")
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
    dialog.checkbox.setChecked(main_window.ignorar_limite_hardware)
    if dialog.exec_() == QDialog.Accepted:
        main_window.ignorar_limite_hardware = dialog.checkbox.isChecked()

def exportar_registro(main_window):
    """Exporta el archivo de registro del mallado"""
    success, message = main_window.export_manager.export_log_file()
    
    if not success:
        if message == "no_log_file":
            QMessageBox.information(
                main_window,
                "Información", 
                "No hay registro de mallado disponible.\n"
                "Ejecute el algoritmo de mallado primero para generar un registro."
            )
        elif message == "export_cancelled":
            pass
        else:
            QMessageBox.warning(
                main_window,
                "Error al exportar",
                f"No se pudo exportar el registro:\n{message}"
            )

def cambiar_visualizador(main_window, index):
    if index == 0:  # Tab de refinamiento
        main_window.refinement_viewer.vtk_widget.show()
        main_window.refinement_viewer.vtk_widget.GetRenderWindow().Render()
        # HABILITAR panel derecho
        if hasattr(main_window, 'panel_derecho'):
            main_window.panel_derecho.show()  # Quitar estilo de deshabilitado

    else:  # Tab de paso a paso
        # DESHABILITAR panel derecho
        if hasattr(main_window, 'panel_derecho'):
            main_window.panel_derecho.hide()
        main_window.vtk_player.vtk_widget.show()
        main_window.vtk_player.vtk_widget.GetRenderWindow().Render()

        # VALIDAR que switcher existe y tiene archivos cargados
        if not main_window.switcher:
            QMessageBox.warning(
                main_window, 
                "Sin archivos cargados", 
                "No hay archivos cargados.\nPrimero carga un archivo .poly para generar una malla."
            )
            # Regresar al tab de refinamiento
            main_window.tab_widget.setCurrentIndex(0)
            return

        
        if not main_window.switcher.current_poly:
            QMessageBox.warning(
                main_window, 
                "Sin malla seleccionada", 
                "No hay una malla seleccionada.\nSelecciona una malla de la lista para visualizar el paso a paso."
            )
            # Regresar al tab de refinamiento
            main_window.tab_widget.setCurrentIndex(0)
            return

        archivos = main_window.switcher.file_dict.get(main_window.switcher.current_poly, [])
        if not archivos:
            QMessageBox.warning(
                main_window, 
                "Sin archivos generados", 
                "No hay archivos generados para la malla seleccionada.\nGenera la malla primero."
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
        if os.path.exists(ruta_quadtree):
            historial_path = ruta_quadtree
        elif os.path.exists(ruta_octree):
            historial_path = ruta_octree
        else:
            # ⚠️ Mensaje original restaurado
            QMessageBox.warning(
                main_window, 
                "Historial no disponible", 
                f"El modo paso a paso aún no está implementado para mallas 3D.\n\n"
                f"Archivo de historial no encontrado:\n{historial_quadtree} / {historial_octree}\n\n"
                f"Esta funcionalidad estará disponible próximamente."
            )
            main_window.tab_widget.setCurrentIndex(0)
            return

        # Ejecutar normalmente
        main_window.vtk_player.run_script(ruta_vtk, historial_path)

        try:
            interactor = main_window.vtk_player.vtk_widget.GetRenderWindow().GetInteractor()
            interactor.Initialize()
            # Reaplicar el estilo personalizado después del Initialize
            main_window.vtk_player.apply_custom_style()
        except Exception:
            pass

def closeEvent(main_window, event):
    reply = QMessageBox.question(
        main_window,
        "Limpiar outputs",
        "¿Desea eliminar todos los archivos output generados?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.Yes
    )
    if reply == QMessageBox.Yes:
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            outputs_path = os.path.join(current_dir, "../../outputs")
            if os.path.exists(outputs_path):
                shutil.rmtree(outputs_path)
                os.makedirs(outputs_path)
                msg = "Outputs limpiados exitosamente."
                print(msg)
                QMessageBox.information(main_window, "Outputs limpiados", msg)
            else:
                msg = "La carpeta 'outputs' no se encontró. No se necesita limpieza."
                print(msg)
                QMessageBox.information(main_window, "Outputs no encontrados", msg)
        except Exception as e:
            msg = f"Error al limpiar outputs: {e}"
            print(msg)
            QMessageBox.critical(main_window, "Error al limpiar outputs", msg)
    event.accept()

def abrir_manual(main_window):
    dialog = ManualDialog(main_window)
    dialog.exec_()