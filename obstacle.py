""" Module for defining obstacles in the game """

from abc import ABC, abstractmethod
from point import Point
import pygame
import res

class ObstacleEntry:
    """ 
    Offers globally accesible info for each type of obstacle
    Attributes:
        damage (int): The damage the obstacle deals
        name (str): The name of the obstacle
        constructor (callable): The class constructor for the obstacle
        image (pygame.Surface): The image representing the obstacle
    """
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
        """ 
        Initialize an obstacle at position (x, y)
        Args:
            x (int): The x coordinate of the obstacle
            y (int): The y coordinate of the obstacle
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hitbox_padding = (0, 0, 0, 0)
    
    @abstractmethod
    def load_image(self) -> pygame.Surface:
        """
        Create an image of the obstacle, and fill it with a color.
        This could also be an image loaded from the disk.
        Returns:
            pygame.Surface: The image representing the obstacle
        """
        pass
    
    def as_point(self) -> Point:
        """
        Wraps the object as a point for tree-lookup.
        Lookup has to be easy, but comparison operators can't be overloaded without making this unhashable
        Returns:
            Point: A point representing the obstacle's position
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

class EvilTaxi(Obstacle, damage=30):
    """ An orange cone """
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
    
    def load_image(self):
        return res.Image.EVIL_TAXI.value

class SolidPetro(Obstacle, damage=30):
    """ An orange cone """
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
    
    def load_image(self):
        return res.Image.PETRO.value

def obstacle_damage_from_index(i) -> int:
    """ 
    Returns the damage of an obstacle given it's type
    Args:
        i (int): The index of the obstacle type
    Returns:
        int: The damage the obstacle deals
    """
    try:
        return obstacle_registry[i].damage
    except KeyError:
        return 0

def obstacle_texture_from_index(i) -> pygame.Surface:
    """ 
    Returns the texture of an obstacle given it's type
    Args:
        i (int): The index of the obstacle type
    Returns:
        pygame.Surface: The image representing the obstacle
    """
    try:
        return obstacle_registry[i].image
    except KeyError:
        return res.Image.HOLE.value

def obstacle_from_index(i: int, x: int = 0, y: int = 0) -> Obstacle:
    """ 
    Returns an instance of an obstacle given it's type 
    Args:
        i (int): The index of the obstacle type
        x (int): The x coordinate of the obstacle
        y (int): The y coordinate of the obstacle
    Returns:
        Obstacle: An instance of the obstacle
    """
    try:
        return obstacle_registry[i].constructor(x, y)
    except KeyError:
        return Hole(x, y)

def get_obstacle_types_count() -> int:
    """ 
    Get the obstacle variants count
    Returns:
        int: The number of obstacle types
    """
    return len(obstacle_registry)