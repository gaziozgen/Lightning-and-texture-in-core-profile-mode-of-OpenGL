# CENG 487 Assignment7 by
# Gazi Özgen
# StudentId: 250201051
# 1 2022

from shapes import _Shape
from vector import *


class ObjectReader:

    @staticmethod
    def read(file_name, shader):
        try:
            f = open(file_name)

            vertices = []
            vertex_normals = []
            vertex_textures = []
            faces = []

            for line in f:

                # read vertices
                if line[:2] == "v ":
                    values = line.split()
                    vertex = (float(values[1]), float(values[2]), float(values[3]))
                    vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))

                    vertex = Point3f(vertex[0], vertex[1], vertex[2])
                    vertices.append(vertex)

                # read vertex normals
                elif line[:3] == "vn ":
                    values = line.split()
                    normal = (float(values[1]), float(values[2]), float(values[3]))
                    normal = (round(normal[0], 2), round(normal[1], 2), round(normal[2], 2))

                    normal = Vector3f(normal[0], normal[1], normal[2])
                    vertex_normals.append(normal)

                # read vertex texture coordinates
                elif line[:3] == "vt ":
                    values = line.split()
                    texture_coordinates = (float(values[1]), float(values[2]))
                    texture_coordinates = (round(texture_coordinates[0], 2), round(texture_coordinates[1], 2))

                    texture_coordinates = (texture_coordinates[0], texture_coordinates[1])
                    vertex_textures.append(texture_coordinates)

                # read faces
                elif line[:2] == "f ":
                    values = line.split()
                    face_data = []
                    for i in range(1, 5):
                        vertex_data = []
                        indexes = values[i].split("/")

                        for j in range(len(indexes)):
                            if indexes[j] == "":
                                vertex_data.append(0)
                            else:
                                vertex_data.append(int(indexes[j]) - 1)
                        face_data.append(vertex_data)

                    faces.append(face_data)
            f.close()
            new_object = _Shape("shape", vertices, faces, vertex_normals, vertex_textures, shader)
            return new_object

        except IOError:
            print(".obj file not found.")
            return None
