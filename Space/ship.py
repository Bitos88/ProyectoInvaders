from Space import DIMENSIONS, FPS
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
import enum



class Status(enum.Enum):
    viva = "viva"
    explotando = "explotando"
    muerta = "muerta"

class Ship(Sprite):

    shipsList = ["navep1.png", "navep2.png", "navep3.png", "navep4.png", "navep5.png"]
    explosionList = ["explosion00.png", "explosion01.png", "explosion02.png", "explosion03.png", "explosion04.png", "explosion05.png", "explosion06.png", "explosion07.png",]
    retardo_animaciones = 2
    retardo_animacionesE = 5
    def __init__(self, x, y, vy):

        pg.sprite.Sprite.__init__(self)

        #self.x = x
        #self.y = y
        self.vy = vy
        self.activeImage = 0
        self.activeImageE = 0
        self.imagenes = self.imageLoad()
        self.imagenesExplosion = self.explosionLoad()

        self.ciclos_tras_refresco = 0
        self.ciclos_tras_refresco_explosion = 0
        self.ticks_acumulados = 0
        self.ticks_por_frame_de_animacion = 1000//FPS * self.retardo_animaciones

        self.image = self.imagenes[self.activeImage]
        self.rect = self.image.get_rect(x=x, y=y)

        self.status = Status.viva

    def imageLoad(self):
        listaNaves = []
        for img in self.shipsList:
            listaNaves.append(pg.image.load((f"images/{img}")))

        return listaNaves

    def explosionLoad(self):
        listaExplosion = []
        for img in self.explosionList:
            listaExplosion.append(pg.image.load((f"images/{img}")))
        return listaExplosion

    def fireAnimation(self):

        self.ciclos_tras_refresco += 1

        if self.ciclos_tras_refresco % self.retardo_animaciones == 0:
            self.activeImage += 1
            if self.activeImage >= len(self.imagenes):
                self.activeImage = 0
        self.image = self.imagenes[self.activeImage]

    def explosion(self):
        self.ciclos_tras_refresco_explosion += 1

        if self.ciclos_tras_refresco_explosion % self.retardo_animacionesE == 0:
            self.activeImageE += 1
            if self.activeImageE >=len(self.imagenesExplosion):
                self.activeImageE = 0
                self.status = Status.viva
        self.image = self.imagenesExplosion[self.activeImageE]

        #CREAR TEXTO VIDAS


    '''
    @property
    def rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))
    '''

    def movement(self):
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[K_UP] and self.rect.top >= 0:
            self.rect.y -= 5
        elif teclas_pulsadas[K_DOWN] and self.rect.bottom <= 800:
            self.rect.y += 5
        
        else:
            self.vy = 0


    def update(self):
        if self.status == Status.explotando:
            self.explosion()
            print(self.status)
        if self.status == Status.viva:
            self.fireAnimation()
            self.movement()
            