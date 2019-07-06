# Split statements into two group (Slide statement ⇧⌘↑ or ⇧⌘↓)

def test():
    x = 1
    a = 'A'
    y = 1
    b = 'B'
    r_1 = x + y
    c = a + b
    r_2 = x - y
    d = c ** 3
    r_3 = r_1 * r_2

    return r_3, d
