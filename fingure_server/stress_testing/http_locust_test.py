from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    # Locust任务集，定义每个locust的行为"
    @task(1)  # 任务的权重为1，如果有多个任务，可以将权重值定义成不同的值，
    def get_root(self):
        # 模拟发送数据
        response = self.client.get('/Hello', name='get_root')
        if not response.ok:
            print(response.text)
            response.failure('Got wrong response')


class TestLocust(HttpLocust):
    """自定义Locust类，可以设置Locust的参数。"""
    task_set = UserBehavior
    host = "https://www.baidu.com"  # 被测服务器地址
    # 最小等待时间，即至少等待多少秒后Locust选择执行一个任务。
    min_wait = 5000

    # 最大等待时间，即至多等待多少秒后Locust选择执行一个任务。
    max_wait = 9000


@task(1)
def index1(self):
    r = self.client.get('/test/index.html')
    print(r.text)


@task(2)
def search1(self):
    r = self.client.get('/test/search.html')
    print(r.text)


if __name__ == '__main__':
    # cmd
    # locust - f locu.py --logfile = locustfile.log
    ...