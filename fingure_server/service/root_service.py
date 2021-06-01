from lib.decorator_mode import *
from lib.network import Server
from lib.config import Config
from service.net_service import NetService
from service.login_service import LoginService
from service.game_room_service import GameRoomService
from service.cache_service import CacheService
from service.db_service import MysqlDBService
from service.heart_beat_service import HeartBeatService


@singleton
class ServerRoot(object):
    m_cache = None
    m_server = None
    m_db = None
    m_net_service = None
    m_heart_beat = None

    def init(self):
        # 各种service初始化
        NetService().init()
        LoginService().init()
        GameRoomService().init()
        CacheService().init()
        MysqlDBService().init()
        HeartBeatService().init()
        self.m_cache = CacheService()
        self.m_server = Server()
        self.m_net_service = NetService()
        self.m_db = MysqlDBService()
        self.m_heart_beat = HeartBeatService()
        self.m_server.start_server(addr=(Config.server_ip, Config.server_port))

    def updata(self):
        # tick
        self.m_net_service.update()
        self.m_cache.update()
        self.m_heart_beat.update()
