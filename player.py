""" Module for defining the player in the game """

import pygame
import math
import time
from road import Road

MAX_LANES = 3

class Player(pygame.sprite.Sprite):
    """ Player class, handles the player drawing and logic """
    def __init__(self, road: Road):
        """ 
        Initialize the player
        Args:
            road (Road): The road the player is on
        """
        pygame.sprite.Sprite.__init__(self)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load("img/player.png").convert_alpha()
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.road = road
        self.lane = 0
        self.y = 0
        self.jump_timer = 0
        self.jump_distance = 32
        self.jumping = False
        self.HP = 100
        self.max_HP = 100
        self.damaged_timer = 0
    
    def update(self, *args, **kwargs):
        """ Update the player state """
        if self.damaged_timer > 0:
            self.damaged_timer -= 1
        if self.jumping:
            self.jump_timer += 1
            if self.jump_timer > self.jump_distance:
                self.jumping = False
                self.jump_timer = 0
        self.lane = min(MAX_LANES - 1, max(0, self.lane))
        self.rect.x = 10
        self.y = (self.lane * self.rect.h) 
        self.y += self.road.rect.y 
        self.y -= self.rect.h // 2 - 4
        self.rect.y = (self.rect.y + self.y) // 2
        return super().update(*args, **kwargs)

    def lane_up(self):
        """ Trigger move up """
        self.lane -= 1
    
    def lane_down(self):
        """ Trigger move down """
        self.lane += 1
    
    def jump(self):
        """ Trigger jump """
        self.jumping = True
    
    def damage(self, damage: int = 0):
        """ 
        Inflict damage to the player
        Args:
            damage (int): The amount of damage to inflict
        """
        if self.damaged_timer == 0:
            self.HP = max(self.HP - damage, 0)
            self.damaged_timer = 30
    
    def draw(self, screen: pygame.Surface):
        """ 
        Draw the player to a surface
        Args:
            screen (pygame.Surface): The surface to draw the player on
        """
        swing_y = 2 * math.sin(time.time() * 3)
        # Calcula la altura del salto basandose en el seno de jump_timer restringido en [ 0, pi ]
        jump_y = self.rect.h * math.sin( math.pi * float(self.jump_timer) / self.jump_distance )
        # Calcula el angulo del jugador basandose en el seno de jump_timer restringido en [ 0, 2 * pi ] subida y bajada
        jump_angle = round(math.sin( math.pi * 2 * float(self.jump_timer) / self.jump_distance ) * 15)
        rot_image = None
        rot_rect = self.rect
        if jump_y > 0:
            rot_image = self.image.copy()
            rot_image = pygame.transform.rotate(self.image, jump_angle)
            rot_rect = rot_image.get_rect(center=self.rect.center)
        else:
            rot_rect = self.image.get_rect(center=self.rect.center)
            rot_image = self.image
        pygame.draw.ellipse(screen, (92, 19, 19), (self.rect.x + 2, self.y + self.rect.h - 3 + swing_y, self.rect.w-4, 4))
        if self.damaged_timer % 2 == 0:
            screen.blit(rot_image, (rot_rect.x, round(rot_rect.y - jump_y + swing_y), rot_rect.w, rot_rect.h))