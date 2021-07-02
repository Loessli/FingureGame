import unittest
from game_play.game_room import Room, Player
from unittest import mock


class GameRoomTest(unittest.TestCase):
    def setUp(self) -> None:
        self.m_room = Room(30)

    def test_01_room_is_all_playing(self):
        assert self.m_room.is_all_playing() is None, '??????'

    def test_02_room_is_all_playing(self):
        # 1没发指令，2发出了指令
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player1.set_play_state(1)
        self.player2.set_play_state(1)
        # self.m_room.m_players = mock.Mock(return_value={
        #     'player1': self.player1,
        #     'player2': self.player2
        # })
        self.m_room.m_players = {
            'player1': self.player1,
            'player2': self.player2
        }
        # print(self.m_room.m_players)
        # print('111111111111111', self.m_room.is_all_playing())
        assert self.m_room.is_all_playing(), 'ttt'
        self.player1.set_play_state(0)
        self.player2.set_play_state(1)
        assert not self.m_room.is_all_playing(), 'aaa'

        self.player1.set_play_state(0)
        self.player2.set_play_state(0)
        assert not self.m_room.is_all_playing(), 'bbb'

        self.player1.set_play_state(1)
        self.player2.set_play_state(0)
        assert not self.m_room.is_all_playing(), 'ccc'

    def test_03_judge_result(self):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player1.set_play_state(1)
        self.player2.set_play_state(1)
        self.m_room.m_players = {
            'player1': self.player1,
            'player2': self.player2
        }
        self.player1.set_order(1)
        self.player2.set_order(2)
        self.m_room.judge_result()


if __name__ == '__main__':
    unittest.main()