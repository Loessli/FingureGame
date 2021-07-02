import time


if __name__ == '__main__':
    user_list = list()
    for i in range(10):
        user_list.append(i ** 2)
    print(user_list)

    original_list = [1, 2, 3, 4, 5, 6, 7, 8]
    user_list = [x for x in original_list if x > 5]
    print(user_list)
    class A:
        a = 0

    temp_a = A()
    temp_a.a = 1

    print('start time', time.time())
    temp_a.a += 1
    print('end time', time.time())