# coding: UTF-8
import csv
import pandas as pd
import numpy as np


class CsvDatUtil:

    def __init__(self, str_fullname):
        """
        构造方法
        示例  CsvUtil(csv_fullname)
        :param str_fullname: csv文件路径
        :auther xiehao 00336957
        :date 2019/2/25
        """
        with open(str_fullname) as csv_file:
            self.__csv_name = str_fullname.split("/")[-1]
            self.__csv_df = pd.read_csv(csv_file, header=0, low_memory=False)  # 从csv文件读取pd数据， low_memory=False混合类型
            self.__csv_key = self.__csv_df.columns.tolist()  # list(self.__csv_df)
        csv_file.close()

    def get_df(self):
        return self.__csv_df

    def get_key(self):
        return self.__csv_key

    def get_name(self):
        return self.__csv_name

    def get_cols(self, lst_keys):
        _col_keys = []
        for _item in lst_keys:
            if _item in self.__csv_key:
                _col_keys.append(_item)

        return self.__csv_df[_col_keys]

    def group_by(self, *args):
        """
        args: 传入列标题数组，第一组作为排序依据by_keys
              第二组为提取的数据列group_keys，如果不传递group_keys则选取全部数据列
        返回: 分组名称（数组），分组数据帧（数组）
        """
        _group_name = []
        _group_df = []
        _df = self.__csv_df

        _by_keys = []
        for _item in args[0]:
            if _item in self.__csv_key:
                _by_keys.append(_df[_item])
            else:
                print("Key {} doesn't exist.".format(_item))
                args[0].remove(_item)

        _group_keys = []
        if len(args) > 1:
            for _item in args[1]:
                if _item in self.__csv_key:
                    _group_keys.append(_df[_item])
                else:
                    print("Key {} doesn't exist.".format(_item))
                    args[0].remove(_item)

        if len(_by_keys) > 0:
            if len(_group_keys) > 0:
                selected_keys = args[0] + args[1]
                _df = self.__csv_df[selected_keys]  # 获取部分数据列
            for name, group in _df.groupby(_by_keys):
                _group_name.append(name)
                _group_df.append(group)
        else:
            print('key err.')

        return _group_name, _group_df


# 获取csv表头
def aw_get_csv_dict(csv_fullname):
    with open(csv_fullname) as csv_file:
        _reader = csv.DictReader(csv_file)
        _field_names = _reader.fieldnames
        for row__item in _reader:
            print(row__item)
        return _field_names


# 逐行读取csv文件内容，reader.line_num获取行号
def aw_get_csv_rows(csv_fullname):
    with open(csv_fullname) as csv_file:
        _reader = csv.reader(csv_file)
        # reader只能被遍历一次，可用next方法一次获取一行, line_num获取行号
        print(next(_reader))
        for row__item in _reader:
            print(_reader.line_num, list(row__item))


# 写入内容
def aw_read_csv_rows(file_name):
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
    # df1 = pd.DataFrame({'key1': list('ABACCBBAAA'),
    #                    'key2': ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'],
    #                    'data1': np.random.randn(10),
    #                    'data2': np.random.randn(10)})
    # save_as = r'D:\test.csv'
    # df1.to_csv(save_as, index=False, sep=',')   # 存为csv文件

    my_dir = r'D:\Python\PycharmProjects\data_samples\csv_sample.csv'

    my_csv = CsvDatUtil(my_dir)

    # ========================================
    # my_by_keys = ['PCC Power Headroom(dB)', 'PCC Transmission Mode']
    # my_grp_keys = ['PCC Average SINR(Normal/csi-MeasSubframeSet1)(dB)', 'PCC MAC Throughput DL(kbit/s)']
    #
    # grp_name, grp_df = my_csv.group_by(my_by_keys)
    # for index in range(len(grp_name)):
    #     print(grp_name[index])
    #     print(grp_df[index])
    # pass

    # ========================================
    cols = ['PCC Average SINR(Normal/csi-MeasSubframeSet1)(dB)', 'PCC MAC Throughput DL(kbit/s)']
    df2 = my_csv.get_cols(cols)


