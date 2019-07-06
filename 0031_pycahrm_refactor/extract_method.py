# Tasks:
# (1) extract triangle surface calculation into method (Extract Method, ⌥⌘M)
# (2) convert method into static method (intention actions, ⌥⏎)
# (3) convert static method into function (intention actions, ⌥⏎)


class Triangle:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        p = (self.x + self.y + self.z) / 2
        self.s = (p(p - self.x) * (p - self.y) * (p - self.z)) ** 0.5
