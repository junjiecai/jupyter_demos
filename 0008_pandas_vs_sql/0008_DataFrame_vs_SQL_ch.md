
# 创建实验环境

## DataFrame中的同名列
大部分情况下，DataFrame都不鼓励DataFrame中出现同名列，单并不是完全禁止。

### merge的情况


```python
from pandas import DataFrame, Series
import pandas as pd
```


```python
df_1 = DataFrame({'A':[1,2,3],'B':[1,2,3]})
df_1
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
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_2 = DataFrame({'A':[1,2,3],'B':[1,2,3]})
df_2
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
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_1.merge(df_2,on='A')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B_x</th>
      <th>B_y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



可以看到merge函数会自动给两张表的同名列加上前缀以区分

如果强行去掉前缀， 那么会报错


```python
df_1.merge(df_2, on = 'A', suffixes = ['',''])
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-5-bd2fee1ec62b> in <module>()
    ----> 1 df_1.merge(df_2, on = 'A', suffixes = ['',''])
    

    /home/exolution/venv3.5/lib/python3.5/site-packages/pandas/core/frame.py in merge(self, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator)
       4435                      right_on=right_on, left_index=left_index,
       4436                      right_index=right_index, sort=sort, suffixes=suffixes,
    -> 4437                      copy=copy, indicator=indicator)
       4438 
       4439     def round(self, decimals=0, *args, **kwargs):


    /home/exolution/venv3.5/lib/python3.5/site-packages/pandas/tools/merge.py in merge(left, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator)
         37                          right_index=right_index, sort=sort, suffixes=suffixes,
         38                          copy=copy, indicator=indicator)
    ---> 39     return op.get_result()
         40 if __debug__:
         41     merge.__doc__ = _merge_doc % '\nleft : DataFrame'


    /home/exolution/venv3.5/lib/python3.5/site-packages/pandas/tools/merge.py in get_result(self)
        221 
        222         llabels, rlabels = items_overlap_with_suffix(ldata.items, lsuf,
    --> 223                                                      rdata.items, rsuf)
        224 
        225         lindexers = {1: left_indexer} if left_indexer is not None else {}


    /home/exolution/venv3.5/lib/python3.5/site-packages/pandas/core/internals.py in items_overlap_with_suffix(left, lsuffix, right, rsuffix)
       4443         if not lsuffix and not rsuffix:
       4444             raise ValueError('columns overlap but no suffix specified: %s' %
    -> 4445                              to_rename)
       4446 
       4447         def lrenamer(x):


    ValueError: columns overlap but no suffix specified: Index(['B'], dtype='object')


reset_index的时候，如果index的列名和已有的列名重复，那么会报错


```python
try:
    df = DataFrame({'A':[1,2,3]})
    df.index.name = 'A'
    df.reset_index()
except Exception as e:
    print(e)
```

    cannot insert A, already exists



```python
df = DataFrame({'A':[1,2,3,4],'B':[1,2,3,4]})
df
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
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



pd.concat则不会检查是否存在重名列


```python
df = pd.concat([df_1, df_2],axis=1)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>B</th>
      <th>A</th>
      <th>B</th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



renname函数也不会去检查列名是否一致


```python
df = DataFrame({'A':[1,2,3],'B':[1,2,3]})
df.rename(columns = {'B':'A'})
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



insert函数则会提供allow_duplicates参数，让用户去决定是否允许重名列存在。


```python
df_1.insert(0,'B',1,allow_duplicates=True)
df_1
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>B</th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>3</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



如果同名列存在， 那么用列名去选取列的是否， 会同时把所有的列名都选择出来

### 总结：
DataFrame中对于列名是否一致， 不同的函数表现并不一致。 有些允许， 有些禁止， 有些交由用户自己决定。 实践中， 我并没有遇到什么场景需要让两列的列名相同，建议避免出现这种情况。


```python
user = 'test'
password = 'test'
dbname = 'test'
port = '5432'
schema = 'test'

url = 'postgresql://{user}:{password}@localhost:{port}/{dbname}'.format(**locals())
```


```python
from sqlalchemy import create_engine, join, select

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from pandas import DataFrame, Series

drop_sql = 'drop table table_one'

engine = create_engine(url)
metadata = MetaData()
table_one = Table('table_one', metadata,
    Column('A', String),
    Column('B', Integer),
    Column('C', Integer),
    schema = 'test'
)

with engine.connect() as conn:
    try:
        conn.execute(drop_sql)
    except:
        pass    
    
metadata.create_all(engine)
```

