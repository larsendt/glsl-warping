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
        
        print glGetString(GL_VERSION)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        self.time = time.clock()
        self.aspect_ratio = 1.0
        self.width = 800
        self.height = 600
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
        self.offset = [0, 0]
        self.last_pos = [0, 0]
        self.mouse_pressed = False
        
        self.fragfiles = [item for item in os.listdir("./shaders") if item.endswith("frag")]
        for shaderfile in self.fragfiles:
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
        glLoadIdentity()
        
        shader = self.shaders[self.current_shader_index]
        shader.bind()
        shader.setUniform1f("time", self.time)
        shader.setUniform1f("screen", self.aspect_ratio)
        shader.setUniform2f("offset", self.offset[0]/float(self.width), self.offset[1]/float(self.height))
        glScalef(self.aspect_ratio, 1.0, 1.0)
        self.quad.draw()
        shader.release()
        
        glFlush();
        glutSwapBuffers();
    
    def reshape(self, width, height):
        self.width = width
        self.height = height
        if height > 0:
            self.aspect_ratio = float(width)/height
        else:
            self.aspect_ratio = 1.0
        
        glViewport(0,0, width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.aspect_ratio, self.aspect_ratio, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def mouse_drag(self, x, y):
        diff = map(lambda (a, b): a - b, zip((x, y), self.last_pos))
        self.offset[0] -= diff[0] * 2
        self.offset[1] += diff[1] * 2
        self.last_pos = [x, y]
            
    def mouse_press(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.last_pos = [x, y]
            self.mouse_pressed = True
        else:
            self.mouse_pressed = False
            
    def keyboard(self, key, x, y):
        if key == '\x1b': #escape key
            print "Quit"
            sys.exit(0)
        elif key == 'h' or key == "H":
            self.current_shader_index += 1
            if self.current_shader_index >= len(self.shaders):
                self.current_shader_index = 0
            print "Using:", self.fragfiles[self.current_shader_index], ("[%d]" % self.current_shader_index)
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
