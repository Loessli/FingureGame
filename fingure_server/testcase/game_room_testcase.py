import unittest
from game_play.game_room import Room
from unittest import mock


class GameRoomTest(unittest.TestCase):
    def test_01_room_ctor(self):
        room = Room(30)

    def test_02_room_play_game(self):
        room = Room(30)
        temp = mock.Mock(30)
        print(temp)


if __name__ == '__main__':
    L = [1, 2, 3, 4, 5, 6, 7, 8, 9, 6, 4, 3]
    L.sort()
    print(L)