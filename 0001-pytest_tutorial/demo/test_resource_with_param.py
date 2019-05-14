def decrator_creator(n):
    def decrator(func):
        def wrapper():
            print('\n----------------')
            print('Setup resource of type {}'.format(n))
            resource = 'resource {}'.format(n)
            func(resource)
            print('Teardown resource of type {}'.format(n))
            print('----------------')

        return wrapper

    return decrator


@decrator_creator(1)
def test_1(resource):
    print('running test case 1')
    print('using {}'.format(resource))

    assert True


@decrator_creator(2)
def test_2(resource):
    print('running test case 2')
    print('using {}'.format(resource))

    assert True
