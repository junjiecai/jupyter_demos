from IPython.display import display


def comparator_factory(string_before, string_after):
    def comparator(target, func, *args, **kwargs):
        print(string_before.format(func.__name__ + '()'))
        display(target)

        print(string_after)
        display(func(target, *args, **kwargs))

    return comparator


def comparator_method_factory(string_before, string_after):
    def comparator(target, method_name, *args, **kwargs):
        print(string_before.format(method_name + '()'))
        display(target)

        print(string_after)
        display(getattr(target, method_name)(*args, **kwargs))

    return comparator


def comparator_eval_factory(string_before, string_after):
    def comparator(uneval):
        print(string_before)
        display(uneval)

        print(string_after)
        display(uneval.doit())

    return comparator
