class Test1:
    call = None

    def __init__(self) -> None:
        self.call = "Hii Guna is Working"
        # Test1.call = self.call


c = Test1()
print(c.call)
print(Test1.call)
