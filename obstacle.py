from abc import ABC, abstractmethod
from point import Point
import pygame

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

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load("img/cono.png").convert_alpha()
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
    
    def as_point(self):
        """
        Wraps the object as a point for tree-lookup.
        Lookup has to be easy, but comparison operators can't be overloaded without making this unhashable
        """
        return Point(self.rect.x, self.rect.y, self)