如果创表的时候用了大写， 时候， 只能用'A'来选择


```python
s = "select 'A' from test.table_one"

with engine.connect() as conn:
    print(conn.execute(s).fetchall())
```

    []


sqlalchemy的话可以用A选择, 自动转成了'A'


```python
t = Table('table_one',metadata,schema = 'test')

s  = select(
    [t.c.A]
)

with engine.connect() as conn:
    print(conn.execute(s).fetchall())
```

    []



```python
print(s.compile())
```

    SELECT test.table_one."A" 
    FROM test.table_one


如果建表的时候用小写， 那么怎么选都可以


```python
from sqlalchemy import create_engine, join, select

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from pandas import DataFrame, Series

drop_sql = 'drop table table_one'

engine = create_engine(url)
metadata = MetaData()
table_one = Table('table_one', metadata,
    Column('a', String),
    Column('b', Integer),
    Column('c', Integer),
    schema = 'test'
)

with engine.connect() as conn:
    try:
        conn.execute(drop_sql)
    except:
        pass    
    
metadata.create_all(engine)
```


```python
s = "select 'a' from test.table_one"

with engine.connect() as conn:
    print(conn.execute(s).fetchall())
```

    []



```python
t = Table('table_one',metadata,schema = 'test')

s  = select(
    [t.c.a]
)

with engine.connect() as conn:
    print(conn.execute(s).fetchall())
```

    []


最简单的方法就是sqlalchemy中一律使用小写建表


```python
如果直接用SQL建表

sql = '''
    creat test.table(
        A INTEGER,
        B INTEGER
    )
'''
```


```python
with engine.connect() as conn:
    try:
        conn.execute(drop_sql)
    except:
        pass
        
    conn.execute(sql)
```


```python
user = 'test'
password = 'test'
dbname = 'test'
port = '5432'
schema = 'test'

url = 'postgresql://{user}:{password}@localhost:{port}/{dbname}'.format(**locals())

create_schema_sql = 'CREATE SCHEMA IF NOT EXISTS {schema_name}'.format(schema_name=schema)

engine = create_engine(url)
metadata = MetaData()
table_one = Table('table_one', metadata,
    Column('A', String),
    Column('B', Integer),
    Column('C', Integer),
    schema = schema
)

table_two = Table('table_two', metadata,
  Column('A', String),
  Column('B', Integer),
  Column('D', Integer),
  schema = schema                  
)

with engine.connect() as conn:
    conn.execute(create_schema_sql)
    
metadata.create_all(engine)

df_one = DataFrame.from_records(
    [
        ('a',1,1,),
        ('a',2,2,),        
        ('b',1,3,),                
        ('b',2,4,),   
    ]
    ,columns = ['a','b','c']
)
df_one


df_two = DataFrame.from_records(
    [
        ('a',1,11,),
        ('a',2,22,),        
        ('b',1,33,),                
        ('b',2,44,)      
    ]
    ,columns = ['a','b','d']
)
df_two

with engine.connect() as conn:
    df_one.to_sql('table_one', engine, if_exists = 'replace', schema = schema,index = False)
    df_two.to_sql('table_two', engine, if_exists = 'replace', schema = schema, index = False)  
    
```


```python
select 
    t.a
from
(
    select
        *
    from
        table_one
        full join
        table_two
        on table_one.a=table_two.a and table_one.b=table_two.b
) t;
```


```python
# astype(object)
```


```python
import numpy as np
import pandas as pd
```


```python
from sqlalchemy import case, literal, cast, literal_column, String, create_engine, MetaData, Table, select, and_, or_, func
import pandas as pd

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import warnings
warnings.filterwarnings('ignore')

from datetime import datetime, date
```

# PITFALL_1

## np.nan vs None
### 往数据库中写入时np.nan不可处理，需转换成None

在pandas.DataFrame中，np.nan和None是等价的。

但是，column.type是float64时，是以np.nan形式存在的；column.type是object时，是以None存在的。

而往数据库里insert(dataframe.to_records('dict'))时，存在np.nan会报错。必须转化成None。

to_sql中的表现


