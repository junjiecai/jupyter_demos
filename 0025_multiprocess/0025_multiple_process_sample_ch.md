
# Python多进程的演示

多进程模式常见的模式
* 主进程和子进程之间通过Queue传递数据
* 主进程开启多个process, 并且负责往Queue中不断的放入数据。主进程可以通过传递特殊的信息例如None， 表示没有更多的数据。
* 子进程不断的从Queue获取数据（可以用```while True```实现）,并进行处理。如果接受到特殊的终止信息， 则退出函数结束进程。

## 代码示例

* run_parallel负责自进程的建立和往Queue放数据和传递终止信息
* task是子进程的运算内容


```python
from multiprocessing import Process, Queue
from datetime import datetime
```


```python
def task(queue, n):
    from random import randint
    from time import sleep    
    print('Worker {} is starting'.format(n))
    
    # 不断的尝试从Queue获取数据
    while True:
        data = queue.get()  
        
        # 如果拿到终止信息， 退出函数
        if data is None:
            print('No more jobs. Worker {} is quiting'.format(n))
            return
        else:
            # 实际的处理内容， 这里为了演示， 只是简单的将拿到的数据开方并print。
            # 为了模拟较慢的运算， 每次处理时随机休眠0.5~0.6秒
            
            sleep(randint(50,60)/100)
            print('Worker {} is inputing {}'.format(n,data**2))
            
def run_parallel(njob, join = True):
    queue = Queue()
    # 创建子进程， 配置子进程所需的函数和函数参数
    workers = [Process(target = task, args = (queue,n)) for n in range(njob)]
    for worker in workers:
        worker.start()

    ## 放入待处理的数据    
    for data_chunk in range(1,8):
        queue.put(data_chunk)
    ## 传递终止信息， 数量要和njob保持一直
    for i in range(njob):
        queue.put(None)    
    
    if join:
        # 这段功能是让主进程的函数等待所有的字进程函数完成后在返回, 
        # 如果不加这一段, 主进程的函数会立即返回。
        for worker in workers:
            worker.join()

if __name__ == '__main__':
    # 子进程数量, 可以调整下观察效果
    n_job = 10
    
    # 启用worker.join()
    t1 = datetime.now() #开始时间
    run_parallel(n_job, True)
    t2 = datetime.now() # 结束时间
    time = (t2-t1).total_seconds() #时间差(秒)
    print('***run_parallel(n_job,True) returned***')
    print('Time spent: {} seconds'.format(time))
    
    print('\n')
    # 不启用worker.join()    
    t1 = datetime.now()    
    run_parallel(n_job, False)
    t2 = datetime.now()
    time = (t2-t1).total_seconds()    
    print('***run_parallel(n_job,False) returned***')
    print('Time spent: {} seconds'.format(time))                
```

    Worker 3 is starting
    Worker 4 is starting
    Worker 5 is starting
    Worker 6 is starting
    Worker 7 is starting
    Worker 1 is starting
    Worker 0 is starting
    Worker 2 is starting
    Worker 9 is starting
    Worker 8 is starting
    No more jobs. Worker 9 is quiting
    No more jobs. Worker 8 is quiting
    No more jobs. Worker 2 is quiting
    Worker 0 is inputing 36
    No more jobs. Worker 0 is quiting
    Worker 4 is inputing 4
    No more jobs. Worker 4 is quiting
    Worker 1 is inputing 49
    No more jobs. Worker 1 is quiting
    Worker 5 is inputing 9
    Worker 6 is inputing 16
    No more jobs. Worker 5 is quiting
    No more jobs. Worker 6 is quiting
    Worker 3 is inputing 1
    No more jobs. Worker 3 is quiting
    Worker 7 is inputing 25
    No more jobs. Worker 7 is quiting
    ***run_parallel(n_job,True) returned***
    Time spent: 0.642116 seconds
    
    
    Worker 2 is starting
    Worker 5 is starting
    Worker 3 is starting
    Worker 4 is starting
    Worker 1 is starting
    Worker 7 is starting
    Worker 9 is starting
    Worker 8 is starting
    Worker 6 is starting
    Worker 0 is starting
    ***run_parallel(n_job,False) returned***
    Time spent: 0.037395 seconds
    No more jobs. Worker 1 is quiting
    No more jobs. Worker 8 is quiting
    No more jobs. Worker 0 is quiting
    Worker 5 is inputing 4
    No more jobs. Worker 5 is quiting
    Worker 6 is inputing 16
    No more jobs. Worker 6 is quiting
    Worker 2 is inputing 1
    No more jobs. Worker 2 is quiting
    Worker 3 is inputing 9
    No more jobs. Worker 3 is quiting
    Worker 7 is inputing 36
    No more jobs. Worker 7 is quiting
    Worker 9 is inputing 49
    No more jobs. Worker 9 is quiting
    Worker 4 is inputing 25
    No more jobs. Worker 4 is quiting



```python

```
