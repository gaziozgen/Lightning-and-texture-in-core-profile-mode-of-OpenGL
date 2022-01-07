# CENG 487 Assignment7 by
# Gazi Özgen
# StudentId: 250201051
# 1 2022

from ObjectReader import ObjectReader
from camera import *
from shader import Shader
from view import *

v = open("shaders/vertexShader.vert", "r")
vertexShader = v.read()
v.close()

f = open("shaders/fragmentShader.frag", "r")
fragmentShader = f.read()
f.close()

shader = Shader(vertexShader, fragmentShader)

v = open("shaders/lightVertexShader.vert", "r")
lightVertexShader = v.read()
v.close()

f = open("shaders/lightFragmentShader.frag", "r")
lightFragmentShader = f.read()
f.close()

lightShader = Shader(lightVertexShader, lightFragmentShader)

# create camera
camera = Camera()
camera.createView(Point3f(0.0, 0.0, 10.0),
                  Point3f(0.0, 0.0, 0.0),
                  Vector3f(0.0, 1.0, 0.0))
camera.setNear(1)
camera.setFar(1000)

# create View
view = View(camera, None)  # changed to None from grid

# init scene
scene = Scene()
view.setScene(scene)

"""
# Called whenever the window's size changes (including once when the program starts)
def reshape(w, h):
    glViewport(0, 0, w, h)
"""


# The main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

    width = 500
    height = 500
    glutInitWindowSize(width, height)

    glutInitWindowPosition(300, 200)

    window = glutCreateWindow("CENG488 Add light support to Core Profile mode")

    pointLightMesh = ObjectReader.read("Objects/sphere.obj", lightShader)
    scene.add(pointLightMesh)

    spotlightMesh = ObjectReader.read("Objects/cube.obj", lightShader)
    scene.add(spotlightMesh)

    shape = ObjectReader.read("Objects/CornellManifold.obj", shader)

    shape.Translate(0, -20, -90)
    scene.add(shape)

    scene.activate_lights()

    scene.pointLight.addShape(pointLightMesh)
    scene.spotLight.addShape(spotlightMesh)

    # define callbacks
    glutDisplayFunc(view.display)
    glutIdleFunc(view.display)
    glutReshapeFunc(view.resizeView)
    glutKeyboardFunc(view.keyPressed)
    glutSpecialFunc(view.specialKeyPressed)
    glutMouseFunc(view.mousePressed)
    glutMotionFunc(view.mouseMove)

    glutMainLoop()


if __name__ == '__main__':
    main()
