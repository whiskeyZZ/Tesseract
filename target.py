import pygame
from random import randrange, choice

class Target:

    def __init__(self, first: bool):
        self.position = (960, 540)
        self.timer = self.set_timer()
        self.first = first
        self.set_position()

    def set_timer(self) -> int:
        return randrange(5, 10, 1)
    
    def start_timer(self):
        start_ticks = pygame.time.get_ticks()
        while self.timer > 0:
            self.timer = (pygame.time.get_ticks() - start_ticks)/100

    def set_position(self): 
        pos = [(960, 540), (760, 540), (1160, 540), (560, 540), (1360, 540)]
        if not self.first:
            self.position = choice(pos)

    def get_position(self):
        return self.position
        

    