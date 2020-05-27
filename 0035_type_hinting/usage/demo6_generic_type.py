from typing import Generic, TypeVar, List, Dict, Union

T = TypeVar('T')


class MyContainer(Generic[T]):  # 注意不要和继承混淆
    def __init__(self, iterable: List[T]):
        self.iterable = iterable


data: MyContainer[int] = MyContainer([1, 2])

data_1: MyContainer[str] = MyContainer(["apple", "bird"])

data_2: MyContainer[int] = MyContainer(["apple", "bird"])


class MyContainer2:
    def __init__(self, iterable: List[Union[str, int, float]]):
        self.iterable = iterable


data_3: MyContainer2 = MyContainer2(["apple", 1, 1.0])

K = TypeVar('K')
V = TypeVar('V')


class MyDict(Generic[K, V]):
    def __init__(self, data: Dict[K, V]):
        self.data = data

    def keys(self) -> List[K]:
        return list(self.data.keys())

    def values(self) -> List[V]:
        return list(self.data.values())


data2: MyDict[str, int] = MyDict({'1': 1})

keys: List[int] = data2.keys()
