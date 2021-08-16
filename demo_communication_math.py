from matplotlib import pyplot as plt
import numpy as np
import scipy.signal
from scipy.io import loadmat
from scipy.linalg import norm


def mat_multiply(ax, bx):
    # 二维矩阵乘法实现
    try:
        ax, bx = np.asmatrix(ax), np.asmatrix(bx)
    except Exception as e:
        raise e
    m, p = ax.shape
    q, n = bx.shape
    if p == q:
        res = np.zeros([m, n])
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    res[i, j] += (ax[i, k] * bx[k, j])
        return res
    else:
        print(p, q, 'shapes', ax.shape, 'and', bx.shape, 'not aligned')


def demo_function_convolution(p0=[1, 2, 3], p1=[4, 5, 6]):
    a = np.array(p0)
    b = np.array(p1)
    c = np.convolve(a, b)
    print('使用np.convolve函数卷积：\n', c)

    c = scipy.signal.convolve(a, b)
    print('使用scipy.signal.convolve函数卷积：\n', c)

    c = []
    for iii in range(len(a)+len(b)-1):
        s = 0
        for jjj in range(iii+1):
            if 0+jjj < len(a) and iii-jjj < len(b):
                s += a[0+jjj] * b[iii-jjj]
        c.append(s)
    print('使用反褶循环位移乘法实现卷积：\n', c)


def demo_function_matrix_multiply(mat0=[[1, 2], [3, 4]], mat1=[[6], [5]]):
    print('自定义函数实现矩阵乘法：\n', mat_multiply(mat0, mat1))
    print('使用numpy.dot函数矩阵乘法：\n', np.dot(mat0, mat1))


if __name__ == "__main__":
    # demo_function_convolution([1, 3, 6], np.arange(10))
    demo_function_matrix_multiply()
