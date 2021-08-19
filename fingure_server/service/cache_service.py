from lib.log_info import log
# from lib.network import AsyncSession
from service.db_service import MysqlDBService
from lib.decorator_mode import *
import time


@singleton
class CacheService(object):
    temp_time = time.time()
    end_time = None
    m_db_svc = None
    # 玩家数据缓存 主要和数据库对应
    user_data_cache = {}
    '''
    {
        "username" : { 
            "username":"",
            "password":"",
            "win": 0,
            "lose": 0
        }
    }
    '''
    # 玩家线上数据缓存
    online_user_data_cache = {}
    '''
    {
        Session : {
            "room_id":"",
            "username": ""
        }
    }
    {
        session_id: {
            "session" : Session,
            "data": {
                "room_id": "",
                "username": ""
            }
        }
    }
    '''
    # 初始化
    def init(self):
        log(0, "CacheService启动")
        self.m_db_svc = MysqlDBService()

    def send_msg_by_session_id(self, session_id, send_data: dict):
        self.get_session_by_session_id(session_id).send_msg(send_data)

    def add_online_user_cache(self, session):
        # 添加线上玩家的数据缓存
        log(0, f"当前添加的cache为{session}, id为 {session.get_id()}")
        temp_data = {'session': session, 'data': {}}
        self.online_user_data_cache.update({session.get_id(): temp_data})

    def add_online_user_cache_by_id(self, session_id, data):
        # 通过session_id添加数据
        if self.online_user_data_cache.get(session_id):
            self.online_user_data_cache.get(session_id).update({'data': data})

    def get_online_user_cache(self, session):
        # 获取线上玩家的缓存数据
        session_id = session.get_id()
        if session_id in self.online_user_data_cache.keys():
            return self.online_user_data_cache.get(session_id)['data']

    def remove_online_user_cache(self, session):
        # 移除线上玩家的缓存数据
        session_id = session.get_id()
        if session_id in self.online_user_data_cache.keys():
            self.remove_user_cache(self.online_user_data_cache[session_id].get("username"))
            self.online_user_data_cache.pop(session_id)

    def get_session_by_username(self, username: str):
        # 通过username获取online的session，如果不存在，则返回None
        for session_id in list(self.online_user_data_cache.keys()):
            if self.online_user_data_cache.get(session_id).get('data').get('username') == username:
                return self.online_user_data_cache.get(session_id).get("session")

    def get_session_by_session_id(self, session_id):
        # 通过session id获取session
        return self.online_user_data_cache.get(session_id).get('session')

    def add_user_cache(self, userdata: dict):
        # 添加玩家数据缓存，如果数据库中不存在，写入到数据库中
        self.user_data_cache.update({userdata.get('username'): userdata})
        if not self.get_user_cache(userdata.get('username')):
            self.m_db_svc.insert_userdata(userdata)

    def get_user_cache(self, username: str):
        # 通过username获取userdata，如果cache中不存在，就从数据库拉取
        userdata = self.user_data_cache.get('username')
        if userdata:
            return userdata
        else:  # 如果user_data_cache里面不存在，那就从数据库里面读取了
            user_data = self.m_db_svc.get_userdata(username)
            if user_data:
                # 添加到user_data_cache缓存
                self.user_data_cache.update({user_data.get("username"): user_data})
                return user_data
            else:
                # 如果数据库没有数据
                log(0, f"当前数据库没有该玩家{username}的数据")
                return None

    def remove_user_cache(self, username: str):
        if not username:
            return
        temp_data = self.user_data_cache[username]
        if temp_data:
            # 移除user data的缓存数据'''
            log(0, f"{username} remove and cache delete!")
            self.user_data_cache.pop(username)
        else:
            log(1, f"{username} 玩家数据缓存不存在")
        # if username in list(self.user_data_cache.keys()):
        #     # 移除user data的缓存数据'''
        #     log(0, f"{username} remove and cache delete!")
        #     self.user_data_cache.pop(username)
        # else:
        #     log(1, f"{username} 玩家数据缓存不存在")

    def update(self):
        # tick每隔3min自动存一次数据'''
        current_time = time.time()
        if current_time - self.temp_time > 180:
            log(0, "3min已到,存储一次数据")
            for key in list(self.user_data_cache.keys()):
                userdata = self.user_data_cache.get(key)
                self.m_db_svc.update_userdata(userdata)
            self.temp_time = current_time