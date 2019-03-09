# coding: UTF-8
import io
import os
import util_file_sys as fs


def str_replace(str_file, old_str, new_str):
    """
    替换文件中的字符串
    :param str_file:文件名（含路径）
    :param old_str:旧字符串
    :param new_str:新字符串
    :return:
    """
    # new_txt_dat = ""
    # with io.open(file, "r", encoding="utf-8") as my_file:
    #     for line in my_file:
    #         if old_str in line:
    #             line = line.replace(old_str, new_str)
    #         new_txt_dat += line
    #
    # with io.open(file, "w", encoding="utf-8") as my_file:
    #     my_file.write(new_txt_dat)
    #
    # my_file.close()

    # 功能相同，执行时间短
    with io.open(str_file, "r+", encoding="utf-8") as my_file:
        all_lines = my_file.readlines()
        my_file.seek(0, 0)
        for line_item in all_lines:
            line_new = line_item.replace(old_str, new_str)
            my_file.write(line_new)
        my_file.close()


def probe_fmt(str_dir):
    _my_fs = fs.get_file_lst(str_dir, '.csv')
    fs.set_path(str_dir)
    for _item in _my_fs:
        str_replace(_item, '| | | ', '')


if __name__ == "__main__":
    _str_dir = r'D:\深研TDD多天线能力中心\04 版本档案\eRAN 15.1\20190223 eRAN15.1 G3板链路测试\GENEX Logfile\fmt'
    my_fs = fs.get_file_lst(_str_dir)
    fs.set_path(_str_dir)

    for item in my_fs:
        str_replace(item, '| | | ', '')

    pass


