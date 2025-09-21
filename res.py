import pygame
from enum import Enum

class Font(Enum):
    """ Preloaded fonts """
    NJ = pygame.font.Font("font/credits-small.ttf", 12)

class Image(Enum):
    """ Preloaded textures """
    HOLE = pygame.image.load("img/hueco.png").convert_alpha()
    CONE = pygame.image.load("img/cono.png").convert_alpha()
    BG = pygame.image.load("img/bg.png")
    WIN = pygame.image.load("img/msg-win.png")
    LOSE = pygame.image.load("img/msg-lose.png")
    PETRO = pygame.image.load("img/petro.png")
    EVIL_TAXI = pygame.transform.flip(pygame.image.load("img/taxi.png").convert_alpha(), True, False) 
    EVIL_BUS = pygame.transform.flip(pygame.image.load("img/luna-bus.png").convert_alpha(), True, False) 