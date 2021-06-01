from service.root_service import ServerRoot
from lib.config import Config
import time

if __name__ == '__main__':
    '''启动入口'''
    root = ServerRoot()
    root.init()  # 初始化
    while True:
        root.updata()  # 总update函数
        time.sleep(Config.tick_frame)