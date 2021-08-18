import time
from socket import socket, AF_INET, SOCK_STREAM
import threading
import socket
import gevent


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
        sock, add = tctime.accept()
        print('Accept new connection from %s:%s...' % add)
        t = threading.Thread(target=tcplink, args=(sock, add))
        t.start()


if __name__ == "__main__":
    import select
    import socket
    import sys
    import queue
    import os

    m_session_dict = {}
    m_id = 1

    class Session(object):

        def __init__(self, connect: socket.socket):
            self.m_client = connect

        def receive(self, buff_size: int = 1024):
            data = self.m_client.recv(buff_size)
            print(data)
            return data

    def id_change():
        return m_id+1

    # create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(1000)

    inputs = [server, ]
    outputs = []

    def start():
        while True:
            readable, writeable, exceptional = select.select(inputs, outputs, inputs)
            # print('select back', readable, writeable, exceptional)
            # print('input msg', inputs, outputs, len(inputs))
            for r in readable:
                if r is server:  # 代表来了一个新连接
                    conn, addr = server.accept()
                    print("来了一个新连接", conn, addr)
                    m_session_dict[conn] = Session(conn)
                    id_change()
                    inputs.append(conn)  # 是因为这个新建立的连接还没发数据过来，现在就接收的话程序就报错，
                    # 所以要想实现这个客户端发数据来时server端能知道就需要让select再检测这个conn
                else:
                    try:
                        session = m_session_dict.get(r)
                        data = session.receive()
                        # data = r.recv(1024)
                        # print("收到的数据：", data.decode())
                        r.send(data)
                        # print("send done....")
                    except Exception as e:
                        inputs.remove(r)
                        print('catch exception', e)

            for send_msg in writeable:
                print('sssssssssend', send_msg)

            for e in exceptional:
                print('eeeeeeeeeeeeeeeeeeeee', e)
            gevent.sleep(0)
    gevent.spawn(start).join()
