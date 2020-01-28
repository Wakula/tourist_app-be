from .otc_exceptions import OtcNoneError, OtcInsertionError
import redis

class BaseOtc:
    def __init__(self, otc_type):
        self._otc_type = otc_type
        self._code = None

    def get_otc(self):
        if self._code:
            return self._code
        raise OtcNoneError

    def get_otc_type(self):
        return self._otc_type

    def add_otc_to_redis(self):
        if not self._code:
            raise OtcNoneError
        with redis.Redis() as redis_client:
            res = redis_client.set(self._code, self._otc_type)
            if res == False:
                raise OtcInsertionError("redis insertion failed")

    def create_otc(self):
        raise NotImplementedError
