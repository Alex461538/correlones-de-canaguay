from abc import ABC, abstractmethod
from point import Point
import pygame
import res

obstacle_damage = [5, 20]
obstacle_variants = 0

def new_variant(damage = 0):
    global obstacle_variants
    obstacle_damage[obstacle_variants] = damage
    obstacle_variants += 1
    return obstacle_variants - 1

class Obstacle(pygame.sprite.Sprite):
    type = -1
    
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hitbox_padding = (0, 0, 0, 0)
    
    @abstractmethod
    def load_image(self):
        """
        Create an image of the obstacle, and fill it with a color.
        This could also be an image loaded from the disk.
        **Subclasses must return a pygame.Surface.**
        """
        pass

    @abstractmethod
    def set_damage(self, damage = 0):
        """Subclasses must return a pygame.Surface."""
        pass
    
    def as_point(self):
        """
        Wraps the object as a point for tree-lookup.
        Lookup has to be easy, but comparison operators can't be overloaded without making this unhashable
        """
        return Point(self.rect.x, self.rect.y, self)

class Hole(Obstacle):
    type = new_variant(damage=20)

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
    
    def load_image(self):
        return res.Image.HOLE.value

    def set_damage(self, damage = 20):
        obstacle_damage[self.type] = damage

class Cone(Obstacle):
    type = new_variant(damage=10)

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.hitbox_padding = (2, 2, 13, -4)
    
    def load_image(self):
        return res.Image.CONE.value

    def set_damage(self, damage = 5):
        obstacle_damage[self.type] = damage

def obstacle_texture_from_index(i):
    if i == 1:
        return res.Image.CONE.value
    return res.Image.HOLE.value

def obstacle_from_index(i: int, x: int = 0, y: int = 0):
    if i == 1:
        return Cone(x, y)
    return Hole(x, y)