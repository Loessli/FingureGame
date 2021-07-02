import time
import socket, struct, json, random
from locust import Locust, TaskSet, events, task


class TcpSocketClient(socket.socket):
    def __init__(self, af_inet, socket_type):
        super(TcpSocketClient, self).__init__(af_inet, socket_type)

    def connect(self, addr):
        start_time = time.time()
        try:
            super(TcpSocketClient, self).connect(addr)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="connect", response_time=total_time,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="connect", response_time=total_time,
                                        response_length = 0)

    def send_msg(self, msg):
        start_time = time.time()
        try:
            if type(msg) == str:
                msg = msg.encode('utf-8')
            super(TcpSocketClient, self).send(msg)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="send", response_time=total_time,
                                        response_length = 0)

    def receive_msg(self, buffsize):
        recv_data = ''
        start_time = time.time()
        try:
            recv_data = super(TcpSocketClient, self).recv(buffsize)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="recv", response_time=total_time,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="recv", response_time=total_time,
                                        response_length = 0)
        return recv_data


class TcpSocketLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an TCP socket client
    that can be used to make TCP socket requests that will be tracked in Locust's statistics.
    author: Max.bai@2017
    """

    def __init__(self, *args, **kwargs):
        super(TcpSocketLocust, self).__init__(*args, **kwargs)
        self.client = TcpSocketClient(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (self.host, self.port)
        self.client.connect(ADDR)


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


class UserBehavior(TaskSet):
    @task
    def login(self):
        msg = {
            "type": 0,
            "data": {
                "username": "lealli" + str(random.randint(1, 100)),
                "password": "z1314123"
            }
        }
        self.client.send_msg(encode(msg))  # 发送的数据
        data = self.client.recv(2048)
        print(decode(data))
        msg = {
            "type": 2,
            "data": {
                "c_time": 123456,
                "s_time": 23456
            }
        }
        self.client.send_msg(encode(msg))  # 发送的数据
        data = self.client.recv(2048)
        print(decode(data))

    # @task(2)  #这里会有一个权重的问题，权重越高，发送包里面，这个信息的占比就越高
    # def heart_beat(self):
    #     msg = {
    #         "type": 2,
    #         "data": {
    #             "c_time": 123456,
    #             "s_time": 23456
    #         }
    #     }
    #     self.client.send_msg(encode(msg))  # 发送的数据
    #     data = self.client.recv(2048)
    #     print(decode(data))


class TcpTestUser(TcpSocketLocust):
    host = "10.1.55.77"  # 连接的TCP服务的IP
    port = 12456  # 连接的TCP服务的端口
    min_wait = 100
    max_wait = 1000
    # must be task_set
    task_set = UserBehavior


if __name__ == "__main__":
    user = TcpTestUser()
    user.run()
    '''
    使用命令：locust -f E:/PyProject/locust-test/tcp_locust_test.py --csv=test --no-web -c10 -r10 -t2，
    如以下图显示为请求发送成功，并生成了以test开头的测试报告
    命令解释：
    --no-web 
    无web界面模式运行测试，需要-c和-r配合使用
    -c
    指定并发用户数，no-web模式下可用
    -r  
    指定每秒启动的用户数，no-web模式下可用
    -t
    指定运行的时间，no-web模式下可用，0.8.1版本不再提供t参数来指定运行时间，用-n来指定运行次数
    '''
