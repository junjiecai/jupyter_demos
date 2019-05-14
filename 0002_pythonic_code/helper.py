from timeit import timeit


def func_compare(func_1, func_2, args=None, kwargs=None, n=1000000):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    print("func_1 result:")
    print(func_1(*args, **kwargs))
    print()

    print("func_2 result:")
    print(func_2(*args, **kwargs))
    print()

    t1 = timeit(lambda: func_1(*args, **kwargs), number=n)
    t2 = timeit(lambda: func_2(*args, **kwargs), number=n)

    print('time: {t1:0.3f}s vs {t2:0.3f}s'.format(t1=t1, t2=t2))
    print('----------------------')
