from lib.decorator_mode import *
from lib.log_info import log
from queue import Queue
from lib.config import MsgType
from service.login_service import LoginService
from service.game_room_service import GameRoomService
from service.cache_service import CacheService
from service.heart_beat_service import HeartBeatService
import gevent


@singleton
class NetService(object):
    m_sessions = None
    m_login_srv = None
    m_cache = None
    m_heart_beat = None
    m_lock = None

    def init(self):
        log(0, "NetService启动!")
        self.m_sessions = Queue()  # 消息队列
        self.m_login_srv = LoginService()
        self.m_cache = CacheService()
        self.m_heart_beat = HeartBeatService()
        gevent.spawn(self.start_handle_msg)

    def handle_msg(self, msg_pkt):
        '''
        服务器收包处理
        :param msg_pkt:(Session, Data)
        '''
        receive_data = msg_pkt[1]
        log(0, "[ReceiveInfo]", receive_data)
        if receive_data['type'] == MsgType.heart_beat:  # 心跳处理 2
            self.m_heart_beat.heart_beat_handle(msg_pkt)
        elif receive_data['type'] == MsgType.login:
            self.m_login_srv.login_handle(msg_pkt)  # 登陆结果处理  0
        elif receive_data['type'] == MsgType.game_room:
            GameRoomService().join_room_handle(msg_pkt)  # 加入房间处理 1

    def start_handle_msg(self):
        while True:
            if self.m_sessions.qsize() > 0:
                temp = self.m_sessions.get()
                self.handle_msg(temp)
            gevent.sleep(0)

    def player_add(self, session):
        log(0, f"current session id is {session.get_id()}")
        self.m_cache.add_online_user_cache(session)

    def player_remove(self, session):
        # 玩家离开
        self.m_heart_beat.player_remove(session)
        cache_data = self.m_cache.get_online_user_cache(session)
        if cache_data:
            self.m_cache.remove_online_user_cache(session)
            room_id = cache_data.get('room_id')
            if room_id:
                GameRoomService().leaving_room(session, room_id)