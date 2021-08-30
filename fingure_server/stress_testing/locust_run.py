import os
import time


LOCUST_FILE = "tcp_locust_test.py"  # "http_locust_test.py"  "tcp_locust_test.py"


class StressConfig(object):
    # 对应的locust python文件地址   同级目录下的tcp_locust_test文件
    py_file_path = os.path.dirname(__file__) + "\\" + LOCUST_FILE
    # 压测结果文件地址    放到同级目录test_report下面
    out_report_path = os.path.dirname(__file__) + "\\test_report\\" + str(time.strftime("%Y-%m-%d-%H-%M-%S",
                                                                           time.localtime(time.time())))
    # 指定并发用户数
    total_users = 5
    # 每秒启动用户数
    per_second_user = 1
    # 指定运行时间 单位s
    running_time = 100

    # 是否启动web模式
    is_web = False
    # web ip
    web_ip = "127.0.0.1"
    # web port
    web_port = 8089

    @staticmethod
    def path_init():
        report_path = os.path.dirname(__file__) + "\\test_report"
        if not os.path.isdir(report_path):
            os.mkdir(report_path)


def env_initialize():
    StressConfig.path_init()


def run_without_web():
    # csv --> csv path
    # --headless --> run without web
    # -u --> total user number
    # -r --> instance user per seconds
    # -t --> locust running time
    cmd = f"locust -f {StressConfig.py_file_path} --csv={StressConfig.out_report_path} --headless " \
        f"-u {StressConfig.total_users} -r {StressConfig.per_second_user} -t {StressConfig.running_time}"
    return cmd


def run_with_web():
    return f"locust -f {StressConfig.py_file_path} --web-host {StressConfig.web_ip} --web-port {StressConfig.web_port}"


if __name__ == '__main__':
    env_initialize()
    stress_cmd = run_with_web() if StressConfig.is_web else run_without_web()
    os.system(stress_cmd)