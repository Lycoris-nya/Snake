import unittest
from main import Play_zone


class MakeStepTest(unittest.TestCase):
    def test_step_up(self):
        self.assertEqual(Play_zone.make_step("up", 0, 1), [0, 0])

    def test_step_right(self):
        self.assertEqual(Play_zone.make_step("right", 0, 0), [1, 0])

    def test_step_down(self):
        self.assertEqual(Play_zone.make_step("down", 0, 0), [0, 1])

    def test_step_left(self):
        self.assertEqual(Play_zone.make_step("left", 1, 0), [0, 0])

    def test_step_up_out_of_zone(self):
        self.assertEqual(Play_zone.make_step("up", 0, 0), [0, Play_zone.NUMBER_BLOCKS_Y])

    def test_step_right_out_of_zone(self):
        self.assertEqual(Play_zone.make_step("right", Play_zone.NUMBER_BLOCKS_X - 1 , 0), [0, 0])

    def test_step_down_out_of_zone(self):
        self.assertEqual(Play_zone.make_step("down", 0, Play_zone.NUMBER_BLOCKS_Y - 1), [0, 0])

    def test_step_left_out_of_zone(self):
        self.assertEqual(Play_zone.make_step("left", 0, 0), [Play_zone.NUMBER_BLOCKS_X - 1, 0])


if __name__ == '__main__':
    unittest.main()
