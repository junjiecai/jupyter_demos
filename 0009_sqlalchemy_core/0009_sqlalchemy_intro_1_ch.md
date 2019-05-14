
## 说明

SQLAlchemy包含SQLAlchemy Core和SQLAlchemy ORM两部分, 这个系列只包含SQLAlchemy Core的内容。

由于内容较多，教程被分成了上，下两部分。 Select,Update,Delete本身内容较为丰富，放在[sqlalchemy入门(下)](http://junjiecai.github.io/posts/2017/Jan/17/sqlalchemy_intro_2/)行演示讲解。

## 准备

### 安装sqlalchemy
```pip install SQLAlchemy```

### 安装postgresql数据库
如果想运行文中的代码,请安装postgresql数据库并且建立相应的测试用户和测试数据库。

### 导入helper.py

为了方便代码实现的进行，我编写了helper.py，里面提供的函数功能如下

* reset_tables:在名为'test'的schema下重置users,addresses两张表的数据
* clear_tables:在名为'test'的schema下删除users和addresses两张表并返回两张表对应的object
* clear_schema:删除名为'test'的schema
* get_table:获得名为'test'的schema中指定表的数据(DataFrame形式)
* get_select:获得名为'test'的schema中指定查询语句得到数据(DataFrame形式)
* print_sql:print sqlalchemy object编译后对应的sql语句

读者暂时先不必关心这些函数是怎么实现的，等完成这份教程后自然有能力自己去实现同样的功能。


```python
from helper import reset_tables,clear_tables,clear_schema,get_select,get_table,print_sql
```

### 导入其它代码实验要用到的库


```python
from IPython.display import display
```

### 创建engine

SQLAlchemy通过engine和目标数据库建立连接，它是后面所有的数据库操作都需要使用的object。
我本机的使用的用户名,数据库名,密码都是'test',端口为'5432'。如果不一致请相应的对下面的代码做出修改。


```python
from sqlalchemy import create_engine

user = 'test'
password = 'test'
port = '5432'
dbname = 'test'

engine = create_engine('postgresql://{user}:{password}@localhost:{port}/{dbname}'.format(**locals()))
```

### 测试数据
教程中用到的测试数据如下


```python
from helper import users_data, addresses_data
```

users表和user是一一对应关系,它包含的测试数据是id为1,2的用户的name和fullname


```python
display(users_data)
```


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


addresses表和user是一对多的关系,它包含的测试数据是id为1,2的用户的email_addresses


```python
display(addresses_data)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>email_address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack@yahoo.com</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>jack@msn.com</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>www@www.org</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>wendy@aol.com</td>
    </tr>
  </tbody>
</table>
</div>


## SQLAlchemy Core初印象
SQLAlchemy Core提供了一套SQL Expression language,它提供了一套用Python construct(Python object)去表达SQL逻辑的体系。下面通过一些代码演示一下SQL Expression language的基本特征。这里读者只需要有大致的感觉即可，如果有一些细节不理解不用在意，后面都会有详细的解释。

传统的SQL语句是用文本方式编写的。


```python
sql = '''
    select 
        users.id, users.fullname
    from
    (
        users join addresses
        on
            users.id = addresses.user_id
    )
    group by
        users.id
    having
        count(addresses.email_address)>1
    order by users.fullname
'''
```

在SQLAlchemy Core中是这样表达的


```python
from sqlalchemy import select, func

users, addresses = reset_tables(engine)

s = (
    select(
        [
            users.c.id,
            users.c.fullname    
        ]
    ).select_from(
        users.join(
            addresses,
            users.c.id==addresses.c.user_id    
        )
    ).group_by(users.c.id)
    .having(func.count(addresses.c.email_address)>1)
)

print_sql(engine, s)
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.fullname 
    FROM test.users JOIN test.addresses ON test.users.id = test.addresses.user_id GROUP BY test.users.id 
    HAVING count(test.addresses.email_address) > 1
    >>>


上面的SQL逻辑可以看作是很多更基本的元件构成的，包括表,列,条件,join语句等等。整个Select逻辑和这些组成元件，对应的都是sqlalchemy object


```python
l = [
    users,
    users.c.id,
    users.c.id==addresses.c.user_id,
    s
]

for obj in l:
    print(type(obj))
```

    <class 'sqlalchemy.sql.schema.Table'>
    <class 'sqlalchemy.sql.schema.Column'>
    <class 'sqlalchemy.sql.elements.BinaryExpression'>
    <class 'sqlalchemy.sql.selectable.Select'>


由于因此使用SQLAlchemy Core表达SQL逻辑的时候，是一个从代表基本SQL逻辑模块的object逐步组装成复杂object的过程。这样做有几个好处。

### 容易拆分
当SQL逻辑复杂的时候，可以分阶段的构造。先构造简单的SQL逻辑模块，再逐步组装成复杂的SQL逻辑。相比一次性构造完整的复杂SQL逻辑相比，头脑的负担更低，也不容易出错。

下面的例子里，我们可以把前面例子中的要选择的columns,join语句,having条件先构造好,然后再组装成完整的SQL逻辑。每一个SQL逻辑模块构造好后我们都可以观察一下对应的SQL语句是什么。


```python
from sqlalchemy import select, func

columns_selection = select(
    [users.c.id, users.c.fullname]
)
print_sql(engine,columns_selection)

join_clause = users.join(
    addresses,
    users.c.id==addresses.c.user_id    
)
print_sql(engine,join_clause)

condition = func.count(addresses.c.email_address)>1
print_sql(engine,condition)

s = (
    columns_selection
    .select_from(join_clause)
    .group_by(users.c.id)
    .having(condition)
)
print_sql(engine,s)
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.fullname 
    FROM test.users
    >>>
    ***Compiled SQL***
    <<<
    test.users JOIN test.addresses ON test.users.id = test.addresses.user_id
    >>>
    ***Compiled SQL***
    <<<
    count(test.addresses.email_address) > 1
    >>>
    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.fullname 
    FROM test.users JOIN test.addresses ON test.users.id = test.addresses.user_id GROUP BY test.users.id 
    HAVING count(test.addresses.email_address) > 1
    >>>


### 容易复用
由于使用SQLAlchemy Core去表达SQL，本质上是使用python语言写代码。　因此我们可以利用python提供的一切工具和手段将重复出现的SQL逻辑抽提成可复用的python代码。

例如我们在多个地方要根据fullname的长度，和首字母去筛选user。那么可以用一个函数生成这个条件，以后直接调用这个函数即可。


```python
from sqlalchemy import Table, and_, func, bindparam

def email_condition(users, init, length):
    return and_(
        users.c.fullname.like('{}%'.format(init)),
        func.len(users.c.fullname)==length
)

c = email_condition(users,'J',5)
print_sql(engine,c)
```

    ***Compiled SQL***
    <<<
    test.users.fullname LIKE 'J%' AND len(test.users.fullname) = 5
    >>>


### 处理数据库差异

在用SQLAlchemy Core表达SQL逻辑的时候，只是表达了用户的意图，并未生成最终的SQL语句。

同样的SQL逻辑，在不同的database中语法可能会有变化，因此对应的SQL语句是不同的。 而SQLAlchemy Core会根据database的种类，编译出和这个database匹配的SQL语句。这样用户用SQLAlchemy Core组织一次SQL逻辑，就可以在多个数据库中复用。

当然每个database都有一些自己独有的功能，对于这部分差异SQLAlchemy是不能自动处理的。

## SQLAlchemy Core使用详解

### 查看编译后的语句
使用SQLAlchemy Core一个基本的需求是查看sqlalchemy object编译后的SQL语句是什么样的。这个可以用object提供的compile方法实现。


```python
condition = users.c.name == 'jack'
compiled = condition.compile()
print(compiled)
```

    test.users.name = :name_1


默认情况下编译后的SQL语句是带参数的形式,并没有把'jack'代入name_1。可以通过调用params属性查看对应的数值是多少。


```python
print(compiled.params)
```

    {'name_1': 'jack'}


如果希望编译后的SQL语句是非参数化的形式，可以添加```compile_kwargs={"literal_binds": True}```选项。


```python
compiled = condition.compile(compile_kwargs={"literal_binds": True})
print(compiled)
```

    test.users.name = 'jack'


由于具体的SQL逻辑在不同的database对应的语法并不完全相同，所以建议传入一个指向特定数据库的engine,可以得到更准确的编译结果。(在这个例子里没有差别)


```python
compiled = condition.compile(engine, compile_kwargs={"literal_binds": True})
print(compiled)
```

    test.users.name = 'jack'


### schema操作

#### 创建schema


```python
from sqlalchemy.schema import CreateSchema

clear_schema(engine)

schema_name = 'test'
obj = CreateSchema(schema_name)
engine.execute(obj)

print_sql(engine,obj,False)
```

    ***Compiled SQL***
    <<<
    CREATE SCHEMA test
    >>>


如果创建已经存在的schema,会导致异常。例如，刚才已经创建了名为'test'的schema，如果再创建一遍的话,会提示schema "test" already exists


```python
try:
    engine.execute(obj)
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.ProgrammingError'> (psycopg2.ProgrammingError) schema "test" already exists
     [SQL: 'CREATE SCHEMA test']


<div class = 'warning'>注意</div>

有些sqlalchemy object，例如这个例子中的```CreateSchema(schema_name)```，结果为None。


```python
type(obj.compile().params)
```




    NoneType



对于这类object,```compile```的时候添加```compile_kwargs={"literal_binds": True}```会导致异常。


```python
try:
    obj.compile(compile_kwargs={"literal_binds": True})
except Exception as e:
    print(type(e),e)
```

    <class 'TypeError'> visit_create_schema() got an unexpected keyword argument 'literal_binds'


默认情况```print_sql```函数会添加```"literal_binds": True```， 可以将第三个参数设置成```False```关闭这个设置。

#### 删除schema

和新建schema类似。不过如果这个schema下有一些依赖于这个schema存在的资源，比如tables,那么只有先删除了这些资源后才能删除这个schema，否则会异常。

这里有一个有用的参数cascade，设置成True的话会自动删除所有依赖于这个schema的资源。


```python
from sqlalchemy.schema import DropSchema

schema_name = 'test'
obj = DropSchema(schema_name, cascade = True)
print_sql(engine,obj,False)

engine.execute(obj)
```

    ***Compiled SQL***
    <<<
    DROP SCHEMA test CASCADE
    >>>





    <sqlalchemy.engine.result.ResultProxy at 0x7f734fa1cd30>



同样, 如果删除已经不存在的schema,会报ProgrammingError

同样，如果删除并不存在的schema，会报异常，这个不演示了。

### table操作

#### 定义ｔａble
定义SQLAlchemy可理解的table数据结构，主要参数是table名,schema名以及相关的column的名称,类型，是否是primary_key等信息。

定义table是进行新建表，构建select语句等操作的基础。


```python
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence
from sqlalchemy.schema import CreateTable

schema='test'
table_name = 'users'

metadata = MetaData()

table = Table(
    table_name,
    metadata,
    Column('id',Integer,primary_key=True),
    Column('name',String), 
    Column('fullname',String),
    schema = schema
)
```

如果是数据库中已经存在的表,可以直接使用autoload功能从数据库中读取表的列信息，可以免去很多麻烦。下面reset_db确保test.users表存在后用autoload自动读取users表的信息。


```python
reset_tables(engine);

metadats = MetaData()
users = Table('users', metadata, schema = 'test', autoload=True, autoload_with=engine)
```

可以看到users中自动包含了column的定义信息。


```python
users.c.values()
```




    [Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
     Column('name', String(), table=<users>),
     Column('fullname', String(), table=<users>)]



<div class = "article warning">注意</div>

如果table中定义了foreign key信息,SQLAlchemy Core构建join语句的时候能够自动将foreign key作为join的条件。 但是autoload得到的table会失去这个便利，暂时没找到解决方法。(见join章节的演示)

#### 新建table
再定义了table后，可以在数据库中新建这张表。

先清空数据库


```python
clear_tables(engine)
```

新建表


```python
obj = CreateTable(table)

print_sql(engine,obj,False)

engine.execute(obj);
```

    ***Compiled SQL***
    <<<
    
    CREATE TABLE test.users (
    	id SERIAL NOT NULL, 
    	name VARCHAR, 
    	fullname VARCHAR, 
    	PRIMARY KEY (id)
    )
    
    
    >>>


SQLAlchemy会根据数据库的类型，将String等列类型信息转化成数据库中对应的信息，例如Oracle中的VARCHAR2。

注意，不同的数据库对于configs的要求会不同。例如，postgresql只需要写String,不需要指定长度；而Oracle在定义时，必须指定长度，得改成类似下面的设置才会生效。
```
    Column('id',Integer,primary_key=True),
    Column('name',String(20)), 
    Column('fullname',String(20)),     
```


同样, 如果尝试新建已经存在的表，会出错,这个不演示了。

## drop table

drop table的处理方法和create table类似。不过在定义


```python
from sqlalchemy.schema import DropTable

reset_tables(engine)

metadata = MetaData()
table = Table(
        'users',
        metadata,
        schema = 'test'
    )

print_sql(engine,obj,False)

obj = DropTable(table)
```

    ***Compiled SQL***
    <<<
    
    CREATE TABLE test.users (
    	id SERIAL NOT NULL, 
    	name VARCHAR, 
    	fullname VARCHAR, 
    	PRIMARY KEY (id)
    )
    
    
    >>>


不过运行的话会报错


```python
users, addresses = reset_tables(engine)

try:
    engine.execute(obj)
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.InternalError'> (psycopg2.InternalError) cannot drop table users because other objects depend on it
    DETAIL:  constraint addresses_user_id_fkey on table addresses depends on table users
    HINT:  Use DROP ... CASCADE to drop the dependent objects too.
     [SQL: '\nDROP TABLE test.users']


这是由于在定义addresses表的时候,定义了addresses的user_id是users表的foreign key,因此foreign key依赖于users表，只有Drop时指定CASCADE选项才能顺利的删除这张表。(它会删除所有依赖于users表的foreign_key),遗憾的是，我并没有在sqlalchemy中找到相关的选项启动CASCADE。

不过SQLAlchemy的一个好处是，它完全可以接受原生的SQL语句去对数据库进行操作。我们在语句中加上CASCADE和IF EXISTS来进行drop table的操作。


```python
table_name = 'users'
schema = 'test'
sql = "DROP TABLE IF EXISTS {schema}.{table_name} CASCADE".format(table_name = table_name, schema = schema)

engine.execute(sql)
```




    <sqlalchemy.engine.result.ResultProxy at 0x7f7350290198>



<div class = 'article tip'>提示</div>

SQLAlchemy的优势更多的是体现在构造和复用复杂的SQL逻辑上。在删除table的这个例子里。SQLAlchemy Core实际上并不如原生的SQL语句好用。我们完全可以针对自己的场景，选择适合的工作去完成任务。 

### 插入数据

#### 插入单行数据


```python
users, addresses = reset_tables(engine)

ins = users.insert().values(name='Junjie', fullname='Junjie Cai')
print_sql(engine, ins)

result = engine.execute(ins)
```

    ***Compiled SQL***
    <<<
    INSERT INTO test.users (name, fullname) VALUES ('Junjie', 'Junjie Cai') RETURNING test.users.id
    >>>


可以用result.insered_primary_key很方便的找到插入记录的id


```python
result.inserted_primary_key
```




    [3]



验证一下插入数据后的结果


```python
display(get_table(engine, users))
```


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
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Junjie</td>
      <td>Junjie Cai</td>
    </tr>
  </tbody>
</table>
</div>


注意也可以在engine.execute中传入数据


```python
users, addresses = reset_tables(engine)

ins = users.insert()
print_sql(engine, ins)

engine.execute(ins,name='jack', fullname='Jack Jones')

display(get_table(engine, users))
```

    ***Compiled SQL***
    <<<
    INSERT INTO test.users (id, name, fullname) VALUES (%(id)s, %(name)s, %(fullname)s)
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
    <tr>
      <th>2</th>
      <td>3</td>
      <td>jack</td>
      <td>Jack Jones</td>
    </tr>
  </tbody>
</table>
</div>


#### 插入多行数据
如果是插入部分列的话，可以用list of dict的结构。


```python
data = [
    {'name':'Junjie','fullname':'CaiJunjie'},
    {'name':'Xu','fullname':'ZhangXu'}
]

ins = users.insert().values(data)

engine.execute(ins)

display(get_table(engine,users))
```


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
    <tr>
      <th>2</th>
      <td>3</td>
      <td>jack</td>
      <td>Jack Jones</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Junjie</td>
      <td>CaiJunjie</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Xu</td>
      <td>ZhangXu</td>
    </tr>
  </tbody>
</table>
</div>


注意如果要插入dict list,sqlalchemy会以list中第一条记录的key为准


```python
data = [
    {'name':'Name1'},
    {'name':'Name2','fullname':'FULLNAME2'}
]
ins = users.insert().values(data)

engine.execute(ins)

display(get_table(engine,users))
```


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
    <tr>
      <th>2</th>
      <td>3</td>
      <td>jack</td>
      <td>Jack Jones</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Junjie</td>
      <td>CaiJunjie</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Xu</td>
      <td>ZhangXu</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>Name1</td>
      <td>None</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>Name2</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>


如果第一行包含了所有的key,后面的记录key缺失的话，会直接报错。


```python
try:
    data = [
        {'name':'Name3','fullname':'FULLNAME3'},
        {'name':'Name4'},    
    ]
    ins = users.insert().values(data)

    engine.execute(ins)
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.CompileError'> INSERT value for column users.fullname is explicitly rendered as a boundparameter in the VALUES clause; a Python-side value or SQL expression is required


如果插入数据时会使用所有的列,那么可以简化成直接用tuple list插入数据。但是这是就不能利用自动编号id，而是要传入id。


```python
data = [
    (8,'Cai','Junjie'),
    (9,'Zhang','Xu')
]
ins = users.insert().values(data)

engine.execute(ins)

display(get_table(engine,users))
```


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
    <tr>
      <th>2</th>
      <td>3</td>
      <td>jack</td>
      <td>Jack Jones</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Junjie</td>
      <td>CaiJunjie</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Xu</td>
      <td>ZhangXu</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>Name1</td>
      <td>None</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>Name2</td>
      <td>None</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>Cai</td>
      <td>Junjie</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>Zhang</td>
      <td>Xu</td>
    </tr>
  </tbody>
</table>
</div>


但是用这种方式传入数据的话，自动id的状态并不会做出相应的调整,而是继续从上次终止的地方开始，不会跳过用上面方式插入的id。 如果再利用dict list插入数据，生成id就可能和以后的重复，导致异常。

例如下面的例子里,最后一次自动id是7，继续使用自动id的话，会从8开始。可以上面再用tuple list插入数据的时候已经把8占用了，于是导致异常。


```python
ins = users.insert()
print_sql(engine, ins)

try:
    engine.execute(ins,name='jack', fullname='Jack Jones')
except Exception as e:
    print(type(e),e)
```

    ***Compiled SQL***
    <<<
    INSERT INTO test.users (id, name, fullname) VALUES (%(id)s, %(name)s, %(fullname)s)
    >>>
    <class 'sqlalchemy.exc.IntegrityError'> (psycopg2.IntegrityError) duplicate key value violates unique constraint "users_pkey"
    DETAIL:  Key (id)=(8) already exists.
     [SQL: 'INSERT INTO test.users (name, fullname) VALUES (%(name)s, %(fullname)s) RETURNING test.users.id'] [parameters: {'fullname': 'Jack Jones', 'name': 'jack'}]


#### 从DataFrame插入数据

pandas DataFrame是数据工作者经常使用的数据结构。


```python
from pandas import DataFrame
df = DataFrame({'name':['Xu','Junjie'],'fullname':['ZhangXu','CaiJunjie']})
display(df)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fullname</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ZhangXu</td>
      <td>Xu</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CaiJunjie</td>
      <td>Junjie</td>
    </tr>
  </tbody>
</table>
</div>


可以利用```to_dict()```方法很方便的把```dataframe```转成dict list


```python
display(df.to_dict(orient = 'records'))
```


    [{'fullname': 'ZhangXu', 'name': 'Xu'},
     {'fullname': 'CaiJunjie', 'name': 'Junjie'}]


<div class = 'article warnings'>注意</div>

尽管```list(df.to_records())```转成的结果看上去是tuple list


```python
df = DataFrame(
    {'id':[15,16],'name':['Xu','Junjie'],'fullname':['ZhangXu','CaiJunjie']}
    ,columns = ['id','name','fullname']
)
display(list(df.to_records(index = False)))
```


    [(15, 'Xu', 'ZhangXu'), (16, 'Junjie', 'CaiJunjie')]


但是直接插入这个数据的话会导致异常


```python
data = list(df.to_records(index = False))

try:
    ins = users.insert().values(data)
    engine.execute(ins)
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.ProgrammingError'> (psycopg2.ProgrammingError) can't adapt type 'record' [SQL: 'INSERT INTO test.users (id, name) VALUES (%(id)s, %(name)s)'] [parameters: {'id': (15, 'Xu', 'ZhangXu'), 'name': (16, 'Junjie', 'CaiJunjie')}]


原因是list中的数据类型是numpy.record,不是tuple。 


```python
display(type(data[0]))
```


    numpy.record


即使修复了这个问题


```python
data = [tuple(r) for r in data]
display(type(data[0]))
```


    tuple


也依然会因为数据结构类型不一致导致异常


```python
try:
    ins = users.insert().values(data)
    engine.execute(ins)
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.ProgrammingError'> (psycopg2.ProgrammingError) can't adapt type 'numpy.int64' [SQL: 'INSERT INTO test.users (id, name, fullname) VALUES (%(id_0)s, %(name_0)s, %(fullname_0)s), (%(id_1)s, %(name_1)s, %(fullname_1)s)'] [parameters: {'name_1': 'Junjie', 'fullname_1': 'CaiJunjie', 'id_0': 15, 'name_0': 'Xu', 'fullname_0': 'ZhangXu', 'id_1': 16}]



```python
data = df.to_dict(orient = 'record')
try:
    ins = users.insert().values(data)
    engine.execute(ins)
except Exception as e:
    print(type(e),e)
```

因此建议直接使用to_dict(orient = 'record')方式转化数据。

## Select, Update, Delete
这部门内容比较丰富，这里只演示最基本的应用。更详细的说明放在下一期的的文章讲解。

### 基本的select结构


```python
from sqlalchemy import select

s = select(
    [
        users.c.id,
        users.c.name        
    ]
).select_from(
    users
).where(
    users.c.id==1
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name 
    FROM test.users 
    WHERE test.users.id = 1
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack</td>
    </tr>
  </tbody>
</table>
</div>


其中select_from相当于SQL中的FROM。 如果不会产生歧义，select_from部分可以省略不写。SQLAlchemy会自动补齐相关的FROM语句。


```python
from sqlalchemy import select

s = select(
    [
        users.c.id,
        users.c.name        
    ]
).where(
    users.c.id==1
)

print_sql(engine,s)

display(get_select(engine,s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name 
    FROM test.users 
    WHERE test.users.id = 1
    >>>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>jack</td>
    </tr>
  </tbody>
</table>
</div>


## 带参数的SQL逻辑

如果希望生成的SQL逻辑支持参数,有两种实现方式。

### 函数生成方式
用函数生成SQL逻辑，用函数的参数去实现SQL逻辑参数可变的效果。例如我们构造一个针对user.id的条件。


```python
def condition(user_id):
    return users.c.id == user_id

print_sql(engine,condition(1))
print_sql(engine,condition(2))
```

    ***Compiled SQL***
    <<<
    test.users.id = 1
    >>>
    ***Compiled SQL***
    <<<
    test.users.id = 2
    >>>


上面这种方式每次运行函数的时候都会构建新的SQLAlchemy object。

### 用bindparam指定参数
另一种方式是构建SQLAlchemy object时,用bindparam指定参数部分。 然后用```.params```绑定数值。


```python
from sqlalchemy.sql import bindparam
condition = (users.c.id == bindparam('id')).params({'id':1})

print_sql(engine,condition,False)
print_sql(engine,condition)
```

    ***Compiled SQL***
    <<<
    test.users.id = %(id)s
    >>>
    ***Compiled SQL***
    <<<
    test.users.id = 1
    >>>


实际上,在SQLAlchemy中使用常数的时候,只是把定义参数和绑定数据两步一起做而已。


```python
from sqlalchemy.sql import bindparam
condition = users.c.id == 1

print_sql(engine,condition,False)
print_sql(engine,condition)
```

    ***Compiled SQL***
    <<<
    test.users.id = %(id_1)s
    >>>
    ***Compiled SQL***
    <<<
    test.users.id = 1
    >>>


如果定义了参数后没有通过params绑定数值，那么在execute阶段传入数值也是可以的。


```python
s = users.select().where(users.c.id==bindparam('id'))
print_sql(engine,s,False)

display(engine.execute(s,id=1).fetchone())
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, test.users.fullname 
    FROM test.users 
    WHERE test.users.id = %(id)s
    >>>



    (1, 'jack', 'Jack Jones')


上面这种方式, obj生成一次后可以反复被利用,不必重复的生成object。

### 类型提示

有些场景下，需要指定变量类型，帮助sqlalchemy正确的编译语句。下面的例子里,即使后面绑定了string类型的数据，```+```依然没能正确的编译成字符串的连接符。应该是"||"。


```python
from sqlalchemy import text

s = users.select(users.c.name.like(bindparam('username') + text("'%'")))

s = s.params({'username':'jack'})

print_sql(engine,s)


try:
    display(get_select(engine, s))
except Exception as e:
    print(type(e),e)
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, test.users.fullname 
    FROM test.users 
    WHERE test.users.name LIKE NULL + '%%'
    >>>
    <class 'sqlalchemy.exc.ProgrammingError'> (psycopg2.ProgrammingError) operator is not unique: unknown + unknown
    LINE 3: WHERE test.users.name LIKE 'jack' + '%'
                                              ^
    HINT:  Could not choose a best candidate operator. You might need to add explicit type casts.
     [SQL: "SELECT test.users.id, test.users.name, test.users.fullname \nFROM test.users \nWHERE test.users.name LIKE %(username)s + '%%'"] [parameters: {'username': 'jack'}]


这时候，需要主动在bindparam中通过type_指定数据类型，帮助SQLAlchemy正确的编译


```python
from sqlalchemy import text,String

s = users.select(users.c.name.like(bindparam('username',type_=String) + text("'%'")))

s = s.params({'username':'jack'})

print_sql(engine,s,compile_kwargs={'literal_binds':True})

display(get_select(engine, s))
```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, test.users.name, test.users.fullname 
    FROM test.users 
    WHERE test.users.name LIKE ('jack' || '%%')
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
      <td>3</td>
      <td>jack</td>
      <td>Jack Jones</td>
    </tr>
  </tbody>
</table>
</div>


## 用text定义sqlalchemy object
除了用纯粹的sqlalchemy object去定义SQL逻辑的各种组件,有时候我们希望将文本形式的sql直接转化成sqlalchemy object。例如下面两种场景。

* 已经存在现成的sql代码片段，不想用SQLAlchemy重写
* 遇到SQLAlchemy无法表达，只有原生的SQL能表达的场景

例如下面这样包含待定参数的SQL语句,```:id```是名为id的参数。在传入实际的数值前,这个语句是不完整的，如果直接传入engine.execute的话，会出错。


```python
s = 'select users.id, users.name, users.fullname from test.users where users.id=:user_id'

try:
    engine.execute(s).fetchall()
except Exception as e:
    print(type(e),e)
```

    <class 'sqlalchemy.exc.ProgrammingError'> (psycopg2.ProgrammingError) syntax error at or near ":"
    LINE 1: ...name, users.fullname from test.users where users.id=:user_id
                                                                   ^
     [SQL: 'select users.id, users.name, users.fullname from test.users where users.id=:user_id']


这时可以用text处理并且用bindparams函数绑定数据


```python
s = 'select users.id, name, users.fullname from test.users where users.id=:user_id'

s = text(s).bindparams(user_id=1)


print_sql(engine,s)
print(engine.execute(s).fetchone())

```

    ***Compiled SQL***
    <<<
    select users.id, name, users.fullname from test.users where users.id=1
    >>>
    (1, 'jack', 'Jack Jones')


绑定参数调用的方法是bindparams,不是params,也不是bindparam! 注意区分!

也可以不绑定参数，而是在execute阶段传入数据


```python
s = 'select users.id, users.name, users.fullname from test.users where users.id=:user_id'

s = text(s)

print_sql(engine,s,False)

print(engine.execute(s,user_id=1).fetchone())
```

    ***Compiled SQL***
    <<<
    select users.id, users.name, users.fullname from test.users where users.id=%(user_id)s
    >>>
    (1, 'jack', 'Jack Jones')


除了用文本定义大段的SQL逻辑外，也可以用文本SQL的片段去定义部分的SQL组件。


```python
s = (
    select(
            [
               text("users.fullname || ', ' || addresses.email_address AS title"),
            ]
        ).select_from(
            text('test.users, test.addresses'),
        ).where(
            text(
                "users.id = addresses.user_id and "
                "users.id = :user_id"        
            )
        )
    )

s = s.params({'user_id':1})

print_sql(engine, s)

engine.execute(s).fetchall()
```

    ***Compiled SQL***
    <<<
    SELECT users.fullname || ', ' || addresses.email_address AS title 
    FROM test.users, test.addresses 
    WHERE users.id = addresses.user_id and users.id = NULL
    >>>





    [('Jack Jones, jack@yahoo.com',), ('Jack Jones, jack@msn.com',)]



注意上面例子中s构造的时候，用到了text生成的带参数的SQL逻辑组件，但是本身的数据类型是sqlalchemy.sql.selectable.Select,因此绑定数据的时候调用的方法是params，而不是bindparam


```python
print(type(s))
```

    <class 'sqlalchemy.sql.selectable.Select'>


如果用文本定义的SQL片段是table,和column, 可以用literal_column, table代替text去处理文本SQL。


```python
from sqlalchemy import literal_column, String,table,literal

users = table('users')
users.schema = 'test' #注意指定schema的方式

s = select(
    [
        literal_column('users.id').label('id'),
        (literal('=<')+literal_column('users.fullname',type_ = String)+literal('>=')).label('name')        
    ]
).select_from (
    users
)

print_sql(engine,s)


```

    ***Compiled SQL***
    <<<
    SELECT users.id AS id, '=<' || users.fullname || '>=' AS name 
    FROM test.users
    >>>


注意schema不能在构造table时以字符串传入，否则生成的语句执行时会错误。尽管构造出来的SQL看上去是完全正确的。


```python
from sqlalchemy import literal_column, String,table,literal

users = table('test.users') #这样是不行的


s = select(
    [
        literal_column('users.id').label('id'),
        (literal('=<')+literal_column('users.fullname',type_ = String)+literal('>=')).label('name')        
    ]
).select_from (
    users
)

print_sql(engine,s)

try:
    display(get_select(engine,s))
except Exception as e:
    print(type(e),e)
```

    ***Compiled SQL***
    <<<
    SELECT users.id AS id, '=<' || users.fullname || '>=' AS name 
    FROM "test.users"
    >>>
    <class 'sqlalchemy.exc.ProgrammingError'> (psycopg2.ProgrammingError) relation "test.users" does not exist
    LINE 2: FROM "test.users"
                 ^
     [SQL: 'SELECT users.id AS id, %(param_1)s || users.fullname || %(param_2)s AS name \nFROM "test.users"'] [parameters: {'param_2': '>=', 'param_1': '=<'}]


用literal_column和table相比text,构造出的object能够更好的被SQLAlchemy支持。看下面的例子。


```python
users, addresses = reset_tables(engine)
s1 = select(
    [
        users.c.id,
        text('users.fullname AS name')
    ]
)

print_sql(engine,s1)

s2 = select(
    [
        users.c.id,
        literal_column('users.fullname').label('name')
    ]
)

print_sql(engine,s2)

```

    ***Compiled SQL***
    <<<
    SELECT test.users.id, users.fullname AS name 
    FROM test.users
    >>>
    ***Compiled SQL***
    <<<
    SELECT test.users.id, users.fullname AS name 
    FROM test.users
    >>>


尽管编译出的语句是一样的，但是观察SQLAlchemy识别出的column names,发现SQLAlchemy无法识别text函数构造出的列。


```python
print(s1.c.keys())
print(s2.c.keys())
```

    ['id']
    ['id', 'name']


因此应该优先考虑使用literal_column, table等更确切具体的构造方式以获得SQLAlchemy更好的支持。
