import socket


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
        # await self.send(b"?????????fuck")
        # await self.heart_beat()
        pass

    async def run(self):
        try:
            await self.runner_loop.sock_connect(self.m_client, self.address)
            # self.m_reader, self.m_writer = await asyncio.open_connection(
            #     host=self.host, port=self.port, loop=self.runner_loop)
        except Exception as e:
            print('connect error', e)
        else:
            await self.start()

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