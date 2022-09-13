import time
import os
import random
from copy import deepcopy
from datetime import datetime

import numpy as np


def random_key(length):
    from secrets import token_bytes
    key = token_bytes(nbytes=length)
    key_int = int.from_bytes(key, 'big')
    return key_int


def get_key(key, save_path=r'C:\pykey.txt'):
    """
    秘钥处理，不论输入的key是什么类型，都会转换为字节格式
    :param key:      提供key值，将秘钥文件保存至path
    :param save_path: 不提供key值, path读取key
    :return: 返回保存的文件路径（写）或返回key值字节（读）
    """
    decoding = "utf-8"
    if os.path.isfile(key):
        key_obj = open(save_path, "rb")
        key_bytes = key_obj.read()
        key_obj.close()
    else:
        key_bytes = bytes(str(key), decoding)
        if os.path.isfile(save_path):
            key_obj = open(save_path, "wb")
            key_obj.write(key_bytes)
            key_obj.close()
    return key_bytes  # 解码: bytes.decode(key, decoding)


def crypt_file(path: str, key: bytes, ext=None, replace=False):
    """
    加密文件样例：crypt_file(r'D:\test.txt', get_key(123456))
    :param path:    支持单个文件或路径（路径下所有文件）
    :param key:     秘钥
    :param ext:     对特定后缀名的文件加密
    :param replace: 默认保留原文件, 设置为True时会替换原文件
    :return:
    """
    if os.path.isfile(path):
        _p, _f = os.path.split(path)
        _name, _ext = os.path.splitext(_f)
        if ext and ext != _ext:
            return
        enc_file = os.path.join(_p, '%s_enc%s' % (_name, _ext))

        f_raw = open(path, 'rb')   # 原始文件
        f_bytes = f_raw.read()
        name_bytes = _f.encode()

        f_enc = open(enc_file, 'wb')    # 加密文件
        # 对目标文件进行一次xor操作是加密, 用同一个密钥文件加密文件进行一次xor操作就是解密
        enc_bytes = [f_bytes[i] ^ key[i % len(key)] for i in range(len(f_bytes))]
        f_enc.write(bytes(enc_bytes))

        f_raw.close()
        f_enc.close()
        if replace:
            os.replace(enc_file, path)

    elif os.path.isdir(path):
        for f in os.listdir(path):
            crypt_file(os.path.join(path, f), key, ext, replace)


def str_code(s):
    k = list(range(97, 123))
    if s.isdigit():
        shift = int(s[-1] + s[0])
        decoder = dict(zip(k[:shift][::-1] + k[shift:][::-1], k))
        return ''.join([chr(decoder[int(s[i: i + 2]) + 97]) for i in range(1, len(s) - 2, 2)])
    else:
        s, shift = s.lower(), random.randint(1, 25)
        coder = dict(zip(k, k[:shift][::-1] + k[shift:][::-1]))
        _shift = '%02d' % shift
        return _shift[1] +''.join(['%02d' % (coder[ord(c)]-97) for c in s]) + _shift[0]


def compress(path, single_mode=False, ext='.rar', tool=None):
    """
    压缩文件
    :param path:        文件名或路径
    :param single_mode: 路径下每个文件单独打包
    :param ext:         压缩文件后缀
    :param tool:        指定压缩工具路径
    :return:
    """
    search = [r'C:\Program Files\WinRAR\WinRAR.exe',
              r'C:\Program Files (x86)\WinRAR\WinRAR.exe']

    if tool is None:
        for _p in search:
            if os.path.exists(_p):
                tool = _p
                break
    if tool is None:
        raise RuntimeError('Can not find compress tool.')

    if os.path.isfile(path):
        os.system('"%s" a %s%s %s' % (tool, path, ext, path))
        return
    if os.path.isdir(path):
        if single_mode:
            # 文件名不要有特殊符号譬如&/+等,没有保护
            for _f_name in os.listdir(path):
                _f, _x = os.path.splitext(_f_name)
                if _x in ['.rar', '.zip', '7z']:
                    continue
                _z_name = os.path.join(path, _f)
                _f_name = os.path.join(path, _f_name)
                os.system('"%s" a -ep %s%s %s' % (tool, _z_name, ext, _f_name))
        else:
            os.system('"%s" a -ep %s%s %s' % (tool, path, ext, path))
        return


def encrypt(f_path):
    t = '{}{}{}{}'.format(datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute)

    # compress(f_path, single_mode=True)
    crypt_file(f_path, get_key(12345678), replace=True)
    i = 1
    for f in os.listdir(f_path):
        _, ext = os.path.splitext(f)
        if ext == '.rar':
            os.rename(os.path.join(f_path, f), os.path.join(f_path, 'en_%s_(%s).csv' % (t, i)))
            i += 1


def digitization(path: str, ext=None, decode=False):
    """
    数字化/逆数字化（小文件)
    :param path:    支持单个文件或路径（路径下所有文件）
    :param ext:     对特定后缀名的文件处理
    :param decode:  逆数字化
    :return:
    """
    if not os.path.isfile(path):
        return
    _p, _f = os.path.split(path)
    _name, _ext = os.path.splitext(_f)
    if ext and ext != _ext:
        return

    if decode:
        digits = np.loadtxt(path, delimiter=",", skiprows=0).flatten()
        end = 0
        while digits[end-1] < 0:
            end -= 1
        if end < 0:
            digits = digits[:end]
        f_bytes = int(digits[0]).to_bytes(1, 'big')
        for i in digits[1:]:
            f_bytes += int(i).to_bytes(1, 'big')

        f_rebuild = open(os.path.join(_p, _name + '_rebuild' + _ext), 'wb')
        f_rebuild.write(bytes(f_bytes))
        f_rebuild.close()

    else:
        width = 32
        f_raw = open(path, 'rb')   # 原始文件
        f_bytes = list(f_raw.read())
        padding = width - len(f_bytes) % width
        if padding > 0:
            shape_x = len(f_bytes) // width + 1
            f_bytes.extend([-1] * padding)
        else:
            shape_x = len(f_bytes) / width
        arr = np.reshape(f_bytes, (shape_x, width)).astype(np.int16)
        np.savetxt(os.path.join(_p, '%s_2d.csv' % _name), arr, delimiter=',')
        f_raw.close()


if __name__ == '__main__':
    encrypt(r'D:\temp\test')
