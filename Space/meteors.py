import pygame
import random
from pygame.locals import *
from pygame.sprite import Sprite
from Space import DIMENSIONS

class Meteor(Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/meteorito.png")
        self.rect = self.image.get_rect(x=x, y=y)

        self.speed = random.randint(3, 5)

        self.x = float(self.rect.x)

    def update(self):
        self.rect.x -= self.speed

