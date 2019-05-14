
# Closure(闭包) 和相关实现方案

python中, function本身也是object， 可以直接被作为变量传入函数或者被作为结果返回(Java等语言就不能这么干)。 这种灵活性带来很多有趣的应用，其中一个就是closure。 上一个最简单的代码的例子。


```python
def outer():
    a = 1    
    def inner(b):
        print(a+b)
        
    return inner
```

## closure的三个基本要素
* 存在一个外层函数(outer)。在outer函数的内部，定义了一个(inner)函数
* inner函数内部使用outer函数中存在的数据， 这个例子中是a
* outer函数返回inner函数

下面例举几个可以用到closure的场景

### 场景一
需要很多功能类似， 但是具体功能又有一定变化的函数。

这时， 可以把outer函数看做是另外一个函数的“制造工厂”, inner函数看做是“工厂”的产出。 通过给outer函数传入参数， 控制制造出的inner函数的具体行为。

例如有一个自动决策系统,可以接受用户自己编写的决策器函数。 这个例子里面
* 假设决策器只是简单的判断传入数据知否大于某个阈值。
* 假设框架约定， 传入的决策器函数， 只能接受一个变量。 这个变量是待判断的数值。

#### 懒方案
预先定义一大堆决策器， 每个决策器中的阈值都不同


```python
def decision_1(x):
    return x>1

def decision_2(x):
    return x>2

def decision_3(x):
    return x>3
```

显然， 这种方法是不现实的。 我们显然不可能穷尽所有可能的阈值并且会造成大量的重复代码。

#### closure方案
利用closure


```python
def decision_factory(threshold):
    def inner(x):
        return x>=threshold        
    return inner
```

这样如果要得到不用阈值的决策器， 只要把阈值传给“工厂”， 让它“生产”我们需要的决策器函数即可。 我们通过传入不同的阈值， 可以得到几百， 几千个不同的决策器函数， 但是"工厂"函数只需要写一个即可。


```python
decision = decision_factory(1)
print(decision(0.9),decision(1.1))
```

    False True


#### 其它方案
实现一个特定的目的，不一定只有一种方案。 为了实现之前的需求，除了用closure， 当然也可以用其它的方式实现。可以先写一个接受双参数的函数


```python
def decision(x, threshold):
    return x>=threshold
```

这个函数不符合只接受“待判断”数值的约定，不过可以用python的partial函数实现。


```python
from functools import partial
d = partial(decision, threshold = 1)
```

上面这段代码把threshold参数固定成1， 并且返回只需要接受x的新函数，起到的功能和closure是一样的。


```python
print(d(0.99),d(1.1))
```

    False True


如果不想引入functools这个库， 其实写个lambda函数也是可以起到一样的作用的


```python
d = lambda x:decision(x,1)
print(d(0.99),d(1.1))
```

    False True


### 场景二
#### closure的应用

outer函数中的数据， 在每次inner函数被执行的时候， 并不会被清除而是会记忆之前的状态。 因此可以利用这点，创造一个能记录状态的函数。典型的场景是一个计数器。


```python
def counter_factory():
    state = {'count':0}
    def counter():
        state['count'] = state['count']+1
        return state['count']
    return counter

counter = counter_factory()
```


```python
print(counter())
print(counter())
```

    1
    2


不错要注意的是，inner函数只能修改outer函数中mutable类型的数据。 如果尝试修改mutable类型的数据， 会导致出错。


```python
def counter_factory():
    a = 0
    def counter():
        a = a+1
        return a
    return counter

counter = counter_factory()
```


```python
counter()
```


    ---------------------------------------------------------------------------

    UnboundLocalError                         Traceback (most recent call last)

    <ipython-input-50-3c75396f9759> in <module>()
    ----> 1 counter()
    

    <ipython-input-49-5d16bee0ed08> in counter()
          2     a = 0
          3     def counter():
    ----> 4         a = a+1
          5         return a
          6     return counter


    UnboundLocalError: local variable 'a' referenced before assignment


#### object方案

创建一个object, 让object内部的属性去记录自己的状态


```python
class Counter:
    def __init__(self):
        self.count = 0
        
    def run(self):
        self.count+=1
        return self.count
    
counter = Counter()
```


```python
print(counter.run())
print(counter.run())
```

    1
    2


通过添加一个\__call__特殊method, 可以让上面的counter像函数那样被使用， 这样和closure的例子就更像了。(能够像函数那样被调用的object称为functor)


