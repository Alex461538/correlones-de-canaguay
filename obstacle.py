from abc import ABC, abstractmethod
from point import Point
import pygame
import res

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    @abstractmethod
    def load_image(self):
        """
        Create an image of the obstacle, and fill it with a color.
        This could also be an image loaded from the disk.
        **Subclasses must return a pygame.Surface.**
        """
        pass

    @abstractmethod
    def set_damage(self, damage = None):
        """Subclasses must return a pygame.Surface."""
        pass
    
    def as_point(self):
        """
        Wraps the object as a point for tree-lookup.
        Lookup has to be easy, but comparison operators can't be overloaded without making this unhashable
        """
        return Point(self.rect.x, self.rect.y, self)

class Hole(Obstacle):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
    
    def load_image(self):
        return res.Image.HOLE.value

    def set_damage(self, damage = None):
        return 20

class Cone(Obstacle):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
    
    def load_image(self):
        return res.Image.CONE.value

    def set_damage(self, damage = None):
        return 5

obstacle_variants = 2

def obstacle_texture_from_index(i):
    if i == 1:
        return res.Image.CONE.value
    return res.Image.HOLE.value

def obstacle_from_index(i: int, x: int = 0, y: int = 0):
    if i == 1:
        return Cone(x, y)
    return Hole(x, y)