class Settings:
    """A class to store all setting for Alien Invision."""
    def __init__(self):
        """initialize the game's settings."""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #set ship speed.
        self.ship_speed = 5
        self.ship_limit = 3
        #Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 7   # Thala for a reason.
        #Alien settings.
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        #Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.fleet_direction = -1