```python
df = pd.DataFrame({'A':[np.nan, 1, 2], 'B':[1,2,None]})
print(df)
for column in df:
    print(df.loc[df[column].isnull(),column])
```

         A    B
    0  NaN  1.0
    1  1.0  2.0
    2  2.0  NaN
    0   NaN
    Name: A, dtype: float64
    2   NaN
    Name: B, dtype: float64



```python
type(df['A'].iloc[0])
```




    numpy.float64




```python
type(df['B'].iloc[2])
```




    numpy.float64




```python
df = pd.DataFrame({'A':[np.nan, 1, 2], 'B':[1,2,None]})
print(df)
for column in df:
    print(df.loc[pd.isnull(df[column]),column])
```

         A    B
    0  NaN  1.0
    1  1.0  2.0
    2  2.0  NaN
    0   NaN
    Name: A, dtype: float64
    2   NaN
    Name: B, dtype: float64



```python
df = pd.DataFrame({'A':[np.nan, '1', '2'], 'B':['1','2',None]})
print(df)

for column in df:
    df.loc[pd.isnull(df[column]),column] = None
    df[column] = df[column].astype(float)
df
```

         A     B
    0  NaN     1
    1    1     2
    2    2  None





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
      <td>NaN</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = pd.DataFrame({'A':[np.nan, '1', '2'], 'B':['1','2',None]})
print(df)

for column in df:
    df[column] = df[column].astype(float)
    df.loc[pd.isnull(df[column]),column] = None
df
```

         A     B
    0  NaN     1
    1    1     2
    2    2  None





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
      <td>NaN</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = pd.DataFrame({'A':[np.nan, '1', '2'], 'B':['1','2',None]})
print(df)

for column in df:
    df.loc[pd.isnull(df[column]),column] = None
    df[column] = df[column].astype(object)
df
```

         A     B
    0  NaN     1
    1    1     2
    2    2  None





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
      <td>None</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



# PITFALL_2
## 判断两个dataframe是否相同
__注意行和列的顺序都要一致,且数据类型要一致。__
* assert df1.equals(df2) 
* np.testing.assert_equal(df1.values, df2.values)

pandas中默认空值=空值（np.nan 和 None等价），np认为它们不一样

df1.values == df2.values 无法处理空值的情况，慎用！


```python
df1 = pd.DataFrame({'A':[1,3,2],'B':[4,6,None]})
df2 = pd.DataFrame({'A':[1,2,3],'B':[4,None,6]})
```


```python
df2.dtypes
```




    A      int64
    B    float64
    dtype: object




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
      <td>4.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>NaN</td>
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
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>6.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
df2.values
```




    array([[  1.,   4.],
           [  2.,  nan],
           [  3.,   6.]])




```python
df1.sort_values('A').values == df2.values
```




    array([[ True,  True],
           [ True, False],
           [ True,  True]], dtype=bool)




```python
df2.equals(df1) #错误原因：顺序不对
```




    False




```python
df2.equals(df1.sort_values('A')) #顺序对了，但是index不一致
```




    False




```python
new_df1 = df1.sort_values('A').reset_index().drop('index', axis=1)
new_df2 = df2.sort_values('A').reset_index().drop('index', axis=1)
new_df2.equals(new_df1)#此方法是先排序再删掉index再重构index
```




    True




```python
np.testing.assert_equal(df1.sort_values('A').values, df2.values)
#此方法只要顺序对了就好，index不影响，但是存在下面的问题
```

### 类型一致时：pandas中默认空值=空值（np.nan 和 None等价），np认为它们不一样


```python
df4 = df2.copy()
df4['B']=df4['B'].astype(object)
df4.dtypes
```




    A     int64
    B    object
    dtype: object




```python
df4
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
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>




