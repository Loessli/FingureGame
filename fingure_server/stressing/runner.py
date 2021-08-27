from .users import User
from typing import List
from asyncio.events import AbstractEventLoop
from asyncio import Task
import asyncio
from multiprocessing import Queue


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

    async def spawn_user(self, user_ids: Queue):
        # spawn_user should wait some times, or else socket ConnectionResetError
        # --> https://blog.csdn.net/xunxue1523/article/details/104662965
        while self.user_count > 0:
            user_id = user_ids.get()
            client = self.user_class(self.runner_loop, user_id, self.env["host"], self.env["port"])
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

    def start(self, user_ids: Queue):
        self.runner_loop = asyncio.new_event_loop()
        spawn_task = self.spawn_user(user_ids)
        try:
            self.runner_loop.create_task(spawn_task)
            self.runner_loop.run_until_complete(self.limit())
        except Exception as e:
            print('runner run error', e)

    @property
    def count(self):
        return len(self.m_clients)
