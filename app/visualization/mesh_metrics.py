import vtk

import math
import numpy as np
from collections import defaultdict

def calcular_angulo(p1, p2, p3):
    # Calcula el ángulo en p2 formado por p1-p2-p3 (en radianes)
    v1 = [p1[i] - p2[i] for i in range(3)]
    v2 = [p3[i] - p2[i] for i in range(3)]
    def norma(v): return math.sqrt(sum(c*c for c in v))
    def dot(a, b): return sum(a[i]*b[i] for i in range(3))

    nv1 = norma(v1)
    nv2 = norma(v2)
    if nv1 == 0 or nv2 == 0:
            return 0
    cos_theta = dot(v1, v2) / (nv1 * nv2)
    cos_theta = max(-1.0, min(1.0, cos_theta))  # Evitar errores numéricos
    return math.acos(cos_theta)

def calcular_metricas_calidad(grid):
    """
    Calcula métricas de calidad para triángulos y cuadriláteros usando filtros VTK
    Retorna un diccionario con estadísticas para cada tipo de elemento
    """
    if grid.GetNumberOfCells() == 0:
        return {"error": "No hay celdas en la malla"}
    
    resultados = {
        'triangulos': defaultdict(list),
        'cuadrilateros': defaultdict(list),
        'estadisticas_generales': {}
    }
    
    # Contar tipos de elementos y separar celdas por tipo
    triangulos = []
    cuadrilateros = []
    
    for i in range(grid.GetNumberOfCells()):
        cell = grid.GetCell(i)
        if cell.GetCellType() == vtk.VTK_TRIANGLE:
            triangulos.append(i)
        elif cell.GetCellType() == vtk.VTK_QUAD:
            cuadrilateros.append(i)
    
    resultados['estadisticas_generales']['total_triangulos'] = len(triangulos)
    resultados['estadisticas_generales']['total_cuadrilateros'] = len(cuadrilateros)
    
    # Métricas para triángulos
    if triangulos:
        triangulo_metrics = _calcular_metricas_triangulos(grid, triangulos)
        resultados['triangulos'] = triangulo_metrics
    
    # Métricas para cuadriláteros
    if cuadrilateros:
        quad_metrics = _calcular_metricas_cuadrilateros(grid, cuadrilateros)
        resultados['cuadrilateros'] = quad_metrics
    
    return resultados

def _calcular_metricas_triangulos(grid, triangulo_indices):
    """Calcula métricas de calidad específicas para triángulos"""
    metrics = defaultdict(list)
    
    if not triangulo_indices:
        return metrics
    
    # Crear un grid temporal solo con triángulos
    triangle_points = vtk.vtkPoints()
    triangle_cells = vtk.vtkCellArray()
    triangle_grid = vtk.vtkUnstructuredGrid()
    
    point_id_map = {}
    new_point_id = 0
    
    # Extraer triángulos y sus puntos
    for cell_id in triangulo_indices:
        cell = grid.GetCell(cell_id)
        triangle_cell = vtk.vtkTriangle()
        
        for i in range(cell.GetNumberOfPoints()):
            point_id = cell.GetPointId(i)
            point = grid.GetPoint(point_id)
            
            if point_id not in point_id_map:
                point_id_map[point_id] = new_point_id
                triangle_points.InsertNextPoint(point)
                new_point_id += 1
            
            triangle_cell.GetPointIds().SetId(i, point_id_map[point_id])
        
        triangle_cells.InsertNextCell(triangle_cell)
    
    triangle_grid.SetPoints(triangle_points)
    triangle_grid.SetCells(vtk.VTK_TRIANGLE, triangle_cells)
    
    # Calcular área
    area_filter = vtk.vtkMeshQuality()
    area_filter.SetInputData(triangle_grid)
    area_filter.SetTriangleQualityMeasureToArea()
    area_filter.Update()
    area_array = area_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular aspect ratio
    aspect_filter = vtk.vtkMeshQuality()
    aspect_filter.SetInputData(triangle_grid)
    aspect_filter.SetTriangleQualityMeasureToAspectRatio()
    aspect_filter.Update()
    aspect_array = aspect_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular ángulos mínimos y máximos
    min_angle_filter = vtk.vtkMeshQuality()
    min_angle_filter.SetInputData(triangle_grid)
    min_angle_filter.SetTriangleQualityMeasureToMinAngle()
    min_angle_filter.Update()
    min_angle_array = min_angle_filter.GetOutput().GetCellData().GetArray("Quality")
    
    max_angle_filter = vtk.vtkMeshQuality()
    max_angle_filter.SetInputData(triangle_grid)
    max_angle_filter.SetTriangleQualityMeasureToMaxAngle()
    max_angle_filter.Update()
    max_angle_array = max_angle_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Almacenar todas las métricas
    for i in range(len(triangulo_indices)):
        metrics['area'].append(area_array.GetValue(i))
        metrics['aspect_ratio'].append(aspect_array.GetValue(i))
        metrics['min_angle'].append(min_angle_array.GetValue(i))
        metrics['max_angle'].append(max_angle_array.GetValue(i))
    
    # Calcular estadísticas
    stats = {}
    for metric_name, values in metrics.items():
        if values:
            stats[f'{metric_name}_min'] = min(values)
            stats[f'{metric_name}_max'] = max(values)
            stats[f'{metric_name}_avg'] = sum(values) / len(values)
            stats[f'{metric_name}_std'] = np.std(values) if len(values) > 1 else 0
    
    # Combinar las métricas con las estadísticas
    metrics.update(stats)
    metrics['cell_ids'] = list(triangulo_indices)
    return metrics

