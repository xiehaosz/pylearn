# 类型Python概述

Python官网：https://www.python.org/

多Python并存：电脑-属性-高级系统设置-环境变量-PATH，在最上面的路径为模型启动的Python版本

Python模块的下载路径：https://pypi.org/simple/ 

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

# 装饰器

python装饰器就是用于**拓展原来函数功能的一种函数**，这个函数的特殊之处在于它的返回值也是一个函数，使用python装饰器的好处就是在不用更改原函数的代码前提下给函数增加新的功能。装饰器本质上是一个高级Python函数，通过给别的函数添加@标识的形式实现对函数的装饰。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。

一段原始代码：

```
import time
def func():
    print("hello")
    time.sleep(1)
    print("world")
```

我们试图记录下这个函数执行的总时间：

```
#原始侵入（篡改原函数）
import time
def func():
    startTime = time.time()
    print("hello")
    time.sleep(1)
    print("world")
    endTime = time.time()
    msecs = (endTime - startTime)*1000
    print("time is %d ms" %msecs)
```

但是如果不允许篡改原始代码来实现，就可以使用装饰器了：

```
# 不需要侵入，也不需要函数重复执行
import time
def deco(func):
    def wrapper():
        startTime = time.time()
        func()
        endTime = time.time()
        msecs = (endTime - startTime)*1000
        print("time is %d ms" %msecs)
    return wrapper
# deco函数就是最原始的装饰器，它的参数是一个函数，然后返回值也是一个函数。其中作为参数的这个函数func()就在返回函数wrapper()的内部执行
# 在函数func()前面加上@deco，func()函数就相当于被注入了计时功能
@deco
def func():
    print("hello")
    time.sleep(1)
    print("world")

if __name__ == '__main__':
    f = func #这里f被赋值为func，执行f()就是执行func()
    f()
```

带有不定参数的装饰器：

```
#带有不定参数的装饰器
import time

def deco(func):
    def wrapper(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        endTime = time.time()
        msecs = (endTime - startTime)*1000
        print("time is %d ms" %msecs)
    return wrapper


@deco
def func(a,b):
    print("hello，here is a func for add :")
    time.sleep(1)
    print("result is %d" %(a+b))

@deco
def func2(a,b,c):
    print("hello，here is a func for add :")
    time.sleep(1)
    print("result is %d" %(a+b+c))


if __name__ == '__main__':
    f = func
    func2(3,4,5)
    f(3,4)
    #func()
```

多个装饰器执行的顺序是从最后一个装饰器开始，执行到第一个装饰器，再执行函数本身装饰器的加载顺序是从内到外的(从下往上的)。其实很好理解：装饰器是给函数装饰的，所以要从靠近函数的装饰器开始从内往外加载。

```
#多个装饰器

import time

def deco01(func):
    def wrapper(*args, **kwargs):
        print("this is deco01")
        startTime = time.time()
        func(*args, **kwargs)
        endTime = time.time()
        msecs = (endTime - startTime)*1000
        print("time is %d ms" %msecs)
        print("deco01 end here")
    return wrapper

def deco02(func):
    def wrapper(*args, **kwargs):
        print("this is deco02")
        func(*args, **kwargs)

        print("deco02 end here")
    return wrapper

@deco01
@deco02
def func(a,b):
    print("hello，here is a func for add :")
    time.sleep(1)
    print("result is %d" %(a+b))



if __name__ == '__main__':
    f = func
    f(3,4)
    #func()

'''
this is deco01
this is deco02
hello，here is a func for add :
result is 7
deco02 end here
time is 1003 ms
deco01 end here
'''
```

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

  

1. 变量的定义和声明：定义（建立存储空间），声明（不建立存储空间）。变量可以在多个地方声明，但是只能在一个地方定义。
2. 基本类型变量的声明和定义（初始化）是同时产生的；而对于对象来说，声明（创建一个类对象）和定义（类初始化）是分开的。

数据类型：数字(int)、浮点(float)、字符串(str)，列表(list)、元组(tuple)、字典(dict)、集合(set)

```
def test():
    try:
        print(100) # 一定会执行
    except IndexError as e:
        print(e)  # 如果try中的语句异常则执行这里
    else:
        print(200) # 如果try中的语句正常则执行这里
        return(999) # 函数结束并返回结果
        print(201)
    finally:
        print(666) # 一定会执行
```







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

