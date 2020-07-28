import re
import numpy as np

'''
练习1 =================================================================================================================================================================
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

根据上述正则表达式的含义，可写出如下的表达式："\d+\.?\d*"；
\d + 匹配1次或者多次数字，注意这里不要写成 *，因为即便是小数，小数点之前也得有一个数字；\.?这个是匹配小数点的，可能有，也可能没有；\d * 这个是匹配小数点之后的数字的，所以是0个或者多个；
匹配时间，17: 35:24
pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
匹配指定字符串开头的数字
pattern = re.compile(r'(?<=calibration=)\d+\.?\d*')

其他思路：
# 遍历字符串元素，如果该元素不是数字或字母，则以'.'号替换字符串中的元素，从而得到一个仅包含数字、字母和'.'号的字符串
# 把转换后的字符串以‘.’号分割成一个新的list（这时候list中的元素就是一个个仅包含数字或字母字符串）
# 遍历这个新的list中的元素，如果该元素不为空且同时包含数字和字母，则把该元素添加进list a中，同时把该元素的长度添加进list b 中
# 用下标遍历存储长度的list b ，如果元素的长度等于list b中最大元素的长度，则该元素就是符合条件的最长子字符串了，同时获得了该元素的下标
# 最后再用下标去list a 中取子字符串，并把结果存储在list lg中
# 程序结束，lg中的元素就是所有符合条件的子字符串了

正则表达式
把字符串按非数字或字母分割，返回一个list
这时候list内的结果就是仅包含数字或字母的字符串了
ls = re.split(r'\W', s)
'''

def calc(str_in):
    lst_L = re.findall(r'\-?\d+\.?\d*', str_in)
    lst_L = list(map(float, lst_L))
    print("数组L：", lst_L)

    lst_L_abs = list(map(abs, lst_L))

    if len(lst_L) < 1:
        print(-1)
    elif len(lst_L) == 1:
        print(int(lst_L[0] * lst_L[1]))

    else:
        int_N = int(min(lst_L_abs)) + 1
        while int_N >= len(lst_L):
            int_N = int(int_N / 2) + 1

        lst_A = lst_L[:int_N]
        print('数组A：', lst_A)

        lst_B = lst_L[int_N:]
        print('数组B：', lst_B)

        while len(lst_A) > len(lst_B):
            lst_A.remove(max(lst_A))
        while len(lst_B) > len(lst_A):
            lst_B.remove(max(lst_B))

        arr_A = np.array(lst_A)
        arr_B = np.array(lst_B)

        # print('A/B之差平方和：',int(sum((arr_A - arr_B)**2)))

        return int(sum((arr_A - arr_B) ** 2))


# def main():
#     # str_input = input('请输入任意字符串:')
#     str_input = 'calc(\'a1b2c13d14e15f-\')'
#     print('A/B之差平方和：', calc(str_input))
#
#
# if __name__ == '__main__':
#     main()

'''
练习2 =================================================================================================================================================================
(不允许使用eval()函数和第3方库)
给定一任意字符串，判断该字符串是否为由"+-*/.()0123456789 "组成的合法的算术表达式，
如果是，则计算该表达式的值(float类型，保留2位小数)；不是则返回"ERROR"
说明：
1、操作符"+-*/()"前后有空格认为是合法的，数字中间有空格认为非法(例如"1 1+1"或"1. 1+1"非法，但是" 1+ 1"合法)
2、数字不能以0开头，表达式中间的负数和正数必须用括号括起来，否则认为非法(例如"1+-1"非法，"1+(-1)"合法)
3、算术表达式合法时，value为float类型的值；否则，value为"ERROR"

算法思路1：
表达式求值其实是《数据结构》课程里一个基本且重要的问题之一，一般作为 “栈” 的应用来提出。
问题的关键就是需要按照人们通常理解的运算符的优先级来进行计算，而在计算过程中的临时结果则用 栈 来存储。
为此，我们可以首先构造一个 “表” 来存储当不同的运算符 “相遇” 时，它们谁更 “屌” 一些（优先级更高一些）。这样就可以告诉计算机，面对不同的情形，它接下来应该如何来处理。
其次，我们需要构造两个栈，一个运算符栈，一个运算数栈。
运算符栈是为了搞定当某个运算符优先级较低时，暂时先让它呆在栈的底部位置，待它可以 “重见天日” 的那一天（优先级相对较高时），再把它拿出来使用。正确计算完成后，此栈应为空。
运算数栈则是为了按合理的计算顺序存储运算中间结果。正确计算完成后，此栈应只剩下一个数，即为最后的结果。

其中需要稍微注意的细节有：
1. 表达式处理前，前后都插入一个 '#' 作为一个特殊的运算符，这样做是为了方便统一处理，即不用再去特别判断表达式是否已经结束（从而引发一系列边界问题导致代码冗长复杂，这种处理也可称之为 “哨兵” 技巧）。
如果最后两个运算符相遇则说明表达式处理完毕，这个运算符的优先级也是最低的（在 prior 表中也有体现）。
2. 高精度使用decimal模块，配合getcontext().prec = 10设置精度
https://www.cnblogs.com/maples7/p/5212744.html
'''

