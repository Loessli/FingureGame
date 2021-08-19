import socket, struct
import json
import queue


class ClientTcp(object):
    def __init__(self):
        self._address = ("10.1.55.77", 12456)
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

    def stop(self):
        self.m_client.close()


class User(object):

    def __init__(self):
        self.m_client = ClientTcp()

    def login(self, account_id: int):
        login_msg = {

        }
        self.m_client.send(login_msg)

    def tick(self):
        ...


if __name__ == '__main__':
    import time
    login_msg={
        "type": 0,
        "data": {
            "username": "123",
            "password": "123456",
            "room_id": 0,
            "play_state": 0,
            "play_order": 0,
            "leave_room": False
        }
    }


    client = ClientTcp()
    client.send(login_msg)
    # client.receive()
    time.sleep(2)
