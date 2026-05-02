from __future__ import annotations
import pygame
from constants import (
    GAME_OVER_RETRY_TEXT_SIZE,
    GAME_OVER_SUBTEXT_SIZE,
    GAME_OVER_TEXT_SIZE,
    MAX_DELTA_TIME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from asteroids import Asteroid
from logger import log_state, log_event, reset_logger
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
    font_large = pygame.font.SysFont(None, GAME_OVER_TEXT_SIZE)
    font_medium = pygame.font.SysFont(None, GAME_OVER_SUBTEXT_SIZE)
    font_small = pygame.font.SysFont(None, GAME_OVER_RETRY_TEXT_SIZE)

    game_over_text = font_large.render("GAME OVER", True, "white")
    score_text = font_medium.render(f"Score: {score}", True, "white")
    retry_text = font_small.render("Press ENTER to retry or ESC to quit", True, "white")

    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60)))
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
    screen.blit(retry_text, retry_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)))


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
        if a.collides_with(player):
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        result, score = run_game(screen)
        if result is False:
            return

        retry = False
        while not retry:
            draw_game_over(screen, score)
            pygame.display.flip()

            event = poll_events()
            if event == "quit":
                return
            if event == "retry":
                retry = True


if __name__ == "__main__":
    main()
