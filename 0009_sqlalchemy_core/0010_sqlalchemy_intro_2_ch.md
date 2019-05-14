
## 说明

接[sqlalchemy入门(上)](http://junjiecai.github.io/posts/2017/Jan/17/sqlalchemy_intro_1/)，这篇会更详细的讲解和演示如果用SQLAlchemy完成Select, Update, Delete的操作。

## 准备
实验准备内容和[sqlalchemy入门(上)](http://junjiecai.github.io/posts/2017/Jan/17/sqlalchemy_intro_1/)的内容一致，这里不在重复多说。


```python
from sqlalchemy import create_engine

user = 'test'
password = 'test'
port = '5432'
dbname = 'test'

engine = create_engine('postgresql://{user}:{password}@localhost:{port}/{dbname}'.format(**locals()))

from helper import reset_tables,clear_tables,clear_schema,get_select,get_table,print_sql
from IPython.display import display
```

## 选择

### 选择全部列
选择全部的列


```python
users, addresses = reset_tables(engine)

s = users.select()

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, test.users.fullname 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>fullname</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack</td>
      <td>Jack Jones</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>wendy</td>
      <td>Wendy Williams</td>
    </tr>
  </tbody>
</table>
</div>


可以用下面方法得到涉及的列名


```python
s.c.keys()
```




    ['id', 'name', 'fullname']



另一种稍繁琐但是更通用的方法


```python
from sqlalchemy import select

s = select(
    [
        users
    ]
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, test.users.fullname 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>fullname</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack</td>
      <td>Jack Jones</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>wendy</td>
      <td>Wendy Williams</td>
    </tr>
  </tbody>
</table>
</div>


### 选择指定列
可以在select的list中指定需要的列


```python
s = select(
    [
        users.c.id,
        users.c.fullname,
    ]
)
print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.fullname 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>fullname</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Jack Jones</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Wendy Williams</td>
    </tr>
  </tbody>
</table>
</div>


也可以用下面这种语法指定要选择的列。好处是可以支持变量作为列名。


```python
colname = 'fullname'

s = select(
    [
        users.c['id'],
        users.c[colname]
    ]
)
print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.fullname 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>fullname</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Jack Jones</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Wendy Williams</td>
    </tr>
  </tbody>
</table>
</div>


<div class='article note'>注意</div>
上面的几个例子,并没有指定FROM条件,SQLAlchemy自动添加了FROM语句。。

### 修改列名
用label实现


```python
s = select(
    [
        users.c.id.label('user_id'),
        users.c.name.label('user_name'),
    ]
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id AS user_id, test.users.name AS user_name 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>user_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>wendy</td>
    </tr>
  </tbody>
</table>
</div>


### 选择计算后的结果
选择的时候也可以进行一些运算。例如字符串拼接。


```python
s = select(
    [
        users.c.id,
        ('Fullname:'+users.c.fullname).label('fullname')
    ]
)
print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, 'Fullname:' || test.users.fullname AS fullname 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>fullname</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Fullname:Jack Jones</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Fullname:Wendy Williams</td>
    </tr>
  </tbody>
</table>
</div>


下面是数值相加的例子。


```python
s = select(
    [
        users.c.id,
        (10+users.c.id).label('new_id')
    ]
)
print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, 10 + test.users.id AS new_id 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>new_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>12</td>
    </tr>
  </tbody>
</table>
</div>


<div class = 'article note'>注意</div>

上面的两个例子里，都使用了'+'号,SQLAlchemy根据数据类型自动决定编译后的结果是字符串连接还是数值相加。

### 使用sql function
可以使用func.func_name的形式应用函数,使用的时候只需要导入func模块,接上数据库中的函数名即可


```python
from sqlalchemy import func

s = select(
    [
        users.c.id.label('user_id'),
        func.upper(users.c.name).label('user_name'),
    ]
)

print_sql(engine,s,False)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id AS user_id, upper(test.users.name) AS user_name 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>user_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>JACK</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>WENDY</td>
    </tr>
  </tbody>
</table>
</div>


注意应用函数的时候，label要放在在函数之外使用，否则是无效的，这是一个容易犯的错误。可以看到下面的例子里，name列采用了自动命名。


```python
from sqlalchemy import func

s = select(
    [
        users.c.id.label('user_id'),
        func.upper(users.c.name.label('user_name')),
    ]
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id AS user_id, upper(test.users.name) AS upper_1 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>upper(test.users.name)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>JACK</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>WENDY</td>
    </tr>
  </tbody>
</table>
</div>


### 使用window function

使用```func.func_name().over()```的方式即可


```python
s = select([
        users.c.id,
        users.c.name,
        func.row_number().over(
            order_by=users.c.name,
        ).label('num')
    ])

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, row_number() OVER (ORDER BY test.users.name) AS num 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>num</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>wendy</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>


### 使用case


```python
from sqlalchemy import case

s = select(
    [
        case(
            [
                (users.c.id == 1, 'A'),
                (users.c.id == 3, 'C'),
            ],
            else_='B'
        ).label('case_test')
    ]
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT CASE WHEN (test.users.id = 1) THEN 'A' WHEN (test.users.id = 3) THEN 'C' ELSE 'B' END AS case_test 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>case_test</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B</td>
    </tr>
  </tbody>
</table>
</div>


### 添加常数列


```python
from sqlalchemy import literal, text,literal_column

s = select(
    [
        users.c.id.label('user_id'),
        literal('AAAAAA').label('constant'),
        literal(None).label('null')        
    ]
)

print_sql(engine,s,False)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id AS user_id, %(param_1)s AS constant, %(param_2)s AS "null" 
    FROM test.users
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>constant</th>
      <th>null</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>AAAAAA</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>AAAAAA</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>


### 指定limit and offset

例如用offset跳过1行，并且用limit只显示2行


```python
s = (
    select(
        [
            addresses.c.id,
            addresses.c.email_address,
        ]
    ).offset(1)
    .limit(2)
)


print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.addresses.id, test.addresses.email_address 
    FROM test.addresses 
     LIMIT 2 OFFSET 1
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>email_address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>jack@msn.com</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>www@www.org</td>
    </tr>
  </tbody>
</table>
</div>


### Order By排序

下面的例子中根据user.id和user.name排序


```python
s = select(
    [users.c.name]
).order_by(
    users.c.id,
    users.c.name
)
print_sql(engine,s)
display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.name 
    FROM test.users ORDER BY test.users.id, test.users.name
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>jack</td>
    </tr>
    <tr>
      <th>1</th>
      <td>wendy</td>
    </tr>
  </tbody>
</table>
</div>


如果要控制升序降序的话。可以调用desc()方法或者使用desc函数。


```python
s = select(
    [users.c.name]
).order_by(
    users.c.id.desc(),    
    users.c.name.desc()
)
print_sql(engine,s)
display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.name 
    FROM test.users ORDER BY test.users.id DESC, test.users.name DESC
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>wendy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>jack</td>
    </tr>
  </tbody>
</table>
</div>



```python
from sqlalchemy import desc
s = select(
    [users.c.name]
).order_by(
    desc(users.c.id),
    desc(users.c.name)
)
print_sql(engine,s)
display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.name 
    FROM test.users ORDER BY test.users.id DESC, test.users.name DESC
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>wendy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>jack</td>
    </tr>
  </tbody>
</table>
</div>


### Group By


```python
s = (
    select(
            [
                users.c.name,
                func.count(addresses.c.id).label('count')
            ]
        ) 
        .select_from(users.join(addresses))
        .group_by(users.c.name)      

)
print_sql(engine,s)
display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.name, count(test.addresses.id) AS count 
    FROM test.users JOIN test.addresses ON test.users.id = test.addresses.user_id GROUP BY test.users.name
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>wendy</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>jack</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>


如果要根据多列去做group by的话


```python
s = (
    select(
            [
                users.c.name,
                func.count(addresses.c.id).label('count')
            ]
        ) 
        .select_from(users.join(addresses))
        .group_by(
            users.c.id,
            users.c.name
    )
)
print_sql(engine,s)
display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.name, count(test.addresses.id) AS count 
    FROM test.users JOIN test.addresses ON test.users.id = test.addresses.user_id GROUP BY test.users.id, test.users.name
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>jack</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>wendy</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>


### 使用Having条件


```python
s = (
    select(
            [
                users.c.name,
                func.count(addresses.c.id).label('count')
            ]
    )
    .select_from(users.join(addresses))
    .group_by(users.c.name)
    .having(func.count(addresses.c.id)>1)
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.name, count(test.addresses.id) AS count 
    FROM test.users JOIN test.addresses ON test.users.id = test.addresses.user_id GROUP BY test.users.name 
    HAVING count(test.addresses.id) > 1
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>wendy</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>jack</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>


## 集合操作
这里至演示```union_all```。 ```union```， ```except_```， ```except_all```， ```intersect```， ```intersect_all```同理，不再演示。


```python
from sqlalchemy.sql import union, union_all, except_, except_all, intersect,intersect_all

s = union_all(
    addresses.select().where(addresses.c.email_address == 'foo@bar.com'),
    addresses.select().where(addresses.c.email_address.like('%@yahoo.com')),
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.addresses.id, test.addresses.user_id, test.addresses.email_address 
    FROM test.addresses 
    WHERE test.addresses.email_address = 'foo@bar.com' UNION ALL SELECT test.addresses.id, test.addresses.user_id, test.addresses.email_address 
    FROM test.addresses 
    WHERE test.addresses.email_address LIKE '%@yahoo.com'
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>user_id</th>
      <th>email_address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>jack@yahoo.com</td>
    </tr>
  </tbody>
</table>
</div>


### where条件


```python
s = select(
    [
        users,
        addresses.c.user_id,
        addresses.c.email_address,        
    ]
).where(
    users.c.id == addresses.c.user_id
)

print_sql(engine,s)
display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, test.users.fullname, test.addresses.user_id, test.addresses.email_address 
    FROM test.users, test.addresses 
    WHERE test.users.id = test.addresses.user_id
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>fullname</th>
      <th>user_id</th>
      <th>email_address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack</td>
      <td>Jack Jones</td>
      <td>1</td>
      <td>jack@yahoo.com</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>jack</td>
      <td>Jack Jones</td>
      <td>1</td>
      <td>jack@msn.com</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>wendy</td>
      <td>Wendy Williams</td>
      <td>2</td>
      <td>www@www.org</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>wendy</td>
      <td>Wendy Williams</td>
      <td>2</td>
      <td>wendy@aol.com</td>
    </tr>
  </tbody>
</table>
</div>


常见的where条件

#### 等于


```python
print_sql(engine,users.c.id == addresses.c.user_id)
```

    ***Compiled SQL***
    <<<
    test.users.id = test.addresses.user_id
    >>>


#### 大于


```python
print_sql(engine,users.c.id > addresses.c.user_id)
```

    ***Compiled SQL***
    <<<
    test.users.id > test.addresses.user_id
    >>>


#### 不等于


```python
print_sql(engine,users.c.id != addresses.c.user_id)
```

    ***Compiled SQL***
    <<<
    test.users.id != test.addresses.user_id
    >>>


有些条件需要调用方法实现，例如表现SQL中的IN的时候，这样是不行的


```python
print(users.c.id in [1,2,3])
```

    False


而是应该用object本身提供的函数in_


```python
s = users.c.id.in_([1,2,3])
print_sql(engine,s,compile_kwargs={"literal_binds": True})
```

    ***Compiled SQL***
    <<<
    test.users.id IN (1, 2, 3)
    >>>


类似的有between


```python
s = users.c.id.between(1,3)
print_sql(engine,s,compile_kwargs={"literal_binds": True})
```

    ***Compiled SQL***
    <<<
    test.users.id BETWEEN 1 AND 3
    >>>


字符串匹配like


```python
s = users.c.name.like('C%')
print_sql(engine,s,compile_kwargs={"literal_binds": True})
```

    ***Compiled SQL***
    <<<
    test.users.name LIKE 'C%'
    >>>


### 特殊的算符

如果有一些非常规的operator，总是可以用.op方法取实现


```python
s = users.c.id.op('special_operator')('foo')
print_sql(engine,s)
```

    ***Compiled SQL***
    <<<
    test.users.id special_operator 'foo'
    >>>


### 逻辑连词
最常用的有```and_```, ```or_```, ```not_```


```python
from sqlalchemy.sql import and_, or_, not_

s = and_(
    users.c.name.like('j%'),
    users.c.id == addresses.c.user_id,
    or_(
        addresses.c.email_address == 'wendy@aol.com',
        addresses.c.email_address == 'jack@yahoo.com'
    ),
    not_(users.c.id > 5)
)

print_sql(engine,s)
```

    ***Compiled SQL***
    <<<
    test.users.name LIKE 'j%' AND test.users.id = test.addresses.user_id AND (test.addresses.email_address = 'wendy@aol.com' OR test.addresses.email_address = 'jack@yahoo.com') AND test.users.id <= 5
    >>>


连续多个where连用也可以起到and的效果


```python
s=(
    select(
        [users]
    )
    .where(users.c.name.like('j%'))
    .where(users.c.id == addresses.c.user_id)
)

print_sql(engine,s,compile_kwargs={"literal_binds": True})
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, test.users.fullname 
    FROM test.users, test.addresses 
    WHERE test.users.name LIKE 'j%' AND test.users.id = test.addresses.user_id
    >>>


也可以用python的```&```,```|```,```~```等逻辑连接符号代替```and_()```, ```or_()```, ```not_```


```python
s = (
    users.c.name.like('j%') &
    users.c.id == addresses.c.user_id &
    (
        (addresses.c.email_address == 'wendy@aol.com') |
        (addresses.c.email_address == 'jack@yahoo.com')
    ) &
    (~(users.c.id > 5))
)
print_sql(engine,s,compile_kwargs={"literal_binds": True})
```

    ***Compiled SQL***
    <<<
    (test.users.name LIKE 'j%' AND test.users.id) = (test.addresses.user_id AND (test.addresses.email_address = 'wendy@aol.com' OR test.addresses.email_address = 'jack@yahoo.com') AND test.users.id <= 5)
    >>>


### join表


```python
s = users.join(
    addresses,
    users.c.id==addresses.c.user_id
)

print_sql(engine,s)
```

    ***Compiled SQL***
    <<<
    test.users JOIN test.addresses ON test.users.id = test.addresses.user_id
    >>>


#### 自动Join

如果join时没有指定on条件。SQLAlchemy会去检查是否存在foreign key的定义。

helper.py的reset_tables函数中，已经定义了users.id是addresses.user_id的外键。所以下面的语句能自动添加```test.users.id = test.addresses.user_id```的条件。


```python
s = users.join(addresses)
print_sql(engine,s)
```

    ***Compiled SQL***
    <<<
    test.users JOIN test.addresses ON test.users.id = test.addresses.user_id
    >>>


<div class = 'article warning'>注意</div>

auto_load得到的表无法找到正确的foreign_key


```python
from sqlalchemy import MetaData, Table
metadata = MetaData()
addresses = Table('addresses', metadata, schema = 'test', autoload=True, autoload_with=engine)
addresses.c.values()
```




    [Column('id', INTEGER(), table=<addresses>, primary_key=True, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f77c191f588>, for_update=False)),
     Column('user_id', INTEGER(), ForeignKey('test.users.id'), table=<addresses>),
     Column('email_address', VARCHAR(length=20), table=<addresses>, nullable=False)]



看上去定义了foreign key的信息,但是运行的话会出错


```python
try:
    s = users.join(addresses)
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.NoForeignKeysError'> Can't find any foreign key relationships between 'users' and 'addresses'.


#### select_from
如果要将join语句用于select的话，可以用select_from语句,功能相当于SQL中的FROM。


```python
s = (
    select(
        [
            users.c.id, 
            addresses.c.email_address
        ]
    )
    .select_from(
        users.join(addresses)
    )
    .where(users.c.id==1)    
)

print_sql(engine,s)

display(get_select(engine,s))
```


    ---------------------------------------------------------------------------

    NoForeignKeysError                        Traceback (most recent call last)

    <ipython-input-39-cbf3aec0ec91> in <module>()
          7     )
          8     .select_from(
    ----> 9         users.join(addresses)
         10     )
         11     .where(users.c.id==1)


    /home/exolution/venv3.5/lib/python3.5/site-packages/sqlalchemy/sql/selectable.py in join(self, right, onclause, isouter, full)
        446         """
        447 
    --> 448         return Join(self, right, onclause, isouter, full)
        449 
        450     def outerjoin(self, right, onclause=None, full=False):


    /home/exolution/venv3.5/lib/python3.5/site-packages/sqlalchemy/sql/selectable.py in __init__(self, left, right, onclause, isouter, full)
        792 
        793         if onclause is None:
    --> 794             self.onclause = self._match_primaries(self.left, self.right)
        795         else:
        796             self.onclause = onclause


    /home/exolution/venv3.5/lib/python3.5/site-packages/sqlalchemy/sql/selectable.py in _match_primaries(self, left, right)
        926         else:
        927             left_right = None
    --> 928         return self._join_condition(left, right, a_subset=left_right)
        929 
        930     @classmethod


    /home/exolution/venv3.5/lib/python3.5/site-packages/sqlalchemy/sql/selectable.py in _join_condition(cls, a, b, ignore_nonexistent_tables, a_subset, consider_as_foreign_keys)
        974                 "Can't find any foreign key relationships "
        975                 "between '%s' and '%s'.%s" %
    --> 976                 (a.description, b.description, hint))
        977 
        978         crit = [(x == y) for x, y in list(constraints.values())[0]]


    NoForeignKeysError: Can't find any foreign key relationships between 'users' and 'addresses'.


#### Left Join
如果要使用left outer join，把join换成outerjoin


```python
s = (
    select(
        [
            users.c.id, 
            addresses.c.email_address
        ]
    )
    .where(users.c.id==1)
    .select_from(users.outerjoin(addresses))
)

print_sql(engine,s,compile_kwargs={"literal_binds": True})
```

#### Outer Join
如果要使用outer join，把join换成outerjoin,并且加上参数```full = True```


```python
s = (
    select(
        [
            users.c.id, 
            addresses.c.email_address
        ]
    )
    .where(users.c.id==1)
    .select_from(
        users.outerjoin(addresses,full = True)
    )
)

print_sql(engine,s,compile_kwargs={"literal_binds": True})

display(get_select(engine,s))
```

### Alias

要把一个子查询结果像一张表那样被使用时,需要使用alias()给子查询命名。


```python
email_count = (
    select(
        [
            addresses.c.email_address,
            func.count(addresses.c.email_address).label('count')            
        ]
    ).group_by(
        addresses.c.email_address
    ).alias('email_count')
)

print_sql(engine, email_count)


s = (
    select(
        [
            addresses.c.email_address,
            email_count.c.count
        ]
    )
    .select_from(
        email_count.outerjoin(addresses,email_count.c.email_address == addresses.c.email_address)
    )
)

print_sql(engine,s)

display(get_select(engine,s))
```

使用SQLAlchemy的时候，由于可以通过python变量名来找到正确的查询，因此并不一定要去指定命名，SQLAlchemy会添加自动的命名。下面的例子里，SQLAlchemy采用了自动命名anon_1


```python
email_count = (
    select(
        [
            addresses.c.email_address,
            func.count(addresses.c.email_address).label('count')            
        ]
    ).group_by(
        addresses.c.email_address
    )
).alias()

print_sql(engine, email_count)


s = (
    select(
        [
            addresses.c.email_address,
            email_count.c.count
        ]
    )
    .select_from(
        email_count.outerjoin(addresses,email_count.c.email_address == addresses.c.email_address)
    )
)

print_sql(engine,s,compile_kwargs={"literal_binds": True})

display(get_select(engine,s))
```

### 关联子查询

#### 基本概念
先用一个例子演示一下关联子查询,这个查询的功能是找出每个用户的id和拥有的邮箱的个数。


```python
s = '''
SELECT 
    test.users.id, 
    (
        SELECT 
            count(test.addresses.id)
        FROM
            test.addresses
        WHERE
            test.users.id = test.addresses.user_id
    ) AS email_count
FROM test.users
'''

print(engine.execute(s).fetchall())
```

这里需要注意的是,子查询有以下几个特点，

* 子查询中使用了test.users.id,但是子查询的FROM语句中并没有出现test.users。
* 子查询返回的结果为一行,一列。

实际上，这种情况下子查询的test.users是由外层的test.users关联的，如果外层是id为1的user，那么子查询的test.users.id就是1;如果外层是id为2的user，那么子查询的test.users.id就是2。

为了方便理解，可以想象有一个根据传入的user id，查找拥有的邮箱数的函数email_count，那么下面的例子和上面的例子是等价的。

```
SELECT 
    test.users.id, 
    email_count(test.users.id) #假象的函数
FROM test.users
```

#### SQLAlchemy中的实现

上面例子中的查询方式称为关联子查询，下面演示怎么在SQLAlchemy中构造关联子查询。


```python
from sqlalchemy import func

email_count = (
    select(
        [
            func.count(addresses.c.id) #返回的结果只有1列
        ]
    ).
    where(users.c.id == addresses.c.user_id) #返回的结果只有1行
    .label('email_count') # 最后需要用label而不是alias
)


s = select(
    [
        users.c.id,
        email_count
    ]
)

print_sql(engine,s)

display(get_select(engine, s))
```

这里要注意关联子查询的结尾必须是label，label一般用于给列重命名。 (实际上由于关联子查询返回一行一列，的确像是一个列。) 如果关联子查询最后没有加label而是alias，那么就不会编译成关联子查询。


```python
from sqlalchemy import func

email_count = (
    select(
        [
            func.count(addresses.c.id).label('email_count') #返回的结果只有1列
        ]
    ).
    where(users.c.id == addresses.c.user_id) #返回的结果只有1行
    .alias()
)


s = select(
    [
        users.c.id,
        email_count.c.email_count
    ]
)

print_sql(engine,s)

display(get_select(engine, s))
```

可以看到上面编译后的SQL语句中,FROM语句添加了test.users。子查询本身就构成了一个完整的查询，统计了所有邮箱的计数，结果为固定的4。

#### 关联行为的调整

可以通过correlate, correlate_except指定或排除sub query中需要关联的外层的table范围。例如通过```correlate(None)```或者```correlate_except(users)```禁止sub query关联外层的users


```python
email_count = (
    select(
        [
            func.count(addresses.c.id)
        ]
    ).
    where(users.c.id == addresses.c.user_id)
    .correlate(None) #.correlate_except(users)在这个例子里也能起到同样的效果
    .label('email_count') #！！
)

s = select(
    [
        users.c.id,
        email_count #!!
    ]
)

print_sql(engine,s)

display(get_select(engine, s))
```

可以看到上面的例子里，sub query中自动在From语句中补充了users，成为完成的select语句，结果也变成了固定的4

#### join lateral
目前只有postgresql支持。 join lateral实际上可以看做另一种形式的关联子查询。


```python
from sqlalchemy import true

sub_query = (
    select(
        [
            func.count(addresses.c.id).label('count') #返回一列
        ]
    ).
    where(users.c.id == addresses.c.user_id) #返回一行
    .lateral('sub_query') #！！用lateral()代替常规的label()
)

s = select(
    [
        users.c.id,
        sub_query.c.count
    ]
).select_from(
    users.join(
        sub_query,
        true() #用这个代替常规的on条件
    )
)

print_sql(engine,s)

display(get_select(engine, s))
```

join lateral语句实际上也起到了遍历users,取出id和对应email_address个数的功能。

```
SELECT 
    test.users.id, sub_query.count 
FROM 
    test.users #被sub query关联的表
        JOIN LATERAL 
    (
        SELECT
            count(test.addresses.id) AS count 
        FROM
            test.addresses
        WHERE
            test.users.id = test.addresses.user_id 
            #users关联了join lateral左边的test.users
    ) AS sub_query ON true
```
这段代码等价于

```
SELECT 
    sub_query.id, sub_query.count 
FROM
    (
        select
            users.id as id,
            email_count(user.id) as count #email_count是假想的函数
        from users
    ) AS sub_query
```



## Update

最基本的update，不指定任何条件，相当于对所有的row做了遍历。


```python
stmt = (
    users.update().
            values(fullname="Fullname: " + users.c.name)
    )

print_sql(engine, stmt, compile_kwargs={"literal_binds": True})

engine.execute(stmt)

s = users.select()

display(get_select(engine,s))
```

选择单行并进行遍历


```python
users, addresses = reset_tables(engine)

stmt = (
    users.update().
    where(users.c.name == 'jack').
    values(name='JACK')
)


print_sql(engine, stmt, compile_kwargs={"literal_binds": True})

engine.execute(stmt)

s = users.select()

get_select(engine,s)
```

## 更新数据
### 对全数据更新

下面是最基本的update方式,在values方法中指定数据的更新方法。 

如果不加where条件对的话，这个更新逻辑会应用与所有的数据。


```python
users,addresses = reset_tables(engine)

stmt = (
    users.update().
            values(fullname="Fullname: " + users.c.name)
    )

print_sql(engine, stmt, compile_kwargs={"literal_binds": True})

engine.execute(stmt)

s = users.select()

display(get_select(engine,s))
```

### 对单行更新


```python
users,addresses = reset_tables(engine)

stmt = (
    users.update().
    values(
        name='Name:'+users.c.name
    ).
    where(users.c.name == 'jack')   
)


print_sql(engine, stmt)

engine.execute(stmt)

display(get_table(engine,users))
```

也可以用dict的方式去指定更新方式。 如果用这种方式的话, object和列名都可以作为key。


```python
users,addresses = reset_tables(engine)

stmt_1 = (
    users.update().
    values(
        {users.c.name:'Name:'+users.c.name} # object作为key
    ).
    where(users.c.name == 'jack')   
)

stmt_2 = (
    users.update().
    values(
        {'name':'Name:'+users.c.name} # 列名作为key
    ).
    where(users.c.name == 'jack')   
)

print_sql(engine, stmt_1)

print_sql(engine, stmt_2)

engine.execute(stmt_1)

display(get_table(engine,users))
```

### 对多行进行更新

#### 用给定的数据进行更新

可以借助上一个教程提到过的bindparam。 编写针对单个row的update逻辑， 但是将需要更新的多条数据用list传入即可实现批量的更新。


```python
from sqlalchemy import bindparam

users, addresses = reset_tables(engine)


stmt = (
    users.update().
    where(users.c.name == bindparam('oldname')).
    values(name=bindparam('newname'))
)

data =  [
    {'oldname':'jack', 'newname':'JACK'},
    {'oldname':'wendy', 'newname':'mary'},
    {'oldname':'jim', 'newname':'jake'}
]   

engine.execute(stmt,data)


print_sql(engine, stmt, False)

engine.execute(stmt,data)

s = users.select()

display(get_select(engine,s))
```

不过update语句的参数数值只能在execute阶段传入，不能使用params()传入


```python
from sqlalchemy import bindparam

users, addresses = reset_tables(engine)

try:
    stmt = (
        users.update().
        where(users.c.name == bindparam('oldname')).
        values(name=bindparam('newname'))
    ).params(data)
except Exception as e:
    print(type(e),e)
```

#### 用另一个select结果更新数据

关键是通过where条件去指定一下数据源(select结果)和待更新的表之间是怎么的匹配的。


```python
from sqlalchemy import bindparam,func,select

users, addresses = reset_tables(engine)

first_addresses = (
    select(
        [
            addresses.c.user_id.label('user_id'),
            func.min(addresses.c.email_address).label('name')
        ]
    ).group_by(
        addresses.c.user_id
    )
).alias('first_address')


s = (
    users
    .update()
    .values(
        {
            users.c.name:first_addresses.c.name
        }

    ).where(
        first_addresses.c.user_id == users.c.id
    )
)

engine.execute(s)

print_sql(engine, s)

s1 = users.select()

display(get_select(engine,s1))
```

也可以用类似关联子查询的方式那样去进行数据升级。

下面我们用每个人字典排序的第一个邮箱去替换原来的name。


```python
from sqlalchemy import bindparam,func

users, addresses = reset_tables(engine)

first_address = (
    select(
        [
            func.min(addresses.c.email_address)
        ]
    ).group_by(
        addresses.c.user_id
    ).where(
        addresses.c.user_id == users.c.id #users没有定义来源，会自动和待升级的表进行关联。
    )
).label('name')


s = (
    users
    .update()
    .values(   
        {
            users.c.name:first_address
        }
    )
)

engine.execute(s)

print_sql(engine, s)

display(get_table(engine,users))
```


```python
from sqlalchemy import bindparam,func

users, addresses = reset_tables(engine)

first_address = (
    select(
        [
            func.min(addresses.c.email_address).label('name')
        ]
    ).group_by(
        addresses.c.user_id
    ).where(
        addresses.c.user_id == users.c.id #users没有定义来源，会自动和待升级的表进行关联。
    )
).label('first_address')


s = (
    users
    .update()
    .values(   
        {
            users.c.name:first_address
        }
    )
)

engine.execute(s)

print_sql(engine, s)

display(get_table(engine,users))
```

和关联子查询一样，用这种方式修改数据时，返回的数据也必须是单行单列。

### 控制列操作的顺序

由于SQLAlchemy编译update语句的时候，默认是按照列在users表中的出现顺序去编译。


```python
users, addresses = reset_tables(engine)

s = (
    users
    .update()
    .values(   
        {
            users.c.fullname:users.c.name,            
            users.c.name:'*****',            
        }
    )
)

engine.execute(s)

print_sql(engine, s)

display(get_table(engine,users))
```

    ***Compiled SQL***
    <<<
    UPDATE test.users SET name='*****', fullname=test.users.name
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>fullname</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>*****</td>
      <td>jack</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>*****</td>
      <td>wendy</td>
    </tr>
  </tbody>
</table>
</div>


编译的语句中，顺序是```name='*****', fullname=test.users.name```。如果我们需要精确的去控制编译后语句列更新的顺序，可以用下面的方式


```python
users, addresses = reset_tables(engine)

s = (
    users
    .update(preserve_parameter_order=True) #添加preserve_parameter_order=True
    .values(   #使用tuple list定义列更新逻辑
        [
            (users.c.fullname,users.c.name),
            (users.c.name,'*****'),
        ] 
    )
)

engine.execute(s)

print_sql(engine, s)

display(get_table(engine,users))
```

    ***Compiled SQL***
    <<<
    UPDATE test.users SET fullname=test.users.name, name='*****'
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>fullname</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>*****</td>
      <td>jack</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>*****</td>
      <td>wendy</td>
    </tr>
  </tbody>
</table>
</div>


现在可以看到编译的语句是```SET fullname=test.users.name, name='*****'```，反映了tuple list的顺序。通过这种方式我们就可以改变编译的SET语句操作列的顺序。

<div class = 'article warning'>注意</div>

对于postgresql，上面两种SET的顺序结果都是一致的。但是对于MYSQL数据库，如果编译结果是

```
UPDATE test.users SET name='*****', fullname=test.users.name
```

在执行```fullname=test.users.name```部分的时候，会采用"*****"作为name的数值，导致最后fullname也变成'*****'，只有用

```
UPDATE test.users SET fullname=test.users.name, name='*****'
```

才能得到正确的结果。

这时就有必要去指定SET语句中列操作的顺序。

## 删除数据
掌握了修改数据的操作后, 删除的操作就非常简单。不过要注意约束条件。例如addresses的user_id是users表的外键，那么在删除addresses表的数据前，是不能删除users表的数据的。

### 删除全量数据


```python
users, addresses = reset_tables(engine)
```

由于外键造成的约束，直接删除users表是会报错的。


```python
d = users.delete()

try:
    engine.execute(d)    
    display(get_table(engine,users))
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.IntegrityError'> (psycopg2.IntegrityError) update or delete on table "users" violates foreign key constraint "addresses_user_id_fkey" on table "addresses"
    DETAIL:  Key (id)=(1) is still referenced from table "addresses".
     [SQL: 'DELETE FROM test.users']


需要先删除addresses, 再删除users


```python
del_addresses = addresses.delete()
del_users = users.delete()

engine.execute(del_addresses)    
engine.execute(del_users)

display(get_table(engine,users))
display(get_table(engine,addresses))
```
