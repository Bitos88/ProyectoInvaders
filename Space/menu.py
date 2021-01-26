import pygame as pg
import random
from pygame.locals import *
from pygame.sprite import Sprite
from Space import DIMENSIONS


class Menu(Sprite):
    def __init__(self, x, y, vy, puntuacion):

        pg.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.vy = vy
        self.puntuacion = puntuacion

        self.image = pg.image.load("images/UI.png")
        self.rect = self.image.get_rect(x= x, y= y)


        self.topText = pg.font.Font("images/BungeeRegular.ttf", 45)

        self.SPuntuacion = self.topText.render(f":{self.puntuacion}", True, (255,255,255))
        self.RPuntuacion = self.SPuntuacion.get_rect(topleft=(130, -50))


    def update(self):

        self.rect.y += self.vy

        self.RPuntuacion.y += self.vy

        if self.rect.y == 50:
            self.vy = 0

        elif self.RPuntuacion.y == 130:
            self.vy = 0

