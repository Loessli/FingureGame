import time
from gevent import socket
import struct, json
from locust import User, events, task, TaskSet
import gevent
from locust.user.task import (
    LOCUST_STATE_RUNNING,
)
from gevent import (GreenletExit, )
from locust.exception import StopUser
from typing import Tuple


class TcpSocketClient(object):
    def __init__(self):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, addr: Tuple):
        start_time = time.time()
        try:
            self.m_socket.connect(addr)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcp", name="connect", response_time=total_time,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcp", name="connect", response_time=total_time,
                                        response_length=0)

    def send_msg(self, msg):
        start_time = time.time()
        try:
            if type(msg) == str:
                msg = msg.encode('utf-8')
            self.m_socket.send(msg)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcp", name="send", response_time=total_time,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcp", name="send", response_time=total_time,
                                        response_length=0)

    def receive_msg(self, buffsize):
        receive_data = b''
        start_time = time.time()
        try:
            receive_data = self.m_socket.recv(buffsize)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcp", name="recv", response_time=total_time,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcp", name="recv", response_time=total_time,
                                        response_length=0)
        return receive_data


# 序列化
def encode(msg: dict):
    msg = json.dumps(msg).encode('utf-8')
    return struct.pack(">i", len(msg)) + msg


# 反序列化
def decode(msg: bytes):
    length = struct.unpack(">i", msg[0:4])[0]
    if len(msg) - 4 == length:
        return json.loads(msg[4:].decode('utf-8'))
    else:
        print('??????????')


USER_ID_LIST = list(range(500))


class TcpTestUser(User):
    host: str = "127.0.0.1"  # 连接的TCP服务的IP
    port: int = 12457  # 连接的TCP服务的端口
    # must be task_set
    tasks = []
    heart_beat_green_let: gevent.Greenlet = None
    tick_delta: float = 2

    def __init__(self, env):
        super().__init__(env)
        self.client = TcpSocketClient()
        self.client.connect((self.host, self.port))
        self.duration = 150
        self.start_time = time.time()
        self.m_id = USER_ID_LIST.pop(0)

    def run(self):
        self._state = LOCUST_STATE_RUNNING
        try:
            self.on_start()
            while True:
                self.tick()
                gevent.sleep(self.tick_delta)
        except (GreenletExit, StopUser):
            # run the on_stop method, if it has one
            self.on_stop()

    def on_start(self):
        print('user on start', self.m_id)
        login_msg = {
            'type': 0,
            'data': {
                'username': 'lealli' + str(self.m_id),
                'password': 'z1314123',
                "room_id": 0,
                "play_state": 0,
                "play_order": 0,
                "leave_room": False
            }
        }
        self.client.send_msg(encode(login_msg))
        print('login result', decode(self.client.receive_msg(1024)))

    def stop(self, force=False):
        print('user stop', self.m_id)
        super().stop(force)

    def on_stop(self):
        print('user on stop', self.m_id)
        if self.heart_beat_green_let:
            self.heart_beat_green_let.kill()

    def heart_beat(self):
        while time.time() - self.start_time <= self.duration:
            print(id(self), time.time(), 'heart_beat', self.m_id)
            gevent.sleep(2)

    def tick(self):
        send_msg = {
            'type': 2,
            'data': {
                'c_time': time.time(),
                's_time': time.time()
            }
        }
        self.client.send_msg(encode(send_msg))
        print('heart beat result', decode(self.client.receive_msg(1024)))


if __name__ == "__main__":
    # print(User.on_stop.__doc__)
    print(list(range(10)))