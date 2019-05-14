
python原生的None和pandas, numpy中的numpy.NaN尽管在功能上都是用来标示空缺数据。但它们的行为在很多场景下确有一些相当大的差异。由于不熟悉这些差异，曾经给我的工作带来过不少麻烦。　特此整理了一份详细的实验，比较None和NaN在不同场景下的差异。

实验的结果有些在意料之内，有些则让我大跌眼镜。希望读者看过此文后会None和NaN这对“小妖精”有更深的理解。

为了理解本文的内容,希望本文的读者需要对pandas的Series使用有一定的经验。

首先，导入所需的库


```python
from numpy import NaN
from pandas import Series, DataFrame
import numpy as np
```

## 数据类型?
None是一个python特殊的数据类型， 但是NaN却是用一个特殊的float


```python
type(None)
```




    NoneType




```python
type(NaN)
```




    float



## 能作为dict的key?


```python
{None:1}
```




    {None: 1}




```python
{NaN:1}
```




    {nan: 1}




```python
{None:1, NaN:2}
```




    {nan: 2, None: 1}



都可以，而且会被认为是不同的key

## Series函数中的表现

### Series.map


```python
s = Series([None, NaN, 'a'])
s
```




    0    None
    1     NaN
    2       a
    dtype: object




```python
s.map({None:1,'a':'a'})
```




    0    1
    1    1
    2    a
    dtype: object



可以看到None和NaN都会替换成了1


```python
s.map({NaN:1,'a':'a'})
```




    0    1
    1    1
    2    a
    dtype: object



同样None和NaN都会替换成了1


```python
s.map({NaN:2,'None':1,'a':'a'})
```




    0    2
    1    2
    2    a
    dtype: object



将None替换成1的要求被忽略了


```python
s.map({'None':1,NaN:2,'a':'a'})
```




    0    2
    1    2
    2    a
    dtype: object



将NaN替换成1的要求被忽略了

**总结:**
用Series.map对None进行替换时,会“顺便”把NaN也一起替换掉；NaN也会顺便把None替换掉。

如果None和NaN分别定义了不同的映射数值，那么只有一个会生效。

### Series.replace中的表现


```python
s = Series([None, NaN, 'a'])
s
```




    0    None
    1     NaN
    2       a
    dtype: object




```python
s.replace([NaN],9)
```




    0    9
    1    9
    2    a
    dtype: object




```python
s.replace([None],9)
```




    0    9
    1    9
    2    a
    dtype: object



和Series.map的情况类似,指定了None的替换值后,NaN会被替换掉;反之亦然。

## 对函数的支持

numpy有不少函数可以自动处理NaN。


```python
np.nansum([1,2,NaN])
```




    3.0



但是None不能享受这些函数的便利，如果数据包含的None的话会报错


```python
try:
    np.nansum([1,2,None])
except Exception as e:
    print(type(e),e)
```

    <class 'TypeError'> unsupported operand type(s) for +: 'int' and 'NoneType'


pandas中也有不少函数支持NaN却不支持None。(毕竟pandas的底层是numpy)


```python
import pandas as pd
pd.cut(Series([NaN]),[1,2])
```




    0    NaN
    dtype: category
    Categories (1, object): [(1, 2]]




```python
import pandas as pd
try:
    pd.cut(Series([None]),[1,2])
except Exception as e:
    print(type(e),e)
```

    <class 'TypeError'> unorderable types: int() > NoneType()


## 对容器数据类型的影响

### 混入numpy.array的影响

如果数据中含有None,会导致整个array的类型变成object。


```python
np.array([1, None]).dtype
```




    dtype('O')



而np.NaN尽管会将原本用int类型就能保存的数据转型成float，但不会带来上面这个问题。


```python
np.array([1, NaN]).dtype
```




    dtype('float64')



### 混入Series的影响

下面的结果估计大家能猜到


```python
Series([1, NaN])
```




    0    1.0
    1    NaN
    dtype: float64



下面的这个就很意外的吧


```python
Series([1, None])
```




    0    1.0
    1    NaN
    dtype: float64



**pandas将None自动替换成了NaN！**


```python
Series([1.0, None])
```




    0    1.0
    1    NaN
    dtype: float64



