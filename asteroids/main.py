from __future__ import annotations
import sys
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from asteroids import Asteroid
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from shot import Shot

def main():

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame and create the game window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a clock to manage the frame rate and a variable to track delta time
    clock = pygame.time.Clock()
    dt = 0
    
    # Create groups for updatable and drawable sprites
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # Add the objects to the groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    
    print("Import test:")
    print(Asteroid)           # Should print something like <class 'asteroids.Asteroid'>

    # Create the player instance at the center of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Event game loop
    while True:
        
        # Log the current state of the game
        log_state()
        for event in pygame.event.get():
            
            # Monitor for a QUIT event
            if event.type == pygame.QUIT:
                return
        
        # Display a black background
        screen.fill("black")
        
        # Tick the clock
        clock.tick(60)  # Limit to 60 frames per second
        dt = clock.tick(60) / 1000  # Convert milliseconds to seconds

        # Update the player
        updatable.update(dt)

        # Check for collisions between asteroids...
        for a in asteroids:

            # ... and the player
            if a.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            # ... and shots
            for s in shots:
                if a.collides_with(s):
                    log_event("asteroid_shot")
                    print("Asteroid shot!")
                    a.split()
                    s.kill()
        
        # Draw the player
        for d in drawable:
            d.draw(screen)

        # Present the finished frame
        pygame.display.flip()

if __name__ == "__main__":
    main()
