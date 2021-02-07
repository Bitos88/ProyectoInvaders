import pygame
from pygame.locals import *

canciones = {
    "inicio" : "StarWars.mp3",
    "partida" : "ImperialSong.mp3"

}

class Musica():
    def __init__(self, cancion):
        
        self.cancion = pygame.mixer.music.load(f"images/{canciones[cancion]}")

    def playMusic(self):
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)