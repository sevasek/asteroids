import random
import math
import pygame
from constants import HYPERDRIVE_DURATION, HYPERDRIVE_STAR_COUNT, HYPERDRIVE_FOV, HYPERDRIVE_SHIP_FLY_IN_TIME, HYPERDRIVE_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT


class HyperdriveStar:
    def __init__(self):
        self.reset()

    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, 50)
        self.x = math.cos(angle) * radius
        self.y = math.sin(angle) * radius
        self.z = random.uniform(100, 500)
        self.speed = random.uniform(200, 400)

    def update(self, dt):
        self.z -= self.speed * dt
        if self.z <= 10:
            self.reset()

    def get_screen_position(self):
        if self.z <= 0:
            return None, None, 0
        scale = HYPERDRIVE_FOV / self.z
        screen_x = self.x * scale + SCREEN_WIDTH // 2
        screen_y = self.y * scale + SCREEN_HEIGHT // 2
        size = max(1, int(3 * scale / 20))
        return screen_x, screen_y, size


class Hyperdrive:
    def __init__(self):
        self.stars = [HyperdriveStar() for _ in range(HYPERDRIVE_STAR_COUNT)]
        self.elapsed = 0
        self.ship_scale = 0
        self.ship_fly_in_start = HYPERDRIVE_DURATION - HYPERDRIVE_SHIP_FLY_IN_TIME
        self.ship_fly_in_end = HYPERDRIVE_DURATION
        self._star_surface = None

    def _get_surface(self):
        if self._star_surface is None:
            self._star_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        return self._star_surface

    def update(self, dt):
        self.elapsed += dt
        for star in self.stars:
            star.update(dt)

        if self.elapsed >= self.ship_fly_in_start:
            fly_in_progress = (self.elapsed - self.ship_fly_in_start) / HYPERDRIVE_SHIP_FLY_IN_TIME
            self.ship_scale = min(1.0, fly_in_progress)
        else:
            self.ship_scale = 0

    def is_complete(self):
        return self.elapsed >= HYPERDRIVE_DURATION

    def draw(self, screen):
        screen.fill("black")

        for star in self.stars:
            screen_x, screen_y, size = star.get_screen_position()
            if screen_x is not None:
                pygame.draw.circle(screen, HYPERDRIVE_COLOR, (int(screen_x), int(screen_y)), size)

    def _draw_ship(self, screen):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        base_size = 20
        scaled_size = int(base_size * self.ship_scale)

        if scaled_size < 1:
            return

        forward = pygame.Vector2(0, 1)
        right = pygame.Vector2(0, 1).rotate(90) * scaled_size / 1.5

        a = pygame.Vector2(center_x, center_y) + forward * scaled_size
        b = pygame.Vector2(center_x, center_y) - forward * scaled_size - right
        c = pygame.Vector2(center_x, center_y) - forward * scaled_size + right

        triangle = [(int(a.x), int(a.y)), (int(b.x), int(b.y)), (int(c.x), int(c.y))]
        pygame.draw.polygon(screen, "white", triangle, 2)