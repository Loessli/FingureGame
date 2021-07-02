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
    total_users = 20
    # 每秒启动用户数
    per_second_user = 20
    # 指定运行时间 单位s
    running_time = 300

    @staticmethod
    def path_init():
        report_path = os.path.dirname(__file__) + "\\test_report"
        if not os.path.isdir(report_path):
            os.mkdir(report_path)


if __name__ == '__main__':
    # D:/test/test
    '''
    使用命令：locust -f E:/PyProject/locust-test/tcp_locust_test.py --csv=test --no-web -c10 -r10 -t2，
    如以下图显示为请求发送成功，并生成了以test开头的测试报告
    命令解释：
    --no-web 
    无web界面模式运行测试，需要-c和-r配合使用
    -c
    指定并发用户数，no-web模式下可用
    -r  
    指定每秒启动的用户数，no-web模式下可用
    -t
    指定运行的时间，no-web模式下可用，0.8.1版本不再提供t参数来指定运行时间，用-n来指定运行次数
    '''
    StressConfig.path_init()
    stress_cmd = f"locust -f {StressConfig.py_file_path} --csv={StressConfig.out_report_path} --no-web " \
        f"-c{StressConfig.total_users} -r{StressConfig.per_second_user} -t{StressConfig.running_time}"
    os.system(stress_cmd)