# import re

def func_exp_format(str_exp):
    lst_ptn = list()
    lst_ptn.append(r'[^\+\-\*\/\.\(\)\d\s]')  # 无效字符
    lst_ptn.append(r'[\+\-\*\/\.]\s*[\+\-\*\/\.\)]')  # 表达式规则：连续符号
    lst_ptn.append(r'\(\s*[\+\*\/\.\)]')  # 表达式规则：左括号
    lst_ptn.append(r'\)\s*[\(\.\d]')  # 表达式规则：右括号
    lst_ptn.append(r'\.[\s\(]|\s\.|\.\d+\.')  # 表达式规则：点号
    lst_ptn.append(r'^[\)\*\/\.]|[\+\-\*\/\.\(]$')  # 表达式规则：起始/结束
    lst_ptn.append(r'\d\s+\d|[^\.\d]0\d')  # 无效数字

    for ptn in lst_ptn:
        err = re.search(ptn, str_exp)
        # print(err)
        if err:
            return 0

    if str_exp.count('(') != str_exp.count(')'):
        return 0
    else:
        return ''.join(str_exp.split())


def func_precede(opra_a, opra_b):
    opra_prior = (
        # '+'   '-'   '*' '/'  '('  ')'   '#'
        ('>', '>', '<', '<', '<', '>', '>'),  # '+'
        ('>', '>', '<', '<', '<', '>', '>'),  # '-'
        ('>', '>', '>', '>', '<', '>', '>'),  # '*'
        ('>', '>', '>', '>', '<', '>', '>'),  # '/'
        ('<', '<', '<', '<', '<', '=', ' '),  # '('
        ('>', '>', '>', '>', ' ', '>', '>'),  # ')'
        ('<', '<', '<', '<', '<', ' ', '=')  # '#'
    )
    opra_idx = {'+': 0, '-': 1, '*': 2, '/': 3, '(': 4, ')': 5, '#': 6}
    return opra_prior[opra_idx[opra_a]][opra_idx[opra_b]]


def func_operate(num_a, num_b, operator):
    if operator == '+':
        ans = num_a + num_b
    elif operator == '-':
        ans = num_a - num_b
    elif operator == '*':
        ans = num_a * num_b
    elif operator == '/':
        if num_b == 0:
            ans = 'ERROR'
        else:
            ans = num_a / num_b
    return ans


def calc(str_exp):

    str_exp = func_exp_format(str_exp)
    if str_exp:
        str_exp += '#'
        opra_set = "+-*/()#"

        stack_opra, stack_num = ['#'], []
        pos, ans, idx, ubound = 0, 0, 0, len(str_exp)

        while idx < ubound:

            elm = str_exp[idx]

            if elm in opra_set:
                if elm == '(' and str_exp[idx + 1] == '-':  # 表示负数的'-'号作为数字的部分，不是运算符
                    stack_opra.append(elm)
                    pos = idx + 1
                    idx += 2
                    while not str_exp[idx] in opra_set:
                        idx += 1
                    try:
                        num = float(str_exp[pos:idx])
                    except:
                        return 'ERROR'
                    stack_num.append(num)
                else:
                    top_opra = stack_opra.pop()
                    opra_prec = func_precede(top_opra, elm)

                    if opra_prec == '>':
                        try:
                            num_a = stack_num.pop()
                            num_b = stack_num.pop()
                        except:
                            return 'ERROR'
                        ans = func_operate(num_b, num_a, top_opra)
                        if ans == 'ERROR':
                            return ans
                        else:
                            stack_num.append(ans)

                    elif opra_prec == '<':
                        stack_opra.append(top_opra)
                        stack_opra.append(elm)
                        idx += 1

                    elif opra_prec == '=':
                        idx += 1
            else:
                pos = idx
                while not str_exp[idx] in opra_set:
                    idx += 1
                try:
                    num = float(str_exp[pos:idx])
                except:
                    return 'ERROR'
                stack_num.append(num)

        if len(stack_num) == 1 and stack_opra == []:
            return round(stack_num.pop(), 2)
        else:
            return 'ERROR'
    else:
        return 'ERROR'


