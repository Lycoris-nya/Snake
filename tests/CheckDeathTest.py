import unittest
from main import Play_zone


class CheckDeathTest(unittest.TestCase):
    def test_snake_crashed_into_wall(self):
        self.assertTrue(Play_zone.check_death([0, 0], [[0, 0]], [[0, 0], [0, 1]]))

    def test_snake_crashed_into_itself(self):
        self.assertTrue(Play_zone.check_death([0, 0], [[5, 5]], [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]))

    def test_snake_not_crashed(self):
        self.assertFalse(Play_zone.check_death([0, 0], [[5, 5]], [[0, 0], [1, 0], [1, 1], [0, 1]]))


if __name__ == '__main__':
    unittest.main()
