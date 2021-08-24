import asyncio
import multiprocessing
import socket
from typing import (List, Dict)
import time


class Config(object):
    user_count = 100
    host = "127.0.0.1"
    port = 12457


class Client(object):
    def __init__(self, _event_loop):
        self.m_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_client.setblocking(False)

        self.main_loop = _event_loop
        self.address = (Config.host, Config.port)

        # for async io.open_connection
        # self.m_reader = None
        # self.m_writer = None

    async def run(self):
        try:
            await self.main_loop.sock_connect(self.m_client, self.address)
            # self.m_reader, self.m_writer = await asyncio.open_connection(
            #     host=Config.host, port=Config.port, loop=self.main_loop)
            await asyncio.sleep(1)
        except Exception as e:
            print('connect error', e)
        else:
            await self.send(b"?????????fuck")
            await self.heart_beat()

    async def heart_beat(self):
        await asyncio.sleep(2)
        send_msg = (str(id(self)) + str(time.time())).encode('utf-8')
        await self.send(send_msg)
        await self.heart_beat()

    def stop(self):
        pass

    async def receive(self, buff_size: int = 1024) -> bytes:
        data = await self.main_loop.sock_recv(self.m_client, buff_size)
        # data = self.m_reader.reader(buff_size)
        # TODO receive success
        return data

    async def send(self, buff: bytes):
        await self.main_loop.sock_sendall(self.m_client, buff)
        # self.m_writer.write(buff)
        # TODO send success


_env: Dict = {
    "event_loop": None,
    "user_count": None,
    "user_class": Client,
    "run_time": None
}


class Runner(object):
    m_clients: List[Client] = []
    user_class = None
    main_loop = None

    def __init__(self, _env: dict):
        self.user_count = _env['user_count']
        self.user_class = _env['user_class']
        self.run_time = _env['run_time']

    def spawn_user(self):
        while self.user_count > 0:
            client = self.user_class(self.main_loop)
            self.m_clients.append(client)
            self.main_loop.create_task(client.run())
            self.user_count -= 1

    def stop(self):
        for client in self.m_clients:
            client.stop()
            del client
        self.m_clients = []
        self.main_loop.stop()

    async def limit(self):
        await asyncio.sleep(self.run_time)
        self.stop()

    def start(self):
        self.main_loop = asyncio.new_event_loop()
        self.spawn_user()
        try:
            self.main_loop.run_until_complete(self.limit())
        except Exception as e:
            print('???????????', e)

    @property
    def count(self):
        return len(self.m_clients)


class RunnerManager(object):

    def __init__(self, _env: dict):
        # 一个核对应一个进程，完美利用多核
        self.env = _env
        self.m_runners = []
        self.core_count = multiprocessing.cpu_count()

    def get_core_count(self):
        self.core_count = multiprocessing.cpu_count()

    def start(self):
        user_count_per_core = int(self.env['user_count'] / self.core_count)
        left = self.env['user_count'] % self.core_count
        if user_count_per_core == 0:
            user_count_per_core = 1
        # cpu有几个核创建几个进程
        for per_core in range(0, self.core_count):
            if per_core == 0:
                user_count = user_count_per_core + left
            else:
                user_count = user_count_per_core
            runner_env = {
                "user_count": user_count,
                "user_class": self.env['user_class'],
                "run_time": self.env['run_time']
            }
            temp_runner = Runner(runner_env)
            self.m_runners.append(temp_runner)
            multiprocessing.Process(target=temp_runner.start).start()


if __name__ == '__main__':
    # env = {"user_count": 4000, "user_class": Client, "run_time": 300}
    # runner = RunnerManager(env)
    # runner.start()
    print(str(time.time()))