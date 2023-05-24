
class Pjsua2AccountException(Exception):
    pass
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.with_traceback(self.__traceback__.tb_lineno)

