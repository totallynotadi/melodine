from typing_extensions import Self


class TestTwo:
    def __init__(self) -> None:
        print('two')

class Test:
    test = 'yis'

    def __new__(cls, tupe: str) -> Self:
        # print(f'cls - {cls}')
        # if tupe == 'lmao':
        #     cls.tupe = 'lol'
        cls.test = 'lul'
        print(cls.test)
        # test = 'lmao'

        # return TestTwo()
        return super().__new__(cls)

    def __init__(self, tupe) -> None:
        self.test = 'lmao'
        print(self.test)
        # print(f'self - {self}')
        # self.tupe = tupe

t = Test('lmao')
# print(t.tupe)

import pytube