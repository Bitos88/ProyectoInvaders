import pygame as pg
import pygame.locals
import random
import sys, os
from Space import DIMENSIONS, FPS
from Space import ship
from Space import meteors
from Space import planet
from pygame.sprite import Sprite

pg.init()



class Game(Sprite):
    def __init__(self):
        self.screen = pg.display.set_mode(DIMENSIONS)
        self.background = pg.image.load("images/javier.jpg")
        self.rectBG = self.background.get_rect()
        pg.display.set_caption("Space Invaders")

        self.texto = pg.font.Font("images/FredokaOne-Regular.ttf", 80)


        self.background_x = 0

        self.clock = pg.time.Clock()

        self.meteor1 = meteors.Meteor(DIMENSIONS[0] + 32, random.randint(0, DIMENSIONS[1] - 32))
        self.meteoritos = pg.sprite.Group()
        self.naves = pg.sprite.Group(ship.Ship(1,500,5))
        self.planeta1 = planet.Planet(DIMENSIONS[0]+ 900, 400, 10)

        self.maxMeteo = 4

        self.ct = 0

        self.puntuacion = 0

        self.exp = False
        
        


    def mainLoop(self):
        
        gameOver = False

        while not gameOver:
            dt = self.clock.tick(FPS)
            self.ct += dt
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            x_rel = self.background_x % self.rectBG.width
            self.screen.blit(self.background, (x_rel - self.rectBG.width ,0))
            if x_rel < DIMENSIONS[0]:
                self.screen.blit(self.background, (x_rel,0))
            self.background_x -= 1

            if self.ct >= 2000:

                for x in range(1):
                    self.meteoritos.add(meteors.Meteor(DIMENSIONS[0] - 32, random.randint(0, DIMENSIONS[1] - 32)))
                self.ct = 0    


            for meteor in self.meteoritos:
                self.screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

                if meteor.rect.x < 0:
                    self.meteoritos.remove(meteor)
                    self.puntuacion += 1
            
            if pg.sprite.groupcollide(self.naves, self.meteoritos, False, True):
                for nave in self.naves:
                    nave.status = ship.Status.explotando
                
            if self.puntuacion == 3:
                self.screen.blit(self.planeta1.image, (planeta1.x, planeta1.y))
                self.planeta1.update()
            
            self.meteoritos.update()
            self.naves.update()


            
            SPuntuacion = self.texto.render(f"Points: {self.puntuacion}", True, (255,255,255))
            RPuntuacion = SPuntuacion.get_rect(bottomright=(800, 200))

            self.screen.blit(SPuntuacion, (RPuntuacion.x, RPuntuacion.y))

            for nave in self.naves:
                self.screen.blit(nave.image, (nave.rect.x, nave.rect.y))

            if self.rectBG.left < 0:
                self.rectBG.left = 800
            self.rectBG.left -= 5

            

            pg.display.flip()