```python
df3=df4.copy()
df3.loc[1,'B']=None
df3
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
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>




```python
df3.dtypes
```




    A     int64
    B    object
    dtype: object




```python
df3.equals(df4)
```




    True




```python
np.testing.assert_equal(df3.values, df4.values)
```


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    <ipython-input-146-10cc9a42b1e3> in <module>()
    ----> 1 np.testing.assert_equal(df3.values, df4.values)
    

    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/numpy/testing/utils.py in assert_equal(actual, desired, err_msg, verbose)
        320     from numpy.lib import iscomplexobj, real, imag
        321     if isinstance(actual, ndarray) or isinstance(desired, ndarray):
    --> 322         return assert_array_equal(actual, desired, err_msg, verbose)
        323     msg = build_err_msg([actual, desired], err_msg, verbose=verbose)
        324 


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/numpy/testing/utils.py in assert_array_equal(x, y, err_msg, verbose)
        811     """
        812     assert_array_compare(operator.__eq__, x, y, err_msg=err_msg,
    --> 813                          verbose=verbose, header='Arrays are not equal')
        814 
        815 def assert_array_almost_equal(x, y, decimal=6, err_msg='', verbose=True):


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/numpy/testing/utils.py in assert_array_compare(comparison, x, y, err_msg, verbose, header, precision)
        737                                 names=('x', 'y'), precision=precision)
        738             if not cond:
    --> 739                 raise AssertionError(msg)
        740     except ValueError:
        741         import traceback


    AssertionError: 
    Arrays are not equal
    
    (mismatch 16.66666666666667%)
     x: array([[1, 4.0],
           [2, None],
           [3, 6.0]], dtype=object)
     y: array([[1, 4.0],
           [2, nan],
           [3, 6.0]], dtype=object)


# PIDFALL_3
## 列名重复问题

在panda中，表格merge之后，不同表中的相同名字的列会被以_x,_y结尾保留下来，

但在sqlalchemy中，列名还维持在原来的状态，编写sql语句时不会报错，但是拉取数据结果时，会报错


```python
df5 = pd.DataFrame({'A':['a','b','c'],'B':['x','y','x'],'C':[4,6,7]})
df6 = pd.DataFrame({'B':['x','y','x'],'C':[4,6,8]})
```


```python
df5
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
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>x</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>




```python
df6
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>x</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>y</td>
      <td>6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>x</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
df5.merge(df6,on='B',how='left')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C_x</th>
      <th>C_y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
      <td>6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>c</td>
      <td>x</td>
      <td>7</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>c</td>
      <td>x</td>
      <td>7</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
engine = create_engine('postgresql://datascience:Jrsjkxzbbd2333@localhost/etl')
```


```python
df5.to_sql('df5',engine,index=False,if_exists='replace')
df6.to_sql('df6',engine,index=False,if_exists='replace')
```


```python
metadata=MetaData(engine)
table5 = Table('df5',metadata,autoload=True)
table6 = Table('df6',metadata,autoload=True)
```


```python
s = select([table5, table6]).where(table5.c.B == table6.c.B).alias()
```


```python
print(s.c.keys()) # 是否有columns的attribute
```

    ['A', 'B', 'C']



```python
# 在数据库中直接跑sql的情况
```


