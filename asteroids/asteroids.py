import random
from logger import log_event
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_SPLIT_VELOCITY_MULTIPLIER, LINE_WIDTH
import pygame

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        for group in self.containers:
            group.add(self)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()

    def split(self):
        self.kill()

        # If the asteroid is too small, don't split it
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # If the asteroid is big enough...
        # ... get ready to create two new asteroids
        log_event("asteroid_split")
        new_angle = random.uniform(20, 50)
        new_velocity_1 = self.velocity.rotate(new_angle)
        new_velocity_2 = self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Ensure new asteroids are at least the minimum size
        if new_radius < ASTEROID_MIN_RADIUS:
            new_radius = ASTEROID_MIN_RADIUS

        # Create the two new asteroids
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_1.velocity = new_velocity_1 * ASTEROID_SPLIT_VELOCITY_MULTIPLIER
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2.velocity = new_velocity_2 * ASTEROID_SPLIT_VELOCITY_MULTIPLIER        