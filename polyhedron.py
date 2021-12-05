import pygame
from pygame.event import Event
from pygame.locals import *
from math import *
import numpy as np

# pre-defined color and width, height for screen
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLUELIGHT = (0, 0, 95)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 600
projection_matrix = np.matrix([[1, 0, 0], [0, 1, 0]])
scale = 100

# initialize for pygame window
pygame.display.set_caption("3d projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class polyhedron(object):
    def __init__(self, vertexNum, faceNum):
        self.__vertexNum = vertexNum
        self.__faceNum = faceNum
        self.__vertex = []
        self.__face = []

    def get_vertex(self):
        return self.__vertex

    def get_vertexNum(self):
        return self.__vertexNum

    def get_face(self):
        return self.__face

    def setVertex(self, vertex):
        self.__vertex.append(vertex)

    def setFace(self, face):
        self.__face.append(face)

    # get the cordinate of the vertex
    def findVertex(self, i):
        vertices = self.get_vertex()
        for vertex in vertices:
            if (vertex.get_id() == i):
                return [vertex.get_x(), vertex.get_y(), vertex.get_z()]

    # create a list of well-ordered vertex according to vertex id
    def prepareVertices(self):
        vertices = []
        for i in range(1, self.get_vertexNum()+1):
            vertices.append(self.findVertex(i))
        return vertices

    # draw line between two points
    def drawline(self, i, j, points):
        pygame.draw.line(
            screen, RED, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

    # function used to calculate the scale of the angle should be rotated
    def calAngle(self, x1, y1, x2, y2):
        hori = (x1-x2)*1.0/WIDTH * 360
        vert = (y1-y2)*1.0/HEIGHT * 360
        return vert, hori

    # calculate the normal vector for current face
    def cal_normal(self, face):
        point1 = self.findVertex(face.get_p1())
        point2 = self.findVertex(face.get_p2())
        point3 = self.findVertex(face.get_p3())
        a = (point2[1]-point1[1])*(point3[2]-point1[2]) - \
            (point3[1]-point1[1])*(point2[2]-point1[2])
        b = (point2[2]-point1[2])*(point3[0]-point1[0]) - \
            (point3[2]-point1[2])*(point2[0]-point1[0])
        c = (point2[0]-point1[0])*(point3[1]-point1[1]) - \
            (point3[0]-point1[0])*(point2[1]-point1[1])
        return [a, b, c]

    # clolor the surface of each face
    def colorPoly(self, face, points):
        pygame.draw.polygon(screen, BLUELIGHT, ((
            points[face.get_p1()-1]), (points[face.get_p2()-1]), (points[face.get_p3()-1])))

    def draw(self):
        # get Veteice list in order
        points = self.prepareVertices()
        # record the angle that is rotated
        angley = 0
        anglex = 0
        #  create list for projected point
        projected_points = [
            [n, n] for n in range(len(points))
        ]
        # record the positions of mouse before and after mouse movements
        rx = 0
        ry = 0
        rx2 = 0
        ry2 = 0
        # whether the mouse is clicked or not
        press = False

        # the following function is for drawing the shape in 2d graphics
        # it will detect the movements of mouse and calculate the angle it should rotate on y-axis and x-axis
        # After calculation, draw the rotated points and projected points on screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    press = True
                    rx, ry = event.pos

                if event.type == pygame.MOUSEBUTTONUP:
                    press = False

                if event.type == pygame.MOUSEMOTION:
                    if press == True:
                        rx2, ry2 = event.pos
                        anglex, angley = self.calAngle(rx, ry, rx2, ry2)

            # rotation matrix for y-axis
            rotation_y = np.matrix([
                [cos(angley), 0, sin(angley)],
                [0, 1, 0],
                [-sin(angley), 0, cos(angley)],
            ])

           # rotation matrix for x-axis
            rotation_x = np.matrix([
                [1, 0, 0],
                [0, cos(anglex), -sin(anglex)],
                [0, sin(anglex), cos(anglex)],
            ])

            # color the whole screen
            screen.fill(WHITE)
            i = 0

            # calculate the position of the vertices in the screen then color the vertices
            for point in points:
                rotated2d = np.dot(rotation_y, np.mat(point).reshape(3, 1))
                rotated2d = np.dot(rotation_x, rotated2d)
                projected2d = np.dot(
                    projection_matrix, rotated2d)
                print(projected2d)

                # move points to the middle of the screen
                x = int(projected2d[0][0]*scale)+WIDTH/2
                y = int(projected2d[1][0]*scale) + HEIGHT/2
                # store the projected vertices in the list for further use
                projected_points[i] = [x, y]
                i += 1
                pygame.draw.circle(screen, BLUE, (x, y), 5)

            # calculate the normal vector and its dot product with z axis and paint the color
            for face in self.get_face():
                # add two member for face, its normal vector and its dot product with z-axis
                face.norVec = self.cal_normal(face)
                face.dotPro = np.dot(np.mat(face.norVec),
                                     np.mat([0, 0, 1]).reshape(3, 1))

            # draw the line between points
            for face in self.get_face():
                self.drawline(face.get_p1()-1, face.get_p2() -
                              1, projected_points)
                self.drawline(face.get_p2()-1, face.get_p3() -
                              1, projected_points)
                self.drawline(face.get_p1()-1, face.get_p3() -
                              1, projected_points)

            pygame.display.update()