def _calcular_metricas_cuadrilateros(grid, quad_indices):
    """Calcula métricas de calidad específicas para cuadriláteros"""
    metrics = defaultdict(list)
    
    if not quad_indices:
        return metrics
    
    # Crear un grid temporal solo con cuadriláteros
    quad_points = vtk.vtkPoints()
    quad_cells = vtk.vtkCellArray()
    quad_grid = vtk.vtkUnstructuredGrid()
    
    point_id_map = {}
    new_point_id = 0
    
    # Extraer cuadriláteros y sus puntos
    for cell_id in quad_indices:
        cell = grid.GetCell(cell_id)
        quad_cell = vtk.vtkQuad()
        
        for i in range(cell.GetNumberOfPoints()):
            point_id = cell.GetPointId(i)
            point = grid.GetPoint(point_id)
            
            if point_id not in point_id_map:
                point_id_map[point_id] = new_point_id
                quad_points.InsertNextPoint(point)
                new_point_id += 1
            
            quad_cell.GetPointIds().SetId(i, point_id_map[point_id])
        
        quad_cells.InsertNextCell(quad_cell)
    
    quad_grid.SetPoints(quad_points)
    quad_grid.SetCells(vtk.VTK_QUAD, quad_cells)
    
    # Calcular área
    area_filter = vtk.vtkMeshQuality()
    area_filter.SetInputData(quad_grid)
    area_filter.SetQuadQualityMeasureToArea()
    area_filter.Update()
    area_array = area_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular aspect ratio
    aspect_filter = vtk.vtkMeshQuality()
    aspect_filter.SetInputData(quad_grid)
    aspect_filter.SetQuadQualityMeasureToAspectRatio()
    aspect_filter.Update()
    aspect_array = aspect_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular distorsión (skew)
    skew_filter = vtk.vtkMeshQuality()
    skew_filter.SetInputData(quad_grid)
    skew_filter.SetQuadQualityMeasureToSkew()
    skew_filter.Update()
    skew_array = skew_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular relación de aspecto (edge ratio)
    edge_ratio_filter = vtk.vtkMeshQuality()
    edge_ratio_filter.SetInputData(quad_grid)
    edge_ratio_filter.SetQuadQualityMeasureToEdgeRatio()
    edge_ratio_filter.Update()
    edge_ratio_array = edge_ratio_filter.GetOutput().GetCellData().GetArray("Quality")
    
        # Calcular ángulos mínimos y máximos manualmente para cada cuadrilátero
    for i, cell_id in enumerate(quad_indices):
        cell = grid.GetCell(cell_id)
        puntos = [cell.GetPoints().GetPoint(j) for j in range(cell.GetNumberOfPoints())]
        
        # Calcular los 4 ángulos del cuadrilátero
        angulos = []
        n = len(puntos)  # debería ser 4 para cuadriláteros
        for j in range(n):
            p1 = puntos[j-1]  # Punto anterior
            p2 = puntos[j]    # Punto actual
            p3 = puntos[(j+1) % n]  # Punto siguiente
            
            angulo_rad = calcular_angulo(p1, p2, p3)
            angulo_deg = math.degrees(angulo_rad)
            angulos.append(angulo_deg)
        
        # Almacenar ángulo mínimo y máximo
        metrics['min_angle'].append(min(angulos))
        metrics['max_angle'].append(max(angulos))
        
        # Almacenar las otras métricas VTK
        metrics['area'].append(area_array.GetValue(i))
        metrics['aspect_ratio'].append(aspect_array.GetValue(i))
        metrics['skew'].append(skew_array.GetValue(i))
        metrics['edge_ratio'].append(edge_ratio_array.GetValue(i))
    
    # Calcular estadísticas
    stats = {}
    for metric_name, values in metrics.items():
        if values:
            stats[f'{metric_name}_min'] = min(values)
            stats[f'{metric_name}_max'] = max(values)
            stats[f'{metric_name}_avg'] = sum(values) / len(values)
            stats[f'{metric_name}_std'] = np.std(values) if len(values) > 1 else 0
    
    # Combinar las métricas con las estadísticas
    metrics.update(stats)
    metrics['cell_ids'] = list(quad_indices)
    
    return metrics

