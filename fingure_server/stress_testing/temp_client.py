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
    tcp_client()