import pygame
import tkinter
import math

from queue import Queue
from tree import Tree

import config

# ------------------------------------------------
# Pygame init
# ------------------------------------------------

SCREEN_WIDTH = 138
SCREEN_HEIGHT = 224

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()
running = True

nj_font = pygame.font.Font("font/credits-small.ttf", 10) # Load 'myfont.ttf' with size 36
bg_image = pygame.image.load("img/bg.png")

# ------------------------------------------------
# Logic initialization
# ------------------------------------------------

from road import Road
from player import Player

from cone import Cone

road = Road(SCREEN_WIDTH, 5)
player = Player(road)

road.rect.y = (SCREEN_HEIGHT - road.rect.h) / 2

# Grupo de sprites (útil para manejar varios)
# obstacles = pygame.sprite.Group()

# -------------------

player_velocity = 4

tree = Tree()

rendering_queue = []

rendering_queue.append(Cone(150, 10))
rendering_queue.append(Cone(250, 20))
rendering_queue.append(Cone(350, 30))
rendering_queue.append(Cone(450, 40))
rendering_queue.append(Cone(555, 50))
rendering_queue.append(Cone(666, 60))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check for specific key presses
            if event.key == pygame.K_UP:
                player.up()
            if event.key == pygame.K_DOWN:
                player.down()
            if event.key == pygame.K_SPACE or event.key == pygame.K_c or event.key == pygame.K_x:
                player.jump()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((56, 0, 15))

    # RENDER YOUR GAME HERE

    if len(rendering_queue) > 0 and rendering_queue[0].rect.right - road.offset < 0:
        print(f"Removed left: { rendering_queue.pop(0).as_point() }")

    road.update()
    player.update()

    screen.blit(bg_image, (0,24))

    road.draw(screen)

    for object in rendering_queue:
        screen.blit(object.image, (object.rect.x - road.offset, object.rect.y))

    player.draw(screen)

    road_below_y = 0

    screen.blit(nj_font.render(f"HP {player.HP} <{road.completeness}x>", False, (143, 98, 51)), (2, road_below_y))

    print(pygame.mouse.get_pos())

    # flip() the display to put your work on screen
    pygame.display.flip()

    road.offset += player_velocity

    clock.tick(config.framerate)  # limits FPS to 60

pygame.quit()