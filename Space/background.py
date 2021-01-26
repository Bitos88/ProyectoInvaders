import pygame as pg
from Space import DIMENSIONS, FPS
from pygame.locals import *
from pygame.sprite import Sprite


class Background(Sprite):

    backgroundList = ["fondo1.png", "fondo2.png", "fondo3.png"]
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.background = pg.image.load("images/fondo1.png")
        self.background2 = pg.image.load("images/fondo2.png")
        self.background3 = pg.image.load("images/fondo3.png")


        self.rectBG = self.background.get_rect()
        self.rectBG2 = self.background2.get_rect()
        self.rectBG3 = self.background3.get_recto()


        self.background_x = 0


    def update(self):
        x_rel = self.background_x % self.rectBG.width
        self.screen.blit(self.background, (x_rel - self.rectBG.width ,0))
        if x_rel < DIMENSIONS[0]:
            self.screen.blit(self.background, (x_rel,0))
        self.background_x -= 0.5

    def mov1(self):
        pass