class Hi:
    def __init__(self) -> None:
        self.name = "hi"

    def get_name(self, x):
        print(self.name, x)
        return 1, 2

    def get_bla(self, a, b):
        print(a, b)

    def get_gibberish(self):
        print("gibberish")


class Hello(Hi):
    def __init__(self) -> None:
        super().__init__()
        self.name2 = "hello"

    def get_name(self):
        print(self.name2)
        super().get_gibberish()
        return 1, 2, 3

    def get_bla(self, a, b, c):
        super().get_bla(a, b)
        print(a, b, c)


a = Hello()
a.get_bla(1, 2, 3)
