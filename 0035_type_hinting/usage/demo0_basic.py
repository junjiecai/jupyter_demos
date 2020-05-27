def add(x: int, y: int) -> int:
    # def add(x, y):
    return x + y


# 比较存在/缺失type_hinting的情况下， IDE的提示信息

# 注意：type hinting可以帮助IDE进行更好的提示，但是并不会强制的约束。
# 下面的代码尽管被提示类型问题，但是还是可以照常运行。
print(add("aaa", "bbb"))
