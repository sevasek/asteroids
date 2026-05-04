from __future__ import annotations
import random
import sys


def _check_pygame():
    try:
        import pygame.font
    except ImportError:
        print("ERROR: pygame.font module not available")
        print("On macOS: brew install sdl2_ttf && pip install pygame")
        sys.exit(1)


_check_pygame()

import pygame
from constants import (
    EXHAUST_COLORS,
    EXPLOSION_COUNT_LARGE_MAX,
    EXPLOSION_COUNT_LARGE_MIN,
    EXPLOSION_COUNT_MEDIUM_MAX,
    EXPLOSION_COUNT_MEDIUM_MIN,
    EXPLOSION_COUNT_SMALL_MAX,
    EXPLOSION_COUNT_SMALL_MIN,
    EXPLOSION_PARTICLE_LIFETIME_MAX,
    EXPLOSION_PARTICLE_LIFETIME_MIN,
    EXPLOSION_PARTICLE_SIZE_MAX,
    EXPLOSION_PARTICLE_SIZE_MIN,
    EXPLOSION_PARTICLE_SPEED_MAX,
    EXPLOSION_PARTICLE_SPEED_MIN,
    GAME_OVER_RETRY_TEXT_SIZE,
    GAME_OVER_SUBTEXT_SIZE,
    GAME_OVER_TEXT_SIZE,
    LEADERBOARD_ENTRY_SIZE,
    LEADERBOARD_MAX_NAME_LENGTH,
    LEADERBOARD_PROMPT_SIZE,
    LEADERBOARD_TITLE_SIZE,
    MAX_DELTA_TIME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from asteroid import Asteroid
from hyperdrive import Hyperdrive
from leaderboard import Leaderboard
from logger import log_state, log_event, reset_logger
from menu import Menu, MenuElement
from player import Player
from asteroidfield import AsteroidField
from shot import Shot
from starfield import StarField


def create_groups():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    return updatable, drawable, asteroids, shots


def init_game():
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()
    return player


def draw_game_over(screen, score, starfield, leaderboard=None):
    menu = Menu()

    if leaderboard:
        top_scores = leaderboard.get_top()
        if top_scores:
            menu.add_to_top(MenuElement("HIGH SCORES", font_size=LEADERBOARD_ENTRY_SIZE))
            for entry in top_scores:
                menu.add_to_middle(MenuElement(entry['name'], font_size=LEADERBOARD_ENTRY_SIZE, x_offset=-140))
                menu.add_to_middle(MenuElement(str(entry['score']), font_size=LEADERBOARD_ENTRY_SIZE, x_offset=120))
        else:
            menu.add_to_middle(MenuElement("Press ENTER to restart", font_size=GAME_OVER_RETRY_TEXT_SIZE))
            menu.add_to_bottom(MenuElement("Press ESC for menu", font_size=GAME_OVER_RETRY_TEXT_SIZE))
            menu.draw(screen, starfield)
            return
    else:
        menu.add_to_top(MenuElement("GAME OVER", font_size=GAME_OVER_TEXT_SIZE))
        menu.add_to_middle(MenuElement(f"Score: {score}", font_size=GAME_OVER_SUBTEXT_SIZE))

    menu.add_to_bottom(MenuElement("Press ENTER to restart", font_size=GAME_OVER_RETRY_TEXT_SIZE))
    menu.add_to_bottom(MenuElement("Press ESC for menu", font_size=GAME_OVER_RETRY_TEXT_SIZE))
    menu.draw(screen, starfield, middle_pairs=True if leaderboard else False)


def poll_events(menu_mode=False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu" if menu_mode else "quit"
            if event.key == pygame.K_RETURN:
                return "retry"
    return None


def get_explosion_particle_count(radius):
    if radius >= 40:
        return random.randint(EXPLOSION_COUNT_LARGE_MIN, EXPLOSION_COUNT_LARGE_MAX)
    elif radius >= 20:
        return random.randint(EXPLOSION_COUNT_MEDIUM_MIN, EXPLOSION_COUNT_MEDIUM_MAX)
    else:
        return random.randint(EXPLOSION_COUNT_SMALL_MIN, EXPLOSION_COUNT_SMALL_MAX)


def spawn_explosion(position, radius, explosion_particles):
    from player import ExhaustParticle

    particle_count = get_explosion_particle_count(radius)

    for _ in range(particle_count):
        angle = random.uniform(0, 360)
        direction = pygame.Vector2(0, 1).rotate(angle)
        speed = random.uniform(EXPLOSION_PARTICLE_SPEED_MIN, EXPLOSION_PARTICLE_SPEED_MAX)
        velocity = direction * speed
        lifetime = random.uniform(EXPLOSION_PARTICLE_LIFETIME_MIN, EXPLOSION_PARTICLE_LIFETIME_MAX)
        size = random.randint(EXPLOSION_PARTICLE_SIZE_MIN, EXPLOSION_PARTICLE_SIZE_MAX)
        color = random.choice(EXHAUST_COLORS)
        particle = ExhaustParticle(position.copy(), velocity, lifetime, size, color)
        explosion_particles.append(particle)


def check_collisions(asteroids, shots, player, explosion_particles):
    player_hit = False
    score_delta = 0

    for a in list(asteroids):
        if player.collides_with(a):
            log_event("player_hit")
            player_hit = True
            break

        for s in shots.copy():
            if a.collides_with(s):
                log_event("asteroid_shot")
                spawn_explosion(a.position.copy(), a.radius, explosion_particles)
                a.split()
                s.kill()
                score_delta += 10
                break

    return player_hit, score_delta


def draw(screen, drawable, starfield, explosion_particles):
    screen.fill("black")
    starfield.draw(screen)
    for particle in explosion_particles:
        if particle.is_alive():
            particle.draw(screen)
    for d in drawable:
        d.draw(screen)
    pygame.display.flip()


def run_game(screen, starfield, run_hyperdrive=True):
    if run_hyperdrive:
        screen.fill("black")
        pygame.display.flip()
        clock = pygame.time.Clock()
        hyperdrive = Hyperdrive(starfield)
        while not hyperdrive.is_complete():
            dt = min(clock.tick(60) / 1000, MAX_DELTA_TIME)
            hyperdrive.update(dt)
            hyperdrive.draw(screen)
            pygame.display.flip()

    reset_logger()
    updatable, drawable, asteroids, shots = create_groups()
    explosion_particles = []
    player = init_game()
    clock = pygame.time.Clock()
    score = 0
    survival_elapsed = 0

    while True:
        dt = min(clock.tick(60) / 1000, MAX_DELTA_TIME)

        if poll_events() == "quit":
            return False, score

        starfield.update(dt)

        log_state(player, drawable, asteroids, shots)

        updatable.update(dt)

        explosion_particles = [p for p in explosion_particles if not p.update(dt)]

        player_hit, delta = check_collisions(asteroids, shots, player, explosion_particles)
        score += delta

        survival_elapsed += dt
        if survival_elapsed >= 1:
            score += 1
            survival_elapsed -= 1

        if player_hit:
            return True, score

        draw(screen, drawable, starfield, explosion_particles)


def draw_start_menu(screen, leaderboard, starfield):
    menu = Menu()
    menu.add_to_top(MenuElement("ASTEROIDS", font_size=LEADERBOARD_TITLE_SIZE))

    top_scores = leaderboard.get_top()
    if top_scores:
        menu.add_to_top(MenuElement("HIGH SCORES", font_size=LEADERBOARD_ENTRY_SIZE))
        for entry in top_scores:
            menu.add_to_middle(MenuElement(entry['name'], font_size=LEADERBOARD_ENTRY_SIZE, x_offset=-140))
            menu.add_to_middle(MenuElement(str(entry['score']), font_size=LEADERBOARD_ENTRY_SIZE, x_offset=120))
    else:
        menu.add_to_middle(MenuElement("No scores yet", font_size=LEADERBOARD_ENTRY_SIZE))

    menu.add_to_bottom(MenuElement("Press ENTER to start", font_size=LEADERBOARD_PROMPT_SIZE))
    menu.draw(screen, starfield, middle_pairs=True)


def draw_name_entry(screen, score, starfield, name=""):
    menu = Menu()
    menu.add_to_top(MenuElement("NEW HIGH SCORE!", font_size=GAME_OVER_TEXT_SIZE))
    menu.add_to_middle(MenuElement(f"Score: {score}", font_size=GAME_OVER_SUBTEXT_SIZE))
    menu.add_to_middle(MenuElement("Enter your name:", font_size=GAME_OVER_SUBTEXT_SIZE))
    menu.add_to_middle(MenuElement(name + "_", font_size=GAME_OVER_SUBTEXT_SIZE))
    menu.draw(screen, starfield)


def get_player_name(screen, score, starfield):
    name = ""
    drawing = True

    while drawing:
        draw_name_entry(screen, score, starfield, name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                if event.key == pygame.K_RETURN:
                    drawing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < LEADERBOARD_MAX_NAME_LENGTH:
                    if event.unicode.isalnum():
                        name += event.unicode.upper()

    return name


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    leaderboard = Leaderboard()
    starfield = StarField()
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000
        starfield.update(dt)

        draw_start_menu(screen, leaderboard, starfield)

        waiting = True
        while waiting:
            event = poll_events(menu_mode=True)
            if event == "quit":
                return
            if event == "retry":
                waiting = False

        result, score = run_game(screen, starfield)
        if result is False:
            return

        show_leaderboard = False
        if leaderboard.is_high_score(score):
            name = get_player_name(screen, score, starfield)
            if name is None:
                return
            if name:
                leaderboard.add_score(name, score)
                show_leaderboard = True

        go_to_start = False
        retry = False
        while not retry:
            dt = clock.tick(60) / 1000
            starfield.update(dt)

            draw_game_over(screen, score, starfield, leaderboard if show_leaderboard else None)

            event = poll_events()
            if event == "quit":
                return
            if event == "menu":
                retry = True
                go_to_start = True
            if event == "retry":
                retry = True
                go_to_start = False

        if not go_to_start:
            result, score = run_game(screen, starfield)
            if result is False:
                return

            show_leaderboard = False
            if leaderboard.is_high_score(score):
                name = get_player_name(screen, score, starfield)
                if name is None:
                    return
                if name:
                    leaderboard.add_score(name, score)
                    show_leaderboard = True


if __name__ == "__main__":
    main()
