from lib.decorator_mode import *
from lib.network import AsyncServer
from lib.config import Config
from .net_service import NetService
from .login_service import LoginService
from .game_room_service import GameRoomService
from .cache_service import CacheService
from .db_service import MysqlDBService
from .heart_beat_service import HeartBeatService
import gevent
from gevent import monkey


@singleton
class ServerRoot(object):
    m_cache = None
    m_server = None
    m_db = None
    m_net_service = None
    m_heart_beat = None

    def init(self):
        # 各种service初始化
        monkey.patch_all()

        NetService().init()
        LoginService().init()
        GameRoomService().init()
        CacheService().init()
        MysqlDBService().init()
        HeartBeatService().init()
        self.m_cache = CacheService()
        self.m_net_service = NetService()
        self.m_db = MysqlDBService()
        gevent.spawn(self.updata)
        self.m_server = AsyncServer()  # Server()
        self.m_server.start_server(addr=(Config.server_ip, Config.server_port))

    def updata(self):
        while True:
            self.m_cache.update()
            # self.m_heart_beat.update()
            gevent.sleep(Config.tick_frame)
