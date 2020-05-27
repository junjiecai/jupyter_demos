from typing import Union, TypeVar

Number = Union[float, int]  # 注意这里是[ ], 不是( )


def add(x: Number, y: Number) -> Number:
    return x + y


# 比较存在/缺失type_hinting的情况下， IDE的提示信息

# 注意：type hinting可以帮助IDE进行更好的提示，但是并不会强制的约束。下面的代码尽管被提示类型问题，但是还是可以照常运行。
add("aaa", "bbb")
add(1, 2)
add(1.0, 2.0)

Number2 = TypeVar("Number2", int, float)


def subtract(x: Number2, y: Number2) -> Number2:
    return x + y


subtract("aaa", "bbb")
subtract(1, 2)
subtract(1.0, 2.0)
