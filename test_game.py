import unittest
from sprites import Spritesheet
import pygame
from unittest.mock import Mock


class TestGame(unittest.TestCase):
    #Testing the sprite class.
    def test_get_image(self):
        g = Mock()
        Spritesheet = g.pygame.image.load("spritesheet_jumper.png").convert()
        image = g.Spritesheet.get_image(614,1063,120,191)
        image2 = g.Spritesheet.get_image(614, 1063, 120, 191)
        self.assertEqual(image, image2)

if __name__ == '__main__':
    unittest.main()
