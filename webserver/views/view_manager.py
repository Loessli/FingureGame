from django.http import HttpResponse
from django.shortcuts import render, redirect
from lib.log_info import *
from .view_index import Index


# region HttpRequest
'''
https://www.runoob.com/django/django-views.html
HttpRequest对象包含当前请求URL的一些信息：
path: 请求页面的全路径,不包括域名—例如, "/hello/"
method: 请求中使用的HTTP方法的字符串表示。全大写表示。例如:
        if request.method == 'GET':
            do_something()
        elif request.method == 'POST':
            do_something_else()
GET: 数据类型是 QueryDict，一个类似于字典的对象，包含 HTTP GET 的所有参数
POST: 
COOKIES: 包含所有cookies的标准Python字典对象。Keys和values都是字符串。
FILES: 	
        包含所有上传文件的类字典对象。FILES中的每个Key都是<input type="file" name="" />标签中name属性的值.
         FILES中的每个value 同时也是一个标准Python字典对象，包含下面三个Keys:
        filename: 上传文件名,用Python字符串表示
        content-type: 上传文件的Content type
        content: 上传文件的原始内容
        注意：只有在请求方法是POST，并且请求页面中<form>有enctype="multipart/form-data"
        属性时FILES才拥有数据。否则，FILES 是一个空字典。
META:
        包含所有可用HTTP头部信息的字典。 例如:
        CONTENT_LENGTH
        CONTENT_TYPE
        QUERY_STRING: 未解析的原始查询字符串
        REMOTE_ADDR: 客户端IP地址
        REMOTE_HOST: 客户端主机名
        SERVER_NAME: 服务器主机名
        SERVER_PORT: 服务器端口
body: 数据类型是二进制字节流，是原生请求体里的参数内容，在 HTTP 中用于 POST，因为 GET 没有请求体。
        在 HTTP 中不常用，而在处理非 HTTP 形式的报文时非常有用，例如：二进制图片、XML、Json 等
'''
# endregion


# region HttpResponse
'''
HttpResponse(): 返回文本，参数为字符串，字符串中写文本内容。如果参数为字符串里含有 html 标签，也可以渲染。
render(): 返回文本，第一个参数为 request，第二个参数为字符串（页面名称），
        第三个参数为字典（可选参数，向页面传递的参数：键为页面参数名，值为views参数名）
redirect()：重定向，跳转新页面。参数为字符串，字符串中填写页面路径。一般用于 form 表单提交后，跳转到新页面。
'''
# endregion


# 当向对应的url+path发送request的时候，反馈到这里进行处理
# 对应的path的配置在webserver/urls.py urlpatterns参数
class ViewManage(object):

    @staticmethod
    def index_handle(request):
        return Index.index_handle(request)

    @staticmethod
    def search_handle(request):
        log(0, "get search message!", request.body, request.method)
        if request.method == "POST":
            return HttpResponse("search???!~~")

    @staticmethod
    def default_handle(request):
        # return HttpResponse("朱琪是sb")
        return redirect('index/')  # 转到path  index/

    @staticmethod
    def hello_handle(request):
        # path --> /hello/
        context = {}
        context.update({'hello': "Hello World!~"})
        return render(request, 'test\\runoob.html', context)