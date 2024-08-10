class Test:
    def __init__(self):
        self.dat = {1: "one", 2: "two"}

    def ensure_data(func):
        # print("test", test)
        def inner(self, index):
            print(f"self - {self}; self.dat - {self.dat}", end=" :: ")
            print(f"argument - {index}")
            try:
                # func is `ensure_test()` i.e. the caller
                # return from the inner func, whatever the func returns
                return func(self, index)
            except KeyError:
                # func(self, index)
                return self.dat[2]

        return inner

    def _ensure_data(*decoargs, **decokwargs):
        def _ensure_internal(func):
            def internal_wrapper(self, index, **kwargs):
                print(f"decorater args: {decoargs}, decorator kwargs: {decokwargs}")
                print(f"wrapped function: {func}")
                print(f"wrapper args: {self, index}, wrapper kwargs: {kwargs}")
                try:
                    # func is `ensure_test()` i.e. the caller
                    # return from the inner func, whatever the func returns
                    return func(self, index)
                except KeyError:
                    # func(self, index)
                    return self.dat[2]

            return internal_wrapper

        return _ensure_internal

    @_ensure_data(test=True)
    def ensure_test(self, index):
        print(f"element at index {index} in dat '{self.dat[index]}'")
        return self.dat[index]


if __name__ == "__main__":
    t = Test()
    r = t.ensure_test(1)
    print(r)
