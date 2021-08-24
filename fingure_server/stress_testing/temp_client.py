import socket


def tcp_client():
    server_ip = ('127.0.0.1', 8989)
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "hello pi.!".encode('utf-8')
    c_socket.sendto(data, server_ip)
    c_socket.sendto(data, server_ip)


def udp_client():
    ...


def temp_client():
    import socket

    HOST = '127.0.0.1'
    PORT = 12457
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    # print(s.recv(1024))
    while True:
        msg = bytes(input(">>:").strip(), encoding="utf-8")
        if msg == 'q'.encode("utf-8"):
            exit("退出！")
        s.send(msg)
        # data = s.recv(1024)
        # print('Received', data.decode())
    # s.close()


if __name__ == '__main__':
    import asyncio
    async def client():
        reader, writer = await asyncio.open_connection(host="127.0.0.1", port=12457)
