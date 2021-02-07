import pygame

validChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font("images/spaceage.ttf", 50)
        self.image = self.font.render("Enter your name", False, [255, 255, 255])
        self.rect = self.image.get_rect()

    def add_chr(self, char):
        self.update()

    def update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, False, [0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos