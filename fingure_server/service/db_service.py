from lib.log_info import log
from lib.decorator_mode import *
from game_play.mysql_operate import MysqlHandle


@singleton
class MysqlDBService(object):
    m_mysql_conn = None

    def init(self):
        log(0, 'Mysql Service启动！')
        self.m_mysql_conn = MysqlHandle()

    def init_mysql(self):
        # 当数据库整个都是空的的时候，想通过这个函数来初始化创建数据库的所有表格
        ...

    def get_userdata(self, username: str):
        # 通过username获取数据库中user的信息
        username = self.get_real_key(username)
        msg = self.m_mysql_conn.query(f"select * from account where username={username} ;")
        if len(msg) == 0:
            return
        tem_msg = msg[0]
        data_result = {  # tem_msg 第一个值为id
            "username": tem_msg[1],
            "password": tem_msg[2],
            "win": tem_msg[3],
            "lose": tem_msg[4]
        }
        # log(0, f"从数据库中拉出来数据为{data_result}")
        return data_result

    def update_userdata(self, userdata: dict):
        # 更新数据库中user的信息
        username = self.get_real_key(userdata["username"])
        password = self.get_real_key(userdata["password"])
        temp_update_sql = "update account set password={a},win={b},lose={c} where username ={d}".\
            format(a=password, b=userdata["win"], c=userdata["lose"], d=username)
        self.m_mysql_conn.mutation(temp_update_sql)

    def insert_userdata(self, userdata: dict):
        # 插入新的user的信息
        username = self.get_real_key(userdata["username"])
        password = self.get_real_key(userdata["password"])
        temp_insert_sql = "insert into account (username,password,win,lose) values({username},{password},0,0)".\
            format(username=username, password=password)
        self.m_mysql_conn.mutation(temp_insert_sql)

    def get_real_key(self, key: str):
        # sql语句里面的key也需要引号， 所以包一层
        return "\"" + key + "\""