# coding: UTF-8
import os
import io


# 获取文件列表（不含子文件夹）
def get_file_lst(str_dir, str_ext):
    """
    os.walk返回一个三元组 tuple(path, dirs, files)
    path 所有文件夹路径
    dirs 所有文件夹名称
    files 所有文件名称
    """
    # _fs = os.listdir(str_dir) # 获取文件列表和文件夹列表
    _fs = []
    for root, dirs, files in os.walk(str_dir):
        for elm in files:
            if os.path.splitext(elm)[1] == str_ext:  # elm.endswith(str_ext)
                _fs.append(elm)
    return _fs


# 获取后缀名
def get_file_extension(str_file):
    return os.path.splitext(str_file)[1]


# 从路径中截取文件名
def get_file_name(str_fullname):
    return str_fullname.split("/")[-1]
    # return os.path.basename(str_fullname)


# 打开文件
def open_file(str_fullname):
    return io.open(str_fullname, "r", encoding="utf-8")


# 工作路径
def set_path(str_dir):
    old_dir = os.getcwd()
    os.chdir(str_dir)  # 更改当前工作目录
    print('Working dir:{}'.format(old_dir))
    print('Change to:{}'.format(os.getcwd()))


if __name__ == "__main__":
    # lst_file = get_file_lst(r'./')
    # print(lst_file)
    set_path(r'D:\Python\PycharmProjects\my_python_learning')
    pass
