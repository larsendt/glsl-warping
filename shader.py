import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

import sys


class Shader(object):
	def __init__(self, vertex_file, fragment_file):
		vertex_shader = self.compileShader(GL_VERTEX_SHADER, vertex_file)
		fragment_shader = self.compileShader(GL_FRAGMENT_SHADER, fragment_file)
		self.program = self.compileProgram(vertex_shader, fragment_shader)
		
	def compileShader(self, shader_type, shader_file):
		try:
			f = open(shader_file, 'r')
		except IOError:
			print "Could not open shader source file:", shader_file
			sys.exit(1)

		shader_src = f.read()
	
		shader = glCreateShader(shader_type)
		glShaderSource(shader, shader_src)
		glCompileShader(shader)
		self.printShaderLog(shader, shader_file)
		return shader
		
	def setUniform1f(self, name, value):
		loc = glGetUniformLocation(self.program, name)
		glUniform1f(loc, value)
		
	def setUniform2f(self, name, v1, v2):
		loc = glGetUniformLocation(self.program, name)
		glUniform2f(loc, v1, v2)
		
	def setUniform3f(self, name, v1, v2, v3):
		loc = glGetUniformLocation(self.program, name)
		glUniform3f(loc, v1, v2, v3)
		
	def setUniform4f(self, name, v1, v2, v3, v4):
		loc = glGetUniformLocation(self.program, name)
		glUniform4f(loc, v1, v2, v3, v4)	
		
	def setUniform1i(self, name, value):
		loc = glGetUniformLocation(self.program, name)
		glUniform1i(loc, value)
		
	def setUniform2i(self, name, v1, v2):
		loc = glGetUniformLocation(self.program, name)
		glUniform2i(loc, v1, v2)
		
	def setUniform3i(self, name, v1, v2, v3):
		loc = glGetUniformLocation(self.program, name)
		glUniform3i(loc, v1, v2, v3)
		
	def setUniform4i(self, name, v1, v2, v3, v4):
		loc = glGetUniformLocation(self.program, name)
		glUniform4i(loc, v1, v2, v3, v4)	
		
	def setUniformMatrix4x4fv(self, name, mat4):
		loc = glGetUniformLocation(self.program, name)
		glUniformMatrix4fv(loc, 1, False, mat4)
	
	def compileProgram(self, vertex_shader, fragment_shader):
		program = glCreateProgram()
		glAttachShader(program, vertex_shader)
		glAttachShader(program, fragment_shader)
		glLinkProgram(program)
		self.printProgramLog(program)
		return program
		
	def printShaderLog(self, shader, shader_file):
		text = glGetShaderInfoLog(shader)
		if text:
			print "Error compiling:", shader_file
			print text
			sys.exit(1)
			
	def printProgramLog(self, program):
		text = glGetProgramInfoLog(program)
		if text:
			print "Error linking shader program."
			print text
			sys.exit(1)
		
	def bind(self):
		glUseProgram(self.program)
		
	def release(self):
		glUseProgram(0)
