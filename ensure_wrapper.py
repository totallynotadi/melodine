class Test:
    def __init__(self):
        self.dat = {1: "one", 2: "two"}

    def ensure_data(func):
        def inner(self, index):
            print(f"self - {self}", end=" :: ")
            print(f"argument - {index}")
            try:
                # func is `ensure_test()` i.e. the caller
                # return from the inner func, whatever the func returns
                return func(self, index)
            except KeyError:
                # func(self, index)
                return self.dat[2]

        return inner

    @ensure_data
    def ensure_test(self, index):
        print(f"element at index {index} in dat '{self.dat[index]}'")
        return self.dat[index]


if __name__ == "__main__":
    t = Test()
    r = t.ensure_test(1)
    print(r)
