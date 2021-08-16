import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
from scipy import integrate
from pylab import *

C = 299792.458
PI = np.pi


def sigma_sum(start, end, expression):
    return sum(expression(i) for i in range(start, end, 2))


def fourier_series(x, f, n=0):
    """
    Returns a symbolic fourier series of order `n`.
    :param n: Order of the fourier series.
    :param x: Independent variable
    :param f: Frequency of the fourier series
    """
    from symfit import parameters, variables, sin, cos, Fit
    # Make the parameter objects for all the terms
    a0, *cos_a = parameters(','.join(['a{}'.format(i) for i in range(0, n + 1)]))
    sin_b = parameters(','.join(['b{}'.format(i) for i in range(1, n + 1)]))
    # Construct the series
    series = a0 + sum(ai * cos(i * f * x) + bi * sin(i * f * x)
                      for i, (ai, bi) in enumerate(zip(cos_a, sin_b), start=1))
    return series


def beamforming(d_ant, freq, arr_a, arr_p):
    """
    Returns beamforming result as power and phase.
    :param d_ant: antenna unit interval as mm.
    :param freq: Frequency as MHz
    :param arr_a: weight list of amplitude as numpy array
    :param arr_p: weight list of phase as numpy array
    """
    if len(arr_a) == len(arr_p):
        theta_grid = 360
        arr_theta = np.arange(-PI, PI, 2 * PI/theta_grid)
        # 单元阵子+天线增益
        arr_elm = -np.minimum(12 * ((arr_theta/(90 / 180 * PI)) ** 2), 30) + 12

        arr_re, arr_im = np.zeros(theta_grid), np.zeros(theta_grid)
        arr_idx = np.arange(0, len(arr_a))
        d = d_ant/C*freq

        for iii in range(theta_grid):
            delta_p = d * np.sin(arr_theta[iii]) * PI * 2
            arr_re[iii] = sum(arr_a * np.cos(arr_p / 180 * PI + arr_idx * delta_p))
            arr_im[iii] = sum(arr_a * np.sin(arr_p / 180 * PI + arr_idx * delta_p))

        arr_c = np.vectorize(complex)(arr_re, arr_im)
        arr_pwr = np.maximum(10 * np.log10(arr_c ** 2) + arr_elm, np.zeros(arr_c.shape))
        return arr_theta, arr_pwr


def demo_IQ_modulation_demodulation(period=3, weight=1):
    print('_____演示：I/Q数据的生成与解调_____')

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号

    t = np.linspace(0, 2 * np.pi * period, 1000)
    dt = t[1] - t[0]

    # IQ输入
    a, b = 1.68, -1.45
    print('IQ信号输入：', a, b)
    # IQ生成
    y_cos, y_sin = a * np.cos(weight * t), -b * np.sin(weight * t)
    y_iq = y_cos + y_sin

    plt.figure(figsize=(8, 4))
    plt.subplot(211)
    plt.plot(t, y_cos, 'b--', label=r'$ cos ωt $', linewidth=1)
    plt.plot(t, y_sin, 'g--', label=r'$ -sin ωt $', linewidth=1)
    plt.plot(t, y_iq, label=r'$ IQ $', color='red', linewidth=1)
    plt.legend(loc='upper right')

    # IQ解调
    y_i, y_q = y_iq * np.cos(weight * t), y_iq * (-np.sin(weight * t))
    # 解调输出
    demo_a, demo_b = np.sum(y_i * dt)/period/np.pi, np.sum(y_q * dt)/period/np.pi
    print('IQ信号解调：', demo_a, demo_b)

    plt.subplot(212)
    plt.plot(t, y_i, 'b--', label=r'$ I $', linewidth=1)
    plt.plot(t, y_q, 'g--', label=r'$ Q $', linewidth=1)
    plt.plot(t, y_iq, label=r'$ IQ $', color='red', linewidth=1)
    # plt.plot(t, y_iq, label=r'$\cos ωt - sin ωt$', color='red', linewidth=1)

    plt.xlabel('Time(s)')
    plt.ylabel('amplitude')
    # plt.title('A Sample Example')

    # plt.ylim(-2, 2)
    # plt.xlim(0, 10)
    plt.legend(loc='upper right')
    plt.show()


