import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import os

os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

# Data storage
points = []
cells = []
cell_types = []
cell_scalars = []
color_table = []

def parse_vtk(filename):
    global points, cells, cell_types, cell_scalars, color_table
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse points
    reading_points = False
    point_count = 0
    for i, line in enumerate(lines):
        if "POINTS" in line:
            parts = line.split()
            point_count = int(parts[1])
            reading_points = True
            continue
            
        if reading_points and point_count > 0:
            data = list(map(float, line.split()))
            for j in range(0, len(data), 3):
                if len(points) < point_count:
                    points.append((data[j], data[j+1]))
            if len(points) >= point_count:
                reading_points = False
                point_count = 0
                
    # Parse cells
    reading_cells = False
    cell_count = 0
    total_ints = 0
    for i, line in enumerate(lines):
        if "CELLS" in line:
            parts = line.split()
            cell_count = int(parts[1])
            total_ints = int(parts[2])
            reading_cells = True
            continue
            
        if reading_cells and cell_count > 0:
            data = list(map(int, line.split()))
            while data:
                n = data.pop(0)
                indices = data[:n]
                data = data[n:]
                cells.append(indices)
                if len(cells) >= cell_count:
                    reading_cells = False
                    break
                    
    # Parse cell types
    reading_types = False
    for i, line in enumerate(lines):
        if "CELL_TYPES" in line:
            reading_types = True
            continue
            
        if reading_types:
            types = list(map(int, line.split()))
            cell_types.extend(types)
            if len(cell_types) >= len(cells):
                reading_types = False
                break
                
    # Parse cell data and color table
    reading_scalars = False
    reading_color_table = False
    color_count = 0
    
    for i, line in enumerate(lines):
        if "SCALARS" in line:
            reading_scalars = True
            continue
            
        if reading_scalars and "LOOKUP_TABLE" in line:
            parts = line.split()
            if len(parts) == 2:  # Scalar data follows
                reading_scalars = True
            elif len(parts) == 3:  # Color table definition
                color_count = int(parts[2])
                reading_color_table = True
                reading_scalars = False
            continue
            
        if reading_scalars:
            scalars = list(map(int, line.split()))
            cell_scalars.extend(scalars)
            if len(cell_scalars) >= len(cells):
                reading_scalars = False
                
        if reading_color_table and color_count > 0:
            colors = list(map(float, line.split()))
            if len(colors) >= 4:
                color_table.append(tuple(colors[:4]))
                if len(color_table) >= color_count:
                    reading_color_table = False

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)

def draw_mesh():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set up orthographic projection
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    padding = 0.1
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(x_min - padding, x_max + padding, y_min - padding, y_max + padding)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Draw filled polygons
    for i, cell in enumerate(cells):
        if cell_types[i] not in [5, 9]:  # Skip unsupported types
            continue
            
        # Get color from lookup table
        if cell_scalars and color_table:
            scalar_val = cell_scalars[i]
            if scalar_val < len(color_table):
                r, g, b, a = color_table[scalar_val]
                glColor4f(r, g, b, a)
            else:
                glColor4f(0.5, 0.5, 0.5, 1.0)  # Default gray
        else:
            glColor4f(0.8, 0.8, 0.8, 1.0)  # Light gray if no color data
        
        # Draw filled polygon
        glBegin(GL_POLYGON)
        for idx in cell:
            glVertex2f(points[idx][0], points[idx][1])
        glEnd()
    
    # Draw wireframe
    glColor3f(0.0, 0.0, 0.0)  # Black wireframe
    glLineWidth(1.0)
    for cell in cells:
        if cell_types[i] not in [5, 9]:
            continue
            
        glBegin(GL_LINE_LOOP)
        for idx in cell:
            glVertex2f(points[idx][0], points[idx][1])
        glEnd()
    
    glutSwapBuffers()

def main():
    if len(sys.argv) < 2:
        print("Usage: python vtk_viewer.py <filename.vtk>")
        return
        
    parse_vtk(sys.argv[1])
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"VTK Mesh Viewer")
    
    init()
    glutDisplayFunc(draw_mesh)
    glutMainLoop()

if __name__ == "__main__":
    main()