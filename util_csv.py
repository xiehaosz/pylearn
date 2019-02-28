# coding: UTF-8
import csv
import pandas as pd
import numpy as np


class CsvDatUtil:

    def __init__(self, str_fullname):
        """
        构造方法
        示例  CsvUtil(csv_fullname)
        :param csv_fullname: csv文件路径
        :auther xiehao 00336957
        :date 2019/2/25
        """
        with open(str_fullname) as csv_file:
            self.__csv_name = str_fullname.split("/")[-1]
            self.__csv_df = pd.read_csv(csv_file, header=0)  # 从csv文件读取pd数据
            self.__csv_key = self.__csv_df.columns.tolist()  # list(self.__csv_df)
        csv_file.close()

    def get_df(self):
        return self.__csv_df

    def get_key(self):
        return self.__csv_key

    def get_name(self):
        return self.__csv_name

    # def group_by(self, str_key):
    #     csv_dict = self.__csv_dict
    #     csv_dat = self.__csv_dat
    #     if csv_dict.has_key(str_key):
    #         for name, group in csv_dat.groupby([csv_dat.ulCrnti, csv_dat.ulUeMacId]):
    #             self.__user_id_dict[int(name[0])] = int(name[1])
    #         pass
    #     else:
    #         raise ValueError('不存在[{}]数据列!'.format(str_key))




# 获取csv表头
def aw_get_csv_dict(csv_fullname):
    with open(csv_fullname) as csv_file:
        _reader = csv.DictReader(csv_file)
        _field_names = _reader.fieldnames
        for row_elm in _reader:
            print(row_elm)
        return _field_names


# 逐行读取csv文件内容，reader.line_num获取行号
def aw_get_csv_rows(csv_fullname):
    with open(csv_fullname) as csv_file:
        _reader = csv.reader(csv_file)
        # reader只能被遍历一次，可用next方法一次获取一行, line_num获取行号
        print(next(_reader))
        for row_elm in _reader:
            print(_reader.line_num, list(row_elm))


# 写入内容
def aw_read_csv_rows(self, file_name):
    new_lines = [['name', 'age'], ['Bob', 14]]

    # 如果不指定newline = '', 则每写入一行将有一空行被写入
    with open(file_name, 'w', newline='') as my_file:
        writer = csv.writer(my_file)
        for row in new_lines:
            writer.writerow(row)

        # 写入多行
        writer.writerows(new_lines)
        my_file.close()


if __name__ == "__main__":
    df = pd.DataFrame({'key1': list('ABACCBBAAA'),
                       'key2': ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'],
                       'data1': np.random.randn(10),
                       'data2': np.random.randn(10)})

    # print(df)
    # print(df.groupby(['key1', 'key2']))
    # print(df.groupby(['key1', 'key2']).mean())

    # for (k1, k2), group in df.groupby(['key1', 'key2']):
    # for name, group in df.groupby(['key1', 'key2']):
    #     print(name)

    # grp_dict = dict(list(df.groupby(['key1'])))
    # print(grp_dict.keys())
    # print(grp_dict['B'])

    # grp_lst = list(df.groupby(['key1']))
    # print(grp_lst[0])

    grp_lst = list(df.groupby(['key1'])['data1'])  # 等效list(df['data1'].groupby(df['key1']))
    print(grp_lst[1])
    grp_lst = list(df.groupby(['key1'])[['data1']])
    print(grp_lst[1])

    pass

