import socket
import struct
from lib import log_info
import json
from service.net_service import NetService
from lib.config import Config
import gevent
from typing import (Dict)
from gevent.server import StreamServer

HEAD_LEN = 4


class AsyncSession(object):
    def __init__(self, connect: socket.socket, session_id: int):
        self.m_client = connect
        self.m_id = session_id
        self.m_net = NetService()

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
        self.m_net.player_add(self)

    def on_disconnect(self):
        self.m_net.player_remove(self)

    def on_receive(self, info: bytes):
        # 接收数据
        json_data = json.loads(info.decode('utf-8'))
        msg_packet = (self.id, json_data)
        self.m_net.m_sessions.put(msg_packet)

    def close(self):
        self.m_client.close()
        self.on_disconnect()

    def send_msg(self, send_data: dict):
        try:
            # 向客户端发送数据
            temp_data = json.dumps(send_data).encode('utf-8')
            # 心跳包发送的时候可能会crash，就是OSError: [WinError 10038] 在一个非套接字上尝试了一个操作。
            # 查了下，可能是close以后，再send？
            self.m_client.send(struct.pack(">i", len(temp_data)) + temp_data)
        except Exception as error_msg:
            log_info.log(2, "send_msg error!", error_msg)

    @property
    def id(self):
        return self.m_id

    def get_id(self):
        return self.m_id


class AsyncServer(object):
    def __init__(self):
        self.m_id = 1
        self.m_server = None
        self.m_session_dict: Dict[gevent.socket, AsyncSession] = {}

    def start_server(self, addr: tuple):
        self.m_server = StreamServer(addr, self.receive_handle, spawn=Config.max_players)
        # gevent.spawn(self.print_current_user)
        # print('???  server start forever')
        self.m_server.serve_forever()

    def receive_handle(self, client_conn, address):
        session = self.m_session_dict.get(client_conn)
        try:
            if not session:
                session = AsyncSession(client_conn, self.m_id)
                session.on_connect()
                self.session_id_change()
                self.m_session_dict[client_conn] = session
                result = session.start_receive()
            else:
                result = self.m_session_dict[socket].start_receive()
            if not result:
                # 退出的时候，会发送一个消息，receive的时候是b""，这时候表示退出
                if session:
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