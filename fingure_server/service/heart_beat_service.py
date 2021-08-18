from lib.log_info import log
from lib.decorator_mode import *
from service.cache_service import CacheService
from enum import IntEnum
import time
from typing import (Dict)
import gevent


# var
HEART_DELTA = 5


class PlayerState(IntEnum):
    CONNECT = 1,  # 在线
    DISCONNECT = 2  # 离线


class HeartBeat(object):
    def __init__(self, session_id, client_data: dict):
        self.m_cache = CacheService()
        self.m_client_data = client_data
        self.last_c_time = 1
        self.current_c_time: int = 1
        self.m_session = self.m_cache.get_session_by_session_id(session_id)
        self.green_let = gevent.spawn(self.start)

    def __del__(self):
        if self.green_let:
            self.green_let.kill()

    def start(self):
        while True:
            self.heart_beat_handle()
            gevent.sleep(HEART_DELTA)

    def heart_beat_handle(self):
        # TODO 拓展
        if not self.m_client_data:
            self.m_client_data = {
                'c_time': int(time.time()),
            }
        log(0, 'start send heartbeat')
        msg = {
            'type': 2,
            'data': {
                's_time': int(time.time()),
                'c_time': self.m_client_data.get('c_time')
            }
        }
        self.m_session.send_msg(msg)

    def update_client_data(self, client_data: dict):
        self.m_client_data = client_data

    def stop_heart_beat(self):
        self.m_session.close()
        if self.green_let:
            self.green_let.kill()


@singleton
class HeartBeatService(object):
    m_cache = None
    m_running = True
    heartbeat_delta = 5  # 5s一次发送心跳
    m_heartbeat_cache: Dict[int, HeartBeat]  = {}
    temp_time = 0
    m_manager = None

    '''
    data = {
        's_time': 1,
        'c_time': 2
    }
    '''

    def init(self):
        # 初始化
        log(0, "HeartBeatService启动！")
        self.m_cache = CacheService()

    def heart_beat_handle(self, msg_pkt):
        # 心跳网络包接收处理逻辑
        player_session_id = msg_pkt[0]
        player_data = msg_pkt[1]
        # 新进的player
        if player_session_id not in self.m_heartbeat_cache:
            self.m_heartbeat_cache[player_session_id] = HeartBeat(player_session_id, player_data)
        else:
            self.m_heartbeat_cache[player_session_id].update_client_data(player_data)

    def player_remove(self, session_id):
        # 玩家离开
        if self.m_heartbeat_cache.get(session_id):
            self.m_heartbeat_cache[session_id].stop_heart_beat()
            self.m_heartbeat_cache.pop(session_id)