- 单引号和双引号

  ```
  # 没有任何区别
  str1 = 'python'
  str2 = "python" 
  
  # 单/双引号可以减少转移符的使用，当用单/双引号定义字符串的时候，它就会认为字符串里面的另一种引号是普通字符，从而不需要转义
  str3 = 'We all know that \'A\' and \'B\' are two capital letters.'
  str4_ = "We all know that 'A' and 'B' are two capital letters."
  str5 = 'The teacher said: "Practice makes perfect" is a very famous proverb.'
  
  # 三引号可以实现字符串换行
  str1 = """List of name:
  Hua Li
  Chao Deng
  """
  print(str1)
  # 等效于插入换行符
  str1 = "List of name:\nHua Li\nChao Deng"
  
  三引号也可作为多行注释
  ```

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
  
  多个替换
  '替换\n 和空格'
  #方法1
  words = words.replace('\n', '').replace(' ', '')
  print(words)
    
  #方法2
  rep = {'\n':'',' ':''}
  rep = dict((re.escape(k), v) for k, v in rep.items())
  #print(rep)
  #print(rep.keys())
  pattern = re.compile("|".join(rep.keys()))
  #print(pattern)
  my_str = pattern.sub(lambda m: rep[re.escape(m.group(0))], words)
  print(my_str)
  #print(words.replace(['\n',' '],''))
  
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
  list2[0] = -9 # 修改（下标）
  del list[6] # 删除（下标）
  list1 += list2 # 拼接
  ```

  ```
  print(list1 + list2) # 连接
  print(list1 * 3) #重复
  for x in list1: print(x, end="/") # 迭代
  ```

  列表方法

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

  切片

```
# 切片
aList=[3,4,5,6,7,9,11,13,15,17]
print(aList[::])  #[3, 4, 5, 6, 7, 9, 11, 13, 15, 17]
print(aList[::-1])  #[17, 15, 13, 11, 9, 7, 6, 5, 4, 3] # 加负号逆向输出
print(aList[::2])  # [3, 5, 7, 11, 15] # 以步长为2进行输出，输出下标依次为0 2 4 6
print(aList[1::2])  #[4, 6, 9, 13, 17],从一开始步长为2
print(aList[3::])  #[6, 7, 9, 11, 13, 15, 17]
print(aList[3:6])  #省略的是步长，而且不包括下标为6的元素   #[6, 7, 9]

print(List[100]) #IndexError: list index out of range，下标超索引错误
print(List[100:])  #[]，切片不会有下标错误，输出一个空列表

# 利用切片方法实现列表的增加
aList=[3,5,7]
print(aList[len(aList):])   #[]
aList[len(aList):]=[9]  #把原来三位列表的第四位赋值为9
print(aList)  #[3, 5, 7, 9] 

# 利用切片方法实现列表元素的修改
#aList = [3,5,7,9]
aList[:3]=[1,2,3]
print(aList)  #[1, 2, 3, 9]
aList[:3]=[]
print(aList)  #[9]

