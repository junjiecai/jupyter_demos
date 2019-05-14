import pytest


@pytest.fixture(scope="module")
def moudule_level_resource():
    # setup resource and return by yield
    print('\n==========================')
    print('setup module level resource')

    yield 'some module level resource'  # replace into real resource, such as connection

    # teardown resource
    print('teardown module level resource')
    print('==========================')


@pytest.fixture
def function_level_resource():
    # setup resource and return by yield
    print('---------------------')
    print('setup function level resource')

    yield 'some function level resource'  # replace into real resource, such as connection

    # teardown resource
    print('teardown function level resource')
    print('---------------------')


def test_1(moudule_level_resource, function_level_resource):
    print('running test case 1')
    print('Get ' + function_level_resource)  # yield返回的结果在测试用例代码中可以用函数的名字访问

    assert True


def test_2(moudule_level_resource, function_level_resource):
    print('running test case 2')
    print('Get ' + function_level_resource)

    assert True
