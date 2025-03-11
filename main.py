import pygame
import numpy as np
from math import *


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.middle_point = (self.screen_width / 2, self.screen_height / 2)
        self.zoom = 350
        self.zoom_speed = 3
        self.RED = (255, 51, 51)
        self.angle = 0

        self.points = self.create_three_d_matrix()
        self.projection = self.create_projection_matrix()
        self.angle = 0
        self.x_rotation, self.y_rotation, self.z_rotation = self.create_rotation()
        self.projected_points = [
            [n, n] for n in range(len(self.points))
        ]  

        self.start()

    def start(self):

        clock = pygame.time.Clock()
        zoom_out = True
        while self.running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.x_rotation, self.y_rotation, self.z_rotation = self.create_rotation()
            self.angle += 0.01
            self.screen.fill("black")

            self.draw_field()
            self.isometric()

            if zoom_out:
                self.zoom -= self.zoom_speed
            if not zoom_out:
                self.zoom += self.zoom_speed
            if self.zoom == 50:
                zoom_out = False
            if self.zoom == 350:
                zoom_out = True

            pygame.display.flip()

    def draw_field(self):
        pygame.draw.line(self.screen, (255, 255, 255), (0, 0), (self.screen_width // 4, self.screen_height // 3), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.screen_height), (self.screen_width // 4, (self.screen_height // 3) * 2), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width, 0), ((self.screen_width // 4) * 3, self.screen_height // 3), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width, self.screen_height), ((self.screen_width // 4) * 3, (self.screen_height // 3) * 2), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width // 4, self.screen_height // 3), (self.screen_width // 4, (self.screen_height // 3) * 2))
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width // 4, self.screen_height // 3), ((self.screen_width // 4) * 3, self.screen_height // 3))
        pygame.draw.line(self.screen, (255, 255, 255), ((self.screen_width // 4) * 3, (self.screen_height // 3) * 2), (self.screen_width // 4, (self.screen_height // 3) * 2), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), ((self.screen_width // 4) * 3, (self.screen_height // 3) * 2), ((self.screen_width // 4) * 3, self.screen_height // 3), width=2 )

    def create_three_d_matrix(self):
        points = []
        points.append(np.matrix([-1, -1, 1]))
        points.append(np.matrix([1, -1, 1]))
        points.append(np.matrix([1,  1, 1]))
        points.append(np.matrix([-1, 1, 1]))
        points.append(np.matrix([-1, -1, -1]))
        points.append(np.matrix([1, -1, -1]))
        points.append(np.matrix([1, 1, -1]))
        points.append(np.matrix([-1, 1, -1]))
        return points
    
    def create_projection_matrix(self):
        projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
        ])
        return projection_matrix

    def create_rotation(self):
        rotation_z = np.matrix([
            [cos(self.angle), -sin(self.angle), 0],
            [sin(self.angle), cos(self.angle), 0],
            [0, 0, 1],
        ])

        rotation_y = np.matrix([
            [cos(self.angle), 0, sin(self.angle)],
            [0, 1, 0],
            [-sin(self.angle), 0, cos(self.angle)],
        ])

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(self.angle), -sin(self.angle)],
            [0, sin(self.angle), cos(self.angle)],
        ])

        return rotation_x, rotation_y, rotation_z

    def isometric(self):
             
        i = 0
        for point in self.points:
            rotated_two_d = np.dot(self.z_rotation, point.reshape((3, 1)))
            rotated_two_d = np.dot(self.y_rotation, rotated_two_d)
            rotated_two_d = np.dot(self.x_rotation, rotated_two_d)

            projected_two_d = np.dot(self.projection, rotated_two_d)
            x = int(projected_two_d[0][0] * self.zoom) + self.middle_point[0]
            y = int(projected_two_d[1][0] * self.zoom) + self.middle_point[1]
            self.projected_points[i] = [x, y]
            i += 1
        
        for p in range(4):
            self.connect_points(p, (p+1) % 4, self.projected_points)
            self.connect_points(p+4, ((p+1) % 4) + 4, self.projected_points)
            self.connect_points(p, (p+4), self.projected_points)
    
    def connect_points(self, i, j, points):
        pygame.draw.line(
            self.screen, self.RED, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

        


                       
Main()