aList=list(range(10))
print(aList)  #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
aList[::2]=[0]*(len(aList)//2)  #"//"整除
print(aList)  #[0, 1, 0, 3, 0, 5, 0, 7, 0, 9]

# 结合del命令删除列表中的部分元素
aList=[3,5,7,9,11]
del aList[:3]
print(aList)  #[9, 11]

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

#  字典/集合

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
  
  # 合并字典的方法（字典不支持+运算）
  dict{a, **b} #**可以展开一个字典，执行效率最高
  dict{a.items()+b.items()}
  a.update(b) # 更新了a
  
  
  ```

- 集合定义set，集合与字典的区别，字典是key和value的结对，set可以理解为没有value的字典

  因此set元素同样重复（可以利用set(list)获得不重复的值），

  set运算：a|b 并集，a&b 交集， a-b 差集

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

	**引用模块 import re**

- ^ 匹配字符串的开始。
- $ 匹配字符串的结尾。
- \* 匹配前面的子表达式任意次
- \+ 匹配前面的子表达式指定次数
- ？ 匹配前面的子表达式一次或0次
- {n} 匹配确定的n次
- \b 匹配一个单词的边界，例如 匹配never中的er，不匹配verb中的er
- \B 匹配非单词边界
- \d 匹配任意数字。
- \D 匹配任意非数字字符。
- x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
- x* 匹配0次或者多次 x 字符。
- x+ 匹配1次或者多次 x 字符。
- x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
- (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
- (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
- 正则表达式中的点号通常意味着 “匹配任意单字符”

https://blog.csdn.net/caojinfei_csdn/article/details/86495013

http://blog.sina.com.cn/s/blog_6dc145220100zoe2.html

**Python中re的match、search、findall、finditer区别**

- re.match(pattern, string[, flags])

  从首字母开始开始匹配，string如果包含pattern子串，则匹配成功，返回Match对象，失败则返回None，若要完全匹配，pattern要以$结尾

- re.search(pattern, string[, flags])

  若string中包含pattern子串，则返回Match对象，否则返回None，注意，如果string中存在多个pattern子串，只返回第一个

- re.findall(pattern, string[, flags])

  返回string中所有与pattern相匹配的全部字串，返回形式为数组

- re.finditer(pattern, string[, flags])

  返回string中所有与pattern相匹配的全部字串，返回形式为迭代器

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

在正则中，使用.*可以匹配所有字符，其中.代表除\n外的任意字符，*代表0-无穷个,比如说要分别匹配某个目录下的子目录:
match = re.match(r"/(.*)/(.*)/(.*)/", "/usr/local/bin/")


```

---

# 多线程

	**引用模块 import threading as thrd**

- 	https://www.runoob.com/python3/python3-multithreading.html

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



# 模块/函数

[Python里三个好用的调试神器]: http://www.mamicode.com/info-detail-2808051.html

## PySnooper

调试模块

```text
pip install pysnooper
```

以装饰器的形式使用该工具，其包含了四个参数:
1、output参数。该参数指定函数运行过程中产生的中间结果的保存位置，若该值为空，则将中间结果输出到控制台。
2、variables参数。该参数是vector类型, 因为在默认情况下，装饰器只跟踪局部变量，要跟踪非局部变量，则可以通过该字段来指定。默认值为空vector。
3、depth参数。该参数表示需要追踪的函数调用的深度。在很多时候，我们在函数中会调用其他函数，通过该参数就可以指定跟踪调用函数的深度。默认值为1。
4、prefix参数。该参数用于指定该函数接口的中间结果前缀。当多个函数都使用的该装饰器后，会将这些函数调用的中间结果保存到一个文件中，此时就可以通过前缀过滤不同函数调用的中间结果。默认值为空字符串。

output 参数使用，运行该代码后，结果会输出到./log/debug.log：

```text
import pysnooper

def add(num1, num2):
    return num1 + num2

@pysnooper.snoop("./log/debug.log", prefix="--*--")
def multiplication(num1, num2):
    sum_value = 0
    for i in range(0, num1):
        sum_value = add(sum_value, num2)
    return sum_value

value = multiplication(3, 4)
```

variables参数使用，需要查看局部变量以外变量时，通过variables参数将需要查看类实例的变量self.num1, self.num2, self.sum_value作为当参数传入snoop的装饰器中：

```text
import pysnooper

class Foo(object):
    def __init__(self):
        self.num1 = 0
        self.num2 = 0
        self.sum_value = 0

    def add(self, num1, num2):
        return num1 + num2
    @pysnooper.snoop(output="./log/debug.log", variables=("self.num1", "self.num2", "self.sum_value"))
    def multiplication(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        sum_value = 0
        for i in range(0, num1):
            sum_value = self.add(sum_value, num2)
        self.sum_value = sum_value
        return sum_value

foo = Foo()
foo.multiplication(3, 4)
```

depth参数使用：

```text
import pysnooper

def add(num1, num2):
    return num1 + num2

@pysnooper.snoop("./log/debug.log", depth=2)
def multiplication(num1, num2):
    sum_value = 0
    for i in range(0, num1):
        sum_value = add(sum_value, num2)
    return sum_value

value = multiplication(3, 4)
```

prefix参数使用，为中间结果打印增加一个前缀，以区分不同的函数调用：

```text
import pysnooper

def add(num1, num2):
    return num1 + num2

@pysnooper.snoop(prefix="我的函数输出__")
def multiplication(num1, num2):
    sum_value = 0
    for i in range(0, num1):
        sum_value = add(sum_value, num2)
    return sum_value

value = multiplication(3, 4)
```

数据科学模块 NumPy

统计与分析模块 Pandas

数据可视化 Matplotlib 与 Seaborn

数据分析好助手 Jupyter notebook

GUI Tkinter：第一份是Tkinter简明教程，不知所云，几乎没什么帮助；第二份是2014年度辛星Tkinter教程第二版，内容浅显易懂；第三份是Python GUI Programming Cookbook，内容详细，帮助很大。大概用了5-6天的时间，边看文档写出了带有简单GUI界面的Anki2.0。又经过之后的组件升级，增加了许多功能，更新到了Anki3.2  https://www.zhihu.com/question/32703639



# VBA

```
求出A列最后1行：Cells(Rows.Count, 1).End(3).Row
1. "Cells(Rows.Count, 1)"表示是查找A列最后一个非空单元格，按列的可以改成"Cells(1, Columns.count)"
2. "end(3)"表示的向上查找，也可以写成“end(xlup)”,还有其他3个方向，向下，向左，向右：xldown,xltoleft,xltoright
```

正则表达式 http://yshblog.com/blog/94

该对象可以通过引用Microsoft VBScript Regular Expressions 5.5。再声明定义

属性：

1）Global，是否全局匹配，若为False，匹配到一个结果之后，就不再匹配。默认False，建议设为True；

2）IgnoreCase，是否忽略大小写，默认False，建议设为False，这个会影响到正常表达式匹配；

3）Multiline，是否跨行匹配，默认False，建议设为False，这个会影响到正常表达式匹配；

4）Pattern，获取或设置正则表达式。

方法：

1）Execute，执行匹配

2）Replace，根据正确表达式全部替换

3）Test，测试正则表达式能否匹配到内容

```
Public Function CheckNumber(str As String) As Boolean
    Dim reg As Object
    Set reg = CreateObject("VBScript.Regexp")
            
    Dim is_exist As Boolean    
    With reg
        .Global = True
        .Pattern = "\d"        
        is_exist = .Test(str)  # 判断是否匹配到数字   
    End With
    CheckNumber = is_exist
End Function
```

```
Public Sub GetCode()
    Dim reg As Object
    Set reg = CreateObject("VBScript.Regexp")
    
    Dim str As String
    str = "编号：ABC123155 日期：2016-01-11" & _
          "编号：ABD134215 日期：2016-02-21" & _
          "编号：CBC134216 日期：2016-01-15"
    
    reg.Global = True    reg.Pattern = "[A-Z]{3}\d+"        '因为这个编号是3个大写字母和多个数字组成。可以利用代码中的表达式匹配到3个结果：ABC123155、ABD134215和CBC134216。'
    Dim matches As Object, match As Object
    Set matches = reg.Execute(str)
    
    '遍历所有匹配到的结果'
    For Each match In matches
        '测试输出到立即窗口'
        Debug.Print match
    Next
End Sub
```

```
Public Sub GetHref()    
    Dim reg As Object    
    Set reg = CreateObject("VBScript.Regexp")        
    
    Dim str As String    
    str = "<a href='xxx1'>xxx1</a><a href='xxx2'>xxx2</a>"        
    
    reg.Global = True    
    '获取a标签中href的属性值'    
    reg.Pattern = "href='(.+?)'"        
    
    '获取匹配结果'    
    Dim matches As Object, match As Object    
    Set matches = reg.Execute(str)        
    
    '遍历所有匹配到的结果'    
    For Each match In matches        
        '测试输出子表达式到立即窗口'        
        Debug.Print match.SubMatches(0)  用元组可以一次性搞定，通过match的SubMatches集合获取元组里面的内容。轻松得到xxx1和xxx
    Next
End Sub
```

正则的特点是书写方便但是极其不便于阅读

. 匹配任意字符

/ 之后的任意特殊字符 匹配其本身 如 /. 匹配 .

0-9 以及 a-zA-Z 以及汉字字符 匹配其本身 a{5} 即a出现5次 匹配 aaaaa 大括号用法见下文
/d 匹配数字。等价于[0-9]， 25/d 匹配 250 到 259 之间的字符串

/D匹配非数字。等价于[^0-9]

/s 匹配空白，包括空格、制表符、换页符等。等价于"[/f /n /r /t /v ]"

/S 匹配非空白的字符。等价于"[^/f /n /r /t /v ]"

/w 匹配字母、数字，以及下划线。等价于"[A-Za-z0-9_]"

/W 匹配非字符数字。等价于"[^A-Za-z0-9/_]"

我们注意到，大写字母为小写字母所表示模式的补集



定义出现频率

{a,b} 其中 a b分别为相应模式出现次数的上限与下限 /d{1,4} 表示一到四位数字

{a} 其中 a 为相应模式出现次数 /d{4} 表示由任意数字组成的四位字符串

? 出现一次或不出现 Germany? 既可以匹配 German 又可以匹配 Germany

\+ 出现一次以上 a+ 既可以匹配 aaa

\* 可能不出现 出现一次 或出现多次



[] 中括号中的模式选一 如[abcd0123] 表示从abcd0123这几个字符中任意选择一个

也可以表示为 [a-d0-3]

[^] 表示 除括号中元素之外的其他所有



| 表示二选一 ma|en 可以匹配 man 也可以匹配men

() 表示 分组 Eng(lish)|(land) 可以匹配 English 也可以匹配England



^ 为字符串开头

$ 为字符串结尾

VBA图表

https://blog.csdn.net/zishendianxia/article/details/76712366

https://blog.csdn.net/zishendianxia/article/details/76358423

https://www.163.com/dy/article/EFI6565G05368KC4.html

# 其他

[破解xlsm文件的VBA项目密码和xlsx的工作簿保护密码](https://www.cnblogs.com/zeroes/p/reset_vbaproject_password.html)

1.修改.xlsm后缀为.zip

2.使用压缩软件打开，进入xl目录找到vbaProject.bin文件，解压出来

3、使用Hex软件打开vbaProject.bin文件，查找DPB替换成DPx，保存文件，重新压缩，修改后缀名.zip为.xlsm

4、使用excel打开.xlsm文件，开发工具->查看代码，弹出错误提示框，点击“是”或“确定”。在VBAProject上点击右键，打开工程属性，重新填入密码，如：123456，点击确定。
