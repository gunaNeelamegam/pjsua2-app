class Pjsua2Exception(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.with_traceback(self.__traceback__)
