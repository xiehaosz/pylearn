# import collections [内建]

​	Python标准内建容器 [`dict`](https://docs.python.org/zh-cn/3/library/stdtypes.html#dict) , [`list`](https://docs.python.org/zh-cn/3/library/stdtypes.html#list) , [`set`](https://docs.python.org/zh-cn/3/library/stdtypes.html#set) , 和 [`tuple`](https://docs.python.org/zh-cn/3/library/stdtypes.html#tuple) 的**替代选择**

-  **namedtuple() ：** 命名元组

  ```
  # 创建一个元组类型，包含元组名称，元素名称：
  point = collections.namedtuple('Points', ['x', 'y'])
  p1 = point(2, 3) # Points(x=2, y=3)
  p2 = point(4, 2) # Points(x=4, y=2)
  print(isinstance(p1, point)) # True
  print(isinstance(p1, tuple)) # True
  
  # _makef赋值：
  a= [11, 3]; p1._make(a)
  
  # __replace改值：
  p1._replace(x=5)
  ```

  

-  **deque ：** 双端队列，类似列表(list)的容器，实现了在两端快速添加(append)和弹出(pop)

  ```
  q = deque(['a', 'b', 'c'], maxlen=10)
  q.append('d') # 从右边添加元素
  q.popleft() # 从左边删除
  q.extend(['i', 'j']) # 扩展，超长会丢弃另一端
  q.index('c') # 查找下标
  q.remove('d') # 删除元素
  q.reverse() # 逆序
  q.rotate(n) # 循环位移，即q.appendleft(q.pop())
  q.insert(i, x) # 在位置i插入x，队列超长会报错
  ```

  

-  **defaultdict ：**默认值字典，为key不存在提供一个默认值。

  ```
  dd = defaultdict(lambda: 'not exist')
  dd['key1'] = 'abc'
  print(dd['key1']) # key1存在  
  # 'abc'
  print(dd['key2']) # key2不存在，返回默认值
  # 'not exist'
  
  # 很容易将序列作为键值对加入字典
  d = defaultdict(list)
  s = [('a', 1), ('b', 2), ('a', 3), ('b', 4), ('c', 1)]
  for k, v in s:
      d[k].append(v) # {'a': [1, 3], 'b': [2, 4], 'c': [1]})
  
  # 很容易进行计数
  s = 'mississippi'
  d = defaultdict(int)
  for k in s:
      d[k] += 1 # {'m': 1, 'i': 4, 's': 4, 'p': 2})
  ```

  

-  **Counter ：**计数功能

  ```
  # Counter是一个dict的子类，用于计数可哈希对象，特别方便
  c = Counter()
  for i in 'sfsadfsdjklgsdla':
      c[i] +=  1 # Counter({'s': 4, 'd': 3, 'f': 2, 'a': 2, 'l': 2, 'j': 1, 'k': 1, 'g': 1}) 
      
  c = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])
  print(c) # Counter({'blue': 3, 'red': 2, 'green': 1})
  
  most_common([n]) # 返回n个最常见的元素及出现次数，省略n返回所有
  
  c = Counter(a=4, b=2, c=0, d=-2)
  print(sorted(c.elements())) # ['a', 'a', 'a', 'a', 'b', 'b']
  
  # 可用于比较
  c = Counter(a=4, c=2, b=0, d=-2)
  d = Counter(a=1, b=2, c=3, d=4)
  c.subtract(d)
  print(c) # Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
  
  ```

  

---

# import numpy as np

NumPy(Numerical Python) 是 Python 语言的一个扩展程序库，支持大量的维度数组与矩阵运算,通常与 SciPy（Scientific Python）和 Matplotlib（绘图库）一起使用， 这种组合广泛用于替代 MatLab

- **创建nparray对象**

  ```
  data = [[1,2,3],[2,3,4],[4,5,6]] # 二维数组
  ndarray_object = np.array(data)
  
  a = np.array([1,2,3,4,5], ndmin =  2)  # 指定维度
  a = np.array([1,2,3], dtype = complex) # 指定类型

  ndarray_object = np.zeros((3,4)) # 全0矩阵，也可以用ones创建全1矩阵
  ndarray_object = np.zeros(data)
  ```
  
-  **数据类型**

  bool\_，int_，(default)，int8/16/32/64（可以简写为‘i1/2/4/8‘） , unit8/16/32/64，float\_，float16/32/64

  ```
  dt = np.dtype('<i4') # <或>符合指定字节顺序， <表示最小有效字节存储在最小地址中（编码是小端）， >表示最大有效字节存储在最小地址中
  
  student = np.dtype([('name','S20'), ('age', 'i1'), ('marks', 'f4')])  # 创建格式化数据类型，相当于建立列标题
  a = np.array([('Jhon', 21, 50),('Bill', 18, 75)], dtype = student)  # 用于对象
  
  print(a['age']) # 可以根据列表图提取数据
  ```

- **数组属性**

  ```
  a.dtype
  
  a.ndim # 秩/维度
  a.shape # 行列数(n,m)，分别取到每个a.shape[0] 
  
  a = np.arange(24)  
  b = a.reshape(3,8)  # 调整维度大小（2维，24=3*8）
  b = a.reshape(3,2,4)  # （3维,24 = 3*2*4）
  b = a.reshape(2,2,2,3)  # （4维）
  
  a.size  # 元素个数 n*m
  a.itemsize # 每个元素的大小（字节数）
  
  ```

- **截取元素**

  ```
  a = np.array([[1,2,3,4,5],[11,12,13,14,15],[21,22,23,24,25],[31,32,33,34,35]])
  
  # 按index截取
  print(a[0:1]) # 第一行
  print(a[1,2:5]) # 第二行，第三、四、五列
  print(a[1:,:4]) # 第二行到最后，首列到第4列
  
  # 按条件截取(一维)
  print(a%3 == 0)
  print(a[a%3 == 0])
  
  # 按条件修改元素
  a[a%3 == 0] = 0
  print(a)
  
  # 注意！在numpy中切片是浅复制（指向同一个对象，不开辟新存储地址）
  a = np.array([1,2,3])
  b = a[:]
  a[0]=10 # 修改a，b也会跟着变化！
  
  # 深复制
  b = a.copy()
  
  ```

- **矩阵运算**

  ```
  a = np.floor(10*np.random.random((2,2)))
  b = 10*np.random.random((2,2))
  
  a.max([axis=0]) # 可以指定对行/列运算，下同
  a.min()
  a.mean()
  a.median()
  
  a.var() # 均方差，相当于函数mean(abs(a - a.mean())**2)
  a.std() # 标准差, 相当于sqrt(x.var())
  
  a.sum()
  a.cumsum()
  a.ptp() # 极差
  a.average()
  
  # 合并
  np.vstack((a,b)) # 上下合并（列数相同），等效np.concatenate((a1,a2), axis=0) 
  np.hstack((a,b)) # 左右合并（行数相同），等效np.concatenate((a1,a2), axis=1) 
  
  # 矩阵乘法
  a1 = np.array([[1,2,3],[4,5,6]]) # a1为2*3矩阵
  a2 = np.array([[1,2],[3,4],[5,6]]) # a2为3*2矩阵
  
  print(a1.shape[1]==a2.shape[0]) # True, 满足矩阵乘法条件
  print(a1.dot(a2)) 
  
  a.T # 即 a.transpose()
  
  # 矩阵的逆
  # 设A是数域上的一个n阶方阵，若在相同数域上存在另一个n阶矩阵B，使得： AB=BA=E。 则我们称B是A的逆矩阵，而A则被称为可逆矩阵。
  numpy.linalg.inv()
  
  ```

  

- **函数**

  - 序列/转换

    ```
    # 等差序列
    np.linspace(0,10,7) # （起始，解释，序列值个数）
    
    # 字符串ASCII码
    b = np.fromstring(a,dtype=np.int8) # 因为一个字符为8位，所以指定dtype为np.int8
    ```

  - 随机数

    ```
    np.random.rand(d0,d1...,dn) # 0~1随机数，dn是n维上的shape
    np.random.random # 浮点数 [0.0,1.0)
    
    np.random.randint(low[,high,size]) # [low,high)范围的整数 i.e. np.random.randint(3,10,size=(5,5))
    np.random.random_integers # 同上，闭区间 [low,high]
    
    np.random.shuffle # 随机乱序
    np.random.permutation # 同上，返回新对象
    ```

  - 与行列号相关的矩阵

    ```
    # 根据行列号生产矩阵
    def func(i,j,k): 
        return i+j+k
    a = np.fromfunction(func,(5,6,7)) # func的参数必须和矩阵的秩一一对应
    ```

    







 数据帧操作
 grp_dict = dict(list(df.groupby(['key1'])))
 print(grp_dict.keys())
 print(grp_dict['B'])

 grp_lst = list(df.groupby(['key1']))
 print(grp_lst[0])

 grp_lst = list(df.groupby(['key1'])['data1'])   等效list(df['data1'].groupby(df['key1']))
 print(grp_lst[1])
 grp_lst = list(df.groupby(['key1'])[['data1']])
 print(grp_lst[1])
