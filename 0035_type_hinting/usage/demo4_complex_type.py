from typing import Dict, Union

InnerDict = Dict[int, Union[int, float]]
Data = Dict[int, InnerDict]


def f(data: Data):
    return "xxx"


config_1 = {
    1: {
        1: 1.0,
        2: 1.0
    },
    2: {
        1: 2.0,
        2: 3
    }
}
config_2 = {
    '1': {
        1: 1.0,
        2: 1.0
    },
    '2': {
        1: 2.0,
        2: 3
    }
}

f(config_1)
f(config_2)
