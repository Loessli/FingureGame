import gevent, os
from gevent.pool import Group
from gevent import monkey
import asyncio
import time


monkey.patch_all()


# demo for gevent and asyncio

def main_loop():
    while True:
        print('main_loop')
        gevent.sleep(0.2)


def temp_test_loop():
    # while True:
    print('temp_test_loop')
    gevent.sleep(0.1)
        # gevent.sleep(0.3)


def gevent_test():
    green_let = Group()
    green_let_1 = Group()
    green_let.spawn(main_loop)
    # green_let.join()

    green_let_1.spawn(temp_test_loop)
    # must join
    # green_let_1.join()
    gevent.spawn(temp_test_loop).run()


async def async_main_loop():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')


def asyncio_test():
    asyncio.run(async_main_loop())


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


if __name__ == '__main__':
    temp_socket_client()