from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter  # 坐标轴设置

C = 299792.458
PI = np.pi
THETA_GRID = 90


def ant_3d(arr_theta, arr_pwr_3d):

    # 单元阵子 & 天线增益
    elm_bw_h = 90  # 水平阵子半波功率角
    elm_bw_v = 35  # 垂直阵子半波功率角
    ant_gain = 17.5

    arr_elm_h = -np.minimum(12 * ((arr_theta / (elm_bw_h / 180 * PI)) ** 2), 30)
    arr_elm_v = -np.minimum(12 * ((arr_theta / (elm_bw_v / 180 * PI)) ** 2), 30)
    eh, ev = np.meshgrid(arr_elm_h, arr_elm_v)
    sphere_elm = np.maximum(eh + ev, -30)

    arr_db_3d = []
    for polar in arr_pwr_3d:
        arr_db_3d.append(np.maximum(polar + sphere_elm + ant_gain, np.zeros(sphere_elm.shape)))
    # ax = plt.subplot(111, polar=True)  # 极坐标
    # ax.set_thetagrids(np.arange(0.0, 360.0, 10.0))  # 设置角度网格线
    # plt.plot(arr_theta, np.squeeze(arr_db_3d[0][int(THETA_GRID/2), :]))
    # plt.plot(arr_theta, np.squeeze(arr_db_3d[0][:, int(THETA_GRID/2)]))
    # plt.show()
    return arr_db_3d


def beamforming_1d_linear(arr_a, arr_p, d_ant, arr_theta):
    d = d_ant / C * freq
    try:
        arr_idx, arr_re, arr_im = np.arange(0, len(arr_a)), np.zeros(THETA_GRID), np.zeros(THETA_GRID)
        for iii in range(THETA_GRID):
            delta_p = d * np.sin(arr_theta[iii]) * PI * 2
            arr_re[iii] = sum(arr_a * np.cos(arr_p / 180 * PI + arr_idx * delta_p))
            arr_im[iii] = sum(arr_a * np.sin(arr_p / 180 * PI + arr_idx * delta_p))
        arr_c = np.abs(np.vectorize(complex)(arr_re, arr_im)) ** 2
    except ValueError:
        print('处理异常：幅度矩阵和相位矩阵size不一致')
        raise
    return arr_c


def beamforming_3d_liner(arr_a_3d, arr_p_3d, freq, arr_d_ant=(57, 175)):
    try:
        ant_p = arr_a_3d.shape[0]
        ant_h = arr_a_3d.shape[2]
        ant_v = arr_a_3d.shape[1]

        ant_dh = arr_d_ant[0]
        ant_dv = arr_d_ant[1]
        arr_theta = np.arange(-PI/2, PI/2, PI / THETA_GRID)

        arr_pwr_3d = []
        for p in range(ant_p):  # 极化
            # horizontal array
            arr_pwr_h = np.zeros(THETA_GRID)
            for v in range(ant_v):  # 水平每行功率叠加
                arr_c = beamforming_1d_linear(arr_a_3d[p:p+1, v:v+1].squeeze(),
                                              arr_p_3d[p:p+1, v:v+1].squeeze(),
                                              ant_dh, arr_theta)
                arr_pwr_h += arr_c
            arr_db_h = 10 * np.log10(arr_pwr_h / ant_v)

            # vertical array
            arr_pwr_v = np.zeros(THETA_GRID)
            for h in range(ant_h):  # 垂直每列功率叠加
                arr_c = beamforming_1d_linear(arr_a_3d[p:p+1, :, h:h+1].squeeze(),
                                              arr_p_3d[p:p+1, :, h:h+1].squeeze(),
                                              ant_dv, arr_theta)
                arr_pwr_v += arr_c
            arr_db_v = 10 * np.log10(arr_pwr_v / ant_h)

            # 球面坐标theta和phi二维数据功率值
            '''
            sphere_pwr = np.zeros((THETA_GRID, THETA_GRID))
            for i in range(THETA_GRID):
                for j in range(THETA_GRID):
                    sphere_pwr[i, j] = arr_pwr_h[j] + arr_pwr_v[i]
            '''
            dbh, dbv = np.meshgrid(arr_db_h, arr_db_v)
            sphere_db = np.maximum(dbh + dbv, np.zeros(dbh.shape))
            arr_pwr_3d.append(sphere_db)  # 极化

            arr_db_3d = ant_3d(arr_theta, arr_pwr_3d)

        # # 单维度切面天线图
        # arr_db_h = np.maximum(arr_db_h, np.zeros(arr_pwr_h.shape))
        # arr_db_v = np.maximum(arr_db_v, np.zeros(arr_pwr_h.shape))
        # ax = plt.subplot(111, polar=True)  # 极坐标
        # ax.set_thetagrids(np.arange(0.0, 360.0, 10.0))  # 设置角度网格线
        # plt.plot(arr_theta, arr_db_h)
        # plt.plot(arr_theta, arr_db_v)
        # plt.show()

    except ValueError:
        print('处理异常：幅度矩阵和相位矩阵size不一致')
        raise
    return arr_theta, arr_db_3d

