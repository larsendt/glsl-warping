import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Quad(object):
	def __init__(self):
		self.display_list = glGenLists(1)
		glNewList(self.display_list, GL_COMPILE)
		
		glBegin(GL_POLYGON)
		glVertex3f(-1, -1, 0)
		glVertex3f(1, -1, 0)
		glVertex3f(1, 1, 0)
		glVertex3f(-1, 1, 0)
		glEnd()
		
		glEndList()

	def draw(self):
		glCallList(self.display_list)
