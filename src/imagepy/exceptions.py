class FileNotFoundException(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WrongArgumentType(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)