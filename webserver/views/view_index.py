from django.http import HttpResponse
from django.shortcuts import render, redirect
from lib.log_info import *


class Index(object):
    @staticmethod
    def index_handle(request):
        # path --> /index/
        log(0, request)
        context = {}
        context['hello'] = 'Hello World!'
        return render(request, 'index.html', context)