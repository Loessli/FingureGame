import socket,time
import struct
from lib import log_info
import json
import threading
from service.net_service import NetService
from lib.config import Config

HEAD_LEN = 4


def invoke(_fun):
    # 新建一个子线程，用来执行对应的function
    threading.Thread(target=_fun, daemon=True).start()


class Session(object):
    flag = True
    disconnect = True  # 防止disconnect触发多次，同一时间？
    # 不然多次触发，调用remove以后，会有这个报错
    # During handling of the above exception, another exception occurred:

    def __init__(self, conn: socket.socket, session_id: int):
        # 初始化构造函数
        self.conn = conn
        self.m_net = NetService()
        self.m_id = session_id

    def start_receive(self):
        # 对应的socket开始接收数据，用一个无限循环来做
        try:
            while self.flag:
                self.receive_data()
                time.sleep(0.05)
        except Exception as e:
            self.close()
            print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())), "[ERROR]",
                  "socket start receive buffers error!", e)

    def receive_data(self):
        # 实际接收数据逻辑处理
        try:
            head_info = self.conn.recv(HEAD_LEN)
            if len(head_info) > 0:
                body_len = struct.unpack(">i", head_info)[0]
                body_info = self.conn.recv(body_len)
                self.on_receive(body_info)
        except Exception as e:
            self.close()
            print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())), "[WARNING]",
                  "socket receive data error!", e)

    def on_disconnect(self):
        # 离线，离开游戏
        if self.disconnect:
            self.disconnect = False
            print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())), "[WARNING]",
                  "当前socket断线了,player 离开游戏")
            self.m_net.player_remove(self)

    def close(self):
        # 关闭离开
        self.on_disconnect()
        self.conn.close()
        self.flag = False

    def on_connect(self):
        # 链接，加入游戏
        self.m_net.player_add(self)

    def on_receive(self, info: bytes):
        # 接收数据
        json_data = json.loads(info.decode('utf-8'))
        # msg_packet = (self, json_data)
        msg_packet = (self.get_id(), json_data)
        self.m_net.m_sessions.put(msg_packet)

    def send_msg(self, data: dict):
        # temp_data = json.dumps(data).encode('utf-8')
        # self.conn.send(struct.pack(">i", len(temp_data)) + temp_data)
        try:
            # 向客户端发送数据
            temp_data = json.dumps(data).encode('utf-8')
            # 心跳包发送的时候可能会crash，就是OSError: [WinError 10038] 在一个非套接字上尝试了一个操作。
            # 查了下，可能是close以后，再send？
            self.conn.send(struct.pack(">i", len(temp_data)) + temp_data)
        except Exception as error_msg:
            log_info.log(2, "send_msg error!", error_msg)

    def get_id(self) -> str:
        return str(self.m_id)


class Server(object):
    def __init__(self):
        self.socket = None
        self.id = 1

    def start_server(self, addr: tuple):
        # socket server启动
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(addr)
            self.socket.listen(Config.max_players)
        except Exception as e:
            log_info.log(2, e)
        log_info.log(0, "开始接受链接！")
        invoke(_fun=self.accept)

    def accept(self):
        # 开始接收
        while True:
            self.start_accept()

    def session_id_change(self):
        # session id增加
        if self.id < 2133333:
            self.id += 1
        else:
            self.id = 1

    def start_accept(self):
        # 开始接收数据
        conn, addr = self.socket.accept()
        invoke(self.start_accept)
        server_session = Session(conn, self.id)
        self.session_id_change()
        server_session.on_connect()
        server_session.start_receive()

