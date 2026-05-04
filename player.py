import math
import random

import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, EXHAUST_PARTICLE_LIFETIME_MIN, EXHAUST_PARTICLE_LIFETIME_MAX, EXHAUST_PARTICLE_SIZE_MIN, EXHAUST_PARTICLE_SIZE_MAX, EXHAUST_SPREAD_ANGLE, EXHAUST_EMISSION_RATE_MIN, EXHAUST_EMISSION_RATE_MAX, EXHAUST_MAX_PARTICLES, EXHAUST_PARTICLE_SPEED_MIN, EXHAUST_PARTICLE_SPEED_MAX, EXHAUST_COLORS, EXHAUST_INTENSITY_CAP
from circleshape import CircleShape
from shot import Shot


def point_in_triangle(point, tri):
    a, b, c = tri
    v0 = c - a
    v1 = b - a
    v2 = point - a

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return (u >= 0) and (v >= 0) and (u + v <= 1)


def closest_point_on_segment(p, a, b):
    ab = b - a
    ap = p - a
    if ab.length_squared() == 0:
        return a
    t = ap.dot(ab) / ab.length_squared()
    t = max(0, min(1, t))
    return a + ab * t


def triangle_circle_collision(tri, circle_center, circle_radius):
    # Check if circle center is inside triangle
    if point_in_triangle(circle_center, tri):
        return True
    # Check if any triangle vertex is inside circle
    for v in tri:
        if v.distance_to(circle_center) <= circle_radius:
            return True
    # Check if any triangle edge intersects circle
    edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
    for a, b in edges:
        closest = closest_point_on_segment(circle_center, a, b)
        if closest.distance_to(circle_center) <= circle_radius:
            return True
    return False


class ExhaustParticle:
    def __init__(self, position, velocity, lifetime, size, color):
        self.position = position  # pygame.Vector2
        self.velocity = velocity  # pygame.Vector2
        self.lifetime = lifetime  # float seconds
        self.size = size  # int pixels
        self.color = color  # tuple RGB
        self.elapsed = 0.0
        self.max_lifetime = lifetime

    def update(self, dt):
        self.position += self.velocity * dt
        self.elapsed += dt
        return self.elapsed >= self.max_lifetime  # Returns True if expired

    def draw(self, screen):
        if self.elapsed >= self.max_lifetime:
            return
        alpha = int(255 * (1 - self.elapsed / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        # Draw on a temporary SRCALPHA surface and blit to screen
        surf = pygame.Surface((int(self.size * 2 + 2), int(self.size * 2 + 2)), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (int(self.size + 1), int(self.size + 1)), self.size)
        screen.blit(surf, (int(self.position.x - self.size - 1), int(self.position.y - self.size - 1)))

    def is_alive(self):
        return self.elapsed < self.max_lifetime


# Class for player object
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.exhaust_particles = []  # list of active ExhaustParticle instances
        self.thrust_time = 0.0      # tracks continuous thrust duration

    # Transform the player's position and rotation into a triangle shape for drawing
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def get_exhaust_nozzle_position(self):
        """Compute the engine nozzle position at the back of the ship triangle."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        nozzle = self.position - forward * self.radius
        return nozzle

    def emit_exhaust(self, dt):
        """Emit exhaust particles when thrusting."""
        # Calculate intensity based on thrust duration
        intensity = min(self.thrust_time / EXHAUST_INTENSITY_CAP, 1.0)

        # Calculate particles to emit this frame
        rate = int(EXHAUST_EMISSION_RATE_MIN + intensity * (EXHAUST_EMISSION_RATE_MAX - EXHAUST_EMISSION_RATE_MIN))

        # Get emission parameters
        nozzle = self.get_exhaust_nozzle_position()
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        backward = -forward

        for _ in range(rate):
            # Random angular spread (convert degrees to radians)
            spread_rad = math.radians(random.uniform(-EXHAUST_SPREAD_ANGLE, EXHAUST_SPREAD_ANGLE))

            # Compute velocity direction with spread
            vel_dir = backward.rotate(math.degrees(spread_rad)) if spread_rad != 0 else backward
            speed = random.uniform(EXHAUST_PARTICLE_SPEED_MIN, EXHAUST_PARTICLE_SPEED_MAX)
            velocity = vel_dir * speed

            # Random lifetime, size, color
            lifetime = random.uniform(EXHAUST_PARTICLE_LIFETIME_MIN, EXHAUST_PARTICLE_LIFETIME_MAX)
            size = random.randint(EXHAUST_PARTICLE_SIZE_MIN, EXHAUST_PARTICLE_SIZE_MAX)
            color = random.choice(EXHAUST_COLORS)

            # Create and add particle
            particle = ExhaustParticle(nozzle.copy(), velocity, lifetime, size, color)
            self.exhaust_particles.append(particle)

        # Enforce max particle cap - remove oldest
        while len(self.exhaust_particles) > EXHAUST_MAX_PARTICLES:
            self.exhaust_particles.pop()

    # Draw the player as a triangle
    def draw(self, screen):
        # Draw exhaust particles BEFORE ship polygon (behind ship visually)
        if self.exhaust_particles:
            for particle in self.exhaust_particles:
                if particle.is_alive():
                    particle.draw(screen)

        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    # Rotate the player by a certain amount of degrees
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # Update the player's state using the keyboard input
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown <= 0:
                self.shoot()
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        self.shot_cooldown -= dt

        if not keys[pygame.K_w]:
            self.thrust_time = 0.0

        self.exhaust_particles = [p for p in self.exhaust_particles if not p.update(dt)]

    # Move the player by its velocity
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        self.wrap_position()

        if dt > 0:
            self.thrust_time += dt
            self.emit_exhaust(dt)

    def collides_with(self, other):
        return triangle_circle_collision(self.triangle(), other.position, other.radius)

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

