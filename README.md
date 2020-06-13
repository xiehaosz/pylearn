### 调试函数

[Python里三个好用的调试神器]: http://www.mamicode.com/info-detail-2808051.html



### 正则表达式

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
 re.findall(r'\-?\d+\.?\d*',str_in) # 功能：匹配出一个字符串中所有的数值（可能含负数、小数）
```



### 列表

- 列表的基本操作

  > ```
  > lst_A = [1,2,3,4,5,6,7,8,9]
  > lst_B = list(range(-9,0)) # -9 to -1
  > 
  > print(lst_B[0]) # 访问元素
  > lst_B[0] = -9 # 修改元素
  > sdsd
  > 
  > sdsd
  > ```


- 对列表元素的统一操作

  > map()接收一个函数 f 和一个可迭代对象，并把函数 f 依次作用在 list 的每个元素上，**返回一个新的 list**
  > ```
  > lst_A = list(map(int,lst_A)) # 
  > ```

- 列表的基本操作

  > sdd
  >
  > sdsd
  >
  > sdsd



### 数组

​	**引用模块 import numpy as np**

