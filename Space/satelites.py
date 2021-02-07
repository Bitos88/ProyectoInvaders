import pygame
import random
from pygame.locals import *
from pygame.sprite import Sprite
from Space import DIMENSIONS

class Satelite(Sprite):
    sateliteList = ["Satelite1.png", "Satelite2.png", "Satelite3.png"]
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rand = random.randint(0, 2)
        self.image = pygame.image.load(f"images/{self.sateliteList[self.rand]}")
        self.rect = self.image.get_rect(x=x, y=y)

        self.speed = random.randint(3, 7)

        self.x = float(self.rect.x)

    def update(self):
        self.rect.x -= self.speed