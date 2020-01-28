class OtcBaseException(Exception):
    pass


class OtcTypeError(OtcBaseException):
    pass


class OtcOutdatedError(OtcBaseException):
    pass

class OtcNoneError(OtcBaseException):
    pass

class OtcInsertionError(OtcBaseException):
    pass
