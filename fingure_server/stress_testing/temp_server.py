import time
from socket import socket, AF_INET, SOCK_STREAM
import threading
import socket


buffsize = 2048


def tcplink(sock, addr):
    # print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!'.encode('utf-8'))
    while True:
        try:
            # data = sock.recv(buffsize)
            data = sock.recv(buffsize).decode()
            time.sleep(1)
            if data == 'exit' or not data:
                break
            resend_msg = f'Hello, {data}'.encode('utf-8')
            sock.send(resend_msg)
        except Exception as e:
            print(str(e))
            break
        sock.close()
        print('Connection from %s:%s closed.' % addr)


def tcp_server():
    ...


def udp_server():
    server_ip = ("127.0.0.1", 8989)
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_socket.bind(server_ip)
    while True:
        # 只要没有别人发消息过来，就会阻塞住
        # 都是一个一个的，每次只接受一个packet，而不是tcp那样整个流中截取
        data, client_addr = s_socket.recvfrom(2048)
        print('receive data is ', data, client_addr)
        time.sleep(1)


def main():
    host = '127.0.0.1'
    port = 12345
    ADDR = (host, port)
    tctime = socket(AF_INET, SOCK_STREAM)
    tctime.bind(ADDR)
    tctime.listen(3)

    print('Wait for connection ...')
    while True:
        sock, addr = tctime.accept()
        print('Accept new connection from %s:%s...' % addr)
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()


if __name__ == "__main__":
    udp_server()
