import struct
from lib import log_info
import json
import gevent
from typing import Dict
from gevent.server import StreamServer


HEAD_LEN = 4


class AsyncSession(object):
    def __init__(self, connect: gevent.socket.socket, session_id: int):
        self.m_client = connect
        self.m_id = session_id

    def start_receive(self):
        head_info = self.m_client.recv(HEAD_LEN)
        if head_info != b"":
            body_info = self.m_client.recv(struct.unpack(">i", head_info)[0])
            self.on_receive(body_info)
            self.start_receive()
        else:
            return False
        return True

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_receive(self, info: bytes):
        # 接收数据
        # json_data = json.loads(info.decode('utf-8'))
        pass

    def close(self):
        self.m_client.close()
        self.on_disconnect()

    def send_msg(self, send_data: dict):
        try:
            temp_data = json.dumps(send_data).encode('utf-8')
            self.m_client.send(struct.pack(">i", len(temp_data)) + temp_data)
        except Exception as error_msg:
            log_info.log(2, "send_msg error!", error_msg)

    @property
    def id(self):
        return self.m_id

    def get_id(self):
        return self.m_id


class AsyncServer(object):

    m_session_class = None

    def __init__(self, session_class):
        self.m_id = 1
        self.m_server = None
        assert issubclass(session_class, AsyncSession)
        self.m_session_class = session_class
        self.m_session_dict: Dict[gevent.socket, AsyncSession] = {}

    def start_server(self, address: tuple, max_player: int):
        self.m_server = StreamServer(address, self.receive_handle, spawn=max_player)
        self.m_server.serve_forever()

    def receive_handle(self, client_conn, address):
        session = self.m_session_dict.get(client_conn)
        try:
            if not session:
                session = self.m_session_class(client_conn, self.m_id)
                session.on_connect()
                self.session_id_change()
                self.m_session_dict[client_conn] = session
                result = session.start_receive()
            else:
                result = self.m_session_dict[client_conn].start_receive()
            if not result:
                # 退出的时候，会发送一个消息，receive的时候是b""，这时候表示退出
                session.close()
                del self.m_session_dict[client_conn]
        except Exception as e:
            log_info.log(0, "client exist", e)
            if session:
                session.close()
            del self.m_session_dict[client_conn]

    def session_id_change(self):
        # session id增加
        if self.m_id < 2133333:
            self.m_id += 1
        else:
            self.m_id = 1