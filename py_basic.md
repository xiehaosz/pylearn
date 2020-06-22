

# 模块/函数

[Python里三个好用的调试神器]: http://www.mamicode.com/info-detail-2808051.html



- python文件通常有两种使用方法，第一是作为**脚本直接执行**，第二是 import 到其他的 python 脚本中**被调用（模块重用）**

- 每个python模块（python文件，也就是此处的 test.py 和 import_test.py）都包含**内置的变量 \__name__**，当该模块被**直接执行**的时候，\__name__ 等于文件名（包含后缀 .py ）；如果该模块 import到其他模块中，则该模块的 \__name__ 等于模块名称（不包含后缀.py）。而 “\_\_main__” **始终指当前执行模块的名称**（包含后缀.py）

  ```
  # test.py，直接执行会获得2行输出
  print("this is func")
  
  if __name__ == '__main__': # 程序入口
  	print("this is main") 
  ```

  ```
  # test_import.py，调用test.py，只会输出"this is func"
  import test
  ```

- python 中，类型属于对象，变量仅仅是引用（指针）没有类型

  ```
  a=[1,2,3]
  a="Runoob"
  # 以上代码中，[1,2,3]是List类型，"Runoob"是String类型，而变量a没有类型,仅仅是一个对象的引用（指针）
  ```

- 参数

  ```
  def func(param = 'name') # 默认参数值
  	pass
  
  def printinfo( arg1, *vartuple ): # 不定长参数使用*号，以元组形式导入（可以为空）
  	for var in vartuple:
        print (var)
  	return
  	
  def printinfo( arg1, *vartuple ): # 不定长参数使用**号，以字典形式导入（可以为空）
  	print (vardict)
  	return
  	
  # lambda [arg1 [,arg2,.....argn]]:expression # 一种简化的函数定义
  sum = lambda arg1, arg2: arg1 + arg2
  
  func(a = "wang") # 可以在调用中赋值
  printinfo(1, a=2,b=3)
  ```

  

---

# 基础语法

- 指定编码（默认UTF-8）

- 标准数据类型：Number, String, Tuple;   List, Set, Dictionary

   ```
    type(obj) # 获取类型
    isinstance(obj, type) # 判断类型
   ```

- 注释 # 或 ''' '''

- 多行语句 \ 或 在括号内

- 一行多语句 ; 分隔

- 数字类型 int float bool complex

- 代码组 : 和相同缩进，如if while def class等

- print默认换行输出，不换行可加入参数end print( x, end=" " )

- import 模块，from 模块 import 函数

- 允许多变量赋值：a=b=c=1 或 a,b,c = 10,20,30

---

# 常用运算

- 运算符

   ```
   算数运算：+ - * / // % **
   赋值运算：算数运算对应增加=号
   比较运算：== != > < >= <=
   位运算符：& | ^ ~ << >> （二进制）
   逻辑运算：and or not
   成员运算：in not in
   身份运算：is is not
   ```

- 数学函数 **引用模块 import math**

   ```
   绝对值：abs(x), fabs(x)
   上入整：ceil(x)
   下舍整：floor(x)
   对数：log(100, 10)	== 2
   max(x1, x2,...)
   min(x1, x2,...)
   modf(x)	返回x的小数部分与整数部分（浮点型）
   幂运算：pow(x, y)
   四舍五入：round(x [,n])	
   平方根：sqrt(x)
   三角函数：(a)sin, (a)cos, (a)tan, degrees, radians
   ```

- 随机函数 **引用模块 import random**

   ```
   choice(seq)	从序列的元素中随机挑选一个元素，比如random.choice(range(10))，从0到9中随机挑选一个整数。
   randrange ([start,] stop [,step])	从指定范围内，按指定基数递增的集合中获取一个随机数，基数默认值为 1
   random()	随机生成下一个实数，它在[0,1)范围内。
   seed([x])	改变随机数生成器的种子seed。如果你不了解其原理，你不必特别去设定seed，Python会帮你选择seed
   shuffle(lst)	将序列的所有元素随机排序
   uniform(x, y)	随机生成下一个实数，它在[x,y]范围内。
   ```

---

# 字符串

- 字符串 转义符\

  ```
  r	非转义
  \(在行尾时)	续行符
  \\	反斜杠符号
  \'	单引号
  \"	双引号
  \b	退格(Backspace)
  \000	空
  \n	换行
  \v	纵向制表符
  \t	横向制表符
  \r	回车
  \f	换页
  ```

- 字符运算 r 原始字符串，支持切片

