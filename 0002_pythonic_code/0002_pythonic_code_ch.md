
充分利用python的特点和功能， 可以让我们的代码更加的简洁， 有更好的可读性， 很多情况下也会带来更好的性能。 符合这样要求的代码也被python社区称为pythonic的代码。

这里举例一些常见的使用python时遇到的场景。 针对这些场景， 给出两个版本的代码， 它们都实现了同样的功能， 但是第一个版本没有充分利用python特性，另一个版本则比较pythonic。

pythonic的代码除了简介优雅，大部分时候，也会有更好的性能(因为它们经过特别优化)。为了验证这点，我们可以利用helper.py中的func_compare函数比较两个版本的代码的性能。


```python
# 这段代码定义了一个函数， 可以将相同的参数传给两个版本的函数后比较运行时间， 后面的代码实验中会用到， 默认每个函数重复100000次。
from helper import func_compare
```

## tuple/list unpacking

### 批量赋值给多个变量

从一个tuple/list中将数据取出， 赋值给几个不同的变量是一个常见的需求。有时候这个tuple/list中还会嵌套更多的tuple/list。

下面的例子里， 我们有这样一个tuple


```python
d = ('male',('Junjie', 'Cai'), 'cjj@jfpal.com', 'data engineer')
```

现在希望将里面的性别， 姓， 名， 邮箱几个数据取出并赋值给相应的变量后， 然后用这些变量组成一个字符串返回。 

版本1的代码用index一个个的取出数值



```python
def func_ver_1(d):
    sex = d[0]
    email = d[2]
    name = d[1]
    family_name = name[1]
    first_name = name[0]
    title = d[3]
    
    return "{family_name} {first_name} is a {sex} {title} with email:{email}".format(**locals())   

```

版本2的代码则利用tuple unpacking一次性的取出所有数值。


```python
def func_ver_2(d):
    sex, (first_name, family_name), email, title = d
    
    return "{family_name} {first_name} is a {sex} {title} with email:{email}".format(**locals())
    
d = ('male',('Junjie', 'Cai'), 'cjj@jfpal.com', 'data engineer')

func_compare(func_ver_1, func_ver_2, [d])
```

    func_1 result:
    Cai Junjie is a male data engineer with email:cjj@jfpal.com
    
    func_2 result:
    Cai Junjie is a male data engineer with email:cjj@jfpal.com
    
    time: 1.912s vs 1.681s
    ----------------------


### 在循环中利用

上面的技巧可以放在for循环中使用。看下面的例子。


```python
d_list = [
 ('male',('Junjie', 'Cai'), 'cjj@jfpal.com', 'data engineer'),
 ('male',('Hongfei', 'Bao'), 'bhf@jfpal.com', 'data engineer')    
]
```


```python
def func_ver_1(d_list):
    str_list = []
    
    for d in d_list:
        sex = d[0]
        email = d[2]
        name = d[1]
        family_name = name[1]
        first_name = name[0]
        title = d[3]
        
        str_list.append("{family_name} {first_name} is a {sex} {title} with email:{email}".format(**locals()))
        
    return str_list
    
    
def func_ver_2(d):
    str_list = []    
    for sex, (first_name, family_name), email, title in d_list:      
        str_list.append("{family_name} {first_name} is a {sex} {title} with email:{email}".format(**locals()))        
    
    return str_list

func_compare(func_ver_1, func_ver_2, [d_list])
```

    func_1 result:
    ['Cai Junjie is a male data engineer with email:cjj@jfpal.com', 'Bao Hongfei is a male data engineer with email:bhf@jfpal.com']
    
    func_2 result:
    ['Cai Junjie is a male data engineer with email:cjj@jfpal.com', 'Bao Hongfei is a male data engineer with email:bhf@jfpal.com']
    
    time: 3.791s vs 3.231s
    ----------------------


### 选取开头和结尾部分的变量
假设这里只需要取出第一个和最后一个变量。

tuple/list unpacking是不能只选择头尾部分的数据的， 但是如果对tuple/list中间的部分不感兴趣， 可以用 **```*_```** 统一接收， 这样就会将中间段的数据放入变量名为**_**的list中， 后面代码不使用即可。 


```python
def func_ver_1(d):
    sex = d[0]
    email = d[2]
    
    return "Owner of {email} is {sex}".format(**locals())
    
def func_ver_2(d):
    sex, *_, email = d #注意这里
    
    return "Owner of {email} is {sex}".format(**locals())    
    
d = ('male',('Junjie', 'Cai'), 'cjj@jfpal.com')

func_compare(func_ver_1, func_ver_2, [d])
```

    func_1 result:
    Owner of cjj@jfpal.com is male
    
    func_2 result:
    Owner of cjj@jfpal.com is male
    
    time: 1.081s vs 1.230s
    ----------------------


