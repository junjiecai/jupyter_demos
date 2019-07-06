# extract triangle surface calculation into function (⌥⌘M)


def demo():
    x = 3
    y = 4
    z = 5

    p = (x + y + z) / 2

    s = (p * (p - x) * (p - y) * (p - z)) ** 0.5

    return s
