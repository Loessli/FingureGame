from stressing.users import User
from stressing.runner_manager import RunnerManager
import asyncio
import time

_env_example: dict = {
    "user_count": None,
    "user_class": User,
    "run_time": None,
    "host": "127.0.0.1",
    "port": 12457
}


class TempUser(User):

    def __init__(self, _event_loop, host, port):
        super().__init__(_event_loop, host, port)

    async def start(self):
        await self.send(b"?????????fuck")
        await self.heart_beat()

    async def heart_beat(self):
        await asyncio.sleep(5)
        send_msg = (str(id(self)) + str(time.time())).encode('utf-8')
        await self.send(send_msg)
        await self.heart_beat()


if __name__ == '__main__':
    env = {
        "user_count": 100,
        "user_class": TempUser,
        "run_time": 30,
        "host": "127.0.0.1",
        "port": "12457"
    }
    runner_mgr = RunnerManager(env)
    runner_mgr.start()