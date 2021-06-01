from enum import IntEnum
from lib.log_info import log


class PlayerState(IntEnum):
    # 玩家状态
    Waiting = 0,  # 没有发出指令
    Playing = 1   # 发出了指令


class PlayResult(IntEnum):
    # 猜拳结果
    Win = 1,
    Lose = 2,
    Draw = 3  # 平局


class PlayOrder(IntEnum):
    # 猜拳命令
    Scissors = 0,  # 剪刀
    Stone = 1,  # 石头
    Paper = 2  # 布


class _Player(object):
    def __init__(self, msg_pkt):
        self.play_connect = msg_pkt[0].conn
        self.play_sesson = msg_pkt[0]
        self.play_state = PlayerState.Waiting
        self.play_order = None
        self.play_result = None

    def set_order(self,play_order):
        self.play_order = play_order

    def set_result(self,play_result):
        self.play_result = play_result

    def set_play_state(self,state):
        self.play_state = state


class Room(object):
    # 玩家游戏房间
    def __init__(self, room_id: int):
        self.m_players = {}
        self.m_id = room_id

    def play_game(self, msg_pkt):
        # 进入房间逻辑'''
        log(0, f'正在房间{self.m_id} PlayGame')
        for key in self.m_players:
            player = self.m_players.get(key)
            if msg_pkt[0].conn == player.play_connect:
                response_data = msg_pkt[1]['data']
                play_order = response_data.get('play_order')
                play_state = response_data.get('play_state')
                # print(play_state,play_order!=None,player.play_state)
                if player.play_state == PlayerState.Waiting and play_order != None:
                    player.set_play_state(play_state)
                    player.set_order(play_order)

        if len(self.m_players) == 2:
            if self.is_all_playing():
                log(0, '满足条件，开始计算划拳结果')
                self.judge_result()

    def is_all_playing(self):
        # 两个玩家的状态是否都是playing状态'''
        player1 = self.m_players.get('player1')
        player2 = self.m_players.get('player2')
        return (player1.play_state == PlayerState.Playing) and (player2.play_state == PlayerState.Playing)

    def judge_result(self):
        # 判断结果，并发送消息给客户端'''
        player1 = self.m_players.get('player1')
        player2 = self.m_players.get('player2')
        temp_result = player1.play_order - player2.play_order
        if temp_result == 1 or temp_result == -2:
            player1.play_result = PlayResult.Win
            player2.play_result = PlayResult.Lose
        elif player1.play_order == player2.play_order:
            player1.play_result = PlayResult.Draw
            player2.play_result = PlayResult.Draw
        elif temp_result == -1 or temp_result == 2:
            player1.play_result = PlayResult.Lose
            player2.play_result = PlayResult.Win
        player1.play_state = PlayerState.Waiting
        player1.play_state = PlayerState.Waiting
        log(0, f"房间{self.m_id}结果为player1 :{player1.play_result} player2 :{player2.play_result}")
        self.figure_response(player1.play_result, player1.play_sesson)
        self.figure_response(player2.play_result, player2.play_sesson)

    def broadcast_response(self, _data: dict):
        # 向房间内的player广播消息'''
        for key in list(self.m_players.keys()):
            player = self.m_players.get(key)
            if player:
                player.play_sesson.send_msg(_data)

    def figure_response(self,result:int,session):
        # 猜拳结果反送给客户端
        send_data = {
            'type': 1,
            'data': {'play_result':result,"is_over":True}
        }
        session.send_msg(send_data)

    def join_room_response(self, session, game_ready: bool):
        # 加入房间后返回信息
        send_data = {
            "type": 1,
            'data': {
                'room_id': self.m_id,
                'game_ready': game_ready,
                'game_over': False
            }
        }
        session.send_msg(send_data)

    def join_room(self, msg_pkt):
        # 玩家加入房间
        new_player = _Player(msg_pkt)
        self.add_player(new_player)
        if self.get_players() == 1:
            send_data = {
                "type": 1,
                'data': {
                    'room_id': self.m_id,
                    'game_ready': False,
                    'game_over': False
                }
            }
            msg_pkt[0].send_msg(send_data)
        elif self.get_players() == 2:
            send_data = {
                "type": 1,
                'data': {
                    'room_id': self.m_id,
                    'game_ready': True,
                    'game_over': False
                }
            }
            self.broadcast_response(send_data)

    def add_player(self, player):
        # 房间添加一个player
        if self.m_players.get('player1'):
            self.m_players.update({'player2': player})
            log(0, f"player2加入房间{self.m_id}")
        else:
            self.m_players.update({'player1': player})
            log(0, f"player1加入房间{self.m_id}")

    def get_players(self):
        # 当前房间玩家数量
        return len(self.m_players)

    def leaving_room(self,session):
        # 玩家离开房间
        for key in list(self.m_players.keys()):
            player = self.m_players.get(key)
            if player.play_connect == session.conn:
                # player_离开房间
                log(0, f'{key}离开房间')
                self.m_players.pop(key)
        if self.get_players() == 1:
            # 通知另外一个人进入等待状态
            _data = {
                "type": 1,
                "data": {
                    'room_id': self.m_id,
                    'game_ready': False,
                    'game_over': False
                }
            }
            self.broadcast_response(_data)


if __name__ == '__main__':
    data = {
        'player1': 0
    }

    print(len(data), data.get('player2'))