import socket


def tcp_client():
    server_ip = ('127.0.0.1', 8989)
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "hello pi.!".encode('utf-8')
    c_socket.sendto(data, server_ip)
    c_socket.sendto(data, server_ip)


def udp_client():
    ...


if __name__ == '__main__':
    import socket

    HOST = '10.1.55.77'
    PORT = 12456
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(s.recv(1024))
    while True:
        msg = bytes(input(">>:").strip(), encoding="utf-8")
        if msg == 'q'.encode("utf-8"):
            exit("退出！")
        s.send(msg)
        # data = s.recv(1024)
        # print('Received', data.decode())
    # s.close()