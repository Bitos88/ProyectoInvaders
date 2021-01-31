from pygame.sprite import Sprite
import pygame as pg


fuentes = {
    "titulo":"BungeeRegular.ttf",
    "subtitulo":"spaceage.ttf"
}

class Text():
    def __init__(self, tipografia, tamaño, texto, x, y):

        self.x = x
        self.y = y

        self.tamaño = tamaño
        self.texto = texto

        self.texto = pg.font.Font(f"images/{fuentes[tipografia]}", self.tamaño)
        

    def imprimir(self):
        self.render = self.text.render(f"{self.texto}", True, (255,255,255))
        self.rect = self.render.get_rect(topleft= (self.x, self.y))
