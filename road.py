import pygame

class Road(pygame.sprite.Sprite):
    def __init__(self, screen_width = 0, length = 5):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load("img/calle.png").convert_alpha()
       self.goal_image = pygame.image.load("img/goal.png").convert_alpha()
       self.rect = self.image.get_rect()
       self.length = length
       self.offset = 0
       self.screen_width = screen_width
       self.completeness = 0
    
    def update(self, *args, **kwargs):
        self.completeness = round(min(1, max(0, self.offset / self.length / self.rect.w)) * 100)
        return super().update(*args, **kwargs)
    
    def get_size(self):
        return self.length * self.rect.w
    
    def draw(self, screen):
        """
        Draws the road to a pygame screen
        """
        start = -1
        stop = self.screen_width // self.rect.w + 1
        # draw just the sufficient chunks
        for i in range(start, stop):
            # wrap the x to the screen domain and
            # maintain any movement smooth
            x = int(-self.offset) % int(self.rect.w) + i * int(self.rect.w)
            screen.blit(self.image, (x, self.rect.y))
        screen.blit(self.goal_image, (-self.offset + self.length * self.rect.w, self.rect.y))
        screen.blit(self.goal_image, (-self.offset, self.rect.y))