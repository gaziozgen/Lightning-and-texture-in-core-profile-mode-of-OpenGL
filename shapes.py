# CENG 487 Assignment7 by
# Gazi Özgen
# StudentId: 250201051
# 1 2022

import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image

import matrix
from boundingbox import *
from defs import DrawStyle

__all__ = ['_Shape', 'DrawStyle']


class _Shape:
    def __init__(self, name, vertices, faces, normals, tex_coordinates, shader):
        self.position = Point3f(0, 0, 0)
        self.vertices = vertices
        # self.edges = []
        self.faces = faces
        self.normals = normals
        self.tex_coordinates = tex_coordinates
        self.colors = []
        self.obj2World = Matrix()
        self.drawStyle = DrawStyle.NODRAW
        self.wireOnShaded = False
        self.wireWidth = 2
        self.name = name
        self.fixedDrawStyle = False
        self.wireColor = ColorRGBA(0.7, 1.0, 0.0, 1.0)
        self.wireOnShadedColor = ColorRGBA(1.0, 1.0, 1.0, 1.0)
        self.bboxObj = BoundingBox()
        self.bboxWorld = BoundingBox()
        self.calcBboxObj()
        self.VBO = -1
        self.VAO = -1
        self.VBOData = None
        self.programID = -1
        self.vertexDim = 4
        self.nVertices = len(faces) * self.vertexDim
        self.tex1ID = -1
        self.tex2ID = -1
        self.initColors()
        self.init(shader)

    def initColors(self):
        for i in range(0, len(self.faces) + 1):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            self.colors.append(ColorRGBA(1, 1, 1, 1.0))

    def calcBboxObj(self):
        for vertex in self.vertices:
            self.bboxObj.expand(vertex)

    def setDrawStyle(self, style):
        self.drawStyle = style

    def setWireColor(self, r, g, b, a):
        self.wireColor = ColorRGBA(r, g, b, a)

    def setWireWidth(self, width):
        self.wireWidth = width

    def Translate(self, x, y, z):
        self.position += Point3f(x, y, z)

    # Function that accepts a list of shaders, compiles them, and returns a handle to the compiled program
    def createProgram(self, shaderList):
        programID = glCreateProgram()

        for shader in shaderList:
            glAttachShader(programID, shader)

        glLinkProgram(programID)

        status = glGetProgramiv(programID, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(programID)
            print(b"Linker failure: \n" + strInfoLog)

        # important for cleanup
        for shaderID in shaderList:
            glDetachShader(programID, shaderID)

        return programID

    # Function that creates and compiles shaders according to the given type (a GL enum value) and
    # shader program (a string containing a GLSL program).
    def createShader(self, shaderType, shaderCode):
        shaderID = glCreateShader(shaderType)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)

        status = None
        glGetShaderiv(shaderID, GL_COMPILE_STATUS, status)
        if status == GL_FALSE:
            # Note that getting the error log is much simpler in Python than in C/C++
            # and does not require explicit handling of the string buffer
            strInfoLog = glGetShaderInfoLog(shaderID)
            strShaderType = ""
            if shaderType is GL_VERTEX_SHADER:
                strShaderType = "vertex"
            elif shaderType is GL_GEOMETRY_SHADER:
                strShaderType = "geometry"
            elif shaderType is GL_FRAGMENT_SHADER:
                strShaderType = "fragment"

            print(b"Compilation failure for " + strShaderType + b" shader:\n" + strInfoLog)

        return shaderID

    # Set up the list of shaders, and call functions to compile them
    def initProgram(self, shader):
        shaderList = []

        shaderList.append(self.createShader(GL_VERTEX_SHADER, shader.vertexShader))
        shaderList.append(self.createShader(GL_FRAGMENT_SHADER, shader.fragmentShader))

        self.programID = self.createProgram(shaderList)

        for shader in shaderList:
            glDeleteShader(shader)

    # Initialize the OpenGL environment
    def init(self, shader):
        self.initProgram(shader)
        self.initVertexBufferData()
        self.initVertexBuffer()
        self.initTextures("textures/texture1.png", "textures/texture2.png")

    def initVertexBufferData(self):

        finalVertexPositions = []
        finalVertexColors = []
        finalVertexUvs = []
        finalVertexNormals = []

        # go over faces and assemble an array for all vertex data
        for face in self.faces:
            for i in range(len(face)):
                finalVertexPositions.extend(self.vertices[face[i][0]].toArray())
                finalVertexColors.extend(self.colors[i].toArray())
                finalVertexUvs.extend(self.tex_coordinates[face[i][1]])
                finalVertexNormals.extend(self.normals[face[i][2]].toArray())

        self.VBOData = numpy.array(finalVertexPositions + finalVertexColors + finalVertexUvs + finalVertexNormals,
                                   dtype='float32')

    # Set up the vertex buffer that will store our vertex coordinates for OpenGL's access
    def initVertexBuffer(self):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        # bind to our VAO
        glBindVertexArray(self.VAO)

        # now change the state - it will be recorded in the VAO
        # set array buffer to our ID
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # set data
        elementSize = numpy.dtype(numpy.float32).itemsize

        # third argument is criptic - in c_types if you multiply a data type with an integer you create an array of that type
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.VBOData) * elementSize,
                     self.VBOData,
                     GL_STATIC_DRAW
                     )

        # setup vertex attributes
        offset = 0

        # location 0
        glVertexAttribPointer(0, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        # define colors which are passed in location 1 - they start after all positions and has four floats consecutively
        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(1, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)

        # define uvs which are passed in location 2 - they start after all positions and colors and has two floats per vertex
        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, elementSize * 2, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(2)

        # define normals which are passed in location 3 - they start after all positions, colors and uvs and has four floats per vertex
        offset += elementSize * 2 * self.nVertices
        glVertexAttribPointer(3, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(3)

        # reset array buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # texture stuff
    def initTextures(self, texFilename1, texFilename2):
        # we need to bind to the program to set texture related params
        glUseProgram(self.programID)

        self.tex1ID = self.loadTexture(texFilename1)
        self.tex2ID = self.loadTexture(texFilename2)

        # set shader stuff
        tex1Location = glGetUniformLocation(self.programID, "tex1")
        glUniform1i(tex1Location, self.tex1ID)

        tex2Location = glGetUniformLocation(self.programID, "tex2")
        glUniform1i(tex2Location, self.tex2ID)

        # now activate texture units
        glActiveTexture(GL_TEXTURE0 + self.tex1ID)
        glBindTexture(GL_TEXTURE_2D, self.tex1ID)

        glActiveTexture(GL_TEXTURE0 + self.tex2ID)
        glBindTexture(GL_TEXTURE_2D, self.tex2ID)

        ratioLocation = glGetUniformLocation(self.programID, "ratio")
        glUniform1f(ratioLocation, 0)

        glUseProgram(0)

    def loadTexture(self, texFilename):
        # load texture - flip int verticallt to convert from pillow to OpenGL orientation
        image = Image.open(texFilename).transpose(Image.FLIP_TOP_BOTTOM)

        # create a new id
        texID = glGenTextures(1)
        # bind to the new id for state
        glBindTexture(GL_TEXTURE_2D, texID)

        # set texture params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # copy texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                     numpy.frombuffer(image.tobytes(), dtype=numpy.uint8))
        glGenerateMipmap(GL_TEXTURE_2D)

        return texID

    def draw(self, camera):
        # use our program
        programID = self.programID
        glUseProgram(programID)

        viewPosition = glGetUniformLocation(programID, "viewPosition")
        glUniform3f(viewPosition, camera.center.x, camera.center.y, camera.center.z)

        # get matrices and bind them to vertex shader locations
        modelLocation = glGetUniformLocation(programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, matrix.Matrix.getModelMatrix(self.position))
        viewLocation = glGetUniformLocation(programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, matrix.Matrix.getViewMatrix(camera))
        projLocation = glGetUniformLocation(programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE,
                           matrix.Matrix.getProjMatrix(camera.near, camera.far, camera.aspect, camera.fov))

        # bind to our VAO
        glBindVertexArray(self.VAO)

        # draw stuff
        glDrawArrays(GL_QUADS, 0, self.nVertices)

        # reset to defaults
        glBindVertexArray(0)
        glUseProgram(0)
