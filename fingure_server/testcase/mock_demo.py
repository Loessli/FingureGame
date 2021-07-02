import unittest
from unittest import mock
import os


def multiple(a, b):
    return a*b


class Calculator(object):
    def add(self, a, b):
        return a+b

    def is_error(self):
        try:
            os.mkdir("11")
            return False
        except Exception as e:
            return True


class TestProducer2(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    # 1. Mock一个函数。
    # 其实有好几种方法，个人比较推荐下面这种，看上去很清晰：
    @mock.patch(__name__ + '.multiple')  # 看起来如果不是类函数，需要添加对应的file name。确定域？
    def test_multiple(self, mock_multiple):
        mock_multiple.return_value = 3
        print(multiple(4, 20), __name__)
        self.assertEqual(multiple(8, 14), 3)

    # 2. Mock一个对象里面的方法
    @mock.patch.object(Calculator, 'add')
    def test_add(self, mock_add):
        mock_add.return_value = 3
        self.assertEqual(self.calculator.add(8, 14), 3)

    # 3. Mock的函数每次被调用返回不同的值
    @mock.patch.object(Calculator, 'add')
    def test_effect(self, mock_add):
        mock_add.side_effect = [1, 2, 3]
        self.assertEqual(self.calculator.add(8, 14), 1)
        self.assertEqual(self.calculator.add(8, 14), 2)
        self.assertEqual(self.calculator.add(8, 14), 3)

    # 4. 让Mock的函数抛出exception
    @mock.patch('os.mkdir')
    def test_exception(self, mock_mkdir):
        mock_mkdir.side_effect = Exception
        self.assertEqual(self.calculator.is_error(), True)

    # 5. Mock多个函数，主要是注意顺序
    @mock.patch.object(Calculator, 'add')
    # @mock.patch('test_unit.multiple')
    @mock.patch(__name__ + '.multiple')
    def test_both(self, mock_multiple, mock_add):
        mock_add.return_value = 1
        mock_multiple.return_value = 2
        self.assertEqual(self.calculator.add(8, 14), 1)
        self.assertEqual(multiple(8, 14), 2)


if __name__ == '__main__':
    unittest.main()