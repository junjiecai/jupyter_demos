class A:
    def f(self):
        pass


#  比较存在/缺失type hinting条件下，重构函数f的效果。
#  注意，如果有另外一个库也用命名为f的函数，且没有添加type hinting，那么依然会被纳入重构范围。
#  因此不要忘记核对dynamic_references中是否纳入了错误的重构目标。
class B:
    def f(self):
        pass


class C:
    # def __init__(self, a, b):
    def __init__(self, a: A, b: B):
        self.a = a
        self.b = b

    def run(self):
        self.a.f()
        self.b.f()
