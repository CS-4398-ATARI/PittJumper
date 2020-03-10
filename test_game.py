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

    #Test 1a and 1b: Validate user moves left and right as expected.


    #Test 2: Confirm that avatar jumps when initiated.

    #Test 3: Confirm that HP modifies when attacked.

    #Test 4: Validate game clock runs, pauses and stops as expected.


# This allows test_game.py to be executed directly without having
# to run unittest as main module with test_game as argument
if __name__ == '__main__':
    unittest.main()
