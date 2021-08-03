import unittest
from main import Play_zone


class MakeLevelsTest(unittest.TestCase):
    def test_start_snake_not_on_wall(self):
        levels = Play_zone.make_levels()
        for level in levels.keys():
            for coordinates in Play_zone.START_POSITION:
                self.assertFalse(coordinates in levels[level])
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
