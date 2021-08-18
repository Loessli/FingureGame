import threading


class SingleType(type):
    """单例元类"""
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingleType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingleType, cls).__call__(*args, **kwargs)
        return cls._instance


def singleton(cls, *args, **kw):
    """单例"""
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton
