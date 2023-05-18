class GameStats:
    """ Statistiche di gioco """

    def __init__(self, ai_game):
        """ Inizializza """
        self.settings = ai_game.settings
        self.reset_stat()
        # Il punteggio più alto non deve essere azzerato
        self.high_score = 0

    def reset_stat(self):
        """ inizializza statistiche cha cambiano durante il gioco """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
