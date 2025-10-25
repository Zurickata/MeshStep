from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QScrollArea,
                            QSlider, QGridLayout)
from PyQt5.QtCore import Qt

import os
import re
from app.visualization.FeriaVTK import CustomInteractorStyle
from app.logic.main_window_logic import (
    accion_w, accion_s
)
from app.visualization.FeriaVTK import notifier

class PanelDerecho(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.refinement_viewer = None
        self.parent = parent
        self.modo_visualizacion = "solido"  # Estado inicial
        self.threshold_angulo = 30  # Valor inicial del threshold
        self.setup_ui()
        self.metricas_actuales = None
        
    def setup_ui(self):
        """Configura la interfaz del panel derecho"""
        self.setWidgetResizable(True)
        self.setMaximumWidth(480)
        self.setMinimumWidth(320)
        
        # Widget contenedor principal
        self.contenido = QWidget()
        self.layout_principal = QVBoxLayout(self.contenido)
        self.layout_principal.setSpacing(12)
        self.layout_principal.setContentsMargins(12, 12, 12, 12)
        
        # Crear secciones 
        self.crear_seccion_metricas()
        self.crear_seccion_visualizacion()
        self.crear_seccion_coloreos()
        self.crear_seccion_acciones()
        self.crear_seccion_estadisticas()
        #self.crear_seccion_threshold()
        self.crear_seccion_animacion()
        
        # Espaciador final
        self.layout_principal.addStretch()
        
        self.setWidget(self.contenido)
        self.aplicar_estilo_botones()
        self.actualizar_estado_botones_visualizacion()
        #self.actualizar_display_threshold()

        notifier.cell_selected.connect(self.mostrar_info_celda)
        notifier.cell_deselected.connect(self.limpiar_info_celda)

    def mostrar_info_celda(self, cell_id, num_points, min_angle):
        """Muestra información de la celda seleccionada"""
        # Determinar color basado en el ángulo mínimo
        if min_angle < 25:
            color_angle = "#ff6b6b"  # Rojo - crítico
            calidad = "Crítico"
        elif min_angle < 45:
            color_angle = "#ff9f43"  # Naranja - regular
            calidad = "Regular"
        else:
            color_angle = "#4ecdc4"  # Verde - bueno
            calidad = "Bueno"
        
        # Crear HTML para la información de la celda
        celda_html = f"""
        <div style='background-color: #3a3a3a; padding: 8px; border-radius: 4px; margin-top: 8px;'>
            <b style='color: #ffd700;'>Celda seleccionada:</b><br>
            ID: <span style='color:#4ecdc4;'>{cell_id}</span><br>
            Puntos: <span style='color:#ff9f43;'>{num_points}</span><br>
            Ángulo mínimo: <span style='color:{color_angle};'>{min_angle:.2f}°</span><br>
            Calidad: <span style='color:{color_angle};'>{calidad}</span>
        </div>
        """
        
    
        self.actualizar_metricas(self._contenido_base_sin_celda + celda_html)

    def limpiar_info_celda(self):
        
        if hasattr(self, '_contenido_base_sin_celda') and self._contenido_base_sin_celda:
            self.actualizar_metricas(self._contenido_base_sin_celda)
        else:
            # Fallback: mostrar solo el número de refinamiento
            base_path = getattr(self, '_archivo_actual', '')
            if base_path:
                base, _ = os.path.splitext(base_path)
                numero = base.split('_')[-1] if '_' in base else "?"
                contenido_html = f"""
                <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px;'>
                    <b style='color: #ffd700;'>Nivel de Refinamiento: {numero}</b><br><br>
                    <i style='color: #888;'>No hay celda seleccionada</i>
                </div>
                """
                self.actualizar_metricas(contenido_html)
                self._contenido_base_sin_celda = contenido_html


    def actualizar_panel_derecho_custom(self, ruta_archivo):
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
            threshold_actual = self.threshold_angulo

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
            self.actualizar_metricas(contenido_html)

        except Exception as e:
            error_html = f"""
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; color: #ff6b6b;'>
                <b>Error al leer el archivo:</b><br>{str(e)}<br><br>
                <span style='font-size: 12px; color: #cccccc;'>Ruta: {ruta_modificada}</span>
            </div>
            """
            self.panel_derecho.actualizar_metricas(error_html)    
    
    def actualizar_panel_derecho(self, ruta_archivo):
        
        try:
            """
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
            threshold_actual = self.threshold_angulo

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
            contenido_html = f
           

            # Agregar información de triángulos si está disponible
            if min_triangulo and max_triangulo:
                min_tri_formatted = formatear_valor_angular(min_triangulo)
                max_tri_formatted = formatear_valor_angular(max_triangulo)
                color_min_tri = color_por_angulo(min_triangulo)
                color_max_tri = color_por_angulo(max_triangulo)
                
                contenido_html += f
                <b>Triángulos:</b><br>
                <span style='color: {color_min_tri};'>Mín: {min_tri_formatted}</span> | 
                <span style='color: {color_max_tri};'>Máx: {max_tri_formatted}</span><br>
                <span style='color: #ff6b6b;'>⚠️ {criticos_triangulos} ángulos &lt; {threshold_actual}°</span><br><br>
                

            # Agregar información de cuadriláteros si está disponible
            if min_cuadrado and max_cuadrado:
                min_cuad_formatted = formatear_valor_angular(min_cuadrado)
                max_cuad_formatted = formatear_valor_angular(max_cuadrado)
                color_min_cuad = color_por_angulo(min_cuadrado)
                color_max_cuad = color_por_angulo(max_cuadrado)
                
                contenido_html += f
                <b>Cuadriláteros:</b><br>
                <span style='color: {color_min_cuad};'>Mín: {min_cuad_formatted}</span> | 
                <span style='color: {color_max_cuad};'>Máx: {max_cuad_formatted}</span><br>
                <span style='color: #ff6b6b;'>⚠️ {criticos_cuadrados} ángulos &lt; {threshold_actual}°</span><br>
                

            # Agregar calidad general
            

            """
            
            base, _ = os.path.splitext(ruta_archivo)
            numero = base.split('_')[-1]
            contenido_html = f"""
                <div style='margin-top: 10px; padding: 8px; background-color: #3a3a3a; border-radius: 4px;'>
                    <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px;'>
                    <b style='color: #ffd700;'>Nivel de Refinamiento: {numero}</b><br><br>
                </div>
            """
            # Actualizar el panel derecho
            self.actualizar_metricas(contenido_html)
            # Guardar como contenido base limpio (SIN información de celda)
            self._contenido_base_sin_celda = contenido_html

        except Exception as e:
            error_html = f"""
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; color: #ff6b6b;'>
                <b>Error al leer el archivo:</b><br>{str(e)}<br><br>
                <span style='font-size: 12px; color: #cccccc;'>Ruta:</span>
            </div>
            """
            self.actualizar_metricas(error_html)

    def crear_seccion_metricas(self):
        """Sección de métricas de calidad (ahora dinámica)"""
        self.grupo_metricas = QGroupBox("Métricas de Calidad")
        self.grupo_metricas.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Label para mostrar las métricas (inicialmente vacío)
        self.label_metricas = QLabel("Cargue un archivo para ver las métricas")
        self.label_metricas.setWordWrap(True)
        self.label_metricas.setTextFormat(Qt.RichText)
        self.label_metricas.setStyleSheet("""
            QLabel {
                background-color: #2a2a2a;
                padding: 12px;
                border-radius: 6px;
                min-height: 120px;
            }
        """)
        
        layout.addWidget(self.label_metricas)
        self.grupo_metricas.setLayout(layout)
        self.layout_principal.insertWidget(0, self.grupo_metricas)  # Insertar al principio
    
    def actualizar_metricas(self, contenido_html):
        """Actualiza el contenido de las métricas"""
        self.label_metricas.setText(contenido_html)
    
    def crear_seccion_threshold(self):
        """Sección para controlar el threshold de ángulos críticos"""
        grupo = QGroupBox("Umbral de Ángulos Críticos")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Display del valor actual con color (INVERTIDO)
        self.label_threshold = QLabel()
        self.label_threshold.setAlignment(Qt.AlignCenter)
        self.label_threshold.setStyleSheet("""
            QLabel {
                background-color: #2a2a2a;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # Slider para el threshold (INVERTIR MIN/MAX)
        slider_layout = QHBoxLayout()
        label_min = QLabel("10°")
        label_min.setStyleSheet("color: #ff6b6b;")  # ROJO para ángulos bajos (peores)
        
        self.slider_threshold = QSlider(Qt.Horizontal)
        self.slider_threshold.setRange(10, 80)
        self.slider_threshold.setValue(self.threshold_angulo)
        self.slider_threshold.valueChanged.connect(self.actualizar_threshold)
        
        label_max = QLabel("80°")
        label_max.setStyleSheet("color: #4ecdc4;")  # VERDE para ángulos altos (mejores)
        
        slider_layout.addWidget(label_min)
        slider_layout.addWidget(self.slider_threshold)
        slider_layout.addWidget(label_max)
        
        # Leyenda de colores (CORREGIDA)
        leyenda_html = """
        <div style='background-color: #2a2a2a; padding: 8px; border-radius: 4px; font-size: 11px;'>
            <span style='color: #ff6b6b;'>● Crítico</span> | 
            <span style='color: #ff9f43;'>● Regular</span> | 
            <span style='color: #4ecdc4;'>● Bueno</span>
        </div>
        """
        label_leyenda = QLabel(leyenda_html)
        label_leyenda.setTextFormat(Qt.RichText)
        
        layout.addWidget(self.label_threshold)
        layout.addLayout(slider_layout)
        layout.addWidget(label_leyenda)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def actualizar_display_threshold(self):
        """Actualiza el display del threshold con colores (INVERTIDO)"""
        # Determinar color basado en el valor - ÁNGULOS BAJOS = MALOS = ROJO
        if self.threshold_angulo <= 25:
            color = "#f6b6fb"  # ROJO - ángulos muy bajos (críticos)
        elif self.threshold_angulo <= 45:
            color = "#ff9f43"  # NARANJA - ángulos medios (regulares)
        else:
            color = "#4ecdc4"  # VERDE AZULADO - ángulos altos (buenos)
        
        texto = f"Umbral actual: <span style='color: {color}; font-size: 16px;'><b>{self.threshold_angulo}°</b></span>"
        self.label_threshold.setText(texto)
        self.label_threshold.setTextFormat(Qt.RichText)
    
    def crear_seccion_animacion(self):
        """Sección de control de animación"""
        grupo = QGroupBox("Control de Animación")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Control de velocidad
        velocidad_layout = QHBoxLayout()
        label_velocidad = QLabel("Velocidad:")
        self.slider_velocidad = QSlider(Qt.Horizontal)
        self.slider_velocidad.setRange(500, 3000)
        self.slider_velocidad.setValue(1500)
        self.label_velocidad_valor = QLabel("1.5s")
        self.slider_velocidad.valueChanged.connect(self._on_velocidad_cambiada)

        velocidad_layout.addWidget(label_velocidad)
        velocidad_layout.addWidget(self.slider_velocidad)
        velocidad_layout.addWidget(self.label_velocidad_valor)
        
        layout.addLayout(velocidad_layout)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)
    
    def crear_seccion_visualizacion(self):
        """Sección específica para modos de visualización"""
        grupo = QGroupBox("Modo de Visualización")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QHBoxLayout()
        
        # Botones de visualización
        self.boton_wireframe = QPushButton("Wireframe")
        self.boton_solido = QPushButton("Sólido")

        # Tooltips
        self.boton_wireframe.setToolTip("Shortcut: W")
        self.boton_solido.setToolTip("Shortcut: S")

        # Conectar señales
        self.boton_wireframe.clicked.connect(self.activar_wireframe)
        self.boton_solido.clicked.connect(self.activar_solido)
        
        layout.addWidget(self.boton_wireframe)
        layout.addWidget(self.boton_solido)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)
    
    def crear_seccion_acciones(self):
        """Sección de acciones rápidas"""
        grupo = QGroupBox("Acciones Rápidas")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QGridLayout()
        layout.setSpacing(6)
        
        # Botones esenciales
        self.boton_puntos_criticos = QPushButton("Puntos Críticos")
        self.boton_reset_camara = QPushButton("Reset Cámara")
        self.boton_reload = QPushButton("Recargar") 

        self.boton_puntos_criticos.setToolTip("Shortcut: A")
        self.boton_reset_camara.setToolTip("Shortcut: R")
        self.boton_reload.setToolTip("Shortcut: L")

        self.boton_puntos_criticos.clicked.connect(self.toggle_puntos_criticos)
        self.boton_reset_camara.clicked.connect(self.resetear_camara)
        self.boton_reload.clicked.connect(self.reload_modelo)

        # Agregar al layout
        layout.addWidget(self.boton_puntos_criticos, 0, 0)
        layout.addWidget(self.boton_reset_camara, 0, 1)
        layout.addWidget(self.boton_reload, 1, 0, 1, 2)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def actualizar_estadisticas(self, metricas):
        # print("actualizar_estadisticas llamado", metricas)
        """Actualiza la sección de estadísticas con métricas de calidad"""
        self.metricas_actuales = metricas
        
        if not metricas or 'error' in metricas:
            stats_html = """
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #ff6b6b;'>
                <b>❌ No hay métricas disponibles</b><br>
                Carga un modelo primero o verifica el archivo.
            </div>
            """
            self.label_estadisticas.setText(stats_html)
            return
        
        stats = metricas['estadisticas_generales']
        total_triangulos = stats.get('total_triangulos', 0)
        total_cuadrilateros = stats.get('total_cuadrilateros', 0)
        total_caras = total_triangulos + total_cuadrilateros
        
        # Calcular porcentajes
        porc_triangulos = (total_triangulos / total_caras * 100) if total_caras > 0 else 0
        porc_cuadrilateros = (total_cuadrilateros / total_caras * 100) if total_caras > 0 else 0
        
        # Construir HTML en el mismo estilo
        stats_html = f"""
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace;'>
            <b>Topología:</b><br>
            • Caras: <span style='color: #4ecdc4;'>{total_caras}</span><br>
            • Triángulos: <span style='color: #ff9f43;'>{total_triangulos}</span> ({porc_triangulos:.1f}%)<br>
            • Cuadriláteros: <span style='color: #ff9f43;'>{total_cuadrilateros}</span> ({porc_cuadrilateros:.1f}%)<br><br>
            
            <b>Calidad:</b><br>
        """
        
        # Añadir métricas de triángulos si existen
        if metricas['triangulos']:
            triangulos = metricas['triangulos']
            stats_html += f"""
            <b>Triángulos:</b><br>
            • Relación aspecto: <span style='color: #4ecdc4;'>{triangulos.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
            • Ángulo mínimo: <span style='color: #4ecdc4;'>{triangulos.get('min_angle_min', 'N/A'):.1f}°</span><br>
            • Ángulo máximo: <span style='color: #ff6b6b;'>{triangulos.get('max_angle_avg', 'N/A'):.1f}°</span><br>
            • Área promedio: <span style='color: #4ecdc4;'>{triangulos.get('area_avg', 'N/A'):.6f}</span><br>
            """
        
        # Añadir métricas de cuadriláteros si existen
        if metricas['cuadrilateros']:
            cuadrilateros = metricas['cuadrilateros']
            stats_html += f"""
            <b>Cuadriláteros:</b><br>
            • Relación aspecto: <span style='color: #4ecdc4;'>{cuadrilateros.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
            • Ángulo mínimo: <span style='color: #4ecdc4;'>{cuadrilateros.get('min_angle_min', 'N/A'):.1f}°</span><br>
            • Ángulo máximo: <span style='color: #ff6b6b;'>{cuadrilateros.get('max_angle_avg', 'N/A'):.1f}°</span><br>
            • Distorsión: <span style='color: #ff6b6b;'>{cuadrilateros.get('skew_avg', 'N/A'):.3f}</span><br>
            • Relación aristas: <span style='color: #4ecdc4;'>{cuadrilateros.get('edge_ratio_avg', 'N/A'):.3f}</span><br>
            """
        
        stats_html += "</div>"
        self.label_estadisticas.setText(stats_html)
    
    
    def crear_seccion_estadisticas(self):
        """Sección de estadísticas detalladas - Ahora se actualiza dinámicamente"""
        grupo = QGroupBox("Estadísticas Detalladas")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Label para estadísticas (ahora se actualizará dinámicamente)
        self.label_estadisticas = QLabel()
        self.label_estadisticas.setTextFormat(Qt.RichText)
        self.label_estadisticas.setWordWrap(True)
        
        # Mensaje inicial
        html_inicial = """
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #4ecdc4;'>
            <b>🔄 Esperando modelo...</b><br>
            Carga un archivo para ver las estadísticas.
        </div>
        """
        self.label_estadisticas.setText(html_inicial)
        
        layout.addWidget(self.label_estadisticas)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)
    

#---------------------------------------------- Esta es la seccion a modificar xiska ----------------------------------------------------------

    def crear_seccion_coloreos(self):
        """Sección de acciones Coloreo"""
        grupo = QGroupBox("Coloreo")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QGridLayout()
        layout.setSpacing(6)
        
        # Botones esenciales
        self.boton_color = QPushButton("Por área")
        self.boton_color2 = QPushButton("Por ángulo mínimo")
        self.boton_color3 = QPushButton("Relación de aspecto")

        self.boton_color.setToolTip("Shortcut: 1")
        self.boton_color2.setToolTip("Shortcut: 2")

        self.boton_color.clicked.connect(
            lambda: self.refinement_viewer.accion_area() if self.refinement_viewer else None
        )
        self.boton_color2.clicked.connect(
            lambda: self.refinement_viewer.accion_angulo_minimo() if self.refinement_viewer else None
        )
        self.boton_color3.clicked.connect(
            lambda: self.refinement_viewer.accion_relacion_aspecto() if self.refinement_viewer else None
        )

        # Agregar al layout
        layout.addWidget(self.boton_color, 0, 0)
        layout.addWidget(self.boton_color2, 0, 1)
        layout.addWidget(self.boton_color3, 1 , 0 , 1, 2)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)


    def actualizar_threshold(self, valor):
        """Actualiza el threshold y el display"""
        self.threshold_angulo = valor
        self.actualizar_display_threshold()
        print(f"Threshold actualizado: {valor}°")  # Solo para debug
    
    def actualizar_display_threshold(self):
        """Actualiza el display del threshold con colores"""
        # Determinar color basado en el valor
        if self.threshold_angulo <= 25:
            color = "#ff6b6b"  # Verde azulado - muy bajo
        elif self.threshold_angulo <= 45:
            color = "#ff9f43"  # Naranja - medio
        else:
            color = "#4ecdc4"  # Rojo - alto
        
        texto = f"Umbral actual: <span style='color: {color}; font-size: 16px;'><b>{self.threshold_angulo}°</b></span>"
        self.label_threshold.setText(texto)
        self.label_threshold.setTextFormat(Qt.RichText)
    
    def activar_wireframe(self):
        """Activa modo wireframe"""
        self.modo_visualizacion = "wireframe"
        self.actualizar_estado_botones_visualizacion()
        # Llamar a la función del parent si existe
        main_window = self.parentWidget().parentWidget()
        accion_w(main_window)
    
    def activar_solido(self):
        """Activa modo sólido"""
        self.modo_visualizacion = "solido"
        self.actualizar_estado_botones_visualizacion()
        # Llamar a la función del parent si existe
        main_window = self.parentWidget().parentWidget()
        accion_s(main_window)
    
    def actualizar_estado_botones_visualizacion(self):
        """Actualiza el aspecto visual de los botones según el modo activo"""
        estilo_activo = """
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: 2px solid #4caf50;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3d8b40;
            }
        """
        
        estilo_inactivo = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: 1px solid #666;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """
        
        if self.modo_visualizacion == "wireframe":
            self.boton_wireframe.setStyleSheet(estilo_activo)
            self.boton_solido.setStyleSheet(estilo_inactivo)
        else:
            self.boton_wireframe.setStyleSheet(estilo_inactivo)
            self.boton_solido.setStyleSheet(estilo_activo)
    
    def set_modo_visualizacion(self, modo):
        """Sincronizar el modo de visualización desde fuera"""
        if modo in ["wireframe", "solido"]:
            self.modo_visualizacion = modo
            self.actualizar_estado_botones_visualizacion()
    
    def aplicar_estilo_botones(self):
        """Aplica estilo consistente a todos los botones"""
        estilo_base = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: 1px solid #666;
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #777777;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """
        
        # Aplicar a todos los botones
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(estilo_base)

    

    def toggle_puntos_criticos(self):
        if self.refinement_viewer and self.refinement_viewer.switcher:
            self.refinement_viewer.switcher.toggle_load = not self.refinement_viewer.switcher.toggle_load
            if self.refinement_viewer.switcher.toggle_load:
                self.refinement_viewer.switcher.marcar_angulos_extremos()
            else:
                self.refinement_viewer.switcher.clear_extra_models()
            self.refinement_viewer.renderer.GetRenderWindow().Render()

    def resetear_camara(self):
        if self.refinement_viewer and self.refinement_viewer.switcher:
            self.refinement_viewer.switcher.actor.SetOrientation(0, 0, 0)
            self.refinement_viewer.switcher.actor.SetPosition(0, 0, 0)
            self.refinement_viewer.switcher.actor.SetScale(1, 1, 1)
            self.refinement_viewer.renderer.ResetCamera()
            if isinstance(self.refinement_viewer.interactor.GetInteractorStyle(), CustomInteractorStyle):
                self.refinement_viewer.interactor.GetInteractorStyle().reset_camera_and_rotation()
            self.refinement_viewer.renderer.GetRenderWindow().Render()

    def _on_velocidad_cambiada(self, valor):
        """Maneja el cambio de velocidad"""
        segundos = valor / 1000.0
        self.label_velocidad_valor.setText(f"{segundos:.1f}s")
        
        # Ajustar directamente en el refinement viewer si está disponible
        if self.refinement_viewer:
            self.refinement_viewer.ajustar_velocidad(valor)

    def reload_modelo(self):
        """Recarga el modelo actual desde el archivo"""
        if self.refinement_viewer and self.refinement_viewer.switcher:
            switcher = self.refinement_viewer.switcher
            archivos = switcher.file_dict.get(switcher.current_poly, [])
            
            if archivos and 0 <= switcher.current_index < len(archivos):
                archivo_actual = archivos[switcher.current_index]
                print(f"Recargando modelo: {archivo_actual}")

                # LIMPIAR HIGHLIGHTER
                style = switcher.interactor.GetInteractorStyle()
                if isinstance(style, CustomInteractorStyle):
                    if hasattr(style, "highlight_actor") and style.highlight_actor:
                        switcher.renderer.RemoveActor(style.highlight_actor)
                        style.highlight_actor = None
                    style.last_selected_cell = None
                
                # Emitir deselección para limpiar panel
                notifier.cell_deselected.emit()
                
                # Forzar recarga del modelo
                switcher.load_model(archivo_actual)
                
                # Limpiar extras y resetear toggle
                switcher.clear_extra_models()
                switcher.toggle_load = False
                
                # Actualizar panel derecho si es necesario
                if hasattr(self, 'actualizar_panel_derecho'):
                    self.actualizar_panel_derecho(archivo_actual)
                
                print("✅ Modelo recargado exitosamente")
            else:
                print("⚠️ No hay modelo actual para recargar")
        else:
            print("⚠️ No hay refinement viewer o switcher disponible")