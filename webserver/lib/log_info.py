import time
import enum


class _log_lv(enum.IntEnum):
    INFO = 0,
    WARNING = 1,
    ERROR = 2


def log(lv: int, *args):
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    if lv == _log_lv.INFO:
        print(current_time, "[INFO]", *args)
    elif lv == _log_lv.WARNING:
        print(current_time, "[WARNING]", *args)
    elif lv == _log_lv.ERROR:
        print(current_time, "[ERROR]", *args)
    else:
        log(_log_lv.ERROR, "日志等级参数填写错误")