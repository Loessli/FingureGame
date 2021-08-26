from lib.decorator_mode import *
from lib.log_info import log
from .cache_service import CacheService


@singleton
class LoginService(object):
    m_cache = None

    def init(self):
        log(0, 'LoginService启动!')
        self.m_cache = CacheService()

    def login_handle(self, msg_pkt):
        # 登陆消息处理
        session_id = msg_pkt[0]
        login_data = msg_pkt[1].get('data')
        username = login_data.get("username")
        log(0, f"{username}登陆请求{login_data}")
        password = login_data.get("password")
        cache_user_data = self.m_cache.get_user_cache(username)

        if not cache_user_data:  # 新账号
            log(0, f"{username}注册成功，准备登陆")
            user_data = {"username": username, "password": password}
            self.m_cache.add_online_user_cache_by_id(session_id, cache_user_data)
            self.m_cache.add_user_cache(user_data)
            self.login_response(True, session_id, "account register success, login successful", username)
        else:  # 老帐号
            if password == cache_user_data.get("password"):  # 密码正确
                session = self.m_cache.get_session_by_username(username)
                if session:
                    if session.id == session_id:
                        if cache_user_data["username"] == username:
                            # 同一账号登陆两次
                            self.login_response(False, session_id, "already login", username)
                            return
                        else:
                            # 同一台机器，前后登陆两个不同的账号
                            self.m_cache.remove_online_user_cache(session)
                    else:
                        self.m_cache.remove_online_user_cache(session)
                        session.close()  # A先B后，B踢掉A，A close
                self.login_response(True, session_id, username=username)  # 账号登陆成功
                self.m_cache.add_online_user_cache_by_id(session_id, cache_user_data)
            else:  # 密码错误
                self.login_response(False, session_id, "password error!", username)

    def login_response(self, success: bool, session_id, error_msg="", username=""):
        # 登陆消息返回
        send_data ={
            "type": 0,
            "data": {
                "login_result": success,
                "error_msg": error_msg
            }
        }
        log(0, f"user {username} login {'success' if success else 'failed'}")
        self.m_cache.get_session_by_session_id(session_id).send_msg(send_data)
