from stressing.users import User
from stressing.runner_manager import RunnerManager
import asyncio
import time
import struct
import json
from asyncio import Task


_env_example: dict = {
    "user_count": None,
    "user_class": User,
    "run_time": None,
    "host": "127.0.0.1",
    "port": 12457
}


class TempUser(User):
    m_hear_beat_task: Task = None

    def __init__(self, _event_loop, user_id,  host, port):
        super().__init__(_event_loop, user_id, host, port)

    def __del__(self):
        del self.m_hear_beat_task

    async def start(self):
        login_msg = {
            'type': 0,
            'data': {
                'username': 'lealli' + str(self.m_user_id),
                'password': 'z1314123',
                "room_id": 0,
                "play_state": 0,
                "play_order": 0,
                "leave_room": False
            }
        }
        await self.send(self.encode(login_msg))
        login_data = await self.receive()
        print(self.m_user_id, 'login result', login_data)
        await self.heart_beat()

    async def heart_beat(self):
        await asyncio.sleep(5)
        send_msg = {
            'type': 2,
            'data': {
                'c_time': time.time(),
                's_time': time.time()
            }
        }
        await self.send(self.encode(send_msg))
        receive = await self.receive()
        print(self.m_user_id, 'heart msg', receive)
        await self.heart_beat()

    def encode(self, data: dict) -> bytes:
        byte_data = json.dumps(data).encode('utf-8')
        return struct.pack('>i', len(byte_data)) + byte_data

    def decode(self, data: bytes):
        return json.loads(data.decode('utf-8'))

    async def receive(self, buff_size: int = 1024) -> bytes:
        try:
            head_data = await self.runner_loop.sock_recv(self.m_client, 4)
            if len(head_data) > 0:
                head_len = struct.unpack('>i', head_data)[0]
                data = await self.runner_loop.sock_recv(self.m_client, head_len)
                # data = self.m_reader.reader(buff_size)
                # TODO receive success
                return self.decode(data)
        except Exception as exp:
            print('receive msg error', exp)


if __name__ == '__main__':
    env = {
        "user_count": 10,
        "user_class": TempUser,
        "run_time": 10,
        "host": "10.1.55.77",
        "port": "12457"
    }

    runner_mgr = RunnerManager(env)
    runner_mgr.start()