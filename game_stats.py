class GameStats:
    """track statistics for AlienI= Invasion."""
    
    def __init__(self, ai_game):
        """initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0   #High score should never be reset.
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1