if __name__ == "__main__":

    str_input = '2.34-4+((7.8*(-13-2/14)*3/(4-8)/2))/2.1-6.333*2+0.0'

    value = calc(str_input)
    print(value)


'''
算法思路2：
从最内层括号开始（括号内不含括号），从左向右计算先乘除后加减，使用计算值替换括号内容
逐层括号递归
'''
def func_exp_format(str_exp):
    lst_ptn = list()
    lst_ptn.append(r'[^\+\-\*\/\.\(\)\d\s]')            # 无效字符
    lst_ptn.append(r'[\+\-\*\/\.]\s*[\+\-\*\/\.\)]')    # 表达式规则：连续符号
    lst_ptn.append(r'\(\s*[\+\*\/\.\)]')                # 表达式规则：左括号
    lst_ptn.append(r'\)\s*[\(\.\d]')                    # 表达式规则：右括号
    lst_ptn.append(r'\.[\s\(]|\s\.|\.\d+\.')            # 表达式规则：点号
    lst_ptn.append(r'^[\)\*\/\.]|[\+\-\*\/\.\(]$')      # 表达式规则：起始/结束
    lst_ptn.append(r'\d\s+\d|[^\.\d]0\d')               # 无效数字

    for ptn in lst_ptn:
        err = re.search(ptn, str_exp)
        # print(err)
        if err:
            return 0

    if str_exp.count('(') != str_exp.count(')'):
        return 0
    else:
        return ''.join(str_exp.split())


def func_operate(num_a, num_b, operator):
    if operator == '+':
        ans = num_a + num_b
    elif operator == '-':
        ans = num_a - num_b
    elif operator == '*':
        ans = num_a * num_b
    elif operator == '/':
        if num_b == 0:
            ans = 'ERROR'
        else:
            ans = num_a / num_b
    return ans


def func_num_unsigned_on_side(str_exp, idx):
    exp_end = len(str_exp)-1
    idx_0 = idx
    while str_exp[idx_0-1] in '0123456789.':
        idx_0 -= 1
        if idx_0 == 0:
            break

    idx_1 = idx
    if str_exp[idx_1+1] == '-':
        idx_1 += 1
    while str_exp[idx_1+1] in '0123456789.':
        idx_1 += 1
        if idx_1 == exp_end:
            break
    idx_1 += 1  # 切片序号
    return idx_0, idx_1


def func_simple_exp(simple_exp):
    while '*' in simple_exp or '/' in simple_exp:
        for idx in range(1, len(simple_exp)-1):
            if simple_exp[idx] in '*/':
                opra_rng = func_num_unsigned_on_side(simple_exp, idx)

                str_sub = simple_exp[opra_rng[0]:opra_rng[1]]
                num_0 = float(simple_exp[opra_rng[0]:idx])
                num_1 = float(simple_exp[idx+1:opra_rng[1]])
                result = str(func_operate(num_0, num_1, simple_exp[idx]))
                if result == 'ERROR':
                    return result
                else:
                    simple_exp = simple_exp.replace(str_sub, result)
                break
    simple_exp = simple_exp.replace('+-', '-').replace('--', '+')
    arr_nums = re.findall(r'\+?\-?\d+\.?\d*', simple_exp)
    val_sum = 0
    for elm in arr_nums:
        val_sum += float(elm)
    return val_sum


def calc(str_exp):

    str_exp = func_exp_format(str_exp)
    if str_exp:
        bracket_ptn = r'\([^\(\)]+\)'

        while '(' in str_exp:
            sub_exp = re.findall(bracket_ptn, str_exp)
            for elm in sub_exp:
                simple_exp = elm[1:len(elm)-1]
                result = str(func_simple_exp(simple_exp))
                if result == 'ERROR':
                    return 'ERROR'
                str_exp = str_exp.replace(elm, result)

        result = str(func_simple_exp(str_exp))
        if result == 'ERROR':
            return 'ERROR'
        else:
            return round(float(result), 2)
    else:
        return 'ERROR'


if __name__ == "__main__":

    # str_input = '2.34-4+((7.8*(8-13-2/14+(-10)+7)*3/(4-8)/2))/2.1-6.333*2+0.0'
    str_input = '(3.5-1)*((-0.5+1)+(-4.5)/6+(-5)*2)/10.0'

    value = calc(str_input)
    print(value)
