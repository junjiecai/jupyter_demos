from typing import Callable


# Callable可以指定参数的类型，用法：Callable[[Arg1Type, Arg2Type], ReturnType]
def run(f: Callable[[str, int], str]) -> str:
    # Body
    return f('abc')


def f_1(s: str, n: int) -> str:
    return s.capitalize() * n


def f_2(s: str) -> int:
    return len(s)


run(f_1)
run(f_2)
