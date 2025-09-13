from abc import ABC, abstractmethod
from point import Point
import pygame
import res

class ObstacleEntry:
    """ Offers globally accesible info for each type of obstacle """
    def __init__(self, damage, name, constructor, image):
        self.damage = damage
        self.name = name
        self.constructor = constructor
        self.image = image

obstacle_registry: dict[int, ObstacleEntry] = {}

class Obstacle(pygame.sprite.Sprite):
    """ Base class for an obstacle """
    type = -1

    def __init_subclass__(cls, **kwargs):
        """
        Runs automatically whenever a subclass of Obstacle is defined
        Registers each subclass's global info
        """
        super().__init_subclass__()
        cls.type = len(obstacle_registry)
        obstacle_registry[cls.type] = ObstacleEntry(damage=kwargs["damage"], name=__name__, constructor=cls, image=cls().load_image())
    
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
    
    def as_point(self):
        """
        Wraps the object as a point for tree-lookup.
        Lookup has to be easy, but comparison operators can't be overloaded without making this unhashable
        """
        return Point(self.rect.x, self.rect.y, self)

class Hole(Obstacle, damage=20):
    """ A hole in the road """
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
    
    def load_image(self):
        return res.Image.HOLE.value

class Cone(Obstacle, damage=10):
    """ An orange cone """
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.hitbox_padding = (2, 2, 8, -4)
    
    def load_image(self):
        return res.Image.CONE.value

def obstacle_damage_from_index(i):
    """ Returns the damage of an obstacle given it's type """
    tex = obstacle_registry[i]
    if (tex):
        return tex.damage
    return 0

def obstacle_texture_from_index(i):
    """ Returns the texture of an obstacle given it's type """
    tex = obstacle_registry[i]
    if (tex):
        return tex.image
    return res.Image.HOLE.value

def obstacle_from_index(i: int, x: int = 0, y: int = 0):
    """ Returns an instance of an obstacle given it's type """
    tex = obstacle_registry[i]
    if (tex):
        return tex.constructor(x, y)
    return Hole(x, y)

def get_obstacle_types_count():
    """ Get the obstacle variants count """
    return len(obstacle_registry)