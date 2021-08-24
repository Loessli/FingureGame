import asyncio
import functools


def async_method_locker(name: str, wait=True):
    assert isinstance(name, str)

    def decorating_function(method, loop=asyncio.get_event_loop()):
        global METHOD_LOCKERS
        locker = METHOD_LOCKERS.get(name)
        if not locker:
            locker = asyncio.Lock(loop=loop)
            METHOD_LOCKERS[name] = locker

        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            if not wait and locker.locked():
                return
            try:
                await locker.acquire()
                return await method(*args, **kwargs)
            finally:
                locker.release()
        return wrapper
    return decorating_function


if __name__ == '__main__':
    class Test(object):
        _pos_info_dict = {}
        @async_method_locker('get_pos_field_value')
        async def get_pos_field_value(self, instrument_id, field_name):
            return self._pos_info_dict[instrument_id][field_name]