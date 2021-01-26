import pygame
import random
from pygame.locals import *
from pygame.sprite import Sprite
from Space import DIMENSIONS

class Meteor(Sprite):
    meteorList = ["MeteorSmall.png", "MeteorSuperSmall.png", "MeteorSuperUltraSmall.png"]
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rand = random.randint(0, 2)
        self.image = pygame.image.load(f"images/{self.meteorList[self.rand]}")
        self.rect = self.image.get_rect(x=x, y=y)

        self.speed = random.randint(3, 7)

        self.x = float(self.rect.x)

    def update(self):
        self.rect.x -= self.speed