def polt3d_set(ax, title):
    ax.set_title(title, pad=15, fontsize='16')
    ax.set_xlim3d(-90, 90)
    ax.tick_params(axis='x', labelsize=8)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.set_xlabel('Horiontal θ°', color='g', fontsize='14')
    ax.set_ylim3d(-90, 90)
    ax.tick_params(axis='y', labelsize=8)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.set_ylabel('Vertical φ°', color='b', fontsize='14')
    ax.tick_params(axis='z', labelsize=8)
    ax.zaxis.set_major_locator(MultipleLocator(5))
    ax.set_zlabel('Power(dB)', color='r', fontsize='14')


if __name__ == "__main__":
    # 3d weight include (horizontal, vertical, polarization)
    freq = 2600  # MHz
    # 水平，垂直阵子间距
    arr_d_ant = (57, 175)

    # 幅度权值：极化 * 垂直 * 水平
    arr_a_3d = np.array([[[1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1]],
                         [[1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1]]
                         ])
    # 相位权值：极化 * 垂直 * 水平
    arr_p_3d = np.array([[[0, 45, 90, 135, 180, 225, 270, 315],
                          [0, 46, 90, 135, 180, 225, 270, 315],
                          [0, 47, 90, 135, 180, 225, 270, 315],
                          [0, 48, 90, 135, 180, 225, 270, 315]],
                         [[0, 49, 90, 135, 180, 225, 270, 315],
                          [0, 50, 90, 135, 180, 225, 270, 315],
                          [0, 51, 90, 135, 180, 225, 270, 315],
                          [0, 52, 90, 135, 180, 225, 270, 315]]
                         ])

    arr_theta, arr_db_3d = beamforming_3d_liner(arr_a_3d, arr_p_3d, freq, arr_d_ant)

    # 3D天线图（非球面）
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(121, projection='3d')
    X, Y = np.meshgrid(arr_theta / PI * 180, arr_theta / PI * 180)
    Z = arr_db_3d[0]
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))  # YlGnBu_r
    polt3d_set(ax, 'polarization +45')

    ax = fig.add_subplot(122, projection='3d')
    Z = arr_db_3d[1]
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))  # YlGnBu_r
    polt3d_set(ax, 'polarization -45')

    plt.show()
    # # 3D天线图（球面）不太对，待改进
    # theta, phi = np.meshgrid(arr_theta, arr_theta)
    # fig = plt.figure(figsize=(12, 6))
    # ax = fig.add_subplot(111, projection='3d')
    # Z = arr_db_3d[0] * np.cos(phi)
    # X = arr_db_3d[0] * np.sin(phi) * np.cos(theta)
    # Y = arr_db_3d[0] * np.sin(phi) * np.sin(theta)
    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))  # YlGnBu_r



