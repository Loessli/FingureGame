from lib.network import AsyncSession, AsyncServer
from service.net_service import NetService
import json


class Session(AsyncSession):
    m_net: NetService = None

    def __init__(self, connect, session_id):
        super().__init__(connect, session_id)
        self.m_net = NetService()

    def on_connect(self):
        self.m_net.player_add(self)

    def on_receive(self, info: bytes):
        json_data = json.loads(info.decode('utf-8'))
        msg_packet = (self.id, json_data)
        self.m_net.m_sessions.put(msg_packet)

    def on_disconnect(self):
        self.m_net.player_remove(self)


class Server(AsyncServer):
    def __init__(self, session_class):
        super().__init__(session_class)