import asyncio
import multiprocessing
import socket
from typing import (List, Dict)
import time
from asyncio.events import AbstractEventLoop
from asyncio import Task


class User(object):
    def __init__(self, _event_loop, host, port):
        self.m_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_client.setblocking(False)
        self.m_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.runner_loop = _event_loop
        self.address = (host, port)

        # for async io.open_connection
        # self.host = host
        # self.port = port
        # self.m_reader = None
        # self.m_writer = None

    async def start(self):
        await self.send(b"?????????fuck")
        await self.heart_beat()

    async def run(self):
        try:
            await self.runner_loop.sock_connect(self.m_client, self.address)
            # self.m_reader, self.m_writer = await asyncio.open_connection(
            #     host=self.host, port=self.port, loop=self.runner_loop)
        except Exception as e:
            print('connect error', e)
        else:
            await self.start()

    async def heart_beat(self):
        await asyncio.sleep(5)
        send_msg = (str(id(self)) + str(time.time())).encode('utf-8')
        await self.send(send_msg)
        await self.heart_beat()

    def stop(self):
        pass

    async def receive(self, buff_size: int = 1024) -> bytes:
        try:
            data = await self.runner_loop.sock_recv(self.m_client, buff_size)
            # data = self.m_reader.reader(buff_size)
            # TODO receive success
            return data
        except Exception as exp:
            print('receive msg error', exp)

    async def send(self, buff: bytes):
        try:
            await self.runner_loop.sock_sendall(self.m_client, buff)
            # self.m_writer.write(buff)
            # TODO send success
        except Exception as exp:
            print('send msg error', exp)


class Runner(object):
    # 通过async io异步来处理user

    m_clients: List[User] = []

    user_class = None

    m_tasks: List[Task] = []
    # manager task

    runner_loop: AbstractEventLoop = None
    # 一个runner对应一个event loop

    def __init__(self, _env: dict):
        self.env = _env
        self.user_count = _env['user_count']
        self.user_class = _env['user_class']
        assert issubclass(self.user_class, User)
        self.run_time = _env['run_time']

    async def spawn_user(self):
        # spawn_user should wait some times, or else socket ConnectionResetError
        # -->https://blog.csdn.net/xunxue1523/article/details/104662965
        while self.user_count > 0:
            client = self.user_class(self.runner_loop, self.env["host"], self.env["port"])
            self.m_clients.append(client)
            task = client.run()
            self.m_tasks.append(task)
            self.runner_loop.create_task(task)
            self.user_count -= 1
            await asyncio.sleep(0)

    def stop(self):
        for client in self.m_clients:
            client.stop()
        self.m_clients = []
        self.stop_task()
        self.runner_loop.stop()

    def stop_task(self):
        # for task in asyncio.Task.all_tasks(self.runner_loop):
        #     task.cancel()  # -->Task was destroyed but it is pending!

        # assure not exist -->Task was destroyed but it is pending!
        # exist QAQ
        try:
            for task in self.m_tasks:
                task.cancel()
        except Exception as exp:
            # some task is nil, not have attribute cancel
            pass

    async def limit(self):
        await asyncio.sleep(self.run_time)
        self.stop()

    def start(self):
        self.runner_loop = asyncio.new_event_loop()
        spawn_task = self.spawn_user()
        try:
            self.runner_loop.create_task(spawn_task)
            self.runner_loop.run_until_complete(self.limit())
        except Exception as e:
            print('runner run error', e)

    @property
    def count(self):
        return len(self.m_clients)


class RunnerManager(object):
    # 通过多进程来充分利用cpu多核

    m_runners: List[Runner] = []
    env: dict = {}

    def __init__(self, _env: dict):
        self.env = _env
        self.m_runners = []
        self.core_count = multiprocessing.cpu_count()

    def start(self):
        user_count_per_core = int(self.env['user_count'] / self.core_count)
        left = self.env['user_count'] % self.core_count
        if user_count_per_core == 0:
            user_count_per_core = 1
        # cpu有几个核创建几个进程
        for per_core in range(self.core_count):
            if per_core == 0:
                user_count = user_count_per_core + left
            else:
                user_count = user_count_per_core
            self.env["user_count"] = user_count
            temp_runner = Runner(self.env)
            self.m_runners.append(temp_runner)
            multiprocessing.Process(target=temp_runner.start).start()


_env_example: Dict = {
    "user_count": None,
    "user_class": User,
    "run_time": None,
    "host": "127.0.0.1",
    "port": 12457
}


if __name__ == '__main__':
    env = {
        "user_count": 4000,
        "user_class": User,
        "run_time": 100,
        "host": "127.0.0.1",
        "port": "12457"
    }
    runner_mgr = RunnerManager(env)
    runner_mgr.start()