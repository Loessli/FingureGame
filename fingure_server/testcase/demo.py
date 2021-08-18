#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   garbage_test.py
@Time    :   2019/06/15 08:26:17
@Author  :   leal li
@Desc    :   None
'''


import json
import sys
import os


class Student(object):
    def __init__(self, name, age, score,reward):
        self.name = name
        self.age = age
        self.score = score
        self.reward = reward


def json_2str():
    data_json = {'name':'nick',
            'age':12}
    json_str = json.dumps(data_json)
    print(type(json_str), json_str)


def str_2json():
    json_str = '{"age": 12, "name": "nick"}'
    json_class = json.loads(json_str)
    print(type(json_class), json_class)


def class_2jsonStr():
    stu = Student('Bob', 20, 88, ["三好学生", "优秀团干","最佳辩手"])
    print(json.dumps(obj=stu.__dict__, ensure_ascii=False))


def jsonStr_2class():

    def dict2student(d):
        return Student(d['name'], d['age'], d['score'],d['reward'])

    json_str = '{"name": "Bob", "age": 20, "score": 88, "reward": ["三好学生", "优秀团干", "最佳辩手"]}'
    student = json.loads(json_str, object_hook=dict2student)
    print(type(student))
    print(student.__dict__)





sys.setrecursionlimit(100000)


file_list = []
file_path = "F:\\testResource\\Mxd"


def get_png_file(file_path):
    child_file = os.listdir(file_path)
    for c_file in child_file:
        new_file_dir = os.path.join(file_path, c_file)
        if new_file_dir.endswith('.png'):
            file_list.append(new_file_dir)
        if os.path.isdir(new_file_dir):
            get_png_file(new_file_dir)


def bubbleSort(arr):
    n = len(arr)

    # 遍历所有数组元素
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# arr = [64, 34, 25, 12, 22, 11, 90]
#
# bubbleSort(arr)
#
# print("排序后的数组:", arr)

if __name__ == "__main__":
    import sys

    print(sys.argv[1:])

    assert False
