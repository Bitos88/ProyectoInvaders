from Space import DIMENSIONS, FPS
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
import enum


class Planet():
    def __init__(self,x, y, vx):

        pg.sprite.Sprite.__init__(self)

        self.vx = vx
        self.image = pg.image.load("images/planeta.png")
        self.rect = self.image.get_rect(x=x, y=y)

    def update(self):

        self.rect.x -= self.vx

