import pygame as pg
import pygame.locals
import random
import sys, os
from Space import DIMENSIONS, FPS
from Space import ship
from Space import meteors
from Space import planet
from Space import menu
from pygame.sprite import Sprite
import time
import enum





pg.init()

class Estado(enum.Enum):
    inicio = "inicio"
    partida = "partida"
    fin = "fin"

class Game(Sprite):
    def __init__(self):
        self.screen = pg.display.set_mode(DIMENSIONS)
        pg.display.set_caption("Space Invaders")
        


        self.vidas = 3
        self.vidasimg = pg.image.load("images/vidas.png")
        self.vidasRect = self.vidasimg.get_rect()

        self.texto = pg.font.Font("images/FredokaOne-Regular.ttf", 30)
        self.textoTitulo = pg.font.Font("images/spaceage.ttf", 50)
        self.pointText = pg.font.Font("images/BungeeRegular.ttf", 45)


        self.background_x = 0
        self.puntuacion = 0

        #Instancias de los objetos
        self.meteor1 = meteors.Meteor(DIMENSIONS[0] + 32, random.randint(0, DIMENSIONS[1] - 32))
        self.meteoritos = pg.sprite.Group()
        self.naves = pg.sprite.Group(ship.Ship(1,500,5))
        self.planeta1 = planet.Planet(DIMENSIONS[0]+ 900, 400, 4)
        self.menu = menu.Menu(0, -100, 0.5, self.puntuacion)


        #self.music = pg.mixer.music.load("images/music.mp3")

        self.maxMeteo = 4
        #control de tiempo y reloj
        self.ct = 0
        self.clock = pg.time.Clock()
        

        self.exp = False


        self.partida = True
        self.partida2 = True
        self.inicio = False
        self.instructions = True
        self.end = True

        self.SPuntuacion = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))
        self.RPuntuacion = self.SPuntuacion.get_rect(topleft=(130, -50))

        

        #fondo0
        self.bg1 = pg.image.load("images/fondo1_2.png")
        self.dimensionsBg1 = self.bg1.get_rect()
        self.bgx1 = 0.5

        #fondo1
        self.bg2 = pg.image.load("images/fondo2_2.png")
        self.dimensionsBg2 = self.bg2.get_rect()
        self.bgx2 = 2
        #fondo2


        
    def bgMove1(self):
        self.bgx1 -= 2

        if self.bgx1 <= -self.dimensionsBg1.w //2:
            self.bgx1 = 0

        self.screen.blit(self.bg1, (self.bgx1,0))

    def bgMove2(self):
        self.bgx2 -= 2

        if self.bgx2 <= -self.dimensionsBg2.w //2:
            self.bgx2 = 0

        self.screen.blit(self.bg2, (self.bgx2,0))

    def reset(self):
        self.meteoritos.empty()

    def mainLoop(self):

        start = False

        while not start:

            #pg.mixer.music.play()
            
            while not self.partida:
                dt = self.clock.tick(FPS)
                self.ct += dt
                events = pg.event.get()
                for event in events:
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()

                
                
                #movimiento original fondo pantalla
                self.bgMove1()  
            
                
                #mete en el grupo de sprites de Meteoritos la cantidad de meteoritos max expecificada.
                if self.ct >= 2000:

                    for x in range(self.maxMeteo):
                        self.meteoritos.add(meteors.Meteor(DIMENSIONS[0] - 32, random.randint(150, DIMENSIONS[1] - 32)))
                    self.ct = 0    

                #va mostrando en pantalla los meteoritos y los elimina si pasan de cierta posición en pantalla
                for meteor in self.meteoritos:
                    self.screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

                    if meteor.rect.x < -meteor.rect.w:
                        self.meteoritos.remove(meteor)
                        self.puntuacion += 1
                        self.SPuntuacion = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))
                        #self.RPuntuacion = self.SPuntuacion.get_rect(topleft=(130, 10))
                #calcula la colisión de 2 grupos de sprites, nave y meteo, y si detecta colisión elimina el meteorito
                if pg.sprite.groupcollide(self.naves, self.meteoritos, False, True):
                    for nave in self.naves:
                        nave.status = ship.Status.explotando
                        self.vidas -= 1
                    self.reset()
                    
                #mira si la puntuación a llegado al limite y saca el planeta por la parte derecha y elimina los meteoritos    
                if self.puntuacion >= 3:
                    self.maxMeteo = 0
                    for meteor in self.meteoritos:
                        if meteor.rect.x < -80:
                            self.meteoritos.remove(meteor)
                            
                    nave.status = ship.Status.aterrizando                      
                    self.planeta1.update()

                #mostrar vidas en pantalla
                x = 500
                for vida in range(self.vidas):
                    self.screen.blit(self.vidasimg, (x, 75))
                    x += 50

                self.screen.blit(self.planeta1.image, (self.planeta1.rect.x, self.planeta1.rect.y))
                self.screen.blit(self.menu.image, (self.menu.rect.x, self.menu.rect.y))

                self.menu.update()
                self.meteoritos.update()
                self.naves.update()


                self.screen.blit(self.SPuntuacion, (self.RPuntuacion.x, self.RPuntuacion.y))


                if self.RPuntuacion.y < 50:
                    self.RPuntuacion.y += 1
                else:
                    pass
            
                

                

                for nave in self.naves:
                    if nave.status == ship.Status.aterrizando:
                        self.screen.blit(nave.naveRotadaS, (nave.naveRotadaRect.x, nave.naveRotadaRect.y))

                    else:
                        self.screen.blit(nave.image, (nave.rect.x, nave.rect.y))

                if nave.status == ship.Status.aterrizada:
                
                    self.screen.fill((0,0,0))

                    textolevel = self.textoTitulo.render("Level 1 Success", True, (255,255,255))
                    textolevelRect = textolevel.get_rect(center=(self.dimensionsBg1.centerx //4, 200))
                    textolevel2 = self.textoTitulo.render("PRESS SPACE TO CONTINUE", True, (255,255,255))
                    textolevel2Rect = textolevel2.get_rect(center=(self.dimensionsBg1.centerx //4, 400))
                    self.screen.blit(textolevel2, (textolevel2Rect.x, textolevel2Rect.y))
                    self.screen.blit(textolevel, (textolevelRect.x, textolevelRect.y))

                tecla = pg.key.get_pressed()

                if tecla[pg.K_SPACE]:
                    self.inicio = True
                    self.partida = True
                    self.partida2 = False



                pg.display.flip()

            while not self.partida2:
                dt = self.clock.tick(FPS)
                self.ct += dt
                events = pg.event.get()
                for event in events:
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()

                
                
                #movimiento original fondo pantalla
                self.bgMove1()  
            
                
                #mete en el grupo de sprites de Meteoritos la cantidad de meteoritos max expecificada.
                if self.ct >= 2000:

                    for x in range(self.maxMeteo):
                        self.meteoritos.add(meteors.Meteor(DIMENSIONS[0] - 32, random.randint(150, DIMENSIONS[1] - 32)))
                    self.ct = 0    

                #va mostrando en pantalla los meteoritos y los elimina si pasan de cierta posición en pantalla
                for meteor in self.meteoritos:
                    self.screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

                    if meteor.rect.x < -meteor.rect.w:
                        self.meteoritos.remove(meteor)
                        self.puntuacion += 1
                        self.SPuntuacion = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))
                        #self.RPuntuacion = self.SPuntuacion.get_rect(topleft=(130, 10))
                #calcula la colisión de 2 grupos de sprites, nave y meteo, y si detecta colisión elimina el meteorito
                if pg.sprite.groupcollide(self.naves, self.meteoritos, False, True):
                    for nave in self.naves:
                        nave.status = ship.Status.explotando
                        self.vidas -= 1
                    self.reset()
                    
                #mira si la puntuación a llegado al limite y saca el planeta por la parte derecha y elimina los meteoritos    
                if self.puntuacion >= 3:
                    self.maxMeteo = 0
                    for meteor in self.meteoritos:
                        if meteor.rect.x < -80:
                            self.meteoritos.remove(meteor)
                            
                    nave.status = ship.Status.aterrizando                      
                    self.planeta1.update()

                #mostrar vidas en pantalla
                x = 500
                for vida in range(self.vidas):
                    self.screen.blit(self.vidasimg, (x, 75))
                    x += 50

                self.screen.blit(self.planeta1.image, (self.planeta1.rect.x, self.planeta1.rect.y))
                self.screen.blit(self.menu.image, (self.menu.rect.x, self.menu.rect.y))

                self.menu.update()
                self.meteoritos.update()
                self.naves.update()


                self.screen.blit(self.SPuntuacion, (self.RPuntuacion.x, self.RPuntuacion.y))


                if self.RPuntuacion.y < 50:
                    self.RPuntuacion.y += 1
                else:
                    pass
            
                

                

                for nave in self.naves:
                    if nave.status == ship.Status.aterrizando:
                        self.screen.blit(nave.naveRotadaS, (nave.naveRotadaRect.x, nave.naveRotadaRect.y))

                    else:
                        self.screen.blit(nave.image, (nave.rect.x, nave.rect.y))

                if nave.status == ship.Status.aterrizada:
                
                    self.screen.fill((0,0,0))

                    textolevel = self.textoTitulo.render("Level 1 Success", True, (255,255,255))
                    textolevelRect = textolevel.get_rect(center=(self.dimensionsBg1.centerx //4, 200))
                    textolevel2 = self.textoTitulo.render("PRESS SPACE TO CONTINUE", True, (255,255,255))
                    textolevel2Rect = textolevel2.get_rect(center=(self.dimensionsBg1.centerx //4, 400))
                    self.screen.blit(textolevel2, (textolevel2Rect.x, textolevel2Rect.y))
                    self.screen.blit(textolevel, (textolevelRect.x, textolevelRect.y))

                tecla = pg.key.get_pressed()

                if tecla[pg.K_SPACE]:
                    self.inicio = True
                    self.partida = True
                    self.partida2 = False
                    print("1")
                    



                pg.display.flip()
        
            while not self.inicio:
                dt = self.clock.tick(FPS)
                self.ct += dt
                events = pg.event.get()
                for event in events:
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()

                

                tecla = pg.key.get_pressed()

                if tecla[pg.K_SPACE]:
                    self.inicio = True
                    self.partida = False
                elif tecla[pg.K_f]:
                    self.instructions = False
                    self.partida = True
                    self.partida2 = True
                    self.inicio = True


                

                self.bgMove1()

                textoTitulo = self.textoTitulo.render("SPACE INVADERS", True, (255,255,255))
                textoTituloRect = textoTitulo.get_rect(center=(self.dimensionsBg1.centerx //4, 200))

                textoInicio = self.textoTitulo.render("Press Space To Start", True, (255,255,255))
                textoInicioRect = textoInicio.get_rect(center=(self.dimensionsBg1.centerx //4, self.dimensionsBg1.centery))

                textoInstruct = self.texto.render("Press F for instructions", True, (255,255,255))
                textoInstructRect = textoInstruct.get_rect(x=100, y=700)
                
                self.screen.blit(textoTitulo, (textoTituloRect.x, textoTituloRect.y))
                self.screen.blit(textoInicio, (textoInicioRect.x, textoInicioRect.y))
                self.screen.blit(textoInstruct, (textoInstructRect.x, textoInstructRect.y))

                pg.display.flip()

            while not self.instructions:
                dt = self.clock.tick(FPS)
                self.ct += dt
                events = pg.event.get()
                for event in events:
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()


                tecla = pg.key.get_pressed()

                if tecla[pg.K_r]:
                    self.inicio = False
                    self.partida = True
                    self.instructions = True
                

                self.screen.fill((0,0,0))

                textoIns = self.texto.render("INSTRUCTIONS", True, (255,255,255))
                textoInsRect = textoIns.get_rect(center=(self.dimensionsBg1.centerx //4, 150))

                textoReturn = self.texto.render("Press R to Return Main Screen", True, (255,255,255))
                textoReturnRect = textoReturn.get_rect(center = (self.dimensionsBg1.centerx //4, 700))

                self.screen.blit(textoIns, (textoInsRect.x, textoInsRect.y))
                self.screen.blit(textoReturn, (textoReturnRect.x, textoReturnRect.y))

                pg.display.flip()

        


    '''
    def introLoop(self):

        
        
        while not self.inicio:
            dt = self.clock.tick(FPS)
            self.ct += dt
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            tecla = pg.key.get_pressed()

            if tecla[pg.K_SPACE]:
                self.inicio = True
                self.partida = False

            x_rel = self.background_x % self.rectBG.width
            self.screen.blit(self.background, (x_rel - self.rectBG.width ,0))
            if x_rel < DIMENSIONS[0]:
                self.screen.blit(self.background, (x_rel,0))
            self.background_x -= 0.5

            
            textoInicio = self.textoTitulo.render("Press Space To Start", True, (255,255,255))
            textoInicioRect = textoInicio.get_rect(center=(self.rectBG.centerx //2, self.rectBG.centery))

            self.screen.blit(textoInicio, (textoInicioRect.x, textoInicioRect.y))

            pg.display.flip()
    '''
