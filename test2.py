class big_test(object):
    # def test(self, a, s):
    #     print(a)
    #     print(s)
    #     print(self)

    def __init__(self, name, age):
        # self.name = 'zhangjun'
        # self.age = 18
        self.name = name
        self.age = age
        print(self.name)
        print(self.age)

    def test(self):
        print(self.name)

    # def show(self):
    #     print(self.name)
    #     print(self.age)


if __name__ == "__main__":
    # print(a='12333')

    # big_test.test('ada', s=1231, a=123213, )

    c1 = big_test('zhangjun', 18)
    c1.test()
