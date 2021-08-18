import socket, struct
import json
import queue


class ClientTcp(object):
    def __init__(self):
        self._address = ("127.0.0.1", 12346)
        self.m_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_client.connect(self._address)
        self.m_head_len = 4
        self.m_data_queue = queue.Queue()

    @staticmethod
    def pack(data: bytes):
        return struct.pack(">i", len(data)) + data

    @staticmethod
    def unpack(data: bytes):
        return struct.unpack(">i", data)[0]

    def receive(self):
        head_data = self.m_client.recv(self.m_head_len)
        if head_data == b"":
            return
        body_data = self.m_client.recv(ClientTcp.unpack(head_data))
        self.m_data_queue.put(json.loads(body_data))
        self.receive()

    def send(self, data: dict):
        data = json.dumps(data).encode('utf-8')
        self.m_client.send(ClientTcp.pack(data))

    def get_received_data(self):
        if self.m_data_queue.qsize() == 0:
            return
        return self.m_data_queue
