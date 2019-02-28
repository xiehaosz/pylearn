# coding: UTF-8
import matplotlib as mpl
import matplotlib.pyplot as plt

import util_csv as csv

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

if __name__ == "__main__":

    file = r'D:\深研TDD多天线能力中心\04 版本档案\eRAN 15.1\20190223 eRAN15.1 G3板链路测试\GENEX Logfile\fmt\Ubbpd9_awgn_tm8_MS1.csv'
    k1 = r'PCC Average SINR(Normal/csi-MeasSubframeSet1)(dB)'
    k2 = r'PCC MAC Throughput DL(kbit/s)'

    my_csv = csv.CsvDatUtil(file).get_df()

    plt.plot(my_csv[k1], my_csv[k2], 'bo')  # 'ro'表示红色圆点 r g b y m c k （红，绿，蓝，黄，品红，青，黑）

    # plt.axis([0, 6, 0, 20])  # 坐标轴范围，格式[xmin, xmax, ymin, ymax]
    plt.xlabel('SINR(dB)')
    plt.ylabel('MAC Thrp(kbps')
    plt.show()
    pass