```python
pd.read_sql(s,engine)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>x</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>x</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>x</td>
      <td>7</td>
      <td>x</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>c</td>
      <td>x</td>
      <td>7</td>
      <td>x</td>
      <td>8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
      <td>y</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



什么鬼？两个B，而且C不会改名字！！！我要把B拉出来看看～


```python
pd.read_sql(select([s.c.B]),engine)#B拉不出来，因为有两个B，不知道拉哪个，尽管两个B的值是一样的
```


    ---------------------------------------------------------------------------

    ProgrammingError                          Traceback (most recent call last)

    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/base.py in _execute_context(self, dialect, constructor, statement, parameters, *args)
       1181                         parameters,
    -> 1182                         context)
       1183         except BaseException as e:


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/default.py in do_execute(self, cursor, statement, parameters, context)
        468     def do_execute(self, cursor, statement, parameters, context=None):
    --> 469         cursor.execute(statement, parameters)
        470 


    ProgrammingError: column reference "B" is ambiguous
    LINE 1: SELECT anon_1."B" 
                   ^


    
    The above exception was the direct cause of the following exception:


    ProgrammingError                          Traceback (most recent call last)

    <ipython-input-157-c018a36890e8> in <module>()
    ----> 1 pd.read_sql(select([s.c.B]),engine)#B拉不出来，因为有两个B，不知道拉哪个，尽管两个B的值是一样的
    

    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/pandas/io/sql.py in read_sql(sql, con, index_col, coerce_float, params, parse_dates, columns, chunksize)
        413             sql, index_col=index_col, params=params,
        414             coerce_float=coerce_float, parse_dates=parse_dates,
    --> 415             chunksize=chunksize)
        416 
        417 


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/pandas/io/sql.py in read_query(self, sql, index_col, coerce_float, parse_dates, params, chunksize)
       1082         args = _convert_params(sql, params)
       1083 
    -> 1084         result = self.execute(*args)
       1085         columns = result.keys()
       1086 


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/pandas/io/sql.py in execute(self, *args, **kwargs)
        973     def execute(self, *args, **kwargs):
        974         """Simple passthrough to SQLAlchemy connectable"""
    --> 975         return self.connectable.execute(*args, **kwargs)
        976 
        977     def read_table(self, table_name, index_col=None, coerce_float=True,


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/base.py in execute(self, statement, *multiparams, **params)
       2053 
       2054         connection = self.contextual_connect(close_with_result=True)
    -> 2055         return connection.execute(statement, *multiparams, **params)
       2056 
       2057     def scalar(self, statement, *multiparams, **params):


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/base.py in execute(self, object, *multiparams, **params)
        943             raise exc.ObjectNotExecutableError(object)
        944         else:
    --> 945             return meth(self, multiparams, params)
        946 
        947     def _execute_function(self, func, multiparams, params):


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/sql/elements.py in _execute_on_connection(self, connection, multiparams, params)
        261     def _execute_on_connection(self, connection, multiparams, params):
        262         if self.supports_execution:
    --> 263             return connection._execute_clauseelement(self, multiparams, params)
        264         else:
        265             raise exc.ObjectNotExecutableError(self)


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/base.py in _execute_clauseelement(self, elem, multiparams, params)
       1051             compiled_sql,
       1052             distilled_params,
    -> 1053             compiled_sql, distilled_params
       1054         )
       1055         if self._has_events or self.engine._has_events:


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/base.py in _execute_context(self, dialect, constructor, statement, parameters, *args)
       1187                 parameters,
       1188                 cursor,
    -> 1189                 context)
       1190 
       1191         if self._has_events or self.engine._has_events:


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/base.py in _handle_dbapi_exception(self, e, statement, parameters, cursor, context)
       1391                 util.raise_from_cause(
       1392                     sqlalchemy_exception,
    -> 1393                     exc_info
       1394                 )
       1395             else:


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/util/compat.py in raise_from_cause(exception, exc_info)
        200     exc_type, exc_value, exc_tb = exc_info
        201     cause = exc_value if exc_value is not exception else None
    --> 202     reraise(type(exception), exception, tb=exc_tb, cause=cause)
        203 
        204 if py3k:


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/util/compat.py in reraise(tp, value, tb, cause)
        183             value.__cause__ = cause
        184         if value.__traceback__ is not tb:
    --> 185             raise value.with_traceback(tb)
        186         raise value
        187 


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/base.py in _execute_context(self, dialect, constructor, statement, parameters, *args)
       1180                         statement,
       1181                         parameters,
    -> 1182                         context)
       1183         except BaseException as e:
       1184             self._handle_dbapi_exception(


    /home/finance-datascience/CJJ/datascience/venv/lib/python3.5/site-packages/sqlalchemy/engine/default.py in do_execute(self, cursor, statement, parameters, context)
        467 
        468     def do_execute(self, cursor, statement, parameters, context=None):
    --> 469         cursor.execute(statement, parameters)
        470 
        471     def do_execute_no_params(self, cursor, statement, context=None):


    ProgrammingError: (psycopg2.ProgrammingError) column reference "B" is ambiguous
    LINE 1: SELECT anon_1."B" 
                   ^
     [SQL: 'SELECT anon_1."B" \nFROM (SELECT df5."A" AS "A", df5."B" AS "B", df5."C" AS "C", df6."B" AS "B", df6."C" AS "C" \nFROM df5, df6 \nWHERE df5."B" = df6."B") AS anon_1']



```python
print(sql.compile(compile_kwargs={"literal_binds": True}))
```

    df5 LEFT OUTER JOIN df6 ON df5."B" = df6."B"


# PIDFALL_4


```python
df7 = pd.DataFrame({'A':['a','b','c'],'B':['x','y',None],'C':[4,6,7]})
df8 = pd.DataFrame({'A':['a','b','c'],'B':['x','y',None],'D':[1,2,3]})
```


```python
df7
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
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>None</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>




```python
df8
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>None</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
df7.merge(df8,on=['A','B'],how='left')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>None</td>
      <td>7</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
df7.to_sql('df7',engine,index=False,if_exists='replace')
df8.to_sql('df8',engine,index=False,if_exists='replace')

table7 = Table('df7',metadata,autoload=True)
table8 = Table('df8',metadata,autoload=True)
```