- 多行字符串使用 '''内容'''

- 字符串格式化 %

  ```
  print ("我叫 %s 今年 %d 岁!" % ('小明', 10))
   %c	 格式化字符及其ASCII码
   %s	 格式化字符串
   %d	 格式化整数
   %u	 格式化无符号整型
   %o	 格式化无符号八进制数
   %x	 格式化无符号十六进制数
   %X	 格式化无符号十六进制数（大写）
   %f	 格式化浮点数字，可指定小数点后的精度
   %e	 用科学计数法格式化浮点数
   %E	 作用同%e，用科学计数法格式化浮点数
   %g	 %f和%e的简写
   %G	 %f 和 %E 的简写
   %p	 用十六进制数格式化变量的地址
   
   f-string 是python3.6之后版本添加,以 f 开头，后面跟着字符串，字符串中的表达式用大括号 {} 包起来
   f'{1+2}' 不用判断格式
  ```

- 内建函数

  ```
  find(str, beg=0, end=len(string)) 检测 str 是否包含在字符串中，如果指定范围 beg 和 end ，则检查是否包含在指定范围内，如果包含返回开始的索引值，否则返回-1
  rfind(str, beg=0,end=len(string))
  
  replace(old, new [, max]) 将字符串中的 str1 替换成 str2,如果 max 指定，则替换不超过 max 次
  
  len(string)
  join(seq)
  split(str="", num=string.count(str))
  
  isalnum() 如果字符串至少有一个字符并且所有字符都是字母或数字则返 回 True,否则返回 False
  isalpha() 如果字符串至少有一个字符并且所有字符都是字母则返回 True, 否则返回 False
  isdigit() 如果字符串只包含数字则返回 True 否则返回 False
  isdecimal() 检查字符串是否只包含十进制字符，如果是返回 true，否则返回 false
  isnumeric() 如果字符串中只包含数字字符，则返回 True，否则返回 False
  
  title()  返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写(见 istitle())
  lower()
  upper()
  swapcase()
  islower()
  isupper()
  
  isspace()
  
  strip([chars]) 在字符串上执行 lstrip()和 rstrip()
  lstrip() 截掉字符串左边的空格或指定字符 （右侧rstrip()）
  
  capitalize() 将字符串的第一个字符转换为大写
  count(str, beg= 0,end=len(string)) 返回 str 在 string 里面出现的次数，如果 beg 或者 end 指定则返回指定范围内 str 出现的次数
  endswith(suffix, beg=0, end=len(string)) 检查字符串是否以 obj 结束
  expandtabs(tabsize=8) 把字符串 string 中的 tab 符号转为空格，tab 符号默认的空格数是 8 
  
  ```

  

---

# 列表/元组

- 基本操作 [定义，访问，变更（元组不能变更），运算]

  ```
  list1 = [1,2,3,4,5,6,7,8,9] # [元素1,元素2,...]
  list2 = list(range(-9,0)) # list转换函数
  tuple1= (1,2,3,4,5)
  ```

  ```
  print(list1[0]) # 下标从0开始
  print(list1[-1]) # 反向读取
  print(list1[2:6:2]) #切片
  ```

  ```
  list2[0] = -9 # 修改（下标）
  del list[6] # 删除（下标）
  list1 += list2 # 拼接
  ```

  ```
  print(list1 + list2) # 连接
  print(list1 * 3) #重复
  for x in list1: print(x, end="/") # 迭代
  ```

- 列表方法

  ```
  list1.count(obj) # 出现次数
  list1.index(obj) # 获取索引
  
  list1.append(obj)
  list1.insert(index, obj) # 插入对象
  list1.extend([10,11,12]) # 与 += 运算相同
  
  list1.pop([index=-1]) # 移除索引（返回对象值）
  list1.remove(obj) # 移除对象 或 del list1[1]
  
  list1.reverse() # 逆序 reversed()函数返回一个新列表
  list1.sort(key=None, reverse=False) # 排序 sorted()函数返回一个新列表
  
  list1.clear(); list1.copy()
  ```

