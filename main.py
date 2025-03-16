import pygame
import numpy as np
from math import *

from target import Target


class Main:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tesseract")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.middle_point = (self.screen_width / 2, self.screen_height / 2)
        self.zoom = 350
        self.zoom_speed = 3
        self.RED = (255, 51, 51)
        self.WHITE = (255, 255, 255)
        self.BLACK= (0, 0, 0)
        self.input_rects_colors = self.fill_input_colors() 
        self.angle = 0
        self.offset = 0
        self.offset_multiplicator = 1
        self.x_offset = 1
        self.y_offset_set = 1
        self.y_offset_multi = 1
        self.y_offset = 0
        self.y_rect_colors = [self.BLACK, self.BLACK]
        self.targets = [Target(True)]
        self.game_points = 0
        self.font_points = pygame.font.SysFont("monospace", 50)
        self.font_time = pygame.font.SysFont("monospace", 30)

        self.points = self.create_three_d_matrix()
        self.projection = self.create_projection_matrix()
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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.set_offset_multiplicator(True)
                    if event.key == pygame.K_LEFT:
                        self.set_offset_multiplicator(False)
                    if event.key == pygame.K_UP:
                        self.set_y_offset(True)
                    if event.key == pygame.K_DOWN:
                        self.set_y_offset(False)

            for t in self.targets:
                t.call_timer()

            self.x_rotation, self.y_rotation, self.z_rotation = self.create_rotation()
            self.angle += 0.01
            self.screen.fill("black")

            self.draw_field()
            self.draw_left_right_rects()
            self.draw_up_down_rects()
            self.draw_targets()
            self.draw_game_points()
            self.isometric()

            if zoom_out:
                self.zoom -= self.zoom_speed
                if self.x_offset != 1:
                    self.offset += 1
                if self.y_offset_set != 1:
                    self.y_offset += 1
            if not zoom_out:
                self.zoom += self.zoom_speed
                if self.x_offset != 1:
                    self.offset -= 1
                if self.y_offset_set != 1:
                    self.y_offset -= 1
            if self.zoom == 50:
                zoom_out = False
                self.check_for_hit()
            if self.zoom == 350:
                self.x_offset = self.offset_multiplicator
                self.y_offset_set = self.y_offset_multi
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
            x = int(projected_two_d[0][0] * self.zoom) + (self.middle_point[0] + (self.offset * self.x_offset))
            y = int(projected_two_d[1][0] * self.zoom) + (self.middle_point[1] + self.y_offset * self.y_offset_set)
            self.projected_points[i] = [x, y]
            i += 1
        
        for p in range(4):
            self.connect_points(p, (p+1) % 4, self.projected_points)
            self.connect_points(p+4, ((p+1) % 4) + 4, self.projected_points)
            self.connect_points(p, (p+4), self.projected_points)
    
    def connect_points(self, i, j, points):
        pygame.draw.line(
            self.screen, self.RED, (points[i][0], points[i][1]), (points[j][0], points[j][1]))
        
    def draw_left_right_rects(self):
        left = self.screen_width / 2 + 150
        top = self.screen_height - 150
        for c in self.input_rects_colors:
            pygame.draw.rect(self.screen, c, (left, top, 100, 50))
            left -= 150
        
        left = self.screen_width / 2 + 150
        for i in range(4):
            pygame.draw.rect(self.screen, self.WHITE, (left, top, 100, 50), 5)
            left -= 150

    def draw_up_down_rects(self):
        center = self.screen_width / 2 - 75
        top = self.screen_height
        pygame.draw.rect(self.screen, self.y_rect_colors[0], (center, top-225, 100, 50))
        pygame.draw.rect(self.screen, self.WHITE, (center, top-225, 100, 50), 5)
        pygame.draw.rect(self.screen, self.y_rect_colors[1], (center, top-75, 100, 50))
        pygame.draw.rect(self.screen, self.WHITE, (center, top-75, 100, 50), 5)



    def fill_input_colors(self):
        c = [self.BLACK, self.BLACK, self.BLACK, self.BLACK]
        return c
    
    def set_offset_multiplicator(self, right: bool):
        if right:
            if self.offset_multiplicator < 4:
                if self.offset_multiplicator == -2:
                    self.offset_multiplicator = 1
                elif self.offset_multiplicator == 1:
                    self.offset_multiplicator += 1
                elif self.offset_multiplicator == 2 or self.offset_multiplicator == -4:
                    self.offset_multiplicator += 2
        else:
            if self.offset_multiplicator > -4:
                if self.offset_multiplicator == 1:
                    self.offset_multiplicator = -2
                elif self.offset_multiplicator == 2:
                    self.offset_multiplicator -= 1
                elif self.offset_multiplicator == -2 or self.offset_multiplicator == 4:
                    self.offset_multiplicator -= 2

        i = self.offset_multiplicator
        match i:
            case 4:
                self.input_rects_colors[0] = self.WHITE
                self.input_rects_colors[1] = self.WHITE
                self.input_rects_colors[2] = self.BLACK
                self.input_rects_colors[3] = self.BLACK
            case 2:
                self.input_rects_colors[0] = self.BLACK
                self.input_rects_colors[1] = self.WHITE
                self.input_rects_colors[2] = self.BLACK
                self.input_rects_colors[3] = self.BLACK
            case -4:
                self.input_rects_colors[0] = self.BLACK
                self.input_rects_colors[1] = self.BLACK
                self.input_rects_colors[2] = self.WHITE
                self.input_rects_colors[3] = self.WHITE
            case -2:
                self.input_rects_colors[0] = self.BLACK
                self.input_rects_colors[1] = self.BLACK
                self.input_rects_colors[2] = self.WHITE
                self.input_rects_colors[3] = self.BLACK
            case 1:
                self.input_rects_colors[0] = self.BLACK
                self.input_rects_colors[1] = self.BLACK
                self.input_rects_colors[2] = self.BLACK
                self.input_rects_colors[3] = self.BLACK

    def draw_targets(self):
        for t in self.targets:
            pygame.draw.circle(self.screen, self.WHITE, t.get_position(), 60)
            pygame.draw.circle(self.screen, self.BLACK, t.get_position(), 55)
            pygame.draw.circle(self.screen, self.WHITE, t.get_position(), 35)
            pygame.draw.circle(self.screen, self.BLACK, t.get_position(), 30)
            label = self.font_points.render(str(t.get_timer())[:2], 1, (255, 255, 255))
            self.screen.blit(label, np.subtract(t.get_position(), (15, 15)))

    def add_target(self):
        self.targets.append(Target(False))
    
    def check_for_hit(self):
        i = 0
        hit = False
        for t in self.targets:
            if (((self.middle_point[0] + (self.offset * self.x_offset)) - t.get_position()[0])**2 + ((self.middle_point[1] + (self.y_offset * self.y_offset_set))- t.get_position()[1])**2) < 60**2:
                self.targets.pop(i)
                hit = True
                self.game_points += 1
                i -= 1
            i += 1
        if hit:
            self.add_target()

    def draw_game_points(self):
        label = self.font_points.render(str(self.game_points), 1, (255,255,255))
        self.screen.blit(label, (self.screen_width / 2, 30))

    def set_y_offset(self, up: bool):
        if up and self.y_offset_multi == 1:
            self.y_offset_multi = -1.5
        elif up and self.y_offset_multi == 1.5:
            self.y_offset_multi = 1
        elif not up and self.y_offset_multi == -1.5:
            self.y_offset_multi = 1
        elif not up and self.y_offset_multi == 1:
            self.y_offset_multi = 1.5

        match self.y_offset_multi:
            case 1:
                self.y_rect_colors[0] = self.BLACK
                self.y_rect_colors[1] = self.BLACK
            case 1.5:
                self.y_rect_colors[0] = self.BLACK
                self.y_rect_colors[1] = self.WHITE
            case -1.5:
                self.y_rect_colors[0] = self.WHITE
                self.y_rect_colors[1] = self.BLACK

Main()