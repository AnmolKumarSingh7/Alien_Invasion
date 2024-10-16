import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        #Create a bullet rect at (0, 0) and the set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        self.y = float(self.rect.y)   #store buuet's position as a float.
    
    def update(self):
        """move the bullet up the screen."""
        self.y -= self.settings.bullet_speed   #Update the exact position of the bullet.
        self.rect.y = self.y   #Update the rect position
        
    def draw_bullet(self):
        """draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)