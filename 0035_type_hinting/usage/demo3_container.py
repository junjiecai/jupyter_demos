from typing import Dict, List


def f(x: Dict[str, float]):
    return x


f({"a": 1.0})
f({2: 1.0})


def f2(x: List[int]) -> int:
    return 0


f2([1, 2, 3])
f2([1.0, 2, 3.0])  # 注意：对于Item的类型，检查似乎并不严格
f2([1.0, 2.0, 3.0])
