from abc import ABC
from typing import Type


class Parent(ABC):
    pass


class Child(Parent):
    pass



# 区别instance of class和class
d: Parent = Child()

d: Parent = Child

d: Type[Parent] = Child