import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os

os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"
os.environ['PYOPENGL_PLATFORM'] = 'glx'

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background

def draw_square():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw a colored square
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex2f(-0.5, -0.5)
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex2f(0.5, -0.5)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex2f(0.5, 0.5)
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glVertex2f(-0.5, 0.5)
    glEnd()
    
    glutSwapBuffers()

def main():
    # Initialize GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"OpenGL Square Test")
    
    # Set up the callback functions
    glutDisplayFunc(draw_square)
    
    # Initialize OpenGL
    init()
    
    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()