注意这里使用**_**作为变量名， 只是一种约定， 表示unpacking后，这个变量存的信息代码的作者并不关心。 不过实际上使用任何合法的变量名都是可以的。

### 数值交换
有a, b两个变量


```python
a = 1
b = 10
```

我们需要交换a, b两个变量的数值。这时也可以利用tuple unpacking的技巧。


```python
def func_ver_1(a, b):
    temp = b
    b = a
    a = temp
    
    return (a, b)

def func_ver_2(a, b):
    a, b = b, a # 注意这里
    
    return (a, b)

func_compare(func_ver_1, func_ver_2, [a,b])
```

    func_1 result:
    (10, 1)
    
    func_2 result:
    (10, 1)
    
    time: 0.482s vs 0.362s
    ----------------------


注意虽然没有添加()，但是python也是创建了一个tuple哦。


```python
x = 1,2
print(type(x))
```

    <class 'tuple'>


这种场景很容易推广到多个变量数值进行交换的情况


```python
a = 1
b = 2
c = 3

b, c, a = a, b, c

print(a, b, c)
```

    3 1 2


## 字符串连接

一个很常见的任务就是把list中的字符串用某个特定的字符进行拼接， 例如我们有这样一个list


```python
s_list = ['To', 'be', 'or', 'not', 'to', 'be']
```

希望把他们用空格去连接几个单词组成一个句子


```python
def func_1(s_list, sep):
    string = ''
    for i, s in enumerate(s_list):
        if i!=0:
            string += sep+s
        else:
            string += s
    return string

def func_2(s_list,sep):
    return sep.join(s_list)


sep = ' '
func_compare(func_1, func_2, [s_list, sep])
```

    func_1 result:
    To be or not to be
    
    func_2 result:
    To be or not to be
    
    time: 1.557s vs 0.473s
    ----------------------


第二个版本中， 用python内置的函数比自己去实现， 简洁度， 效率都高了不是一点点。

## 二. 创建同值的list

某时候我们需要快速的创建一个list， 里面的值是相同的。 

例如， 我们创建一个长度为4的list, 其中每个位置的内容都是[0,0,0,0] 


```python
def func_1(v, n):
    l = []
    for i in range(n):
        l.append(v)
    return l

def func_2(v, n):
    return [v]*n

func_compare(func_1, func_2, [0,4])
```

    func_1 result:
    [0, 0, 0, 0]
    
    func_2 result:
    [0, 0, 0, 0]
    
    time: 1.103s vs 0.483s
    ----------------------


python提供的**```*```**运算符可以将list复制扩增。

不过这里要注意的是, 用这种方法创建的list中存放的数据如果是object， 它们指向的都是同一个object。 用下面的代码可以验证这点


```python
a = [[0,0,0,0]]*4
print(a)
```

    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]



```python
print(a[0] is a[1])

a[0][0] = 10
print(a)
```

    True
    [[10, 0, 0, 0], [10, 0, 0, 0], [10, 0, 0, 0], [10, 0, 0, 0]]


## for循环是否全通过

有时候我们要判断一个for循环是否中途被break掉还是“寿终正寝”。 

例如下面判断list_a中每一个元素是否都属于list_b(这里只是为了演示for...else...,完成这个需求更好的办法是用set)


```python
list_a = ['java','spark','python']
list_b = ['java','html5','excel','spark','python']
```


```python
def func_1(list_a, list_b):
    is_all_in = True
    
    for x in list_a:
        if not x in list_b:
            is_all_in = False
            break
            
    if is_all_in:
        return 'all item in list_a is in list_b'
    else:
        return 'not all item in list_a is in list_b'        
        
def func_2(available, demand):
    for x in list_a:
        if not x in list_b:
            return 'not all item in list_a is in list_b'        
    else: 
        return 'all item in list_a is in list_b'
        
func_compare(func_1, func_2, [list_a, list_b])
```

    func_1 result:
    all item in list_a is in list_b
    
    func_2 result:
    all item in list_a is in list_b
    
    time: 0.641s vs 0.654s
    ----------------------


for ...else...中的else刚接触会觉得有点别扭， 总之记住如果for循环部分执行了break， 或者出现Exception， else分支就不会被执行即可。 利用这个语句可以省掉一个flag变量标记for循环是否中途被break掉。

## 10>c>b>a>0?

如何判断10>c>b>a>0?


```python
def func_ver_1(a,b,c):
    return (10>c) and (c>b) and (b>a) and (a>0)
        

def func_ver_2(a, b, c):
    return 10>c>b>a>0 #注1

a = 1
b = 3
c = 5

func_compare(func_ver_1, func_ver_2, [a, b, c])
```

    func_1 result:
    True
    
    func_2 result:
    True
    
    time: 0.458s vs 0.408s
    ----------------------


