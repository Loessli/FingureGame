import multiprocessing
from typing import List
from .runner import Runner
from multiprocessing import Queue


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
        print(f"total user count {self.env['user_count']}", user_count_per_core)
        last_count = 0
        for per_core in range(self.core_count):  # self.core_count
            if per_core == 0:
                user_count = user_count_per_core + left
            else:
                user_count = user_count_per_core
            user_ids = Queue()
            for user_id in range(user_count):
                user_ids.put(user_id + last_count)
            last_count += user_count
            self.env["user_count"] = user_count
            temp_runner = Runner(self.env)
            self.m_runners.append(temp_runner)
            multiprocessing.Process(target=temp_runner.start, args=(user_ids, )).start()

    def stop(self):
        for runner in self.m_runners:
            runner.stop()