def mostrar_metricas_calidad(metricas):
    """Muestra las métricas de calidad en el panel derecho en formato HTML"""
    
    if not metricas or 'error' in metricas:
        html = """
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #ff6b6b;'>
            <b>❌ No hay métricas disponibles</b><br>
            Carga un modelo primero o verifica el archivo.
        </div>
        """
        panel_label.setText(html)
        return
    
    stats = metricas['estadisticas_generales']
    total_triangulos = stats.get('total_triangulos', 0)
    total_cuadrilateros = stats.get('total_cuadrilateros', 0)
    total_caras = total_triangulos + total_cuadrilateros
    
    # Calcular porcentajes
    porc_triangulos = (total_triangulos / total_caras * 100) if total_caras > 0 else 0
    porc_cuadrilateros = (total_cuadrilateros / total_caras * 100) if total_caras > 0 else 0
    
    # Preparar HTML base
    html = f"""
    <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace;'>
        <b style='color: #ffffff;'>Topología:</b><br>
        • Vértices: <span style='color: #4ecdc4;'>N/A</span><br>
        • Caras: <span style='color: #4ecdc4;'>{total_caras}</span><br>
        • Triángulos: <span style='color: #ff9f43;'>{total_triangulos}</span> ({porc_triangulos:.1f}%)<br>
        • Cuadriláteros: <span style='color: #ff9f43;'>{total_cuadrilateros}</span> ({porc_cuadrilateros:.1f}%)<br><br>
        
        <b style='color: #ffffff;'>Calidad:</b><br>
    """
    
    # Añadir métricas de triángulos si existen
    if metricas['triangulos']:
        triangulos = metricas['triangulos']
        html += f"""
        <b>Triángulos:</b><br>
        • Relación aspecto: <span style='color: #4ecdc4;'>{triangulos.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
        • Ángulo mínimo: <span style='color: #4ecdc4;'>{triangulos.get('min_angle_avg', 'N/A'):.1f}°</span><br>
        • Ángulo máximo: <span style='color: #4ecdc4;'>{triangulos.get('max_angle_avg', 'N/A'):.1f}°</span><br>
        • Área promedio: <span style='color: #4ecdc4;'>{triangulos.get('area_avg', 'N/A'):.6f}</span><br>
        """
    
    # Añadir métricas de cuadriláteros si existen
    if metricas['cuadrilateros']:
        cuadrilateros = metricas['cuadrilateros']
        html += f"""
        <b>Cuadriláteros:</b><br>
        • Relación aspecto: <span style='color: #4ecdc4;'>{cuadrilateros.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
        • Distorsión: <span style='color: #ff6b6b;'>{cuadrilateros.get('skew_avg', 'N/A'):.3f}</span><br>
        • Relación aristas: <span style='color: #4ecdc4;'>{cuadrilateros.get('edge_ratio_avg', 'N/A'):.3f}</span><br>
        • Área promedio: <span style='color: #4ecdc4;'>{cuadrilateros.get('area_avg', 'N/A'):.6f}</span><br>
        """
    
    html += "</div>"