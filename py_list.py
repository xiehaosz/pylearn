# coding: UTF-8

# 数组操作
lst1 = [1, 2, 3, 4, 5]
lst2 = ['a', 'b', 'c', 'd', 'e']

lst3 = lst1 + lst2  # 返回连接
print(lst3)
lst1.extend(lst2)   # 直接连接
print(lst1)
lst1[1:1] = lst2    # 插入
print(lst1)

del lst1[3]  # 删除元素(序号)
print(lst1)

lst1.pop(2)  # 删除元素(序号)
print(lst1)

lst2.remove('a')  # 删除元素(第一个匹配值)
print(lst2)

lst3 = lst3[:2] + lst3[4:]  # 删除元素
print(lst3)


#  数据帧操作
# grp_dict = dict(list(df.groupby(['key1'])))
# print(grp_dict.keys())
# print(grp_dict['B'])

# grp_lst = list(df.groupby(['key1']))
# print(grp_lst[0])

# grp_lst = list(df.groupby(['key1'])['data1'])  # 等效list(df['data1'].groupby(df['key1']))
# print(grp_lst[1])
# grp_lst = list(df.groupby(['key1'])[['data1']])
# print(grp_lst[1])
