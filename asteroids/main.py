from __future__ import annotations
import pygame
from constants import (
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
from asteroids import Asteroid
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
            menu.add(MenuElement("HIGH SCORES", -80, LEADERBOARD_ENTRY_SIZE))
            for i, entry in enumerate(top_scores):
                y = -40 + i * 30
                menu.add(MenuElement(f"{i + 1}.", y, LEADERBOARD_ENTRY_SIZE, x_offset=-140))
                menu.add(MenuElement(entry['name'], y, LEADERBOARD_ENTRY_SIZE, x_offset=-110))
                menu.add(MenuElement(str(entry['score']), y, LEADERBOARD_ENTRY_SIZE, x_offset=120))
            menu.add(MenuElement("Press ENTER to restart", 220, GAME_OVER_RETRY_TEXT_SIZE))
            menu.add(MenuElement("Press ESC for menu", 250, GAME_OVER_RETRY_TEXT_SIZE))
        else:
            menu.add(MenuElement("Press ENTER to restart", -40, GAME_OVER_RETRY_TEXT_SIZE))
            menu.add(MenuElement("Press ESC for menu", 40, GAME_OVER_RETRY_TEXT_SIZE))
    else:
        menu.add(MenuElement("GAME OVER", -60, GAME_OVER_TEXT_SIZE))
        menu.add(MenuElement(f"Score: {score}", 0, GAME_OVER_SUBTEXT_SIZE))
        menu.add(MenuElement("Press ENTER to restart", 60, GAME_OVER_RETRY_TEXT_SIZE))
        menu.add(MenuElement("Press ESC for menu", 90, GAME_OVER_RETRY_TEXT_SIZE))

    menu.draw(screen, starfield)


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


def check_collisions(asteroids, shots, player):
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
                a.split()
                s.kill()
                score_delta += 10
                break

    return player_hit, score_delta


def draw(screen, drawable, starfield):
    screen.fill("black")
    starfield.draw(screen)
    for d in drawable:
        d.draw(screen)
    pygame.display.flip()


def run_game(screen, starfield):
    reset_logger()
    updatable, drawable, asteroids, shots = create_groups()
    player = init_game()
    clock = pygame.time.Clock()
    score = 0

    while True:
        dt = min(clock.tick(60) / 1000, MAX_DELTA_TIME)

        if poll_events() == "quit":
            return False, score

        starfield.update(dt)

        log_state(player, drawable, asteroids, shots)

        updatable.update(dt)

        player_hit, delta = check_collisions(asteroids, shots, player)
        score += delta
        if player_hit:
            return True, score

        draw(screen, drawable, starfield)


def draw_start_menu(screen, leaderboard, starfield):
    menu = Menu()
    menu.add(MenuElement("ASTEROIDS", -280, LEADERBOARD_TITLE_SIZE))

    top_scores = leaderboard.get_top()
    if top_scores:
        menu.add(MenuElement("HIGH SCORES", -210, LEADERBOARD_ENTRY_SIZE))
        for i, entry in enumerate(top_scores):
            y = -170 + i * 30
            menu.add(MenuElement(f"{i + 1}.", y, LEADERBOARD_ENTRY_SIZE, x_offset=-140))
            menu.add(MenuElement(entry['name'], y, LEADERBOARD_ENTRY_SIZE, x_offset=-110))
            menu.add(MenuElement(str(entry['score']), y, LEADERBOARD_ENTRY_SIZE, x_offset=120))
    else:
        menu.add(MenuElement("No scores yet", -140, LEADERBOARD_ENTRY_SIZE))

    menu.add(MenuElement("Press ENTER to start", 280, LEADERBOARD_PROMPT_SIZE))
    menu.draw(screen, starfield)


def draw_name_entry(screen, score, starfield, name=""):
    menu = Menu()
    menu.add(MenuElement("NEW HIGH SCORE!", -80, GAME_OVER_TEXT_SIZE))
    menu.add(MenuElement(f"Score: {score}", -20, GAME_OVER_SUBTEXT_SIZE))
    menu.add(MenuElement("Enter your name:", 30, GAME_OVER_SUBTEXT_SIZE))
    menu.add(MenuElement(name + "_", 70, GAME_OVER_SUBTEXT_SIZE))
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
            if event == "retry":
                retry = True


if __name__ == "__main__":
    main()
