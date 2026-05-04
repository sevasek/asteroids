import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, TRAIL_LENGTH, TRAIL_FADE_SPEED, TRAIL_COLOR, TRAIL_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT
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


# Class for player object
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.trail = []

    # Transform the player's position and rotation into a triangle shape for drawing
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    # Draw the player as a triangle
    def draw(self, screen):
        if self.trail:
            trail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for i, pos in enumerate(self.trail):
                alpha = int(255 * (1 - i / len(self.trail)))
                if alpha > 0:
                    color = (*TRAIL_COLOR, alpha)
                    pygame.draw.circle(trail_surface, color, (int(pos.x), int(pos.y)), TRAIL_WIDTH)
            screen.blit(trail_surface, (0, 0))

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
                
    # Move the player by its velocity
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        self.wrap_position()

        if dt > 0:
            self.trail.insert(0, self.position.copy())
            if len(self.trail) > TRAIL_LENGTH:
                self.trail.pop()

    def collides_with(self, other):
        return triangle_circle_collision(self.triangle(), other.position, other.radius)

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

