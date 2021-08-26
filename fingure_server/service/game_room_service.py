from game_play.game_room import Room
from lib.decorator_mode import *
from lib.log_info import log
from .cache_service import CacheService
from typing import (Dict)


@singleton
class GameRoomService(object):
    # 房间id的缓存
    m_temp_id = 1
    # 房间缓存 key为id str类型，value为room
    m_rooms: Dict[str, Room] = {}
    # cache服务
    m_cache: CacheService = None

    def init(self):
        log(0, 'GameRoomService启动!')
        self.m_rooms = {}
        self.m_temp_id = 1
        self.m_cache = CacheService()

    def join_room_handle(self, msg_pkt):
        # 加入房间处理
        session_id = msg_pkt[0]
        receive_data = msg_pkt[1]['data']
        room_id = receive_data['room_id']
        # 未分配房间
        if room_id == '' or room_id == 0:
            # 有房间的时候
            if len(self.m_rooms) > 0:
                for temp_key in list(self.m_rooms.keys()):
                    room = self.m_rooms.get(temp_key)
                    # 有空位置
                    if room.get_players() < 2:
                        room.join_room(msg_pkt)
                    else:
                        # 没有空位置
                        self.create_new_room(msg_pkt)
            # 没有房间的时候
            else:
                self.create_new_room(msg_pkt)
        # 已分配房间
        else:
            room = self.m_rooms.get(str(room_id))
            self.m_cache.add_online_user_cache_by_id(session_id, {'room_id': msg_pkt[1]['data']['room_id']})
            room.play_game(msg_pkt)
            if msg_pkt[1]['data'].get('leave_room'):
                self.leaving_room(session_id, room_id)

    def leaving_room(self, session_id, room_id):
        # 玩家离开房间'''
        log(0, f"玩家离开当前房间{room_id}")
        room = self.m_rooms.get(str(room_id))
        room.leaving_room(session_id)
        if room.get_players() == 0:
            self.close_room(room_id)

    def close_room(self, room_id:int):
        # 关闭房间'''
        if self.m_rooms.get(str(room_id)):
            log(0, f"room {room_id} 没有玩家了，自动关闭")
            self.m_rooms.pop(str(room_id))

    def create_new_room(self, msg_pkt):
        # 创建新的房间'''
        log(0, f"创建新的房间{self.m_temp_id}")
        new_room = Room(self.m_temp_id)
        new_room.join_room(msg_pkt)
        self.m_cache.add_online_user_cache_by_id(msg_pkt[0], {'room_id': msg_pkt[1]['data']['room_id']})
        self.m_rooms.update({str(self.m_temp_id): new_room})
        if self.m_temp_id < 210000:
            self.m_temp_id += 1
        else:
            self.m_temp_id = 1