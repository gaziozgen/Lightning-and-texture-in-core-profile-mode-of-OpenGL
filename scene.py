# CENG 487 Assignment7 by
# Gazi Özgen
# StudentId: 250201051
# 1 2022

from OpenGL.GL import *
from OpenGL.GLUT import *
from lights import *
from ObjectReader import ObjectReader

class Scene:
    def __init__(self):
        self.nodes = []
        self.active_object = None
        self.blend_ratio = 0
        self.pointLight = None
        self.directionalLight = None
        self.spotLight = None
        self.specularLight = 1

    def add(self, node):
        self.nodes.append(node)
        self.active_object = self.nodes[-1]

    def activate_lights(self):
        initSpec(self.active_object.programID)
        self.pointLight = PointLight(self.active_object.programID)
        self.pointLight.initLightParams()
        self.directionalLight = DirectionalLight(self.active_object.programID)
        self.directionalLight.initLightParams()
        self.spotLight = SpotLight(self.active_object.programID)
        self.spotLight.initLightParams()



    def increase_ratio(self, amount):
        self.blend_ratio += amount
        if self.blend_ratio > 100:
            self.blend_ratio = 100
        elif self.blend_ratio < 0:
            self.blend_ratio = 0

        glUseProgram(self.active_object.programID)
        ratioLocation = glGetUniformLocation(self.active_object.programID, "ratio")
        glUniform1f(ratioLocation, self.blend_ratio/100)
        glUseProgram(0)

    # printing UI
    def user_information(self):

        glColor3f(0.9, 0.9, 0.9)

        glWindowPos2i(5, 100)
        line = "Blend ratio: " + str(self.blend_ratio) + "%"
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 80)
        line = "Hit + or - key to change blend ratio in textures."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 65)
        line = "Press \"1\" key to switch on/off the point light."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 50)
        line = "Press \"2\" key to switch on/off the directional light."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 35)
        line = "Press \"3\" key to switch on/off the spotlight."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 20)
        line = "Press \"a\" key to switch on/off the rotation of point light."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 5)
        line = "Press \"b\" key to switch on/off the specular light by Blinn's specular formula."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 485)
        line = "\"Alt\" and drag the left mouse button to rotate shape."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 470)
        line = "\"Alt\" and drag the right mouse button to change distance."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 455)
        line = "\"Alt\" and scroll the middle mouse button to move shape."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))

        glWindowPos2i(5, 440)
        line = "Hit ESC key to quit."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))
