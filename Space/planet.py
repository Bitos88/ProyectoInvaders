from Space import DIMENSIONS, FPS
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
import enum


class Planet(Sprite):
    
    def __init__(self,x, y, vx):
        
        pg.sprite.Sprite.__init__(self)
        self.vx = vx
        self.image = pg.image.load("images/planeta.png")
        
        
        self.rect = self.image.get_rect(center = (x, y))

        self.angle = 0


    def rotando(self, screen):
        self.angle = (self.angle + 1) %360   
        self.centerx = 841 // 2
        self.centery = 827 // 2

        self.planetaRot = pg.transform.rotozoom(self.image, self.angle, 1)
        self.planetRect = self.planetaRot.get_rect(centerx = self.centerx, centery = self.centery)
        self.screen.blit(self.planetaRot (self.planetRect.x, self.planetRect.y))

    def reset(self):
        self.rect.x = 2100
        self.vx = 4
        

    def update(self):

        self.rect.x -= self.vx

        if self.rect.x == 700:
            self.vx = 0