```python
s = select(
    [
        table7, 
        table8.c.D
    ]
).where(
    and_(
        table7.c.B == table8.c.B,
        table7.c.A == table8.c.A
    )
).alias()
```


```python
pd.read_sql(s,engine)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```python
s2 = select(
    [
        table7, 
        table8.c.D
    ]
).select_from(
    table7.outerjoin(
        table8,
        and_(
            table7.c.B == table8.c.B,
            table7.c.A == table8.c.A
        )
    )
).alias()
```


```python
pd.read_sql(s2,engine)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>None</td>
      <td>7</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
s3 = select(
    [
        table7, 
        table8.c.D
    ]
).select_from(
    table7.outerjoin(
        table8,
        and_(
            table7.c.B == table8.c.B,
            table7.c.A == table8.c.A
        ),full=True
    )
).alias()
```


```python
pd.read_sql(s3,engine)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>6.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>None</td>
      <td>7.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>3.0</td>
    </tr>
  </tbody>
</table>
</div>



若想要pandas里面的效果，即None=None，


```python
s4 = select(
    [
        table7, 
        table8.c.D
    ]
).select_from(
    table7.outerjoin(
        table8,
        and_(
            
            table7.c.A == table8.c.A,
            or_(
                table7.c.B == table8.c.B,
                and_(
                    table7.c.B ==None,
                    table8.c.B ==None
                )
            )
        )
    )
).alias()
```


```python
pd.read_sql(s4,engine)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>x</td>
      <td>4</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>y</td>
      <td>6</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>None</td>
      <td>7</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
metadata.drop_all(engine, checkfirst=True)
```


```python
from pandas import Series
from numpy import NaN
```


```python
s = Series([None, NaN, 'a'])
s
```




    0    None
    1     NaN
    2       a
    dtype: object




```python
s == None
```




    0    False
    1    False
    2    False
    dtype: bool




```python
s == NaN
```




    0    False
    1    False
    2    False
    dtype: bool




```python
s.isnull()
```




    0     True
    1     True
    2    False
    dtype: bool




```python
s is None
```




    False




```python
s.apply(lambda s:s is None)
```




    0     True
    1    False
    2    False
    dtype: bool




```python
a = [1,2]

b = [1,2]
```


```python
a==b
```




    True




```python
a is b
```




    False




```python
a = [1,2]

b = a

a is b
```




    True




```python
from pandas import DataFrame
```


```python
a=DataFrame(index=[1,2,3,4,5])
```


```python
b=DataFrame(index=['1','2','3','4','5'])
```


```python
a
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
    </tr>
    <tr>
      <th>2</th>
    </tr>
    <tr>
      <th>3</th>
    </tr>
    <tr>
      <th>4</th>
    </tr>
    <tr>
      <th>5</th>
    </tr>
  </tbody>
</table>
</div>




```python
b
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
    </tr>
    <tr>
      <th>2</th>
    </tr>
    <tr>
      <th>3</th>
    </tr>
    <tr>
      <th>4</th>
    </tr>
    <tr>
      <th>5</th>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
and  &

a={'c':1233}
a=None

if （a is not None） & a['c'] =1233 :
    
if pd.notnull(a) and a['c'] =1233 :
```


```python
s1 = Series([1,2,3])
s2 = Series([])
```


```python
s2 and s1
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-24-a87cc019d158> in <module>()
    ----> 1 s2 and s1
    

    /home/exolution/.local/lib/python3.5/site-packages/pandas/core/generic.py in __nonzero__(self)
        890         raise ValueError("The truth value of a {0} is ambiguous. "
        891                          "Use a.empty, a.bool(), a.item(), a.any() or a.all()."
    --> 892                          .format(self.__class__.__name__))
        893 
        894     __bool__ = __nonzero__


    ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().



```python
bool([1,2,3] and [])
```




    False




```python
[1,2,3] or []
```




    [1, 2, 3]




```python
x  = [1,2,3,4]


x or [1,1,1]
```




    [1, 2, 3, 4]




```python
s1 = Series([True, False])
s1
```




    0     True
    1    False
    dtype: bool




```python
s2 = Series([True, True])
s2
```




    0    True
    1    True
    dtype: bool




```python
s1&s2
```




    0     True
    1    False
    dtype: bool




```python

```