def demo_rectangular_wave_fourier_series(period=3, sigma_lv=5):
    figure(figsize=(20, 6), dpi=80)
    shift_t, shift_p = 0, 0
    x = np.linspace(0, 2 * np.pi * period, 2048)
    y = shift_p + sigma_sum(1, sigma_lv*2 + 1, lambda i: pow(-1, int(i/2)) / i * np.cos(i * (x + np.pi * shift_t)))
    plt.plot(x, y)
    plt.show()


def demo_rectangular_wave_fourier_series_3d(period=3, sigma_lv=5):
    shift_t, shift_p = 0, 0
    x = np.linspace(0, 2 * np.pi * period, 2048)
    y = shift_p + sigma_sum(1, sigma_lv*2 + 1, lambda i: pow(-1, int(i/2)) / i * np.cos(i * (x + np.pi * shift_t)))

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')

    z = np.zeros(x.shape)
    plt.plot(x, z, y)
    # 分量
    for iii in range(1, sigma_lv*2 + 1):
        y = pow(-1, int(iii/2)) / iii * np.cos(iii * (x + np.pi * shift_t))
        z = np.ones(x.shape) * 2 * iii + np.ones(x.shape) * 2
        plt.plot(x, z, y)

    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()


def demo_fourier_series():
    from symfit import parameters, variables, sin, cos, Fit
    x, y = variables('x, y')
    w, = parameters('w')
    model_dict = {y: fourier_series(x, f=w, n=3)}
    print(model_dict)

    # Make step function file_H
    xdata = np.linspace(-np.pi, np.pi)
    ydata = np.zeros_like(xdata)
    ydata[xdata > 0] = 1
    # Define a Fit object for this model and file_H
    fit = Fit(model_dict, x=xdata, y=ydata)
    fit_result = fit.execute()
    print(fit_result)

    # Plot the result
    plt.plot(xdata, ydata)
    plt.plot(xdata, fit.model(x=xdata, **fit_result.params).y, color='green', ls=':')
    plt.show()


def demo_rotation_vector(end=50):
    fig = plt.figure()
    ax1 = Axes3D(fig)
    zt = np.linspace(0, end, end * 20)
    xc = np.cos(zt)
    ys = np.sin(zt)
    ax1.plot3D([0, end], [0, 0], [0, 0])
    ax1.plot3D([end, end], [0, list(xc)[-1]], [0, list(ys)[-1]])
    ax1.plot3D(zt, xc, ys)

    ax1.set_xlabel('Time', color='g', fontsize='14')
    ax1.set_ylabel('real°', color='b', fontsize='14')
    ax1.set_zlabel('image', color='r', fontsize='14')
    plt.show()


def demo_Lissajous_figur(num=3, end=5):
    """李萨育图形:
    由在相互垂直的方向上的两个频率成简朴整数比的简谐振动所合成的规矩的、稳定的闭合曲线
    相成谐波频率关系的两个信号分别作为X和Y偏转信号送入示波器时，这两个信号分别在X轴、Y轴方向同时作用于电子束而描绘出稳定的图形"""
    # figure(figsize=(20, 3.5), dpi=80)
    for n in range(1, num):
        zt = np.linspace(0, end, end*100)
        xc = np.cos(2 * np.pi * zt)  # cos(2πft)
        ys = np.sin(2 * np.pi * n * zt)  # sin(2nπft)
    #     subplot(1, 5, n)
    #     plot(xc, ys)
    # plt.show()
    # 李萨育图形3D
    fig = plt.figure()
    ax1 = Axes3D(fig)
    ax1.plot3D([0, end], [0, 0], [0, 0])
    ax1.plot3D([end, end], [0, list(xc)[-1]], [0, list(ys)[-1]])
    ax1.plot3D(zt, xc, ys)
    plt.show()


def demo_cos_sin_function_composition():
    plt.rcParams['font.sans-serif']=['SimHei']#用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False#用来正常显示负号
    # # 一个周期
    # x=np.arange(0,2*np.pi,0.01)
    # y=np.sin(x)

    x = np.linspace(0, 10, 1000)
    y1 = np.sin(x) + 1
    y2 = np.cos(x ** 2) + 1

    plt.figure(figsize=(8, 4))
    plt.plot(x, y1, label=r'$\sin x+1$', color='red', linewidth=2)
    plt.plot(x, y2, 'b--', label=r'$\cos x^2+1$', linewidth=1)
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.title('A Sample Example')
    plt.ylim(0, 2.2)
    plt.xlim(0, 10)
    plt.legend(loc='upper right')
    plt.show()


