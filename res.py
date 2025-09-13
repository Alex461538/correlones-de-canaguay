import pygame
from enum import Enum

class Font(Enum):
    NJ = pygame.font.Font("font/credits-small.ttf", 12)

class Image(Enum):
    HOLE = pygame.image.load("img/hueco.png").convert_alpha()
    CONE = pygame.image.load("img/cono.png").convert_alpha()
    BG = pygame.image.load("img/bg.png")
    WIN = pygame.image.load("img/msg-win.png")
    LOSE = pygame.image.load("img/msg-lose.png")