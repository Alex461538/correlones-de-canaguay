import pygame
import tkinter

import json

from car import Car
from cone import Cone

# pygame setup
pygame.init()
screen = pygame.display.set_mode((128, 128), pygame.SCALED)
clock = pygame.time.Clock()
running = True

loaded_data = {}
with open("data.json", "r") as f:
    loaded_data = json.load(f)

print(loaded_data)

# -------------------

car = Car()

# Grupo de sprites (útil para manejar varios)
obstacles = pygame.sprite.Group()
obstacles.add(Cone())

# -------------------

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    obstacles.draw(screen)

    screen.blit(car.image, car.rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()