却是Object类型的None被替换成了float类型的NaN。 这么设计可能是因为None无法参与numpy的大多数计算， 而pandas的底层又依赖于numpy，因此做了这样的自动转化。

不过如果本来Series就只能用object类型容纳的话， Series不会做这样的转化工作。


```python
Series(['a', None])
```




    0       a
    1    None
    dtype: object



如果Series里面都是None的话也不会做这样的转化


```python
Series([None,None])
```




    0    None
    1    None
    dtype: object



其它的数据类型是bool时，也不会做这样的转化。


```python
Series([True, False, None])
```




    0     True
    1    False
    2     None
    dtype: object



## 等值性判断

### 单值的等值性比较
下面的实验中None和NaN的表现会作为后面的等值性判断的基准(后文称为基准)


```python
None == None
```




    True




```python
NaN == NaN
```




    False




```python
None == NaN
```




    False



### 在tuple中的情况

这个不奇怪


```python
(1, None) == (1, None)
```




    True



这个也不意外


```python
(1, None) == (1, NaN)
```




    False



但是下面这个实验NaN的表现和基准不一致


```python
(1, NaN) == (1, NaN)
```




    True



### 在numpy.array中的情况


```python
np.array([1,None]) == np.array([1,None])
```




    array([ True,  True], dtype=bool)




```python
np.array([1,NaN]) == np.array([1,NaN])
```




    array([ True, False], dtype=bool)




```python
np.array([1,NaN]) == np.array([1,None])
```




    array([ True, False], dtype=bool)



和基准的表现一致。　

但是大部分情况我们希望上面例子中， 我们希望左右两边的array被判定成一致。这时可以用numpy.testing.assert_equal函数来处理。 注意这个函数的表现同assert， 不会返回True, False， 而是无反应或者raise Exception


```python
np.testing.assert_equal(np.array([1,NaN]), np.array([1,NaN]))
```

它也可以处理两边都是None的情况


```python
np.testing.assert_equal(np.array([1,None]), np.array([1,None]))
```

但是一边是None，一边是NaN时会被认为两边不一致, 导致AssertionError


```python
try:
    np.testing.assert_equal(np.array([1,NaN]), np.array([1,None]))
except Exception as e:
    print(type(e),e)
```

    <class 'AssertionError'> 
    Arrays are not equal
    
    (mismatch 50.0%)
     x: array([  1.,  nan])
     y: array([1, None], dtype=object)


### 在Series中的情况

下面两个实验中的表现和基准一致


```python
Series([NaN,'a']) == Series([NaN,'a'])
```




    0    False
    1     True
    dtype: bool




```python
Series([None,'a']) == Series([NaN,'a'])
```




    0    False
    1     True
    dtype: bool



但是None和基准的表现不一致。


```python
Series([None,'a']) == Series([None,'a'])
```




    0    False
    1     True
    dtype: bool



和array类似，Series也有专门的函数equals用于判断两边的Series是否整体看相等


```python
Series([None,'a']).equals(Series([NaN,'a']))
```




    True




```python
Series([None,'a']).equals(Series([None,'a']))
```




    True




```python
Series([NaN,'a']).equals(Series([NaN,'a']))
```




    True



比numpy.testing.assert_equals更智能些， 三种情况下都能恰当的处理

### 在DataFrame merge中的表现

两边的None会被判为相同


```python
a = DataFrame({'A':[None,'a']})
b = DataFrame({'A':[None,'a']})
a.merge(b,on='A', how = 'outer')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
    </tr>
  </tbody>
</table>
</div>



两边的NaN会被判为相同


```python
a = DataFrame({'A':[NaN,'a']})
b = DataFrame({'A':[NaN,'a']})
a.merge(b,on='A', how = 'outer')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
    </tr>
  </tbody>
</table>
</div>



无论两边都是None,都是NaN，还是都有,相关的列都会被正确的匹配。 注意一边是None,一边是NaN的时候。会以左侧的结果为准。


