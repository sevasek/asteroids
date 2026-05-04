import random
import math
import pygame
from constants import (
    HYPERDRIVE_DURATION,
    HYPERDRIVE_STAR_COUNT,
    HYPERDRIVE_FOV,
    HYPERDRIVE_SHIP_FLY_IN_TIME,
    HYPERDRIVE_COLOR,
    HYPERDRIVE_TRANSITION_TIME,
    HYPERDRIVE_WARP_START_TIME,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


class HyperdriveStar:
    def __init__(self):
        self.reset()

    def reset(self):
        self.angle = random.uniform(0, 2 * math.pi)
        self.initial_radius = 1
        self.z = random.uniform(80, 200)
        self.speed = random.uniform(400, 800)

    def update(self, dt):
        self.z -= self.speed * dt

        if self.z <= 10:
            self.reset()

    def get_screen_position(self):
        if self.z <= 0:
            return None, None, 0

        radius = self.initial_radius * (200 / max(self.z, 1))
        x = math.cos(self.angle) * radius
        y = math.sin(self.angle) * radius

        scale = HYPERDRIVE_FOV / self.z
        screen_x = x * scale + SCREEN_WIDTH // 2
        screen_y = y * scale + SCREEN_HEIGHT // 2
        size = max(1, int(3 * scale / 20))
        return screen_x, screen_y, size


class Hyperdrive:
    def __init__(self, starfield=None):
        self.stars = [HyperdriveStar() for _ in range(HYPERDRIVE_STAR_COUNT)]
        self.elapsed = 0
        self.ship_scale = 0
        self.ship_fly_in_start = HYPERDRIVE_DURATION - HYPERDRIVE_SHIP_FLY_IN_TIME
        self.ship_fly_in_end = HYPERDRIVE_DURATION
        self.transition_time = HYPERDRIVE_TRANSITION_TIME
        self._star_surface = None

        self.transition_stars = []
        if starfield:
            self._init_transition_stars(starfield)

    def _init_transition_stars(self, starfield):
        for star in starfield.stars:
            x = star.position.x - SCREEN_WIDTH / 2
            y = star.position.y - SCREEN_HEIGHT / 2
            z = HYPERDRIVE_FOV
            self.transition_stars.append({
                "x": x,
                "y": y,
                "z": z,
                "base_size": star.size,
                "original_x": star.position.x,
                "original_y": star.position.y,
            })

    def _get_surface(self):
        if self._star_surface is None:
            self._star_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        return self._star_surface

    def update(self, dt):
        self.elapsed += dt

        if self.elapsed < self.transition_time:
            progress = self.elapsed / self.transition_time
            acceleration = progress ** 2
            min_speed = 50
            max_speed = 450

            for star in self.transition_stars:
                speed = min_speed + acceleration * max_speed
                star["z"] -= speed * dt

                if star["z"] <= 10:
                    star["z"] = random.uniform(300, 500)
        else:
            for star in self.transition_stars:
                speed = 500
                star["z"] -= speed * dt

                if star["z"] <= 10:
                    star["z"] = random.uniform(300, 500)

        if self.elapsed >= HYPERDRIVE_WARP_START_TIME:
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

        if self.elapsed < self.transition_time or self.elapsed < self.transition_time + 1.0:
            for star in self.transition_stars:
                if star["z"] > 0:
                    scale = HYPERDRIVE_FOV / star["z"]
                    screen_x = star["x"] * scale + SCREEN_WIDTH // 2
                    screen_y = star["y"] * scale + SCREEN_HEIGHT // 2
                    size = max(1, int(star["base_size"] * scale / 20))

                    pygame.draw.circle(screen, HYPERDRIVE_COLOR, (int(screen_x), int(screen_y)), size)

        if self.elapsed >= HYPERDRIVE_WARP_START_TIME:
            for star in self.stars:
                screen_x, screen_y, size = star.get_screen_position()
                if screen_x is not None:
                    pygame.draw.circle(screen, HYPERDRIVE_COLOR, (int(screen_x), int(screen_y)), size)

        self._draw_ship(screen)

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