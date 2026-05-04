import math
import random
import pygame
from constants import STAR_COUNT, STAR_COLOR, STAR_MIN_SIZE, STAR_MAX_SIZE, STAR_TWINKLE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


class Star:
    def __init__(self):
        self.position = pygame.Vector2(
            random.uniform(0, SCREEN_WIDTH),
            random.uniform(0, SCREEN_HEIGHT)
        )
        self.size = random.randint(STAR_MIN_SIZE, STAR_MAX_SIZE)
        self.phase_offset = random.uniform(0, 2 * math.pi)


class StarField:
    def __init__(self):
        self.stars = [Star() for _ in range(STAR_COUNT)]
        self.time_elapsed = 0

    def update(self, dt):
        self.time_elapsed += dt

    def draw(self, screen):
        star_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        for star in self.stars:
            brightness = (math.sin(self.time_elapsed * STAR_TWINKLE_SPEED + star.phase_offset) + 1) / 2
            alpha = int(80 + brightness * 175)
            color = (*STAR_COLOR, alpha)

            pygame.draw.circle(star_surface, color, (int(star.position.x), int(star.position.y)), star.size)

        screen.blit(star_surface, (0, 0))