```python
class Counter:
    def __init__(self):
        self.count = 0
        
    def __call__(self):
        self.run()
        return self.count
        
    def run(self):
        self.count+=1
        return self.count
    
counter = Counter()
```


```python
print(counter())
print(counter())
```

    1
    2


### 各种实现方式对性能的影响

有多种实现方案都能实现“记录状态”或是"固定部分行为"， 不同的实现方式对性能的影响如何？以下是一个实验。


```python
import pandas as pd
```


```python
df = pd.read_csv('pid_region.csv', usecols = ['code','region'])
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>code</th>
      <th>region</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>110000</td>
      <td>北京市</td>
    </tr>
    <tr>
      <th>1</th>
      <td>110100</td>
      <td>市辖区</td>
    </tr>
    <tr>
      <th>2</th>
      <td>110101</td>
      <td>东城区</td>
    </tr>
    <tr>
      <th>3</th>
      <td>110102</td>
      <td>西城区</td>
    </tr>
    <tr>
      <th>4</th>
      <td>110105</td>
      <td>朝阳区</td>
    </tr>
  </tbody>
</table>
</div>



为了比较不同版本的代码消耗的时间， 先写一个函数。功能是重复执行函数n次后显示消耗的时间。


```python
def timming(n, func, args):
    from datetime import datetime

    t1 = datetime.now()
    for i in range(n):
        func(*args)

    t2 = datetime.now()
    print("repeat {} times, elapsed time: {} seconds".format(n, (t2-t1).total_seconds()))

```

接下来准备好五个版本的代码用于比较

双参数版


```python
def func_1(code, df):
    return df[df['code']==code]['region'].iloc[0]
```

partial函数版


```python
from functools import partial
func_2 = partial(func_1, df = df)
```

lambda函数版


```python
func_3 = lambda code:func_1(code, df)
```

closure版


```python
def outer(df):
    def inner(code):
        return df[df['code']==code]['region'].iloc[0]
    return inner

func_4 = outer(df)
```

functor版


```python
class Functor():
    def __init__(self, df):
        self.df = df
        
    def __call__(self,code):
        return df[df['code']==code]['region'].iloc[0]

func_5 = Functor(df)
```


```python
def func_6(code):
    func = lambda code:func_1(code, df)    
    return func(code)
```

然后比较一下它们的速度, 各运行1000次


```python
timming(1000, func_1, [310115,df])
timming(1000, func_2, [310115])
timming(1000, func_3, [310115])
timming(1000, func_4, [310115])
timming(1000, func_5, [310115])
timming(1000, func_6, [310115])
```

    repeat 1000 times, elapsed time: 0.539396 seconds
    repeat 1000 times, elapsed time: 0.564577 seconds
    repeat 1000 times, elapsed time: 0.571492 seconds
    repeat 1000 times, elapsed time: 0.631192 seconds
    repeat 1000 times, elapsed time: 0.556657 seconds
    repeat 1000 times, elapsed time: 0.619901 seconds


似乎效果一样

### lambda lazy binding

lambda是不能配合for循环批量的"制造"函数的


```python
def add(a, b):
    return a+b
```


```python
f_list = [lambda a:a+b for b in [10,20,30]]

print(f_list[0](1))
print(f_list[1](1))
print(f_list[2](1))
```

    31
    31
    31


原因是, lambda函数的lazy binding机制, 导致只有lambda函数被调用的时候，才会去查找b的值。这时循环已经结束，b的数值固定为20

但是closure函数并不会出现这个问题


```python
def add_closure(b):
    def add(a):
        return a+b
    return add

f_list = [add_closure(i) for i in [10,20,30]]

print(f_list[0](1))
print(f_list[1](1))
print(f_list[2](1))
```

    11
    21
    31


如果一定要用lambda函数实现类似效果的话,可以利用默认值来传入b的数值


```python
f_list = [lambda a,b=b:a+b for b in [10,20, 30]]

print(f_list[0](1))
print(f_list[1](1))
print(f_list[2](1))
```

    11
    21
    31


partial版的测试


```python
def add(a,b):
    return a+b

from functools import partial
func_list = [partial(add, b = x) for x in [10,20,30]]
```


```python
func_list[0](1)
```




    11




```python
func_list[1](1)
```




    21




```python
func_list[2](1)
```




    31



可以看到, partial并没有lazy binding的问题
