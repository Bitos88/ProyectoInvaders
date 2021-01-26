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
        
        self.centerx = 841 // 2
        self.centery = 827 // 2
        
        self.rect = self.image.get_rect(center = (x, y))

        self.angle = 0

        #self.planetaRot, self.planetaRotRect = rotate(self.image, self.angle)


    '''    
    def rotate(self, surface, angle):
        rotatedSurface = pg.transform.rotozoom(surface, angle, 1)
        rotatedRect = rotatedSurface.get_rect(center = (x, y))
        return rotatedSurface, rotatedRect
    '''

    def update(self):

        self.angle += 1



        self.rect.x -= self.vx

        if self.rect.x == 700:
            self.vx = 0

