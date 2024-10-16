class Settings:
    """A class to store all setting for Alien Invision."""
    def __init__(self):
        """initialize the game's static settings."""
        
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
        self.bullets_allowed = 7
        
        #Alien settings.
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        
        #Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.fleet_direction = -1
        self.speedup_scale = 1.1   #How quickly the game speeds up
        self.score_scale = 1.5   #How quickly the alien point values increase
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change through the game."""
        self.ship_speed = 5
        self.bullet_speed = 5
        self.alien_speed = 2
        self.alien_points = 5   #Scoring settings
        self.fleet_direction = 1   #fleet_direction of 1 represent right; -1 represents left.
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)