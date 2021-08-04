import collections
import unittest
import copy
from main import Play_zone


def bfs(graph, root):
    queue = collections.deque([root])
    graph = copy.deepcopy(graph)
    graph[root[1]][root[0]] = 2

    while queue:
        neighbours = []
        vertex = queue.popleft()
        if vertex[0] - 1 >= 0 and graph[vertex[1]][vertex[0] - 1] == 0:
            neighbours.append([vertex[0] - 1, vertex[1]])

        if vertex[0] + 1 < Play_zone.NUMBER_BLOCKS_X and graph[vertex[1]][vertex[0] + 1] == 0:
            neighbours.append([vertex[0] + 1, vertex[1]])

        if vertex[1] - 1 >= 0 and graph[vertex[1] - 1][vertex[0]] == 0:
            neighbours.append([vertex[0], vertex[1] - 1])

        if vertex[1] + 1 < Play_zone.NUMBER_BLOCKS_Y and graph[vertex[1] + 1][vertex[0]] == 0:
            neighbours.append([vertex[0], vertex[1] + 1])

        for neighbour in neighbours:
            graph[neighbour[1]][neighbour[0]] = 2
            queue.append(neighbour)

    return graph


class MakeLevelsTest(unittest.TestCase):
    def test_start_snake_not_on_wall(self):
        levels = Play_zone.make_levels()
        for level in levels.keys():
            for coordinates in Play_zone.START_POSITION:
                self.assertFalse(coordinates in levels[level])

    def test_all_place_available(self):
        levels = Play_zone.make_levels()
        for level in levels.keys():
            play_zone = [[0] * Play_zone.NUMBER_BLOCKS_X for i in range(Play_zone.NUMBER_BLOCKS_Y)]
            for coordinates in levels[level]:
                play_zone[coordinates[1]][coordinates[0]] = 1
            play_zone = bfs(play_zone, Play_zone.START_POSITION[0])
            for x in range(Play_zone.NUMBER_BLOCKS_X):
                for y in range(Play_zone.NUMBER_BLOCKS_Y):
                    self.assertTrue(play_zone[y][x] != 0)


if __name__ == '__main__':
    unittest.main()
