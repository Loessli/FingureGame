from lib.log_info import log
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
    '''
    # 初始化
    def init(self):
        log(0, "CacheService启动")
        self.m_db_svc = MysqlDBService()

    # 添加玩家线上数据缓存
    def add_online_user_cache(self, session, data):
        # log(0, f"当前添加的cache为{data}")
        self.online_user_data_cache.update({session: data})

    def get_online_user_cache(self, session):
        if self.online_user_data_cache.get(session) != None:
            return self.online_user_data_cache.get(session)

    def remove_online_user_cache(self, session):
        self.online_user_data_cache.pop(session)
        self.remove_user_cache(self.online_user_data_cache[session].get("username"))

    def add_user_cache(self, userdata: dict):
        self.user_data_cache.update({userdata.get('username'): userdata})
        if not self.get_user_cache(userdata.get('username')):
            self.m_db_svc.insert_userdata(userdata)

    def get_user_cache(self, username: str):
        # 从
        user_data = self.m_db_svc.get_userdata(username)
        if user_data:
            self.user_data_cache.update({user_data.get("username"): user_data})
            return user_data
        else:
            # 如果数据库没有数据
            return

    def remove_user_cache(self,username: str):
        # 移除user data的缓存数据'''
        log(0, f"{username} remove and cache delete!")
        self.user_data_cache.pop(username)

    def update(self):
        # tick每隔3min自动存一次数据'''
        self.end_time = time.time()
        if self.end_time - self.temp_time > 180:
            log(0, "3min已到,存储一次数据")
            for key in list(self.user_data_cache.keys()):
                userdata = self.user_data_cache.get(key)
                self.m_db_svc.update_userdata(userdata)
            self.temp_time = self.end_time