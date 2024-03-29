

buffsize = 2048


# def tcplink(sock, addr):
#     # print 'Accept new connection from %s:%s...' % addr
#     sock.send('Welcome!'.encode('utf-8'))
#     while True:
#         try:
#             # data = sock.recv(buffsize)
#             data = sock.recv(buffsize).decode()
#             time.sleep(1)
#             if data == 'exit' or not data:
#                 break
#             resend_msg = f'Hello, {data}'.encode('utf-8')
#             sock.send(resend_msg)
#         except Exception as e:
#             print(str(e))
#             break
#         sock.close()
#         print('Connection from %s:%s closed.' % addr)
#
#
# def tcp_server():
#     ...
#
#
# def udp_server():
#     server_ip = ("127.0.0.1", 8989)
#     s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s_socket.bind(server_ip)
#     while True:
#         # 只要没有别人发消息过来，就会阻塞住
#         # 都是一个一个的，每次只接受一个packet，而不是tcp那样整个流中截取
#         data, client_addr = s_socket.recvfrom(2048)
#         print('receive data is ', data, client_addr)
#         time.sleep(1)
#
#
# def main():
#     host = '127.0.0.1'
#     port = 12345
#     ADDR = (host, port)
#     tctime = socket(AF_INET, SOCK_STREAM)
#     tctime.bind(ADDR)
#     tctime.listen(3)
#
#     print('Wait for connection ...')
#     while True:
#         sock, add = tctime.accept()
#         print('Accept new connection from %s:%s...' % add)
#         t = threading.Thread(target=tcplink, args=(sock, add))
#         t.start()


def select_server():
    import gevent
    from gevent import select
    from gevent import socket

    m_session_dict = {}
    m_id = 1

    class Session(object):

        def __init__(self, connect):
            self.m_client = connect
            gevent.spawn(self.receive)

        def receive(self):
            while True:
                data = self.m_client.recv(0)
                print(data)
                gevent.sleep(0.01)

    def id_change():
        return m_id + 1

    # create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    # server.setsockopt()

    # Bind the socket to the port
    server_address = ('10.1.55.77', 12457)
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(1000)

    inputs = [server, ]
    outputs = []

    def start():
        while True:
            print(444)
            readable, writeable, exceptional = select.select(inputs, outputs, inputs)
            # print('select back', readable, writeable, exceptional)
            # print('input msg', inputs, outputs, len(inputs))
            for r in readable:
                if r is server:  # 代表来了一个新连接
                    conn, addr = server.accept()

                    #
                    # id_change()
                    gevent.sleep(0.1)
                    print("来了一个新连接", conn, addr)
                    m_session_dict[conn] = Session(conn)
                    inputs.append(conn)  # 是因为这个新建立的连接还没发数据过来，现在就接收的话程序就报错，
                    # 所以要想实现这个客户端发数据来时server端能知道就需要让select再检测这个conn
                else:
                    try:
                        m_session_dict[r].receive()

                    except Exception as e:
                        inputs.remove(r)
                        print('catch exception', e)

            # for send_msg in writeable:
            #     print('sssssssssend', send_msg)
            #
            # for e in exceptional:
            #     print('eeeeeeeeeeeeeeeeeeeee', e)
            gevent.sleep(0)
    from gevent import monkey
    monkey.patch_all(select=False, socket=False)
    gevent.spawn(start).join()


def async_io_server():
    import socket
    import asyncio
    import struct
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12457))
    server.setblocking(False)
    server.listen(5000)
    main_loop = asyncio.get_event_loop()

    class Num(object):
        session_num = 1

    class Session(object):
        def __init__(self, conn: socket.socket):
            self.m_client = conn
            self.m_running = True
            main_loop.create_task(self.start_receive())
            self.m_id = 1

        async def start_receive(self):
            try:
                if self.m_running:
                    head_info = await main_loop.sock_recv(self.m_client, 4)
                    if len(head_info) > 0:
                        body_info = await main_loop.sock_recv(self.m_client, struct.unpack(">i", head_info)[0])
                        self.on_receive(body_info)
                        self.m_id += 1
                        await self.start_receive()
                    else:
                        # 退出的时候发送个b""
                        print('正常退出')
                        self.close()
            except Exception as e:
                print(e, '??????????')
                self.close()

        def on_receive(self, body_info: bytes):
            # print(body_info, '????????', self.m_running)
            pass

        def on_connect(self):
            print('new user add', self.m_running, )

        def on_disconnect(self):
            print('user leave', self.m_running)

        def close(self):
            self.m_running = False
            self.on_disconnect()
            self.m_client.close()

    async def start():
        while True:
            conn, addr = await main_loop.sock_accept(server)
            session = Session(conn)
            Num.session_num += 1
            session.on_connect()

    async def print_numbers():
        await asyncio.sleep(10)
        print(Num.session_num)
        await print_numbers()

    asyncio.get_event_loop().create_task(start())
    asyncio.get_event_loop().create_task(print_numbers())
    asyncio.get_event_loop().run_forever()


def gevent_server():
    from gevent import socket
    import gevent
    from gevent.server import StreamServer
    import json

    class AsyncSession(object):
        def __init__(self, connect: socket.socket, session_id: int):
            self.m_client = connect
            self.m_id = session_id

        def start_receive(self):
            head_info = self.m_client.recv(1024)
            if head_info != b"":
                print(self.m_id, head_info)
                self.start_receive()
            else:
                return False
            return True

        def on_connect(self):
            print('connect', self.m_id)

        def on_disconnect(self):
            print("disconnect", self.m_id)

        def on_receive(self, info: bytes):
            pass

        def close(self):
            self.m_client.close()
            self.on_disconnect()

        def send_msg(self, send_data: dict):
            temp_data = json.dumps(send_data).encode('utf-8')
            self.m_client.send(temp_data)

        @property
        def id(self):
            return self.m_id

        def get_id(self):
            return self.m_id

    class AsyncServer(object):
        def __init__(self):
            self.m_id = 1
            self.m_server = None
            self.m_session_dict = {}

        def start_server(self, addr: tuple):
            self.m_server = StreamServer(addr, self.receive_handle, spawn=5000)
            gevent.spawn(self.print_sessions)
            # print('???  server start forever')
            self.m_server.serve_forever()

        def receive_handle(self, client_conn, address):
            session = self.m_session_dict.get(client_conn)
            try:
                if not session:
                    session = AsyncSession(client_conn, self.m_id)
                    session.on_connect()
                    self.session_id_change()
                    self.m_session_dict[client_conn] = session
                    result = session.start_receive()
                else:
                    result = self.m_session_dict[client_conn].start_receive()
                if not result:
                    # 退出的时候，会发送一个消息，receive的时候是b""，这时候表示退出
                    if session:
                        session.close()
                    del self.m_session_dict[client_conn]
            except Exception as e:
                if session:
                    session.close()
                del self.m_session_dict[client_conn]

        def session_id_change(self):
            # session id增加
            if self.m_id < 2133333:
                self.m_id += 1
            else:
                self.m_id = 1

        def print_sessions(self):
            while True:
                print(len(self.m_session_dict))
                gevent.sleep(2)

    AsyncServer().start_server(("127.0.0.1", 12457))


if __name__ == "__main__":
    gevent_server()

