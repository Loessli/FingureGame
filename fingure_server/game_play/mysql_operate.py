import pymysql
from lib.log_info import log
from lib.config import Config


class MysqlHandle(object):
    connect = None

    def __init__(self):
        self.init_connect()

    def init(self, host: str, port: int, user: str, password: str, db, charset):
        self.connect = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)

    def init_connect(self):
        # 初始化链接
        try:
            self.connect = pymysql.connect(host=Config.db_host, port=Config.db_port,
                                            user=Config.db_user, db=Config.db_db,
                                            password=Config.db_password, charset=Config.db_charset)
        except Exception as excp:
            log(2, '数据库链接失败！', excp)

    def query(self, sql: str):
        # 查
        cur = self.connect.cursor()
        cur.execute(sql)
        query_result = cur.fetchall()
        cur.close()
        return query_result

    def mutation(self, sql: str):
        # 改
        cur = self.connect.cursor()
        try:
            cur.execute(sql)
            self.connect.commit()
        except Exception as e:
            log(2, f"mysql mutation failed, 准备回滚", e)
            self.connect.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    obj_sql = MysqlHandle()
    result = obj_sql.query("select * from account where username=\"aaa\"")
    print(result, type(result), result.__class__)
    # obj_sql.mutation("update account set win=10,lose=3 where username =\"leal\"")
    # obj_sql.mutation("insert into account (username,password,win,lose) values(\"ppp\",\"ppp\",3,3)")