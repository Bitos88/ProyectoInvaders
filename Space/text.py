from pygame.sprite import Sprite
import pygame as pg


fuentes = {
    "titulo":"BungeeRegular.ttf",
    "subtitulo":"spaceage.ttf"
}

class Text():
    def __init__(self, pantalla, tipografia, tamaño, texto, x, y):
        self.x = x
        self.y = y
        self.pantalla = pantalla
        self.tamaño = tamaño
        self.texto2 = texto

        self.texto = pg.font.Font(f"images/{fuentes[tipografia]}", self.tamaño)
        

    def imprimir(self, pantalla):
        self.render = self.texto.render(self.texto2, True, (255,255,255))
        self.rect = self.render.get_rect(center= (self.x , self.y))
        self.pantalla.blit(self.render, (self.rect.x, self.rect.y))