import numpy as np
import matplotlib.pyplot as plt
from math import ceil, log2
from scipy.fftpack import fft, ifft
from matplotlib.pylab import mpl

def func_periodic_detect(series):
    # 用滑窗对比相同连续值识别周期长度，适用简单函数
    window = int(len(series)/2)
    for i in range(1, len(series) - window):
        if (series[0: int(window)] == series[i: int(i + window)]).all():
            break
    return i - 1


def gen_multi_freq_signal(vec_freq, vec_amp, t_unit=0.5, t_num=500):
    """
    :param vec_f: 频率分量，单位Hz
    :param vec_a: 各频率分量对应的幅度系数
    :param vec_a: 各频率分量对应的幅度系数
    :return: 包含多个频率分量的复合信号
    """
    if t_num/t_unit < max(vec_freq) * 2:
        e = '采样定理要求采样频率要大于信号频率的2倍,即t_num不小于' + str(max(vec_freq) * 2)
        raise ValueError(e)
    vec_t = np.linspace(0, t_unit, t_num)
    vec_y = np.zeros(t_num)
    for i in range(len(vec_freq)):
        vec_y += vec_amp[i] * np.sin(2 * np.pi * vec_freq[i] * vec_t)
    return vec_t, vec_y


def demo_discrete_fourier_transform(arr_y=[1, 2, -1, 2]):
    """
    :param h0, h1:信道矩阵格式要求为二维，[基站天线数, 终端天线数]
    :return: DFT result
    """
    arr_x = list(range(len(arr_y)))
    dft_exp = ceil(log2(len(arr_y)))
    # DFT point = 2 ** dft_exp, DFT点数至少大于序列值的个数

    fig = plt.figure(figsize=(16, 6))
    ax = fig.add_subplot(2, 3, 1)
    markerline, stemlines, baseline = plt.stem(arr_x, arr_y, linefmt='-', markerfmt='o', basefmt='--')  # label='TestStem
    ax.set_title('series', pad=15, fontsize='10')
    ax.set_xticks(arr_x)
    plt.setp(markerline, color='k')  # 将棉棒末端设置为黑色
    # plt.setp(baseline, color='b')

    '''序列有效长度为4，用大于4的采样点数即在有限长离散时间序列尾部补零，DFT谱线更密。这是因为增长观察时间，可提高频率分辨率
    但DFT频谱的包络，始终与非周期序列的离散时间傅立叶变换DTFT的连续频谱曲线一致'''
    for iii in range(5):
        dft_series = np.fft.fft(arr_y, 2 ** (dft_exp+iii))
        arr_x = list(range(len(dft_series)))

        ax = fig.add_subplot(2, 3, iii + 2)
        ax.set_title('DFT' + str(2 ** (dft_exp+iii)), pad=15, fontsize='10')
        plt.stem(arr_x, dft_series)
        plt.grid(True)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show()


def demo_fast_fourier_transform_01(vec_t, vec_y, fft_num=100):
    """
    :param vec_f: 频率分量，单位Hz
    :param vec_a: 各频率分量对应的幅度系数
    :param dft_factor: fft的点数系数，值越大点数越多
    :return: FFT result
    """
    # 傅里叶变换实例
    # 在0~t时间内有n个采样点，即采样频率为n/tHz，len(vec_t)/vec_t[-1]
    # 如果n个采样点恰好匹配了一个完整的原始信号周期，那么FFT变换后的频率则非常精准
    # 如果n个采样点没有匹配原始信号周期，那么FFT变换后的频率会多出一些杂散的分量
    period = func_periodic_detect(vec_y)

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(311)
    ax.plot(vec_t, vec_y)

    dft = fft(vec_y, fft_num)  # >FFT点数, 影响频谱的精度
    n = np.array(range(len(dft)))
    ax = fig.add_subplot(312)
    ax.plot(n, np.abs(dft))

    # 第m个采样点对应的频率 f = m * 采样频率 / 采样点数N, 反之f对应的样点n为 n = f * 采样点数N / 采样频率
    f = n * len(vec_t)/vec_t[-1] / (fft_num)
    ax = fig.add_subplot(313)
    ax.plot(f[:int(len(n)/2)], np.abs(dft[:int(len(n)/2)]))
    plt.show()


def demo_fast_fourier_transform_02(vec_t, vec_y):
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
    mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

    fig = plt.figure(figsize=(16, 4))
    ax = fig.add_subplot(141,)
    plt.plot(vec_t, vec_y)
    plt.title('原始波形')

    N = len(vec_t)  # 频率分量个数

    fft_y = fft(vec_y)  # 快速傅里叶变换，未指定fft点数，所以变换后数据长度和原始采样信号长度相同
    vec_n = np.arange(len(vec_t))
    vec_f = vec_n /vec_t[-1]  # 样点对应的频率

    angle_y = np.angle(fft_y)
    ax = fig.add_subplot(142)
    plt.plot(vec_f, angle_y, 'coral')
    plt.title('双边相位谱')

    '''
    假设信号：Y=A1+A2*cos(2πω2+φ2）+A3*cos(2πω3+φ3）+A4*cos(2πω4+φ4）
    经过FFT之后的频谱分量幅度：
    第一个频率位置的模是A1的N倍，N为采样点（直流分量）
    第二个频率位置的模是A2的N/2倍
    第三个频率位置的模是A3的N/2倍
    ...
    因此归一化处理，所有幅值除以N
    '''
    abs_y = np.abs(fft_y)/N
    ax = fig.add_subplot(143)
    plt.plot(vec_f, abs_y, 'g')
    plt.title('双边振幅谱')

    # FFT具有对称性，一般只需要用N的一半即可
    ax = fig.add_subplot(144)
    plt.plot(vec_f[:int(N/2)], abs_y[:int(N/2)], 'b')
    plt.title('单边振幅谱')
    plt.show()


if __name__ == "__main__":
    # demo_discrete_fourier_transform(arr_y=[1, 2, -1, 2])

    vec_t, vec_y = gen_multi_freq_signal(vec_freq=[40, 60, 90],
                                         vec_amp=[1, 0.5, 0.25],
                                         t_unit=0.5, t_num=500)
    demo_fast_fourier_transform_01(vec_t, vec_y, fft_num=1000)

    # vec_t, vec_y = gen_multi_freq_signal(vec_freq=[20, 40, 60],
    #                                      vec_amp=[7, 5, 3],
    #                                      t_unit=1, t_num=140)
    # demo_fast_fourier_transform_02(vec_t, vec_y)
