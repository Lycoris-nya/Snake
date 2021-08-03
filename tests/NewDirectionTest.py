import unittest
from main import Play_zone
from collections import deque


class NewDirectionTest(unittest.TestCase):
    def test_queue_empty(self):
        self.assertEqual(Play_zone.new_direction("up", deque()), "up")

    def test_impossible_direction(self):
        self.assertEqual(Play_zone.new_direction("down", deque(["up"])), "down")
        self.assertEqual(Play_zone.new_direction("left", deque(["right"])), "left")
        self.assertEqual(Play_zone.new_direction("up", deque(["down"])), "up")
        self.assertEqual(Play_zone.new_direction("right", deque(["left"])), "right")

    def test_tern_right(self):
        self.assertEqual("right", Play_zone.new_direction("up", deque(["right"])))
        self.assertEqual(Play_zone.new_direction("right", deque(["down"])), "down")
        self.assertEqual(Play_zone.new_direction("down", deque(["left"])), "left")
        self.assertEqual(Play_zone.new_direction("left", deque(["up"])), "up")

    def test_tern_left(self):
        self.assertEqual(Play_zone.new_direction("down", deque(["right"])), "right")
        self.assertEqual(Play_zone.new_direction("left", deque(["down"])), "down")
        self.assertEqual(Play_zone.new_direction("up", deque(["left"])), "left")
        self.assertEqual(Play_zone.new_direction("right", deque(["up"])), "up")


if __name__ == '__main__':
    unittest.main()
