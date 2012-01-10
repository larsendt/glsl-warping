#!/usr/bin/env python

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
import shader
import time
import math
import random
import quad
import os

class GLWrapper(object):
	def __init__(self):
		glutInit(len(sys.argv), sys.argv)
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
		glutInitWindowSize(800, 600)
		glutCreateWindow('Dynamic FBM Warping')
		#glutFullScreen()
		glutDisplayFunc(self.draw)
		glutMotionFunc(self.mouse_drag)
		glutKeyboardFunc(self.keyboard)
		glutMouseFunc(self.mouse_press)
		glutReshapeFunc(self.reshape)
		glutIdleFunc(self.idle)
		
		glClearColor(0.0, 0.0, 0.0, 1.0)
		
		self.time = time.clock()
		self.screen_width = 1.0
		self.fps = 120
		self.idle_tick = 1.0/self.fps
		self.paused = False
		self.quad = quad.Quad()
		self.high_quality = True
		self.frames_drawn = 0
		self.second_timer = 0
		self.fullscreen = False
		self.scr_width = 800
		self.scr_height = 600
		self.current_shader_index = 3
		self.shaders = []
		
		fragfiles = [item for item in os.listdir("./shaders") if item.endswith("frag")]
		for shaderfile in fragfiles:
			print "Loading shader:", shaderfile
			self.shaders.append(shader.Shader("./shaders/warping.vert", "./shaders/"+shaderfile))
	
	def begin(self):
		glutMainLoop()

	def idle(self):
		if (time.clock() - self.time) > self.idle_tick:
			self.time = time.clock()
			self.frames_drawn += 1
			if time.clock() - self.second_timer > 1:
				glutSetWindowTitle("Dynamic FBM Warping : %d FPS" % self.frames_drawn)
				self.second_timer = time.clock()
				self.frames_drawn = 0
			glutPostRedisplay();
	
	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT)
		glLoadIdentity();
		
		shader = self.shaders[self.current_shader_index]
		shader.bind()
		shader.setUniform1f("time", self.time)
		shader.setUniform1f("screen", self.screen_width)
		glScalef(self.screen_width, 1.0, 1.0)
		self.quad.draw()
		shader.release()
		
		glFlush();
		glutSwapBuffers();
	
	def reshape(self, width, height):
		if height > 0:
			self.screen_width = float(width)/height
		else:
			self.screen_width = 1.0
		
		glViewport(0,0, width,height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-self.screen_width, self.screen_width, -1.0, 1.0, -1.0, 1.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
	def mouse_drag(self, x, y):
		pass
			
	def mouse_press(self, button, state, x, y):
		pass
			
	def keyboard(self, key, x, y):
		if key == '\x1b': #escape key
			print "Quit"
			sys.exit(0)
		elif key == 'h':
			self.current_shader_index += 1
			if self.current_shader_index >= len(self.shaders):
				self.current_shader_index = 0
		elif key == 'f':
			self.fullscreen = not self.fullscreen
			if self.fullscreen:
				glutFullScreen()
			else:
				glutReshapeWindow(self.scr_width, self.scr_height)
		elif key == ' ':
			self.paused = not self.paused
			
	
def main():
	print "Initializing OpenGL..."
	try:
		gl_wrapper = GLWrapper()
		gl_wrapper.begin()
	except Exception as excep:
		print excep
		sys.exit(1)
		
	
if __name__ == "__main__":
	main()
