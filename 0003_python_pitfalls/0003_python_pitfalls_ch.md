
欢迎去[这里](https://github.com/junjiecai/jupyter_labs/tree/master/cjj_notebooks/0014_python_pitfalls)下载到本文对应的jupyter notebook文件，亲自动手实验文中的代码。


```python
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
```

## float的精度问题
float没办法覆盖所有的数值范围，会导致数值计算的不准确。

例如，float没法表示小数点后面任意的精度


```python
def func_1():
    a = 1.13445433423e-300
    return a**2

func_1()
```




    0.0



如果的确需要如此高的精度计算，可以使用decimal.Decimal这种数据类型。


```python
def func_2():
    from decimal import Decimal
    d = Decimal('1.13445433423e-300')
    return d**2

func_2()
```




    Decimal('1.2869866364532325496929E-600')



不过作为代价，Decimal数值类型会消耗更多的计算时间。下面比较两个版本的代码各执行100000次，消耗的时间


```python
from datetime import datetime
def timing(n, func, args, kargs):
    t1 = datetime.now()
    for i in range(n):
        func(*args,**kargs)
    t2 = datetime.now()
    print((t2-t1).total_seconds())
```


```python
timing(100000,func_1,[],{})
```

    0.030747



```python
timing(100000,func_2,[],{})
```

    0.220824


可以看到，有接近7~8倍的差距

float同样无法准确表达过大的数值，例如下面的例子


```python
x = 123123123123123123123123
x = float(x)
int(x)
```




    123123123123123117883392



可以看到, 如果将大整数转化成float,再转回成int,数值上已经发生了偏差。 不过由于python的int类型本来就可以表示任意大的整数(只要内存允许)，直接使用int类型进行计算即可。

## pandas, numpy与大数值int
一些pandas（或是底层用到的numpy）的函数并不支持数值较大的int


```python
try:
    np.isinf(62226003100113821696)
except Exception as e:
    print(type(e),e)
```

    <class 'TypeError'> ufunc 'isinf' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''



```python
try:
    Series([99898989789797878797,99898989789797878797],index = [0,1]).value_counts()
except Exception as e:
    print(type(e),e)
```

    <class 'OverflowError'> Python int too large to convert to C long


如果不想损失精度的话， 部分场景可以使用decimal.Decimal解决


```python
from decimal import Decimal
```


```python
try:
    print(Series([Decimal('99898989789797878797'),Decimal('99898989789797878797')],index = [0,1]).value_counts())
except Exception as e:
    print(type(e),e)
```

    99898989789797878797    2
    dtype: int64


然而，并不是所有的情况都管用


```python
try:
    np.isinf(Decimal('62226003100113821696'))
except Exception as e:
    print(type(e),e)
```

    <class 'TypeError'> ufunc 'isinf' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''


想上面这种情况， 就只能转成float损失精度了。(对于例子中的np.isinf来说，精度是否降低是无关紧要的)


```python
try:
    np.isinf(float('62226003100113821696'))
except Exception as e:
    print(type(e),e)
```

## 操作系统默认encoding

ubuntu下用open新建文件的时候,默认的encoding就是utf8,因此要往文件写入中文等字符都是没有问题的。但是windows的默认encoding不是utf8(似乎是ascii?有windows的同学可以试试)，则需要额外的在open中制定encoding才能顺利写入特殊的字符。

大家可以在自己的操作系统下测试一下下面代码的结果。


```python
import sys
print(sys.getdefaultencoding())
```

    utf-8



```python
with open('test.txt',mode = 'w') as file:
    file.write('测试')
```

可以通过encoding参数强制指定encoding


```python
with open('test.txt',mode = 'w',encoding = 'utf') as file:
    file.write('测试')
```

## cx_Oracle的arraysize


```python
conn.arrayzie = 10000
print(conn.arrayzie)
```

cx_Oracle的connection有一个arraysize控制每次从数据库中一次读取的数据行数， arraysize的设置必须发生在conn.execute(sql)之前，否则是不会生效的。

(这个例子暂时不提供实验， 以后可能要配上docker实验环境)

## 条件判断的括号

下面的例子的结果估计大部分想象的都不太一样


```python
setA = {1}
setB = {2}

True if len(setA)==1 & len(setB)==1 & len(setA|setB)==2 else False
```




    False



如果不想去费无意义的脑力去记忆运算执行顺序规则的话， 多利用括号就好。


```python
True if (len(setA)==1) & (len(setB)==1) & (len(setA|setB)==2) else False
```




    True



## 眼见不为实

在jupyter中使用pandas时， jupyter会将dataframe用比较美观的方式的展现出来。 但是特别要注意的是， 一些不同数据类型的数据， 或者带有空格的字符串， 在jupyter中是看不到区别的，例如:


```python
df1 = DataFrame({'A':[1,2,3],'B':['a','b','c']})
df2 = DataFrame({'A':['1','2','3'],'C':['aa','ba','ca']})
```


```python
df1
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>a</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>b</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>c</td>
    </tr>
  </tbody>
</table>
</div>




```python
df2
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>aa</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>ba</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>ca</td>
    </tr>
  </tbody>
</table>
</div>



看上去A列一模一样， 但是如果merge的话， 是什么也得不到的。


```python
df1.merge(df2, on = 'A') 
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



因此， 使用DataFrame的时候一定要记得检查一下相关列的数据类型是什么。

同理， 如果字符中含有空格， 在jupyter中也不容易被观察出来。


```python
s1 = Series(['a','b']).to_frame()
s2 = Series(['a ','b ']).to_frame()
```


```python
s1
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
    </tr>
  </tbody>
</table>
</div>




```python
s2
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
    </tr>
  </tbody>
</table>
</div>



进行数值比较的时候实际上会被判定为False


```python
s1==s2
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



但是如果转成list然后print出来的话，就很容易看出空格的存在。


```python
list(s1[0])
```




    ['a', 'b']




```python
list(s2[0])
```




    ['a ', 'b ']



## 中英文符号

在写代码的时候最好关闭中文输入法， 避免混入中文或全角标点， 尤其是在编写正则表达式的时候。 例如， 我们希望根据'ab'或者'ad'去分割字符串


```python
import re
string = 'abcadfa'
```


```python
re.split('ab｜ad',string)
```




    ['abcadfa']




```python
re.split('ab|ad',string)
```




    ['', 'c', 'fa']



第一段代码没能生效的原因是'｜'是在全角状态输入的。　像这样的问题是很难观察到的。

## 函数默认初始值

mutable类型的数据不要作为函数的初始值，它并不会每次使用函数的时候被初始化,而是会记忆之前的运行状态。


```python
# mutable作为默认初始值的问题
def test(a = []):
    a.append('*')
    print(a)
```

运行一次的时候，正常


```python
test()
```

    ['*']


运行第二次的时候


```python
test()
```

    ['*', '*']


可以看到a并不是从[]开始运行的。

如果的确需要使用[]作为初始默认值,常见的做法是接受None作为参数后，在函数内部完成初始化。


```python
def test(a = None):
    a = a or []

    a.append('*')
    print(a)
        
```


```python
test()
```

    ['*']



```python
test()
```

    ['*']

