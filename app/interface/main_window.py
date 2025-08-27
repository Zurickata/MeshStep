import sys
import os
import re
import glob
import vtk
from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QMenu, QLabel, QListWidget, QSplitter,
                            QMessageBox, QSizePolicy, QStyle)
from PyQt5.QtCore import (Qt, QTimer)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from app.logic.mesh_generator import MeshGeneratorController

from .panel_derecho import PanelDerecho

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        self.boton_cargar = QPushButton("Cargar archivos", self)
        self.boton_cargar.clicked.connect(self.abrir_dialogo_carga)

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(self.mostrar_contenido)
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        # NUEVOS BOTONES PARA ACCIONES
        

        # self.boton_b = QPushButton("Borrar extras (b)", self)
        # self.boton_b.clicked.connect(self.accion_b)

       

        

        self.rutas_archivos = {}

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(CustomInteractorStyle(self.renderer))
        self.interactor.Initialize()

        # Crear botones de navegación
        
        self.boton_anterior = QPushButton()
        self.boton_anterior.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.boton_anterior.setText("Anterior")

        self.boton_siguiente = QPushButton()
        self.boton_siguiente.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.boton_siguiente.setText("Siguiente")

        # Conectar botones a funciones
        self.boton_anterior.clicked.connect(self.navegar_anterior)
        self.boton_siguiente.clicked.connect(self.navegar_siguiente)



        # Nuevos botones para control de animación
        self.boton_play = QPushButton()
        self.boton_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.boton_play.setText("Play")

        self.boton_pausa = QPushButton()
        self.boton_pausa.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.boton_pausa.setText("Pausa")

        self.boton_reinicio = QPushButton()
        self.boton_reinicio.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.boton_reinicio.setText("Reinicio")
        
        # Configurar timer para animación automática
        self.timer_animacion = QTimer(self)
        self.timer_animacion.setInterval(1500)  # 1.5 segundos
        self.timer_animacion.timeout.connect(self.avance_automatico)
        
        # Conectar botones
        self.boton_play.clicked.connect(self.iniciar_animacion)
        self.boton_pausa.clicked.connect(self.detener_animacion)
        self.boton_reinicio.clicked.connect(self.reiniciar_secuencia)
        
        # Estilo para los nuevos botones
        estilo_botones = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """
        # Aplicar a todos los botones
        for btn in [self.boton_anterior, self.boton_siguiente, 
                    self.boton_play, self.boton_pausa, self.boton_reinicio]:
            btn.setStyleSheet(estilo_botones)

        
        self.boton_pausa.setEnabled(False)

        # Crear layout para los botones de navegación
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.boton_anterior)
        nav_layout.addWidget(self.boton_siguiente)
        nav_layout.addWidget(self.boton_play)
        nav_layout.addWidget(self.boton_pausa)
        nav_layout.addWidget(self.boton_reinicio)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(5)
        
        # Widget contenedor para los botones de navegación
        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        nav_widget.setFixedHeight(40)

        self.switcher = None

        splitter = QSplitter(Qt.Horizontal)

        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        layout_izquierdo.addWidget(self.boton_cargar)
        layout_izquierdo.addWidget(self.lista_archivos)
        panel_izquierdo.setLayout(layout_izquierdo)

        # Layout principal del panel central
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.vtk_widget, 1)  # El widget VTK ocupa la mayor parte
        central_layout.addWidget(nav_widget)          # Los botones de navegación abajo
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Widget contenedor del panel central
        panel_central = QWidget()
        panel_central.setLayout(central_layout)
        """ 
        # Panel derecho
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        self.label_derecho = QLabel("Métricas de ángulos críticos")
        self.label_derecho.setAlignment(Qt.AlignCenter)
        self.label_derecho.setWordWrap(True) 
        layout_derecho.addWidget(self.label_derecho)
            
        # AGREGAR LOS NUEVOS BOTONES
        layout_derecho.addWidget(self.boton_n)
        layout_derecho.addWidget(self.boton_a)
        # layout_derecho.addWidget(self.boton_b)
        layout_derecho.addWidget(self.boton_r)
        layout_derecho.addWidget(self.boton_w)
        layout_derecho.addWidget(self.boton_s)
        panel_derecho.setLayout(layout_derecho)

        # Configurar el tamaño mínimo de los paneles
        panel_derecho.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        panel_derecho.setMinimumWidth(100)  # You can adjust this value

        # Configurar el tamaño de los botones
        self.label_derecho.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        #for btn in [self.boton_n, self.boton_a, self.boton_b, self.boton_r, self.boton_w, self.boton_s]:
        #    btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred) """

        self.panel_derecho = PanelDerecho(self)
        
        # Conectar señales del nuevo panel
        self._conectar_señales_panel_derecho()

        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_central)
        splitter.addWidget(self.panel_derecho)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setAcceptDrops(True)

    def _conectar_señales_panel_derecho(self):
        """Conecta las señales del panel derecho con las funciones existentes"""
        
        # Conectar botones de acciones
        self.panel_derecho.slider_velocidad.valueChanged.connect(self.ajustar_velocidad)
        
        # Conectar botones de navegación
        self.panel_derecho.boton_puntos_criticos.clicked.connect(self.accion_a)
        self.panel_derecho.boton_reset_camara.clicked.connect(self.accion_r)
        self.panel_derecho.boton_limpiar.clicked.connect(self.accion_b)
        
        
      

    def ajustar_velocidad(self, valor):
        """Ajusta la velocidad de la animación"""
        segundos = valor / 1000.0
        self.timer_animacion.setInterval(valor)
        self.panel_derecho.label_velocidad_valor.setText(f"{segundos:.1f}s")

    # Este método se encarga de leer el archivo _histo.txt y actualizar el panel derecho con los ángulos
    def actualizar_panel_derecho(self, ruta_archivo):
        try:
            # Cambiar extensión del archivo de .vtk a _histo.txt
            base, _ = os.path.splitext(ruta_archivo)
            ruta_modificada = f"{base}_histo.txt"
            numero = base.split('_')[-1]

            # Leer el archivo línea por línea
            with open(ruta_modificada, 'r') as f:
                lineas = f.readlines()

            angulo_triangulo = None
            angulo_cuadrado = None
            min_triangulo = None
            max_triangulo = None
            min_cuadrado = None
            max_cuadrado = None
            criticos_triangulos = 0
            criticos_cuadrados = 0

            # Variables para el procesamiento del histograma
            procesando_triangulos = False
            procesando_cuadrados = False
            threshold_actual = self.panel_derecho.threshold_angulo

            for i, linea in enumerate(lineas):
                # Detectar secciones
                if "For Triangles:" in linea:
                    procesando_triangulos = True
                    procesando_cuadrados = False
                    continue
                elif "For Quads:" in linea:
                    procesando_triangulos = False
                    procesando_cuadrados = True
                    continue
                elif "Smallest angle:" in linea and "Largest angle:" in linea:
                    # Extraer valores mínimo y máximo
                    partes = linea.split('|')
                    if len(partes) >= 2:
                        min_val = partes[0].replace('Smallest angle:', '').strip()
                        max_val = partes[1].replace('Largest angle:', '').strip()
                        
                        if procesando_triangulos:
                            min_triangulo = min_val
                            max_triangulo = max_val
                            angulo_triangulo = f"{min_val} | {max_val}"
                        elif procesando_cuadrados:
                            min_cuadrado = min_val
                            max_cuadrado = max_val
                            angulo_cuadrado = f"{min_val} | {max_val}"
                    continue
                
                # Procesar líneas del histograma
                if ("Angle histogram:" in linea or 
                    "0 -   1 degrees:" in linea or 
                    linea.strip().startswith('0 -') or 
                    re.match(r'^\s*\d+ - \s*\d+ degrees:', linea)):
                    
                    # Buscar patrones de histograma: "X - Y degrees: COUNT"
                    match = re.match(r'.*?(\d+)\s*-\s*(\d+)\s*degrees:\s*(\d+)', linea)
                    if match:
                        min_deg = int(match.group(1))
                        max_deg = int(match.group(2))
                        count = int(match.group(3))
                        
                        # Si el rango está por debajo del threshold, sumar al contador
                        if max_deg < threshold_actual:
                            if procesando_triangulos:
                                criticos_triangulos += count
                            elif procesando_cuadrados:
                                criticos_cuadrados += count

            # Determinar color basado en el threshold (lógica invertida: ángulos bajos = malos)
            if threshold_actual <= 25:
                color_threshold = "#ff6b6b"  # ROJO - ángulos muy bajos (críticos)
            elif threshold_actual <= 45:
                color_threshold = "#ff9f43"  # NARANJA - ángulos medios (regulares)
            else:
                color_threshold = "#4ecdc4"  # VERDE AZULADO - ángulos altos (buenos)

            # Función para determinar el color de un ángulo basado en el threshold
            def color_por_angulo(angulo_str):
                try:
                    if angulo_str and '°' in angulo_str:
                        valor = float(angulo_str.replace('°', '').split()[0])
                        if valor < threshold_actual:
                            return "#ff6b6b"  # Rojo para ángulos críticos
                        elif valor < threshold_actual + 15:
                            return "#ff9f43"  # Naranja para ángulos regulares
                        else:
                            return "#4ecdc4"  # Verde para ángulos buenos
                except:
                    pass
                return "#ffffff"  # Blanco por defecto

            # Función para formatear valores angulares
            def formatear_valor_angular(valor):
                try:
                    # Extraer el número y agregar el símbolo de grados
                    num_val = float(valor.split()[0])
                    return f"{num_val:.1f}°"
                except:
                    return valor

            # Determinar calidad general basada en los ángulos críticos
            total_criticos = criticos_triangulos + criticos_cuadrados
            if total_criticos == 0:
                calidad_general = "Excelente"
                color_calidad = "#4ecdc4"
            elif total_criticos <= 5:
                calidad_general = "Buena"
                color_calidad = "#4ecdc4"
            elif total_criticos <= 15:
                calidad_general = "Regular"
                color_calidad = "#ff9f43"
            elif total_criticos <= 30:
                calidad_general = "Mala"
                color_calidad = "#ff6b6b"
            else:
                calidad_general = "Crítica"
                color_calidad = "#ff0000"

            # Construir el contenido HTML con el estilo deseado
            contenido_html = f"""
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px;'>
                <b style='color: #ffd700;'>Nivel de Refinamiento: {numero}</b><br><br>
                
                <b style='color: #ffd700;'>Ángulos Críticos (Umbral: <span style='color: {color_threshold};'>{threshold_actual}°</span>)</b><br><br>
            """

            # Agregar información de triángulos si está disponible
            if min_triangulo and max_triangulo:
                min_tri_formatted = formatear_valor_angular(min_triangulo)
                max_tri_formatted = formatear_valor_angular(max_triangulo)
                color_min_tri = color_por_angulo(min_triangulo)
                color_max_tri = color_por_angulo(max_triangulo)
                
                contenido_html += f"""
                <b>Triángulos:</b><br>
                <span style='color: {color_min_tri};'>Mín: {min_tri_formatted}</span> | 
                <span style='color: {color_max_tri};'>Máx: {max_tri_formatted}</span><br>
                <span style='color: #ff6b6b;'>⚠️ {criticos_triangulos} ángulos &lt; {threshold_actual}°</span><br><br>
                """

            # Agregar información de cuadriláteros si está disponible
            if min_cuadrado and max_cuadrado:
                min_cuad_formatted = formatear_valor_angular(min_cuadrado)
                max_cuad_formatted = formatear_valor_angular(max_cuadrado)
                color_min_cuad = color_por_angulo(min_cuadrado)
                color_max_cuad = color_por_angulo(max_cuadrado)
                
                contenido_html += f"""
                <b>Cuadriláteros:</b><br>
                <span style='color: {color_min_cuad};'>Mín: {min_cuad_formatted}</span> | 
                <span style='color: {color_max_cuad};'>Máx: {max_cuad_formatted}</span><br>
                <span style='color: #ff6b6b;'>⚠️ {criticos_cuadrados} ángulos &lt; {threshold_actual}°</span><br>
                """

            # Agregar calidad general
            contenido_html += f"""
                <div style='margin-top: 10px; padding: 8px; background-color: #3a3a3a; border-radius: 4px;'>
                    <b style='color: {color_calidad};'>Calidad General:</b> 
                    <span style='color: {color_calidad};'>{calidad_general}</span> 
                    <span style='color: #cccccc; font-size: 12px;'>({total_criticos} ángulos críticos)</span>
                </div>
            </div>
            """

            # Actualizar el panel derecho
            self.panel_derecho.actualizar_metricas(contenido_html)

        except Exception as e:
            error_html = f"""
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; color: #ff6b6b;'>
                <b>Error al leer el archivo:</b><br>{str(e)}<br><br>
                <span style='font-size: 12px; color: #cccccc;'>Ruta: {ruta_modificada}</span>
            </div>
            """
            self.panel_derecho.actualizar_metricas(error_html)

    # Métodos para cada acción

    # Moverse entre los poly
    def accion_n(self):
        if not self.switcher:
            return
        polys_cargados = list(self.switcher.file_dict.keys())
        if not polys_cargados:
            return
        
        try:
            i = polys_cargados.index(self.switcher.current_poly)
            next_index = (i + 1) % len(polys_cargados)
            next_poly = polys_cargados[next_index]
        except ValueError:
            next_poly = polys_cargados[0]
        
        archivos = self.switcher.file_dict.get(next_poly, [])
        if archivos:
            self.switcher.current_poly = next_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.actualizar_panel_derecho(archivos[0])

            items = self.lista_archivos.findItems(next_poly, Qt.MatchExactly)
            if items:
                self.lista_archivos.setCurrentItem(items[0])
            
            # Eliminar los puntos críticos si están
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()


    #Toggle puntos críticos
    def accion_a(self):
        if self.switcher:
            self.switcher.toggle_load = not self.switcher.toggle_load
            if self.switcher.toggle_load:
                print("Cargando puntos criticos...")
                self.switcher.marcar_angulos_extremos()
                self.renderer.GetRenderWindow().Render()
            else:
                print("Toggle desactivado puntos criticos.")
                self.switcher.clear_extra_models()
                self.renderer.GetRenderWindow().Render()

    def accion_b(self):
        if self.switcher:
            self.switcher.clear_extra_models()

    def accion_r(self):
        if self.switcher:
            print("🔁 Reseteando cámara y modelo")
            self.switcher.actor.SetOrientation(0, 0, 0)
            self.switcher.actor.SetPosition(0, 0, 0)
            self.switcher.actor.SetScale(1, 1, 1)
            self.renderer.ResetCamera()
            if isinstance(self.interactor.GetInteractorStyle(), CustomInteractorStyle):
                self.interactor.GetInteractorStyle().reset_camera_and_rotation()
            self.renderer.GetRenderWindow().Render()

    def accion_w(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToWireframe()
            self.renderer.GetRenderWindow().Render()
            self.panel_derecho.set_modo_visualizacion("wireframe")

    def accion_s(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToSurface()
            self.renderer.GetRenderWindow().Render()
            self.panel_derecho.set_modo_visualizacion("solido")

    def abrir_dialogo_carga(self):
        dialogo = MeshGeneratorController(self)

        if dialogo.exec_() == QDialog.Accepted:
            ruta_poly = dialogo.archivos_seleccionados[0]
            nombre_poly = os.path.basename(ruta_poly)

            if nombre_poly not in self.rutas_archivos:
                self.rutas_archivos[nombre_poly] = dialogo.generated_files
                self.lista_archivos.addItem(nombre_poly)

            items = self.lista_archivos.findItems(nombre_poly, Qt.MatchExactly)
            if items:
                self.lista_archivos.setCurrentItem(items[0]) 

            if not self.switcher:
                self.switcher = ModelSwitcher(self.renderer, self.interactor, {nombre_poly: dialogo.generated_files})
            else:
                self.switcher.file_dict[nombre_poly] = dialogo.generated_files

            self.switcher.current_poly = nombre_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.actualizar_panel_derecho(dialogo.generated_files[0])

        elif dialogo.exec_() == QDialog.Rejected:
            return
        
        print("Rutas_Archivo:", self.rutas_archivos)
        print("Lista_Archivos:", self.lista_archivos)
        print("Generated_Files:", dialogo.generated_files)

    def mostrar_contenido(self, item):
        nombre_poly = item.text()
        archivos_vtk = self.rutas_archivos.get(nombre_poly)

        if archivos_vtk and self.switcher:
            self.switcher.current_poly = nombre_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.actualizar_panel_derecho(archivos_vtk[0])

    def mostrar_menu_contextual(self, posicion):
        item = self.lista_archivos.itemAt(posicion)
        if item:
            menu = QMenu()
            accion_eliminar = menu.addAction("Eliminar archivo de la lista")
            accion = menu.exec_(self.lista_archivos.mapToGlobal(posicion))
            if accion == accion_eliminar:
                nombre = item.text()
                if nombre in self.rutas_archivos:
                    del self.rutas_archivos[nombre]
                self.lista_archivos.takeItem(self.lista_archivos.row(item))
                

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
        dialogo = MeshGeneratorController(self)
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
    
    def navegar_anterior(self):
        """Función para navegar al modelo anterior numéricamente"""
        if not self.switcher:
            return

        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            return

        if self.switcher.current_index > 0:
            self.switcher.anterior_modelo()
            self.actualizar_panel_derecho(archivos[self.switcher.current_index])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
        else:
            QMessageBox.information(self, "Inicio", "Ya estás en el primer modelo.")

    def navegar_siguiente(self):
        """Función para navegar al siguiente modelo numéricamente"""
        if not self.switcher:
            return

        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            return

        if self.switcher.current_index + 1 < len(archivos):
            self.switcher.siguiente_modelo()
            self.actualizar_panel_derecho(archivos[self.switcher.current_index])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
        else:
            QMessageBox.information(self, "Fin", "Ya estás en el último modelo.")

    def iniciar_animacion(self):
        """Inicia el avance automático de modelos"""
        if self.switcher and self.switcher.file_dict:
            self.boton_play.setEnabled(False)
            self.boton_pausa.setEnabled(True)
            self.timer_animacion.start()
            
    def detener_animacion(self):
        """Detiene el avance automático"""
        self.timer_animacion.stop()
        self.boton_play.setEnabled(True)
        self.boton_pausa.setEnabled(False)
        
    def avance_automatico(self):
        """Función que se ejecuta automáticamente cada intervalo de tiempo"""
        if not self.switcher:
            self.detener_animacion()
            return
            
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            self.detener_animacion()
            return
            
        # Si estamos en el último modelo, volver al primero
        if self.switcher.current_index + 1 >= len(archivos):
            self.reiniciar_secuencia()
        else:
            self.navegar_siguiente()
            
    def reiniciar_secuencia(self):
        """Vuelve al primer modelo de la secuencia actual"""
        if not self.switcher:
            return
            
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if archivos:
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.actualizar_panel_derecho(archivos[0])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
            
            # Resaltar el elemento correspondiente en la lista
            items = self.lista_archivos.findItems(self.switcher.current_poly, Qt.MatchExactly)
            if items:
                self.lista_archivos.setCurrentItem(items[0])

    def _encontrar_serie_completa(self, base_name, extension):
        """Encuentra todos los archivos de la misma serie numérica"""
        print(f"DEBUG: Buscando serie completa para: {base_name}_*.{extension}")
        
        # Patrones a buscar
        patterns = [
            f"{base_name}_*.{extension}",
            f"{base_name}-*.{extension}",
            f"{os.path.basename(base_name)}_*.{extension}",
            f"{os.path.basename(base_name)}-*.{extension}"
        ]
        
        # Directorio donde buscar
        search_dir = os.path.dirname(base_name) if os.path.dirname(base_name) else "."
        print(f"DEBUG: Buscando en directorio: {search_dir}")
        
        # Encontrar todos los archivos que coincidan
        all_files = []
        for pattern in patterns:
            full_pattern = os.path.join(search_dir, pattern)
            print(f"DEBUG: Buscando con patrón: {full_pattern}")
            all_files.extend(glob.glob(full_pattern))
        
        # Eliminar duplicados
        unique_files = list(set(all_files))
        print(f"DEBUG: Archivos encontrados: {unique_files}")
        
        # Ordenar numéricamente
        def extract_number(filepath):
            filename = os.path.basename(filepath)
            match = re.search(r'(\d+)\.'+extension+'$', filename)
            return int(match.group(1)) if match else 0
        
        try:
            unique_files.sort(key=extract_number)
            print(f"DEBUG: Archivos ordenados: {unique_files}")
            return unique_files
        except:
            print("DEBUG: Error al ordenar archivos")
            return []

    def _descomponer_nombre_archivo(self, filepath):
        """Extrae las partes del nombre del archivo para detectar números"""
        filename = os.path.basename(filepath)
        base_dir = os.path.dirname(filepath)
        
        # Busca patrones como: nombre_X.ext o nombre-X.ext (X es el número)
        match = re.match(r'^(.*?)[-_](\d+)\.([^.]+)$', filename)
        if match:
            base_name = match.group(1)
            number = int(match.group(2))
            extension = match.group(3)
            return (os.path.join(base_dir, base_name), number, extension)
        
        # Si no encuentra el patrón, devuelve None para el número
        base, ext = os.path.splitext(filename)
        return (os.path.join(base_dir, base), None, ext[1:] if ext else '')

    def _encontrar_archivo_numerado(self, base_name, number, extension):
        """Busca un archivo con el número especificado"""
        possible_paths = [
            f"{base_name}_{number}.{extension}",
            f"{base_name}-{number}.{extension}",
            f"{base_name}{number}.{extension}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def _cargar_archivo_numerado(self, filepath):
        """Carga un archivo y actualiza la interfaz"""
        # Verificar si el archivo ya está en la lista
        filename = os.path.basename(filepath)
        
        if filename not in self.rutas_archivos:
            # Si no está en la lista, agregarlo
            self.rutas_archivos[filename] = filepath
            self.lista_archivos.addItem(filename)
            if self.switcher:
                self.switcher.add_model(filepath)
        
        # Cargar el archivo
        if self.switcher:
            try:
                self.switcher.load_model(filepath)
                self.actualizar_panel_derecho(filepath)
                # Actualizar el índice actual al nuevo archivo
                if filepath in self.switcher.file_list:
                    self.switcher.current_index = self.switcher.file_list.index(filepath)
                self.renderer.GetRenderWindow().Render()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")
