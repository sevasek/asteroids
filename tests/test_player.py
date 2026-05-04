import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import pygame
    pygame.init()
    from player import Player
    from shot import Shot
except ImportError:
    pygame = None


@unittest.skipIf(pygame is None, "pygame not installed")
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(640, 360)

    def test_initial_position(self):
        self.assertEqual(self.player.position.x, 640)
        self.assertEqual(self.player.position.y, 360)

    def test_initial_rotation(self):
        self.assertEqual(self.player.rotation, 0)

    def test_rotate_positive_dt_increases(self):
        self.player.rotation = 0
        self.player.rotate(0.1)
        self.assertGreater(self.player.rotation, 0)

    def test_rotate_negative_dt_decreases(self):
        self.player.rotation = 0
        self.player.rotate(-0.1)
        self.assertLess(self.player.rotation, 0)

    def test_move_positive_dt_changes_position(self):
        initial_y = self.player.position.y
        self.player.move(0.1)
        self.assertNotEqual(self.player.position.y, initial_y)

    def test_move_negative_dt_moves_backward(self):
        initial_y = self.player.position.y
        self.player.move(-0.1)
        self.assertNotEqual(self.player.position.y, initial_y)


@unittest.skipIf(pygame is None, "pygame not installed")
class TestShot(unittest.TestCase):
    def test_shot_has_position(self):
        shot = Shot(640, 360)
        self.assertEqual(shot.position.x, 640)
        self.assertEqual(shot.position.y, 360)

    def test_shot_can_be_updated(self):
        shot = Shot(640, 360)
        shot.velocity = pygame.Vector2(10, 0)
        shot.update(0.1)
        self.assertEqual(shot.position.x, 641)


if __name__ == "__main__":
    unittest.main()