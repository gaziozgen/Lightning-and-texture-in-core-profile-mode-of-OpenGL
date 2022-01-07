# CENG 487 Assignment7 by
# Gazi Özgen
# StudentId: 250201051
# 1 2022

from OpenGL.GL import *
from OpenGL.GLUT import *

import numpy as np
import matrix
from boundingbox import *


def initSpec(programID):
    glUseProgram(programID)
    location = glGetUniformLocation(programID, "isSpec")
    glUniform1i(location, 1)
    glUseProgram(0)


class PointLight:
    def __init__(self, programID):
        self.shape = None
        self.programID = programID
        self.lightColor = numpy.array([1.0, 1.0, 1.0, 1.0], dtype='float32')
        self.lightIntensity = 1.0
        self.centerPos = [0.0, 5.0, -90.0, 1.0]
        self.lightPos = self.centerPos
        self.initLightParams()
        self.turn_around = True
        self.current_angle = 0
        self.radius = 20

    def turnAround(self):
        if self.turn_around:
            self.current_angle += 0.01
            position = Point3f(self.centerPos[0] + (self.radius * np.cos(self.current_angle)),
                               self.centerPos[1],
                               self.centerPos[2] + (self.radius * np.sin(self.current_angle)))

            self.shape.position = position

            glUseProgram(self.programID)
            lightPosLocation = glGetUniformLocation(self.programID, "pointLightPos")
            glUniform3f(lightPosLocation, position.x, position.y, position.z)
            glUseProgram(0)

    def addShape(self, shape):
        self.shape = shape
        self.shape.Translate(self.lightPos[0], self.lightPos[1], self.lightPos[2])

    def initLightParams(self):
        # we need to bind to the program to set lighting related params
        glUseProgram(self.programID)

        # set shader stuff
        lightPosLocation = glGetUniformLocation(self.programID, "pointLightPos")
        glUniform3f(lightPosLocation, self.centerPos[0], self.centerPos[1], self.centerPos[2])
        lightColorLocation = glGetUniformLocation(self.programID, "pointLightColor")
        glUniform4f(lightColorLocation, self.lightColor[0], self.lightColor[1], self.lightColor[2], self.lightColor[3])
        lightIntensityLocation = glGetUniformLocation(self.programID, "pointLightIntensity")
        glUniform1f(lightIntensityLocation, self.lightIntensity)

        # reset program
        glUseProgram(0)


class DirectionalLight:
    def __init__(self, programID):
        self.programID = programID
        self.lightDir = numpy.array([1.0, -1.0, -1.0, 0.0], dtype='float32')
        self.lightColor = numpy.array([1.0, 1.0, 1.0, 1.0], dtype='float32')
        self.lightIntensity = 1.0
        self.initLightParams()

    def initLightParams(self):
        # we need to bind to the program to set lighting related params
        glUseProgram(self.programID)

        # set shader stuff
        lightDirLocation = glGetUniformLocation(self.programID, "directionalLightDir")
        glUniform3f(lightDirLocation, self.lightDir[0], self.lightDir[1], self.lightDir[2])
        lightColorLocation = glGetUniformLocation(self.programID, "directionalLightColor")
        glUniform4f(lightColorLocation, self.lightColor[0], self.lightColor[1], self.lightColor[2], self.lightColor[3])
        lightIntensityLocation = glGetUniformLocation(self.programID, "directionalLightIntensity")
        glUniform1f(lightIntensityLocation, self.lightIntensity)

        # reset program
        glUseProgram(0)


class SpotLight:
    def __init__(self, programID):
        self.programID = programID
        self.shape = None
        self.lightPos = [8.0, 20.0, -80.0, 1.0]
        self.lightDir = numpy.array([0.0, -1.0, 0.0, 0.0], dtype='float32')
        self.lightColor = numpy.array([1.0, 1.0, 1.0, 1.0], dtype='float32')
        self.innerCuttOff = np.cos(np.radians(12))
        self.outherCuttOff = np.cos(np.radians(15))
        self.lightIntensity = 1.0
        self.initLightParams()

    def addShape(self, shape):
        self.shape = shape
        self.shape.Translate(self.lightPos[0], self.lightPos[1], self.lightPos[2])

    def initLightParams(self):
        # we need to bind to the program to set lighting related params
        glUseProgram(self.programID)

        # set shader stuff
        lightPosLocation = glGetUniformLocation(self.programID, "spotlightPosition")
        glUniform3f(lightPosLocation, self.lightPos[0], self.lightPos[1], self.lightPos[2])
        lightDirLocation = glGetUniformLocation(self.programID, "spotlightDirection")
        glUniform3f(lightDirLocation, self.lightDir[0], self.lightDir[1], self.lightDir[2])
        innerCuttOffLocation = glGetUniformLocation(self.programID, "innerCuttOffLocation")
        glUniform1f(innerCuttOffLocation, self.innerCuttOff)
        outherCuttOffLocation = glGetUniformLocation(self.programID, "outherCuttOffLocation")
        glUniform1f(outherCuttOffLocation, self.outherCuttOff)
        lightColorLocation = glGetUniformLocation(self.programID, "spotlightColor")
        glUniform4f(lightColorLocation, self.lightColor[0], self.lightColor[1], self.lightColor[2], self.lightColor[3])
        lightIntensityLocation = glGetUniformLocation(self.programID, "spotlightIntensity")
        glUniform1f(lightIntensityLocation, self.lightIntensity)

        # reset program
        glUseProgram(0)
