import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import pygame
    pygame.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    raise unittest.SkipTest("pygame not installed")

from player import Player
from asteroid import Asteroid
from shot import Shot


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(640, 360)

    def test_initial_position(self):
        self.assertEqual(self.player.position.x, 640)
        self.assertEqual(self.player.position.y, 360)

    def test_initial_rotation(self):
        self.assertEqual(self.player.rotation, 0)

    def test_rotate_left(self):
        self.player.rotation = 0
        self.player.rotate(0.1)
        self.assertLess(self.player.rotation, 0)

    def test_rotate_right(self):
        self.player.rotation = 0
        self.player.rotate(-0.1)
        self.assertGreater(self.player.rotation, 0)

    def test_move_forward(self):
        initial_x = self.player.position.x
        self.player.move(0.1)
        self.assertNotEqual(self.player.position.x, initial_x)

    def test_shoot_creates_shot(self):
        self.player.rotation = 0
        shot = Shot(self.player.position.x, self.player.position.y)
        self.assertIsNotNone(shot)


class TestAsteroid(unittest.TestCase):
    def test_asteroid_creation(self):
        asteroid = Asteroid(640, 360, 50)
        self.assertEqual(asteroid.radius, 50)
        self.assertEqual(asteroid.position.x, 640)

    def test_asteroid_velocity(self):
        asteroid = Asteroid(640, 360, 50)
        self.assertNotEqual(asteroid.velocity.x, 0)


class TestShot(unittest.TestCase):
    def test_shot_velocity(self):
        shot = Shot(640, 360)
        self.assertNotEqual(shot.velocity.x, 0)


if __name__ == "__main__":
    unittest.main()