几乎每个学C语言的同学都课上都会被强调不能用第二个版本的中的写法，否则无法得到正确的结果。不过这种写法在python确是完全可以的哦。

## 判断空容器和空值

### 判断容器为空

下面的例子里， 我们检查一个list是否为空， 如果是， 返回True， 否则返回False


```python
def func_ver_1(l):
    if len(l)>0:
        return True
    else:
        return False
        
def func_ver_2(l):
    if l: # 不需要用len
        return True
    else:
        return False      
        
l = []

func_compare(func_ver_1, func_ver_2, [[]])
```

    func_1 result:
    False
    
    func_2 result:
    False
    
    time: 0.389s vs 0.304s
    ----------------------


如果把list直接用在if语句中， 那么如果它们是空的， 对于if相当于False， 否则为True。

因此如果目的是判断它们是否为空， 就不用额外的使用len求长度了。 这点同样适用于tuple, set, dict, string, 见下面代码


```python
if ():
    pass
else:
    print('tuple is empty')
    
if set():
    pass
else:    
    print('set is empty')
    
if {}:
    pass
else:    
    print('dict is empty')
    
if "":
    pass
else:    
    print('string is empty')    
```

    tuple is empty
    set is empty
    dict is empty
    string is empty


不过很遗憾， 对于数据分析常用的pandas.DataFrame和pandas.Series， 并不支持这个特征， 直接放在if里会报错。


```python
try:
    from pandas import DataFrame
    if DataFrame():
        pass
    else:
        print('DataFrame is empty')       
except Exception as e:
    print(type(e),e)
```

    <class 'ValueError'> The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().


###  判断是否是None

这里假设数据是None返回False, 否则返回Yes


```python
def func_ver_1(l):
    if x is None:
        return True
    else:
        return False
        
def func_ver_2(l):
    if x: # 注意这里
        return False
    else:
        return True
        
x = None

func_compare(func_ver_1, func_ver_2, [[]])
```

    func_1 result:
    True
    
    func_2 result:
    True
    
    time: 0.347s vs 0.311s
    ----------------------


如果将None直接用在if中， 相当于False， 因此可以利用这点很方便的判断一个数据是否为None

## list/generator/dict/set comprehension

一个很常见的场景是, 把一个容器中的元素进行便利，取出符合条件的值， 进行变换处理，然后存放在另一个容器中。 

例如下面把list中的偶数取出， 求平方后存在另一个list。


```python
l = [1,2,3,4,5,6,7,8,9,10]
```


```python
def func_ver_1(l):
    new_list = []
    for v in l:
        if v%2==0:
            new_list.append(v**2)
    return new_list

def func_ver_2(l):
    return [v**2 for v in l if v%2==0] #注意



func_compare(func_ver_1, func_ver_2, [l])
```

    func_1 result:
    [4, 16, 36, 64, 100]
    
    func_2 result:
    [4, 16, 36, 64, 100]
    
    time: 3.040s vs 2.717s
    ----------------------


版本2的写法叫做list comprehension功能，它有几个组成要素。换行后更容易观察。


```python
[ #定义新容器的类型，这里是list
    v**2 #需要进行的变换方式
    for v in l # 对原容器进行遍历
    if v%2==0 #筛选条件， 这部分是可选的
]
```




    [4, 16, 36, 64, 100]



对应的也有dict comprehension， 例如下面的例子中。


```python
d = {1:'apple', 2:'peach', 3:'melon', 4:'banana'}
```

我们把key为偶数的item取出后， 将value变成大写， 然后将这个key-value pair存入新的dict


```python
def func_ver_1(d):
    new_dict = {}
    for k in d:
        if k%2==0:
            new_dict[k] = d[k].upper()
    return new_dict            
    
def func_ver_2(d):
    return {k:v.upper() for k,v in d.items() if k%2==0} #注1

d = {1:'apple', 2:'peach', 3:'melon', 4:'banana'}

func_compare(func_ver_1, func_ver_2, [d])
```

    func_1 result:
    {2: 'PEACH', 4: 'BANANA'}
    
    func_2 result:
    {2: 'PEACH', 4: 'BANANA'}
    
    time: 1.266s vs 1.397s
    ----------------------


换行后更好的观察各个要素


```python
new_d = { #定义新容器的类型，这里是dict
    k:v.upper() #新的key-value pair,可以分别进行变换
    for k,v in d.items() # 对原来的dict进行遍历
    if k%2==0 #筛选条件，k是偶数
}

print(new_d)
```

    {2: 'PEACH', 4: 'BANANA'}


同样，有set comprehension。 例如将下面list中的偶数取出，放入一个set


```python
l = [1,2,3,4,5,6,7,8,9,10]
s = {v for v in l if v%2==0}

print(s)
```

    {8, 2, 10, 4, 6}