def demo_sinc(points=100):
    plt.rcParams['font.sans-serif']=['SimHei']#用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False#用来正常显示负号
    x = np.linspace(-5 * np.pi, 5 * np.pi, points)
    y = np.sinc(x/np.pi)
    y0 = [0] * points
    # plt.axis([np.min(x), np.max(x), 0, np.max(y)])
    plt.plot(x, y, label="$ function $")
    plt.plot(x, y0, 'b--', linewidth=1)
    # 填充积分区域
    plt.fill_between(x, y1=y, y2=0, where=(x >= 0) & (x <= 2 * np.pi), facecolor='blue', alpha=0.2)
    plt.legend()
    plt.show()


def demo_antenna_unit_pattern():
    # 单环天线 f(θ)=sin(π * cosθ/ λ)
    theta = np.arange(0, 2*np.pi, 0.02)
    d_lambda1 = 0.5
    d_lambda2 = 0.75

    ax = plt.subplot(121, polar=True)  # 极坐标
    ax.set_thetagrids(np.arange(0.0, 360.0, 10.0))  # 设置角度网格线
    # ax.set_rgrids(np.arange(0.1, 1.6, 0.1), angle=45)  # 设置半径网格线
    ax.set_theta_zero_location('N')  # 设置0°位置,其值可为'N','NW','W','SW','S','SE','E','NE'
    ax.set_theta_direction(-1)  # 设置极坐标的正方向，参数为-1时为顺时针方向

    plt.plot(theta, np.abs(np.sin(d_lambda1 * np.pi * np.cos(theta))),  color=[1, 0, 0], lw=1)
    plt.plot(theta, np.abs(np.sin(d_lambda2 * np.pi * np.cos(theta))),  '--', lw=1)

    plt.title("d_lambda="+str(d_lambda1), fontsize=12)
    # plt.savefig('d_lambda='+str(d_lambda)+'.png')
    # plt.show()

    # 复合环天线 f(θ)= sqrt(cosθ**2 + 2kcosρcosθ + k**2)
    k = 0.7
    phi0 = 0

    ax = plt.subplot(122, polar=True)  # 极坐标
    ax.set_thetagrids(np.arange(0.0, 360.0, 10.0))  # 设置角度网格线
    # ax.set_rgrids(np.arange(0.2, 2, 0.2), angle=45)  # 设置半径网格线
    ax.set_theta_zero_location('N')  # 设置0°位置,其值可为'N','NW','W','SW','S','SE','E','NE'
    ax.set_theta_direction(-1)  # 设置极坐标的正方向，参数为-1时为顺时针方向

    plt.plot(theta, np.sqrt(np.square(np.cos(theta))+2*k*np.cos(phi0)*np.cos(theta)+np.square(k)),  color=[1, 0, 0], lw=2)

    plt.title("k="+str(k)+",phi0="+str(phi0), fontsize=12)
    plt.savefig("k="+str(k)+" with phi0="+str(phi0)+'.png')
    plt.show()


def demo_beamforming_patten(d_ant=57, freq=2600,
                            arr_a=[1, 1, 1, 1, 1, 1, 1, 1],
                            arr_p=[0, 45, 90, 135, 180, 225, 270, 315]):
    """
    Returns beamforming result as power and phase.
    :param d_ant: antenna unit interval as mm.
    :param freq: Frequency as MHz
    :param arr_a: weight list of amplitude
    :param arr_p: weight list of phase
    """
    arr_a = np.array(arr_a)
    arr_p = np.array(arr_p)

    arr_theta, arr_pwr = beamforming(d_ant, freq, arr_a, arr_p)
    ax = plt.subplot(111, polar=True)  # 极坐标
    ax.set_thetagrids(np.arange(0.0, 360.0, 10.0))  # 设置角度网格线
    plt.plot(arr_theta, arr_pwr)
    plt.show()




if __name__ == "__main__":
    # demo_IQ_modulation_demodulation(period=3, weight=1)
    # demo_rectangular_wave_fourier_series(period=3, sigma_lv=60)
    # demo_rectangular_wave_fourier_series_3d(period=3, sigma_lv=5)
    # demo_fourier_series()
    # demo_rotation_vector(end=100)
    # demo_Lissajous_figur(num=3, end=100)
    demo_cos_sin_function_composition()
    # demo_sinc()
    # demo_antenna_unit_pattern()
    # demo_beamforming_patten(d_ant=57, freq=2600,
    #                         arr_a=[1, 1, 1, 1, 1, 1, 1, 1],
    #                         arr_p=[0, 45, 90, 135, 180, 225, 270, 315])
