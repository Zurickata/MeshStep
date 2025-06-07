import sys
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Controles básicos del interactor de VTK:
# - Botón izquierdo del mouse: Rotar la escena
# - Tecla 'w': wireframe

vertices = []
cells = []
cell_types = []

angle_x = 0.0
angle_y = 0.0
radius = 1.5
mouse_x = 0
mouse_y = 0
left_mouse_down = False
wireframe_mode = False

model_center = [0.0, 0.0, 0.0]
model_radius = 1.0

# ----------------------------- PARSE .VTK ----------------------------- #
def parse_vtk(filename):
    global vertices, cells, cell_types
    with open(filename, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("POINTS"):
            _, count, _ = line.split()
            count = int(count)
            i += 1
            while len(vertices) < count:
                verts = list(map(float, lines[i].strip().split()))
                for j in range(0, len(verts), 3):
                    vertices.append(verts[j:j+3])
                i += 1
            continue
        if line.startswith("CELLS"):
            _, num_cells, _ = line.split()
            num_cells = int(num_cells)
            i += 1
            for _ in range(num_cells):
                parts = list(map(int, lines[i].strip().split()))
                cells.append(parts[1:])  # skip count
                i += 1
            continue
        
        if line.startswith("CELL_TYPES"):
            _, num_types = line.split()
            num_types = int(num_types)
            i += 1
            count = 0
            while count < num_types and i < len(lines):
                for val in lines[i].strip().split():
                    if count >= num_types:
                        break
                    cell_types.append(int(val))
                    count += 1
                i += 1

            continue
        i += 1

# ----------------------------- CÁLCULO DE BOUNDS ----------------------------- #
def compute_model_bounds():
    global model_center, model_radius
    if not vertices:
        return
    verts_np = np.array(vertices)
    min_bounds = verts_np.min(axis=0)
    max_bounds = verts_np.max(axis=0)
    model_center = (min_bounds + max_bounds) / 2.0
    model_radius = np.linalg.norm(max_bounds - model_center) + 0.1

# ----------------------------- CÁMARA ----------------------------- #
def get_camera_position():
    x = model_center[0] + radius * math.sin(angle_x) * math.cos(angle_y)
    y = model_center[1] + radius * math.sin(angle_y)
    z = model_center[2] + radius * math.cos(angle_x) * math.cos(angle_y)
    return [x, y, z]

# ----------------------------- DISPLAY ----------------------------- #
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    cam = get_camera_position()
    gluLookAt(*cam, *model_center, 0, 1, 0)

    for idx, cell in enumerate(cells):
        if cell_types[idx] == 9 and len(cell) == 4:  # VTK_QUAD poligonos de 4 lados
            glColor3f(0.2, 0.7, 1.0)  # Azul celeste para cuadrados
            glBegin(GL_QUADS)
            for v in cell:
                glVertex3fv(vertices[v])
            glEnd()
        elif cell_types[idx] == 5 and len(cell) == 3:  # VTK_TRIANGLE poligonos de 3 lados
            glColor3f(1.0, 0.2, 0.5)  # Rosa para triángulos
            glBegin(GL_TRIANGLES)
            for v in cell:
                glVertex3fv(vertices[v])
            glEnd()
        else:
            continue  # otros tipos ignorados

    glutSwapBuffers()


# ----------------------------- INTERACCIÓN ----------------------------- #
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height or 1), 0.01, 100.0)
    glMatrixMode(GL_MODELVIEW)

def mouse(button, state, x, y):  # detectar mouse
    global left_mouse_down, mouse_x, mouse_y
    if button == GLUT_LEFT_BUTTON:
        left_mouse_down = (state == GLUT_DOWN)
        mouse_x, mouse_y = x, y

def motion(x, y):     # movimiento de camara
    global angle_x, angle_y, mouse_x, mouse_y
    if left_mouse_down:
        dx = x - mouse_x
        dy = y - mouse_y
        angle_x += dx * 0.005 #sensibiidad
        angle_y += dy * 0.005
        mouse_x, mouse_y = x, y
        glutPostRedisplay()

def keyboard(key, x, y):     #Teclado
    global wireframe_mode
    if key == b'w':
        wireframe_mode = not wireframe_mode
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe_mode else GL_FILL)
        glutPostRedisplay()

# ----------------------------- INIT ----------------------------- #
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1) # color del fondo

# ----------------------------- MAIN ----------------------------- #
def main():
    parse_vtk("output.vtk")
    compute_model_bounds()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"VTK Viewer - Triangles and Quads")
    
    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == '__main__':
    main()