有一点要注意的是,如果使用(),得到的并不是一个tuple,而是generator


```python
l = [1,2,3,4,5,6,7,8,9,10]
g = (v for v in l if v%2==0)

print(g)
print(list(g))
```

    <generator object <genexpr> at 0x7f69f1d8beb8>
    [2, 4, 6, 8, 10]


## 两个list创建一个dict

这也是一个非常常见的场景。一个list提供key, 另一个list提供value


```python
def func_1(l_key, l_value):
    d = {}
    for i, v in enumerate(l_key):
        d[v] = l_value[i]
    return d

def func_2(l_key, l_value):
    return dict(zip(l_key, l_value)) #注1

l_key = [1,2,3,4,5]
l_value = ['a','b','c','d','e']

func_compare(func_1, func_2, [l_key, l_value])
```

    func_1 result:
    {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
    
    func_2 result:
    {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
    
    time: 1.104s vs 1.227s
    ----------------------


这里利用zip函数将两个list合并成一个generator, generator会按顺序输出一系列tuple, tuple中的数据分别来自两个list. 见下面代码。


```python
list_a = ['a','b','c']
list_b = [1,2,3]

z = zip(list_a, list_b)
print(next(z))
print(next(z))
print(next(z))
```

    ('a', 1)
    ('b', 2)
    ('c', 3)


dict()函数可以接受输出一列二元tuple的generator并构造dict，这种写法非常简洁。

##  确保资源被正确关闭

下面的场景里， 我们要确保打开了一个文件后， 要确保它们被关闭


```python
def func_ver_1(file_name):
    try:
        f = open(file_name, 'w')        
    except Exception as e:
        pass
    finally:
        f.close()

def func_ver_2(file_name):
    with open(file_name, 'w') as f: #注1    
        pass
    
file_name = 'test_temp_file.txt'
func_compare(func_ver_1, func_ver_2, [file_name],n=10000)

```

    func_1 result:
    None
    
    func_2 result:
    None
    
    time: 0.355s vs 0.373s
    ----------------------


with语法在python中叫做context manager, 在with语句去打开文件， 将对这个文件所需的处理语句放在with中， 这样无论这些语句是否raise Exception， 都能保证文件都能被关闭。 可以省掉一大块try, except, finnaly组合， 让代码简洁不少。

其他一些连接数据资源， 比如连接数据库的函数， 一般也会支持这种用法。 



## 判断数据的类型

下面我们判断a是否是tuple或list, 是的话返回True, 否则False


```python
a = (1, 2, 3)
```

判断是否是函数可以用callable


```python
def a():
    pass

callable(a)
```




    True




```python
def func_ver_1(a):
    if (str(type(a)) == "<class 'tuple'>") or (str(type(a)) == "<class 'list'>"):
        return True
    else:
        return False
    
def func_ver_2(a):
    if isinstance(a, (tuple, list)): #注1
        return True
    else:
        return False
    

func_compare(func_ver_1, func_ver_2, [a])
```

    func_1 result:
    False
    
    func_2 result:
    False
    
    time: 1.393s vs 0.592s
    ----------------------


注释

1. 由于很多python教材都会在早期的时候引入对type函数的介绍， 因此初学者可能会很长时间内使用type去判断数据的类型。 不过isinstance是更好的选择。

# 应对不合法的输入参数


有时候我们需要考虑到输入的参数可能不合法的问题。 不过与其每次都检查一下输入参数的类型， 不妨将这个问题交给try, except机制去处理。

下面的例子里， 我们实现一个对两个数值求sum的功能， 如果输入参数并不能参与sum计算， 那么返回None


```python

def func_ver_1(a, b):
    if isinstance(a, (float,int)) and isinstance(b, (float, int)):
        return sum([a, b])
    else:
        return None

        
def func_ver_2(a, b):
    try:
        return sum([a, b])
    except TypeError:
        return None
    
func_compare(func1, func2, [5,10])
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-50-b6731c3b81ed> in <module>()
         13         return None
         14 
    ---> 15 func_compare(func1, func2, [5,10])
    

    NameError: name 'func1' is not defined


第二个版本的代码中， 我们不去主动检验输入参数的合法性， 而是由try, except去处理可能发生的问题， 简化了代码。 

而且由于类型判断本身也是一个耗时的步骤， 第二个版本的函书省略了类型判断的步骤， 效率也更高。

# 跨行的字符串连接


```python
my_very_big_string = (
    "For a long time I used to go to bed early. Sometimes, "
    "when I had put out my candle, my eyes would close so quickly "
    "that I had not even time to say “I’m going to sleep.”"
)

my_very_big_string
```




    'For a long time I used to go to bed early. Sometimes, when I had put out my candle, my eyes would close so quickly that I had not even time to say “I’m going to sleep.”'


