import asyncio, time

flag = True


async def async_wait_func():
    print(1, time.time())
    await asyncio.sleep(1)
    print('async_wait_func over')
    if flag:
        await async_wait_func()


async def main_fun():
    print("2")
    await async_wait_func()
    print('main_fun over')


class NetRobot(object):

    _count = 0
    _heart_interval = 2
    _tasks = {}

    def __init__(self):
        ...

    def initialize(self):
        ...

    def tick(self):
        # xin tiao?
        self._count += 1
        # 设置下一次心跳回调
        asyncio.get_event_loop().call_later(self._heart_interval, self.tick)

        # 执行任务回调
        for task_id, task in self._tasks.items():
            interval = task["interval"]
            if self._count % interval != 0:
                continue
            func = task["func"]
            args = task["args"]
            kwargs = task["kwargs"]
            kwargs["task_id"] = task_id
            kwargs["heart_beat_count"] = self._count
            asyncio.get_event_loop().create_task(func(*args, **kwargs))



if __name__ == '__main__':
    asyncio.run(async_wait_func())
    print(3)