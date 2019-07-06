# rename A.execute into A.calculate (Rename ⇧F6)
# Beware of not including wrong dynamic references!
# Add type annotation to run(a, b), try rename again (Rename ⇧F6)

class A:
    def execute(self):
        print('execute A')


class B:
    def execute(self):
        print('execute B')


def run(a, b):
    a.execute()
    b.execute()


if __name__ == '__main__':
    a = A()
    b = B()

    run(a, b)
