from lib.log_info import log
from lib.decorator_mode import *
from service.cache_service import CacheService
from enum import IntEnum
import time


class PlayerState(IntEnum):
    CONNECT = 1,  # 在线
    DISCONNECT = 2  # 离线


@singleton
class HeartBeatService(object):
    m_cache = None
    m_running = True
    heartbeat_delta = 5  # 5s一次发送心跳
    m_heartbeat_cache = {}
    temp_time = 0

    '''
    data = {
        's_time': 1,
        'c_time': 2
    }
    '''

    def init(self):
        # 初始化
        log(0, "HeartBeatService启动！")
        self.temp_time = self.get_current_time()
        self.m_cache = CacheService()

    def heart_beat_handle(self, msg_pkt):
        # 心跳网络包接收处理逻辑
        player_session_id = msg_pkt[0]
        player_data = msg_pkt[1]
        c_time = player_data.get('data').get('c_time')
        s_time = player_data.get('data').get('s_time')
        time_cache = {
            'c_time': c_time,
            's_time': self.get_current_time()
        }
        self.m_heartbeat_cache[player_session_id] = time_cache

    def stop_heart_beat(self):
        # 停止服务器心跳逻辑
        self.m_running = False

    def check_player_states(self):
        ...

    def _update_handle(self):
        for session_id in list(self.m_heartbeat_cache.keys()):
            if session_id:
                send_data = {
                    'type': 2,
                    'data': {
                        'c_time': self.m_heartbeat_cache[session_id]['c_time'],
                        's_time': self.get_current_time()
                    }
                }
                self.m_cache.get_session_by_session_id(session_id).send_msg(send_data)

    def player_remove(self, session_id):
        # 玩家离开
        if self.m_heartbeat_cache[session_id]:
            self.m_heartbeat_cache.pop(session_id)

    def get_current_time(self):
        # 获取当前的时间戳
        return int(time.time())

    def update(self):
        # tick
        if self.m_running:
            current_time = self.get_current_time()
            if current_time - self.temp_time >= self.heartbeat_delta:
                self._update_handle()
                self.temp_time = current_time