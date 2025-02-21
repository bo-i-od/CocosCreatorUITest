class BaseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidOperationError(BaseError):
    """
        超范围，会报错
    """
    pass