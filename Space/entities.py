import pygame as pg
import pygame.locals
import random
import sys, os
from Space import basededatos
from Space import DIMENSIONS, FPS
from Space import ship
from Space import meteors
from Space import planet
from Space import menu
from Space import text
from pygame.sprite import Sprite
import time
import enum





pg.init()

class Estado(enum.Enum):
    inicio = "inicio"
    partida = "partida"
    fin = "fin"

class Game(Sprite):
    listaLetras = [letra for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    listaAlias = ""
    listaNumeros = [numero for numero in range(1,27)]
    DictAlias = dict(zip(listaNumeros, listaLetras))

    def __init__(self):
        self.screen = pg.display.set_mode(DIMENSIONS)
        pg.display.set_caption("Space Invaders")
        self.screenRect = self.screen.get_rect()

        self.LetraElegida = 1
        self.recordIntroducido = False

        self.vidas = 3
        self.vidasimg = pg.image.load("images/vidas.png")
        self.vidasRect = self.vidasimg.get_rect()

        self.texto = pg.font.Font("images/FredokaOne-Regular.ttf", 30)
        self.textoTitulo = pg.font.Font("images/spaceage.ttf", 50)
        self.pointText = pg.font.Font("images/BungeeRegular.ttf", 45)


        self.background_x = 0
        self.puntuacion = 0
        self.meteorsDodge = 0

        #Instancias de los objetos
        self.meteor1 = meteors.Meteor(DIMENSIONS[0] + 32, random.randint(0, DIMENSIONS[1] - 32))
        self.meteoritos = pg.sprite.Group()
        self.naves = pg.sprite.Group(ship.Ship(1,500,5))
        self.navesPosX = 1
        self.navesPosY = 500
        self.planeta1 = planet.Planet(DIMENSIONS[0]+ 900, 400, 4)
        self.menu = menu.Menu(0, -100, 0.5, self.puntuacion)


        self.maxMeteo = 2
        #control de tiempo y reloj
        self.ct = 0
        self.clock = pg.time.Clock()
        

        self.exp = False


        self.partida = True
        self.partida2 = True
        self.inicio = False
        self.instructions = True
        self.gameover = True
        self.end = True

        self.SPuntuacion = self.pointText.render(f":{self.meteorsDodge}", True, (255,255,255))
        self.RPuntuacion = self.SPuntuacion.get_rect(topleft=(130, -50))


        self.Spunt = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))
        self.Rpunt = self.Spunt.get_rect(topleft = (950, -50))

        

        #fondo0
        self.bg1 = pg.image.load("images/fondo1_2.png")
        self.dimensionsBg1 = self.bg1.get_rect()
        self.bgx1 = 0.5

        #fondo1
        self.bg2 = pg.image.load("images/fondo2_2.png")
        self.dimensionsBg2 = self.bg2.get_rect()
        self.bgx2 = 2
        #fondo2

    def resetTotal(self):
        self.background_x = 0
        self.puntuacion = 0
        self.meteorsDodge = 0
        self.vidas = 3
        self.partida = True
        self.partida2 = True
        self.inicio = False
        self.instructions = True
        self.gameover = True
        self.end = True
        
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
                        self.meteorsDodge += 1
                        self.puntuacion += 50
                        self.SPuntuacion = self.pointText.render(f":{self.meteorsDodge}", True, (255,255,255))
                        self.Spunt = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))
                        #self.RPuntuacion = self.SPuntuacion.get_rect(topleft=(130, 10))
                #calcula la colisión de 2 grupos de sprites, nave y meteo, y si detecta colisión elimina el meteorito
                if self.puntuacion < 500:
                    if pg.sprite.groupcollide(self.naves, self.meteoritos, False, True):
                        for nave in self.naves:
                            nave.status = ship.Status.explotando
                            self.vidas -= 1
                        self.puntuacion -= 25
                        self.reset()
                self.Spunt = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))
                self.SPuntuacion = self.pointText.render(f":{self.meteorsDodge}", True, (255,255,255))

    
                #mira si la puntuación a llegado al limite y saca el planeta por la parte derecha y elimina los meteoritos    
                if self.puntuacion >= 500:
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
                self.screen.blit(self.Spunt, (self.Rpunt.x, self.Rpunt.y))


                if self.RPuntuacion.y < 50 and self.Rpunt.y < 50:
                    self.RPuntuacion.y += 1
                    self.Rpunt.y += 1
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
                        nave.reset()
                        self.planeta1.reset()
                        nave.status = ship.Status.viva
                
                if self.vidas == 0:
                    self.partida = True
                    self.gameover = False
                    
                    
                
                tecla = pg.key.get_pressed()
                '''
                if tecla[pg.K_SPACE]:
                    self.inicio = True
                    self.partida = True
                    self.partida2 = False
                    nave.reset()
                    self.planeta1.reset()
                    nave.status = ship.Status.viva
                '''        



                pg.display.flip()

            while not self.partida2:
                dt = self.clock.tick(FPS)
                self.ct += dt
                events = pg.event.get()
                for event in events:
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if ship.Status.aterrizada: 
                            if event.key == pg.K_UP and self.LetraElegida > 1:
                                self.LetraElegida -= 1
                            if event.key == pg.K_DOWN and self.LetraElegida < 26:
                                self.LetraElegida += 1
                            if event.key == pg.K_SPACE and len(self.listaAlias) < 3:
                                self.listaAlias += (self.DictAlias[self.LetraElegida])
                                self.LetraElegida = 1
                            if event.key == pg.K_SPACE and self.recordIntroducido == False and len(self.listaAlias) == 3:
                                basededatos.datosDB(self.puntuacion, (self.listaAlias))
                                self.recordIntroducido = True
                            if event.key == pg.K_r:
                                self.end = False
                            
                        
                #movimiento original fondo pantalla
                self.bgMove1()  
            
                self.maxMeteo = 2
                #mete en el grupo de sprites de Meteoritos la cantidad de meteoritos max expecificada.
                if self.ct >= 2000 and self.puntuacion <= 800:

                    for x in range(self.maxMeteo):
                        self.meteoritos.add(meteors.Meteor(DIMENSIONS[0] - 32, random.randint(150, DIMENSIONS[1] - 32)))
                    self.ct = 0    

                #va mostrando en pantalla los meteoritos y los elimina si pasan de cierta posición en pantalla
                for meteor in self.meteoritos:
                    self.screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

                    if meteor.rect.x < -meteor.rect.w:
                        self.meteoritos.remove(meteor)
                        self.meteorsDodge += 1
                        self.puntuacion += 50
                        self.SPuntuacion = self.pointText.render(f":{self.meteorsDodge}", True, (255,255,255))
                        #self.RPuntuacion = self.SPuntuacion.get_rect(topleft=(130, 10))
                #calcula la colisión de 2 grupos de sprites, nave y meteo, y si detecta colisión elimina el meteorito
                if self.puntuacion < 800:
                    if pg.sprite.groupcollide(self.naves, self.meteoritos, False, True):
                        for nave in self.naves:
                            nave.status = ship.Status.explotando
                            self.vidas -= 1
                        self.puntuacion -= 25
                        self.reset()
                self.Spunt = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))
   
                #mira si la puntuación a llegado al limite y saca el planeta por la parte derecha y elimina los meteoritos    
                if self.puntuacion >= 800:
                    self.maxMeteo = 0
                    self.puntuacion += 0 #<------ a prueba
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
                self.screen.blit(self.Spunt, (self.Rpunt.x, self.Rpunt.y))


                if self.RPuntuacion.y < 50 and self.Rpunt.y < 50:
                    self.RPuntuacion.y += 1
                    self.Rpunt.y += 1
                else:
                    pass

                for nave in self.naves:
                    if nave.status == ship.Status.aterrizando:
                        self.screen.blit(nave.naveRotadaS, (nave.naveRotadaRect.x, nave.naveRotadaRect.y))

                    else:
                        self.screen.blit(nave.image, (nave.rect.x, nave.rect.y))

                if self.vidas == 0:
                    self.partida2 = True
                    self.gameover = False

                if nave.status == ship.Status.aterrizada:

                    

                    
                
                    self.screen.fill((0,0,0))

                    textofin = self.textoTitulo.render("GAME COMPLETE", True, (255,255,255))
                    textofinRect = textofin.get_rect(center=(self.dimensionsBg1.centerx //4, 200))
                    textoScore = self.textoTitulo.render(f"TU PUNTUACIÓN ES DE: {self.puntuacion}", True, (255,255,255))
                    textoScoreRect = textoScore.get_rect(center=(self.dimensionsBg1.centerx //4, 300))
                    textoAlias = self.textoTitulo.render("INTRODUCE TU ALIAS", True, (255,255,255))
                    textoAliasRect = textoAlias.get_rect(center=(self.dimensionsBg1.centerx//4, 400))
                    self.screen.blit(textofin, (textofinRect.x, textofinRect.y))
                    self.screen.blit(textoScore, (textoScoreRect.x, textoScoreRect.y))
                    self.screen.blit(textoAlias,(textoAliasRect.x, textoAliasRect.y))
                    if not self.listaAlias:
                        textoLetras = self.textoTitulo.render(self.DictAlias[self.LetraElegida], True, (255,255,255))
                        textoLetrasRect = textoLetras.get_rect(center=((self.dimensionsBg1.centerx//4)-50, 500))
                        self.screen.blit(textoLetras, (textoLetrasRect.x, textoLetrasRect.y))
                    else:
                        x = 0
                        for letra in self.listaAlias:
                            textoLetras = self.textoTitulo.render(letra, True, (255,255,255))
                            textoLetrasRect = textoLetras.get_rect(center=((self.dimensionsBg1.centerx//4) -50, 500))
                            self.screen.blit(textoLetras, ((textoLetrasRect.x)+x, textoLetrasRect.y))
                            x += 50
                        if len(self.listaAlias) < 3:
                            textoLetras = self.textoTitulo.render(self.DictAlias[self.LetraElegida], True, (255,255,255))
                            textoLetrasRect = textoLetras.get_rect(center=((self.dimensionsBg1.centerx//4)-50, 500))
                            self.screen.blit(textoLetras, ((textoLetrasRect.x) + x, textoLetrasRect.y))
                        else:
                            textograbado = self.textoTitulo.render("PUNTUACIÓN GUARDADA", True, (255,0,0))
                            textograbadoRect = textograbado.get_rect(center=(self.dimensionsBg1.centerx//4, 600))
                            self.screen.blit(textograbado, (textograbadoRect.x, textograbadoRect.y))  

                    

                if self.end == False:
                    self.screen.fill((0,0,0))

                    textoRecords = self.textoTitulo.render("RECORDS", True, (0,0,255))
                    textoRecordsRect = textoRecords.get_rect(center=(self.screenRect.centerx, 150))
                    self.screen.blit(textoRecords, (textoRecordsRect.x, textoRecordsRect.y))
                    tituloPuntuacion = self.texto.render("PUNTUACIÓN", True, (255,255,255))
                    tituloPuntuacionRect = tituloPuntuacion.get_rect(center= (450,300))
                    self.screen.blit(tituloPuntuacion, (tituloPuntuacionRect.x, tituloPuntuacionRect.y))
                    nombrePuntuacion = self.texto.render("NOMBRE", True, (255,255,255))
                    nombrePuntuacionRect = nombrePuntuacion.get_rect(center= (650,300))
                    self.screen.blit(nombrePuntuacion, (nombrePuntuacionRect.x, nombrePuntuacionRect.y))                




                    records = basededatos.elegirDatos()  #contiene una lista de tuplas con los 3 records más altos
                    
                    y = 0
                    y2 = 0
                    for record in records:
                        recordsPlayer = self.texto.render(f"{record[0]}", True, (255,255,255))
                        recordsPlayerRect = recordsPlayer.get_rect(center= (450,400 + y))
                        self.screen.blit(recordsPlayer, (recordsPlayerRect.x , recordsPlayerRect.y))
                        y += 50
                        
                    for nombre in records:
                        puntuacionPlayer = self.texto.render(f"{nombre[1]}", True, (255,255,255))
                        puntuacionPlayerRect = puntuacionPlayer.get_rect(center= (650,400 + y2))
                        self.screen.blit(puntuacionPlayer, (puntuacionPlayerRect.x , puntuacionPlayerRect.y))
                        y2 += 50


                pg.display.flip()
                                
                    
            while not self.gameover:
                dt = self.clock.tick(FPS)
                self.ct += dt
                events = pg.event.get()
                for event in events:
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:
                            self.resetTotal()
                        if event.key == pg.K_e:
                            pg.quit()
                            sys.exit()
                self.screen.fill((0,0,0))

                textogameover = text.Text(self.screen, "titulo", 80,"GAME OVER", self.screenRect.centerx, self.screenRect.centery).imprimir(self.screen)
                textoagain = text.Text(self.screen, "titulo", 20, "Pulsa R para volver a Inicio", 250, 700).imprimir(self.screen)
                textosalir = text.Text(self.screen, "titulo", 20, "Pulsa E para cerrar", 950, 700).imprimir(self.screen)

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

                textoprueba = text.Text(self.screen, "subtitulo", 30,"lo lograste", self.screenRect.centerx, self.screenRect.centery).imprimir(self.screen)

                textoInstrucciones = text.Text(self.screen, "titulo", 25, "INSTRUCCIONES DEL JUEGO",self.screenRect.centerx, 200).imprimir(self.screen)
                textoVolverInicio = text.Text(self.screen, "subtitulo", 25, "PULSA R PARA VOLVER", self.screenRect.centerx, 650).imprimir(self.screen)
                
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
