import re
import numpy as np

def calc(str_in):

	lst_L = re.findall(r'\-?\d+\.?\d*',str_in)
	lst_L = list(map(float,lst_L))
	print("数组L：",lst_L)

	lst_L_abs = list(map(abs,lst_L))

	if len(lst_L)<1:
		print(-1)
	elif len(lst_L)==1:
		print(int(lst_L[0]*lst_L[1]))

	else:
		int_N = int(min(lst_L_abs))+1
		while int_N>=len(lst_L):
			int_N=int(int_N/2)+1

		lst_A = lst_L[:int_N]
		print('数组A：',lst_A)
		
		lst_B = lst_L[int_N:]
		print('数组B：',lst_B)
		
		while len(lst_A)> len(lst_B):
			lst_A.remove(max(lst_A))
		while len(lst_B)> len(lst_A):
			lst_B.remove(max(lst_B))
		
		arr_A = np.array(lst_A)
		arr_B = np.array(lst_B)
		
		# print('A/B之差平方和：',int(sum((arr_A - arr_B)**2)))
		
		return int(sum((arr_A - arr_B)**2))


def main():
	# str_input = input('请输入任意字符串:')
	str_input = 'calc(\'a1b2c13d14e15f-\')'
	print('A/B之差平方和：',calc(str_input))

if __name__ == '__main__':
	main()

	
'''
1、输入任意一个字符串s，按序找出其中所有的尽可能长的数字子字符串(可能为小数、负数)，存入列表L。如果L的长度<2，直接返回-1；如果L
的长度为2，直接返回2个元素的乘积的整数部分值。另有一个正整数N，初始N=L中绝对值最小的值，将N先取绝对值，再取整后加1，重新赋值给N

2、按如下原则将L分成2组A、B：
    如果N小于L的长度，将L的前N个元素放入组A，剩余元素放入组B；
    如果N大于或等于L的长度，令N=取整(N/2)+1，重复步骤2

3、将A、B中长度较长的组的元素按数值从大到小进行删除(不能改变原有列表A/B中元素顺序)，直至2组长度相等，计算2个组对应元素差的平方和之后
返回其整数部分值

4、注意：'a01b'取成'01'再转成数字1而不能取成2个数字0、1； 'a.1b'只能提取出1，而不是0.1;

示例:
输入：calc('a1b2c13d14e15')
输出: 288
计算过程：
L=[1, 2, 13, 14, 15], N=2, 则A=[1, 2], B=[13, 14, 15], B的长度较长，删除B中的元素15，则B=[13, 14]
对应元素差的平方和=(1-13)^2+(2-14)^2=288
'''


'''
## 总结
## ^ 匹配字符串的开始。
## $ 匹配字符串的结尾。
## \b 匹配一个单词的边界。
## \d 匹配任意数字。
## \D 匹配任意非数字字符。
## x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
## x* 匹配0次或者多次 x 字符。
## x+ 匹配1次或者多次 x 字符。
## x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
## (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
## (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
## 正则表达式中的点号通常意味着 “匹配任意单字符”

根据上述正则表达式的含义，可写出如下的表达式："\d+\.?\d*"；
\d+匹配1次或者多次数字，注意这里不要写成*，因为即便是小数，小数点之前也得有一个数字；\.?这个是匹配小数点的，可能有，也可能没有；\d*这个是匹配小数点之后的数字的，所以是0个或者多个；
匹配时间，17:35:24  pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
匹配指定字符串开头的数字 pattern = re.compile(r'(?<=calibration=)\d+\.?\d*')

其他思路：
# 遍历字符串元素，如果该元素不是数字或字母，则以'.'号替换字符串中的元素，从而得到一个仅包含数字、字母和'.'号的字符串
# 把转换后的字符串以‘.’号分割成一个新的list（这时候list中的元素就是一个个仅包含数字或字母字符串）
# 遍历这个新的list中的元素，如果该元素不为空且同时包含数字和字母，则把该元素添加进list a中，同时把该元素的长度添加进list b 中
# 用下标遍历存储长度的list b ，如果元素的长度等于list b中最大元素的长度，则该元素就是符合条件的最长子字符串了，同时获得了该元素的下标
# 最后再用下标去list a 中取子字符串，并把结果存储在list lg中
# 程序结束，lg中的元素就是所有符合条件的子字符串了

正则表达式
把字符串按非数字或字母分割，返回一个list 这时候list内的结果就是仅包含数字或字母的字符串了
ls = re.split(r'\W',s)
