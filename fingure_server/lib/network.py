import socket
import struct
from lib import log_info
import json
from service.net_service import NetService
from lib.config import Config
import gevent
from typing import (Dict)
from gevent.pool import Pool
from gevent.server import StreamServer

HEAD_LEN = 4


# class Session(object):
#     flag = True
#     disconnect = False  # 防止disconnect触发多次，同一时间？
#     # 不然多次触发，调用remove以后，会有这个报错
#     # During handling of the above exception, another exception occurred:
#
#     def __init__(self, conn: socket.socket, session_id: int):
#         # 初始化构造函数
#         self.conn = conn
#         self.m_net = NetService()
#         self.m_id = session_id
#         # self.green_let = gevent.spawn(self.start_receive)
#
#     def __del__(self):
#         pass
#         # if self.green_let:
#         #     self.green_let.kill()
#
#     def start_receive(self):
#         # 对应的socket开始接收数据，用一个无限循环来做
#         try:
#             while self.flag:
#                 self._receive_data()
#                 gevent.sleep(0.05)
#         except Exception as e:
#             self.close()
#             print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())), "[ERROR]",
#                   "socket start receive buffers error!", e)
#
#     def _receive_data(self):
#         # 实际接收数据逻辑处理
#         try:
#             head_info = self.conn.recv(HEAD_LEN)
#             if len(head_info) > 0:
#                 body_len = struct.unpack(">i", head_info)[0]
#                 body_info = self.conn.recv(body_len)
#                 self.on_receive(body_info)
#         except Exception as e:
#             self.close()
#             print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())), "[WARNING]",
#                   "socket receive data error!", e)
#
#     def on_disconnect(self):
#         # 离线，离开游戏
#         if not self.disconnect:
#             self.disconnect = True
#             print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())), "[WARNING]",
#                   "当前socket断线了,player 离开游戏")
#             self.m_net.player_remove(self)
#
#     def close(self):
#         # 关闭离开
#         self.on_disconnect()
#         self.conn.close()
#         self.flag = False
#
#     def on_connect(self):
#         # 链接，加入游戏
#         self.m_net.player_add(self)
#
#     def on_receive(self, info: bytes):
#         # 接收数据
#         json_data = json.loads(info.decode('utf-8'))
#         # msg_packet = (self, json_data)
#         msg_packet = (self.get_id(), json_data)
#         self.m_net.m_sessions.put(msg_packet)
#
#     def send_msg(self, data: dict):
#         try:
#             # 向客户端发送数据
#             temp_data = json.dumps(data).encode('utf-8')
#             # 心跳包发送的时候可能会crash，就是OSError: [WinError 10038] 在一个非套接字上尝试了一个操作。
#             # 查了下，可能是close以后，再send？
#             self.conn.send(struct.pack(">i", len(temp_data)) + temp_data)
#         except Exception as error_msg:
#             log_info.log(2, "send_msg error!", error_msg)
#
#     def get_id(self) -> str:
#         return str(self.m_id)


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
        gevent.spawn(self.print_current_user)
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
                session.start_receive()
            else:
                self.m_session_dict[socket].start_receive()
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

    def print_current_user(self):
        while True:
            for conn in list(self.m_session_dict.keys()):
                if conn.fileno() == -1:
                    log_info.log(0, 'socket fd 状态为-1，client端已经断开，退出游戏')
                    self.m_session_dict.get(conn).close()
                    self.m_session_dict.pop(conn)
            gevent.sleep(1)


# class Server(object):
#     def __init__(self):
#         self.socket = None
#         self.id = 1
#
#     def start_server(self, addr: tuple):
#         # socket server启动
#         try:
#             self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.socket.bind(addr)
#             self.socket.listen(Config.max_players)
#             # self.socket.setblocking(False)
#         except Exception as e:
#             log_info.log(2, e)
#         log_info.log(0, "开始接受链接！")
#         # invoke(_fun=self.accept)
#
#     def accept(self):
#         # 开始接收
#         while True:
#             conn, add = self.socket.accept()
#             server_session = Session(conn, self.id)
#             self.session_id_change()
#             server_session.on_connect()
#             # self.start_accept()
#
#     def session_id_change(self):
#         # session id增加
#         if self.id < 2133333:
#             self.id += 1
#         else:
#             self.id = 1
#
#     def start_accept(self):
#         # 开始接收数据
#         conn, addr = self.socket.accept()
#         # invoke(self.start_accept)
#         server_session = Session(conn, self.id)
#         self.session_id_change()
#         server_session.on_connect()

