import asyncio
import time


def temp_socket_client():
    import socket

    HOST = '10.1.55.77'
    PORT = 12456
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        msg = bytes(input(">>:").strip(), encoding="utf-8")
        if msg == 'q'.encode("utf-8"):
            exit("退出！")
        s.send(msg)
        # data = s.recv(1024)
        # print('Received', data.decode())
    # s.close()


def get_get_get():
    class Temp():
        flag = True
    temp = Temp()

    async def async_main_loop():
        while temp.flag:
            print('Hello ...')
            # print(asyncio.Task.all_tasks())
            await asyncio.sleep(1)
            # print('... World!')

    async def tick_for_heart():
        start_time = time.time()
        while True:
            print('heart beat', time.time())
            if time.time() - start_time > 2:
                print(asyncio.get_running_loop().is_closed())
                temp.flag = False
            await asyncio.sleep(2)

    asyncio.get_event_loop().create_task(tick_for_heart())

    def asyncio_test():
        asyncio.get_event_loop().create_task(async_main_loop())
        asyncio.get_event_loop().run_forever()

    asyncio_test()


def processing1():
    while True:
        print('111111', time.time())


def processing2():
    while True:
        print('222222', time.time())


class A(object):
    def __init__(self, num: int):
        self.num = num


class B(object):
    a: A = None

    def __init__(self, _a):
        self.a_class = _a

    def start(self):
        self.a = self.a_class(10)


if __name__ == '__main__':
    ...
