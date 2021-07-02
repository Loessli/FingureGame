import os
from lib.config import Config


# https://blog.csdn.net/aixiangnan/article/details/90270430
# Django 采用了 MVT 的软件设计模式，即模型（Model），视图（View）和模板（Template）。

'''
webserver: 项目的容器。
    lib: 公用库/自定义目录
    templates: 模板（Template）html目录
    views: 视图（View） 对应path接收到消息以后的处理逻辑
    webapp: 通过django-admin startapp创建的目录
            暂时没看到这里，不用管
    webserver/__init__.py: 一个空文件，告诉 Python 该目录是一个 Python 包。
              ### asgi.py: 一个 ASGI 兼容的 Web 服务器的入口，以便运行你的项目。
              settings.py: 该 Django 项目的设置/配置。
              urls.py: 该 Django 项目的 URL 声明; 一份由 Django 驱动的网站"目录"。
              wsgi.py: 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。
    manage.py: 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。
    run.py: django启动文件
'''


# 没有app这种说法的启动
def get_cmd():
    port = str(Config.port)
    return f"python manage.py runserver {Config.ip}:{port}"


# Django 规定，如果要使用模型，必须要创建一个 app。我们使用以下命令创建一个 TestModel 的 app:
# cmd: django-admin startapp webapp(app name?)


if __name__ == '__main__':
    cmd = get_cmd()
    os.system(cmd)