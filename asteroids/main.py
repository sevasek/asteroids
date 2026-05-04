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


def draw_game_over(screen, score):
    menu = Menu()
    menu.add(MenuElement("GAME OVER", -60, GAME_OVER_TEXT_SIZE))
    menu.add(MenuElement(f"Score: {score}", 0, GAME_OVER_SUBTEXT_SIZE))
    menu.add(MenuElement("Press ENTER to retry or ESC to quit", 50, GAME_OVER_RETRY_TEXT_SIZE))
    menu.draw(screen)


def poll_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
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


def draw(screen, drawable):
    screen.fill("black")
    for d in drawable:
        d.draw(screen)
    pygame.display.flip()


def run_game(screen):
    reset_logger()
    updatable, drawable, asteroids, shots = create_groups()
    player = init_game()
    clock = pygame.time.Clock()
    score = 0

    while True:
        dt = min(clock.tick(60) / 1000, MAX_DELTA_TIME)

        if poll_events() == "quit":
            return False, score

        log_state(player, drawable, asteroids, shots)

        updatable.update(dt)

        player_hit, delta = check_collisions(asteroids, shots, player)
        score += delta
        if player_hit:
            return True, score

        draw(screen, drawable)


def draw_start_menu(screen, leaderboard):
    menu = Menu()
    menu.add(MenuElement("ASTEROIDS", -280, LEADERBOARD_TITLE_SIZE))

    top_scores = leaderboard.get_top()
    if top_scores:
        menu.add(MenuElement("HIGH SCORES", -210, LEADERBOARD_ENTRY_SIZE))
        for i, entry in enumerate(top_scores):
            menu.add(MenuElement(f"{i + 1}. {entry['name']:<12} {entry['score']:>5}", -170 + i * 30, LEADERBOARD_ENTRY_SIZE))
    else:
        menu.add(MenuElement("No scores yet", -140, LEADERBOARD_ENTRY_SIZE))

    menu.add(MenuElement("Press ENTER to start", 280, LEADERBOARD_PROMPT_SIZE))
    menu.draw(screen)


def draw_name_entry(screen, score, name=""):
    menu = Menu()
    menu.add(MenuElement("NEW HIGH SCORE!", -80, GAME_OVER_TEXT_SIZE))
    menu.add(MenuElement(f"Score: {score}", -20, GAME_OVER_SUBTEXT_SIZE))
    menu.add(MenuElement("Enter your name:", 30, GAME_OVER_SUBTEXT_SIZE))
    menu.add(MenuElement(name + "_", 70, GAME_OVER_SUBTEXT_SIZE))
    menu.draw(screen)


def get_player_name(screen, score):
    name = ""
    drawing = True

    while drawing:
        draw_name_entry(screen, score, name)

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

    while True:
        draw_start_menu(screen, leaderboard)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

        result, score = run_game(screen)
        if result is False:
            return

        if leaderboard.is_high_score(score):
            name = get_player_name(screen, score)
            if name:
                leaderboard.add_score(name, score)

        retry = False
        while not retry:
            draw_game_over(screen, score)

            event = poll_events()
            if event == "quit":
                return
            if event == "retry":
                retry = True


if __name__ == "__main__":
    main()
