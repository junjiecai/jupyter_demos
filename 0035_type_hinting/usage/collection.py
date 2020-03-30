from typing import Dict, Tuple, Sequence, Mapping, Generic, TypeVar, List, Iterable


ConnectionOptions = Dict[str, str]
c_1: ConnectionOptions = {'a':'b'}
c_2: ConnectionOptions = {'a': 1}


Address = Tuple[str, int]
a_1: Address = ('Matt Lane', 234)
a_2: Address = ('Matt Lane', '234')



# 定义符合的类型
Server = Tuple[Address, ConnectionOptions]

s_1: Server = (
    ('Matt Lane', 234),
    {'a':'b'}
)

s_1: Server = (
    ('Matt Lane', '234'),
    {'a':'b'}

)



# 自定义container支持Generic
T = TypeVar('T')

class MyContainer(Generic[T]):
    def __init__(self, iterable:List[T]):
        self.iterable = iterable

    def __iter__(self) -> Iterable[T]:
        return self.iterable.__init__()


data: MyContainer[str] = MyContainer([1, 2])

data: MyContainer[str] = MyContainer(["apple", "bird"])

for x in data:
    x.capitalize()









