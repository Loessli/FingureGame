from enum import IntEnum


class Config(object):
    server_ip = "192.168.1.3"
    server_port = 12456
    tick_frame = 0.032    # 30帧
    max_players = 12  # 同时在线player数量

    # 数据库登陆设置
    db_host = "localhost"
    db_port = 3306
    db_user = "root"
    db_password = ""
    db_db = "figuregame"
    db_charset = "utf8"


class MsgType(IntEnum):
    login = 0
    game_room = 1
    heart_beat = 2


protocol_msg = {
    "type": 1,  # 功能名称
    "data": {
        "username": "",  # 玩家name
        "password": "",  # 玩家密码
        "room_id": "",  # 猜拳房间的id
        "play_state": 0,  # 玩家状态
        "play_order": 0,  # 玩家猜拳指令
        "play_result": 0,  # 猜拳结果
        "leave_room": False,
        'c_time': 1,
        's_time': 2
    }
}

if __name__ == '__main__':
    import socket
    # 获取计算机名称
    hostname = socket.gethostname()
    # 获取本机IP
    ip = socket.gethostbyname(hostname)
    print(ip)
