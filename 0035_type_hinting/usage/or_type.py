from typing import TypeVar, Any

T = TypeVar('T')   # can be any thing
T2 = TypeVar('A', str, int) # can be str or int


x: T = 1.1
x: Any = 1.1
x: T2 = 1.1

