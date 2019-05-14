
# pytest的基本文件结构


pytest可以自动遍历文件夹中包含测试用例的.py文件， 并且运行其中的测试用例代码。如何才能被pytest自动识别到呢？只要让.py文件，以及其中测试用例代码用'test_'或者'_test'结尾即可。

例如我们测试文件是这样的组织的

```
|demo
    test_basic.py
    test_resource.py    
```
打开的话可以找到很多'test_'开头的函数，这些都是可以被自动识别的。


(在Jupyter Notebook中用'!'可以运行terminal命令，下面的命令等同于在这个notebook所在的文件夹打开一个terminal,运行```pytest demo```)


```python
! pytest demo
```

    [1m============================= test session starts ==============================[0m
    platform linux -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
    rootdir: /home/junjiecai/Documents/jupyter-blog/content/articles/jupyter_labs/exolution/0001-pytest_tutorial, inifile: 
    collected 4 items / 1 errors [0m[1m
    [0m
    ==================================== ERRORS ====================================
    _____________________ ERROR collecting demo/test_basic.py ______________________
    [31mimport file mismatch:
    imported module 'test_basic' has this __file__ attribute:
      /home/exolution/Documents/jupyter-blog/content/0010-pytest_tutorial/demo/test_basic.py
    which is not the same as the test file we want to collect:
      /home/junjiecai/Documents/jupyter-blog/content/articles/jupyter_labs/exolution/0001-pytest_tutorial/demo/test_basic.py
    HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules[0m
    !!!!!!!!!!!!!!!!!!! Interrupted: 1 errors during collection !!!!!!!!!!!!!!!!!!!!
    [31m[1m=========================== 1 error in 0.13 seconds ============================[0m


上面的例子里， pytest找到了demo文件夹下2个包含测试用例的.py文件， 并且找到其中测试用例代码并且执行。(这里我们的测试用例都是能通过的)

# 用例的基本写法

测试用例的基本思路是， 运行待测函数，然后比较待测函数的行为(生成特定结果， 正确的raise Exception)是否和设计的一致。

例如我们构想一个函数func, 需要满足两个特征。

1. 接受参数字符串s和整数n, 返回将s扩增n次以后拼接在一起的结果
2. 如果s的类型不是str, raise TypeError

针对第一个要求， 我们可以构造一个具体的参数组合, 让待测函数执行， 然后比较返回的结果是否和我们设计的一致。


```python
def test_value():
    assert func('ab',3) == 'ababab'
```

assert语句会判断之后的条件表达式是否成立， 如果成立， 什么都不发生； 如果不成立， 会raise Exception并被pytest捕捉。

针对第二个需求， 无法直接利用assert语句判断， 但是可以利用pytest提供的context manager去表达"这是会raise xx类型的Exception的错误"的要求， 语法如下。


```python
def test_error():
    with pytest.raises(TypeError) as error_info:
        func(1,3)
```

我们一开始的代码是两个测试都能通过的， 大家可以修改一下代码后观察一下pytest的运行结果。

# 创建和销毁资源

有些场合下， 我们需要在测试用例执行前创建一些资源， 以及在测试用例执行后销毁一些资源。 比如在数据库中创建表， 导入数据， 测试一段sql逻辑， 然后销毁这张表。 这种场合可以利用pytest提供的@pytest.fixture和yield语法构造一个资源管理器


```python
@pytest.fixture # pytest提供的装饰器
def function_level_resource():
    # 创建资源的代码
    print('---------------------')
    print('setup function level resource')
    
    # 如果有必要, 返回生成的资源(例如和特定数据库的连接conn); 如果不需要(例如只是在数据库中建张表), 写一个空的yield语句即可
    yield 'some resource' # replace into real resource, such as connection

    # 销毁资源的代码
    print('teardown function level resource')
    print('---------------------')
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-4-8260efed2a58> in <module>()
    ----> 1 @pytest.fixture # pytest提供的装饰器
          2 def function_level_resource():
          3     # 创建资源的代码
          4     print('---------------------')
          5     print('setup function level resource')


    NameError: name 'pytest' is not defined


如果不理解python的decorator和yield语法的话， 对上面这段代码可能会比较迷茫。 如果没有时间去详细理解decorator和yield， 这里只要知道
1. 虽然这段代码用的是函数定义的语法， 但是得到的结果并不是一个函数, 而是一个object， 所以别用函数的观点去理解这段代码
2. 记住生成资源， 返回资源， 销毁资源的代码写哪即可。

如果要在测试用例代码中使用相关的资源， 把这个"函数"名传入测试用例的代码即可


```python
def test_1(function_level_resource):
    print('running test case ',1)
    print('Get '+function_level_resource) #yield返回的结果在测试用例代码中可以用函数的名字访问

    assert True
```

这样在运行这个测试用例前， 就会执行function_level_resource定义的资源创建代码， 将yield返回的资源通过function_level_resource这个变量暴露给测试用例代码。并且在测试用例完成后，执行销毁资源的代码。

如果需要让整个.py文件共享一个资源， 在所有该文件的test case执行前统一创建一次资源， 等所有该文件的test case完成后统一销毁资源。 可以定义一个module level的资源管理器， 像这样。


```python
@pytest.fixture(scope="module")
def moudule_level_resource():
    # setup resource and return by yield
    print('==========================')
    print('setup module level resource')
    
    yield 'some module level resource' # replace into real resource, such as connection

    # teardown resource
    print('teardown module level resource')
    print('==========================')
```

在test_resource.py中， 每个测试用例同时使用了module level的资源和function level的资源。


下面验证一下结果， 可以看到module_level资源只是在测试test_resource.py时被创建和销毁一次， function_level的资源在每个待测函数的起始和终止都被创建和销毁一次。

(注意pytest默认不会输出print的结果， 如果需要显示， 要添加-s的参数)


```python
! pytest demo -s
```
