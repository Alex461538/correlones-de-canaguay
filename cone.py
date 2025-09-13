import pygame
from obstacle import Obstacle

class Cone(Obstacle):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
    
    def load_image(self):
        return pygame.image.load("img/cono.png").convert_alpha()

    def set_damage(self, damage = None):
        return 5