```python
a = DataFrame({'A':[None,'a']})
b = DataFrame({'A':[NaN,'a']})
a.merge(b,on='A', how = 'outer')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
    </tr>
  </tbody>
</table>
</div>




```python
a = DataFrame({'A':[NaN,'a']})
b = DataFrame({'A':[None,'a']})
a.merge(b,on='A', how = 'outer')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
    </tr>
  </tbody>
</table>
</div>



**注意**

这和空值在postgresql等sql数据库中的表现不一样， 在数据库中， join时两边的空值会被判定为不同的数值

## 在groupby中的表现


```python
d = DataFrame({'A':[1,1,1,1,2],'B':[None,None,'a','a','b']})
d.groupby(['A','B']).apply(len)
```




    A  B
    1  a    2
    2  b    1
    dtype: int64



可以看到(1, NaN)对应的组直接被忽略了


```python
d = DataFrame({'A':[1,1,1,1,2],'B':[None,None,'a','a','b']})
d.groupby(['A','B']).apply(len)
```




    A  B
    1  a    2
    2  b    1
    dtype: int64



(1,None)的组也被直接忽略了


```python
d = DataFrame({'A':[1,1,1,1,2],'B':[None,NaN,'a','a','b']})
d.groupby(['A','B']).apply(len)
```




    A  B
    1  a    2
    2  b    1
    dtype: int64



那么上面这个结果应该没啥意外的

**总结**

DataFrame.groupby会忽略分组列中含有None或者NaN的记录

## 支持写入数据库?

往数据库中写入时NaN不可处理，需转换成None,否则会报错。这个这里就不演示了。

相信作为pandas老司机， 至少能想出两种替换方法。


```python
s = Series([None,NaN,'a'])
s
```




    0    None
    1     NaN
    2       a
    dtype: object



方案１


```python
s.replace([NaN],None)
```




    0    None
    1    None
    2       a
    dtype: object



方案２


```python
s[s.isnull()]=None
s
```




    0    None
    1    None
    2       a
    dtype: object



然而这么就觉得完事大吉的话就图样图森破了， 看下面的例子


```python
s = Series([NaN,1])
s
```




    0    NaN
    1    1.0
    dtype: float64




```python
s.replace([NaN], None)
```




    0    NaN
    1    1.0
    dtype: float64




```python
s[s.isnull()] = None
s
```




    0    NaN
    1    1.0
    dtype: float64



当其他数据是int或float时,Series又一声不吭的自动把None替换成了NaN。

这时候可以使用第三种方法处理


```python
s.where(s.notnull(), None)
```




    0    None
    1       1
    dtype: object



where语句会遍历s中所有的元素，逐一检查条件表达式， 如果成立， 从原来的s取元素； 否则用None填充。 这回没有自动替换成NaN

<table>
</table>

## None vs NaN要点总结
1. 在pandas中， 如果其他的数据都是数值类型， pandas会把None自动替换成NaN, 甚至能将```s[s.isnull()]= None```,和```s.replace(NaN, None)```操作的效果无效化。 这时需要用where函数才能进行替换。 

2. None能够直接被导入数据库作为空值处理， 包含NaN的数据导入时会报错。

3. numpy和pandas的很多函数能处理NaN，但是如果遇到None就会报错。

4. None和NaN都不能被pandas的groupby函数处理，包含None或者NaN的组都会被忽略。


等值性比较的总结:（True表示被判定为相等）

|   	|   None对None	| NaN对NaN  	|None对NaN
|---	|---	|---	|
| 单值 | True	| False  	| False
| tuple(整体)|   True	| True  	|False
| np.array(逐个) 	| True  	| False   	|False
| Series(逐个) 	| False  	| False   	|False
| assert_equals 	| True  	| True   	|False
| Series.equals 	| True  	| True   	|True
| merge 	| True  	| True   	|True

由于等值性比较方面，None和NaN在各场景下表现不太一致，相对来说None表现的更稳定。

为了不给自己惹不必要的麻烦和额外的记忆负担。 实践中，建议遵循以下三个原则即可
* 在用pandas和numpy处理数据阶段将None,NaN统一处理成NaN,以便支持更多的函数。
* 如果要判断Series,numpy.array整体的等值性，用专门的Series.equals,numpy.array函数去处理，不要自己用```==```判断
*　如果要将数据导入数据库，将NaN替换成None
