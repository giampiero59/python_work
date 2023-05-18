""" Impostazioni proiettile """

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Classe creata per la gestione del proiettile sparato """

    def __init__(self, ai_game):
        """ Creazione dell'oggetto proiettile alla posizione corrente della navicella """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Crea il rect del proiettile a (0,0) e poi imposta la posizione corretta
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Memorizza la posizione del proiettile come float
        self.y = float(self.rect.y)

    def update(self):
        """ Sposta il proiettile verso l'alto """

        # Aggiorna la posizione esatta
        self.y -= self.settings.bullet_speed

        # Aggiorna la posizione del rect
        self.rect.y = self.y

    def draw_bullet(self):
        """ Disegna il proiettile """
        pygame.draw.rect(self.screen, self.color, self.rect)
