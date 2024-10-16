import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage  game asset and behavior"""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((1200, 700))
        
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")
        
        self.stats = GameStats(self)   #Create an instance to store game statistics.
        self.sb = Scoreboard(self)   #Create a scoreboard.
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.bg_color = (230, 230, 230)   #Set the background color.
        
        self.game_active = True   #Start Alien Invasion in an active state.
        self.game_active = False   #Start Alien Invasion in an inactive state.
        self.play_button = Button(self, "play")   #Make the play button.
    
    def run_game(self):
        """Start thr main loop for the game"""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()
            
            #Get rid of bullets that have disappeared.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))
        
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
            #watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
   
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()            
                    
    def _check_keyup_events(self, event):
        """Respon to releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.ship.rect.x +=1
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """update position of bullets and get rid of old bullets."""
        #Check for any bullets that that have hit aliens.
        # If so, get rid of the bullet and the alien.
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        #Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)  
            self.sb.prep_score()
            self.sb.check_high_score()
    
        if not self.aliens:
            #Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1   #Increase level.
            self.sb.prep_level()
        
    def _create_fleet(self):
        """Create the fleet of aliens."""
        #make an alien and keep adding aliens until there's no room left.
        #spacing between aliens is one aline width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
                #Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""        
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        """update the position of all aliens in the fleet."""
        self.aliens.update()
        # Look for  alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            self._check_aliens_bottom()   #Look for aliens hitting the bottom of the screen.
        
    def _check_fleet_edges(self):
        """Respond appro[riately if any aliens have eached an edge.]"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop the entire fleet and chenge the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            sleep(0.5)   #Pause.
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()  #Treat this the same as if the ship got hit.
                break
            
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        #if self.play_button.rect.collidepoint(mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()   #Reset the game settings.
            self.stats.reset_stats()   #Reset the game statistics.
            self.sb.prep_score()
            self.sb.prep_level()
            self.game_active = True
            
            #Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            
            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            pygame.mouse.set_visible(False)   #Hide the mouse cursor.
    
    def _update_screen(self):
            """update images on the screen, and filp to the new screen."""
            #Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.sb.show_score()   #Draw the score information.
            
            #Draw the play button if the game is inactive.
            if not self.game_active:
                self.play_button.draw_button()
            
            pygame.display.flip()   #Make the most recently drawn screen visible.
            
if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()     