- 其他函数/技巧

  ```
  print(3 in list1) # 判断存在
  len(list1); max(list1); min(list1)
  ```

  ```
  # map()接收一个函数 f 和一个可迭代对象，并把函数 f 依次作用在 list 的每个元素上，返回一个新的 list
  lst_A = list(map(int,lst_A))
  ```
  
  ```
  # 列表推导式：对列表所有元素作用 f 
  [f(elm) for elm in list if ..]
  ```
  
  ```
  # 使用zip()可同时遍历两个或更多的序列
  questions = ['name', 'quest', 'favorite color']
  answers = ['lancelot', 'the holy grail', 'blue']
  for q, a in zip(questions, answers):
  	print('What is your {0}?  It is {1}.'.format(q, a))
  ```
  
  ```
  # 排序（可以用于所有iterable，如字符串、字典）
  sorted(list,[reverse=True]) # list 的 list.sort() 会修改原始的 list（返回值为None）,改函数返回新列表
  
  example_list = [5, 0, 6, 1, 2, 7, 3, 4]
  result_list = sorted(example_list, key=lambda x: x*-1) # 利用key进行倒序排序
  ```
  
  



---

# 集合

- \# 定义

  ```
  set1 = {'Google', 'Taobao', 'Runoob', 'Facebook', 'Zhihu', 'Baidu'}
  set2 = set('abracadabra')
  ```

- \# 运算

  ```
  if 'Google' in set1 : #  判断
  print(a - b)     # a 和 b 的差集
  print(a | b)     # a 和 b 的并集
  print(a & b)     # a 和 b 的交集
  print(a ^ b)     # a 和 b 中不同时存在的元素
  ```

---

#  字典

- \# 定义

  ```
  dict1 = {} # 空字典
  dict1['a'] = 10
  dict2 = {'name': 'runoob','code':1, 'site': 'www.runoob.com'}
  dict3 = {x: x**2 for x in (2, 4, 6)}
  ```
  
- \# 基本操作 

  ```
  print (dict1['a']) 
  print (dict2.keys())   # 输出所有键
  print (dict2.values()) # 输出所有值
  for k, v in dict1.items(): # 同时获取键和值
	print(k, v)
  ```
  
  

---

#  迭代器与生成器

- 迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退

  ```
  list=[1,2,3,4]
  it = iter(list)    # 创建迭代器对象
  print (next(it))   # 输出迭代器的下一个元素
  
  while True:
      try:
          print (next(it))
      except StopIteration: # StopIteration 异常用于标识迭代的完成，防止出现无限循环的情况
          sys.exit()
  
  for x in it:
      print (x, end=" ") 
      
  class MyNumbers:
    def __iter__(self):
      self.a = 1
      return self
   
    def __next__(self):
      if self.a <= 20:
        x = self.a
        self.a += 1
        return x
      else:
        raise StopIteration
   
  myclass = MyNumbers()
  myiter = iter(myclass)
   
  for x in myiter:
    print(x)
  ```

  





---

# 正则表达式

​	**引用模块 import re**

- ^ 匹配字符串的开始。
- $ 匹配字符串的结尾。
- \b 匹配一个单词的边界。
- \d 匹配任意数字。
- \D 匹配任意非数字字符。
- x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
- x* 匹配0次或者多次 x 字符。
- x+ 匹配1次或者多次 x 字符。
- x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
- (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
- (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
- 正则表达式中的点号通常意味着 “匹配任意单字符”

```
# 编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用
re.compile(pattern[, flags])

pattern = re.compile(r'([a-z]+) ([a-z]+)', re.I)
m = pattern.match('Hello World Wide Web') 
m.groups() # 查看所有分组
m.group(1) # 返回分组1子串
m.span(1) # 返回分组1索引
m.start() 
m.end() 

# re.match 只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回 None，而 re.search 匹配整个字符串，直到找到一个匹配。
re.match(pattern, string, flags=0) # flag修饰符
re.search(pattern, string, flags=0)
 
line = "Cats are smarter than dogs"

# 可以使用()标示出要提取的子串，通过group()提取
matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I) # .* 表示任意匹配除换行符（\n、\r）之外的任何单个或多个字符
if matchObj:
   print ("matchObj.group(0) : ", matchObj.group(0)) # group(0)是匹配到的原始字符串
   print ("matchObj.group(1) : ", matchObj.group(1))
   print ("matchObj.group(2) : ", matchObj.group(2))
else:
   print ("No match!!")

# 替换
re.sub(pattern, repl, string, count=0, flags=0) #  替代内容repl可以是函数


# 功能：匹配出一个字符串中所有的数值（可能含负数、小数），以列表返回
re.findall(r'\-?\d+\.?\d*',str_in) 
re.finditer # 返回迭代器
```

---

# 多线程

​	**引用模块 import threading as thrd**

- ​	https://www.runoob.com/python3/python3-multithreading.html

```
#!/usr/bin/python3

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join() # 等待至线程中止(结束/异常/超时)
thread2.join()
print ("退出主线程")
```
