from abc import ABC
from typing import Type


class Parent(ABC):
    pass


class Child(Parent):
    pass


# 区别instance of class和class
d: Parent = Child()

d_1: Parent = Child

d_2: Type[Parent] = Child
