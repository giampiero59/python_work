from typing import Any
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Rappresenta l'alieno """

    def __init__(self, ai_game):
        """ Inizializza alieno e imposta la posizione iniziale"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carica l'immagine ed imposta gli attributi
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        # Angolo in alto a sinistra dello schermo
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Memorizza la esatta posizione orizzontale
        self.x = float(self.rect.x)

    def check_edge(self):
        """ True se l'alieno ha raggiunto il bordo dello schermo """
        screen_rect = self.screen.get_rect()

        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """ Muove l'alieno a destra o sinistra"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
