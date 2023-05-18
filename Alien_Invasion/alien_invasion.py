""" ALIEN INVASION """

import sys
from time import sleep
import pygame
from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """ Gestione delle componenti del gioco e del comportamento """

    def __init__(self):
        """ Inizializza e crea le risorse per il gioco """
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Crezione istanza per memorizzare le statistiche di gioco
        # e dello scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Iniziamo con stato attivo
        self.game_active = False

        # Tasto Play
        self.play_button = Button(self, "Play")

    def _create_fleet(self):
        """ Crea la flotta di alieni """

        # Crea un alieno a ne aggiunge finchè c'è spazio
        # Lo spazio è pari all'ampiezza di un alieno sia x che y

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # finita la riga si ricomincia azzerando x e incrementando y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """ Crea un alieno e lo mette nella riga """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position

        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """ Gestisce il raggiungimento dei bordi"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Abbassa la flotta e cambai al direzioen dimovimento """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ Azione se astronave colpita """
        if self.stats.ships_left > 0:
            # Diminuisce le astronavi di 1
            self.stats.ships_left -= 1

            # Azzera proiettili e alieni
            self.bullets.empty()
            self.aliens.empty()

            # Creazione nuova flotta e astronaneve al centro
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def run_game(self):
        """ Parte il loop del gioco """
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            # Il gioco viene eseguito alla stessa velocità su qualsiasi sistema
            self.clock.tick(60)

    def _check_events(self):
        """ Aspetto un evento tastiera o mouse """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """ Inizia il gioco quando si preme il tasto Play """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.game_active = True
            # Nasconde mouse
            pygame.mouse.set_visible(False)
            # Reset delle impostazioni di gioco
            self.settings.initialize_dynamic_settings()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """ Crea unproiettile e lo aggiunge al gruppo dei proiettili """
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Aggiorna posizione ed elimina i proiettili """
        # Aggiorna posizione
        self.bullets.update()

        # Eliminazione proiettile fuori schermo
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Azione in base alla collisione con alieni"""

        # Controlla se sono stati colpiti alieni
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Distruzione proiettili rimasti e creazione di nuova flotta
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Aumenta il livello
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """ Verifica se gli alieni hanno raggiunto il fondo dello schermo """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Considera come se l'astronave fosse stata colpita
                self._ship_hit()
                break

    def _update_aliens(self):
        """ Aggiorna la posizione degli alieni nella flotta"""
        self._check_fleet_edges()
        self.aliens.update()

        # Verifica collisione con l'astronave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Verifica collisione con il fondo dello schermo
        self._check_aliens_bottom()

    def _update_screen(self):
        """ Aggiorna lo schermo """
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Scoreboard
        self.sb.show_score()

        # Disegna il tasto Play se il gioco è nello stato inattivo
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Instanzia il gioco e lo esegue
    ai = AlienInvasion()
    ai.run_game()
