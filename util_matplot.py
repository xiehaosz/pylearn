# coding: UTF-8
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import util_csv as csv


def plot_function():
    x_val = np.linspace(-10, 40, 50)
    y1_val = 2*x_val + 1
    y2_val = x_val**2/10

    y3_val = np.arange(5)

    # np类型数据连接，先将数组转成列表拼接处理，再将列表转成数组
    lst_y1_val = list(y1_val)
    y1_val = np.array(lst_y1_val)
    # np类型数据连接，使用np.append连接数组和值，或两个数组，超过3个使用np.concatenate（高效优选）

    # 使用plt.figure定义一个图像窗口：编号为3（或用字符串名称）；大小为(8, 5)
    plt.figure(num=100, figsize=(8, 5),)

    # 加入数据系列并命名（用于图例）
    plt.plot(x_val, y1_val, label='Line_A')
    plt.plot(x_val, y2_val, color='red', linewidth=1.0, linestyle='--', label='Line_B')

    # 添加图例 'best':0,'upper right':1,'upper left':2,'lower left':3,'lower right':4,
    #  'right':5,'center left':6,'center right':7,'lower center':8,'upper center':9,'center':10
    plt.legend(loc='upper right')

    # 坐标轴标题
    plt.xlabel('x_value')
    plt.ylabel('y_value')

    # 坐标轴范围设置
    plt.xlim(min(x_val), max(x_val))
    # y_all = np.append(y1_val, y2_val)
    y_all = np.concatenate((y1_val, y2_val, y3_val))
    plt.ylim(min(y_all), max(y_all))

    # 坐标轴刻度设置(tick, label)
    plt.xticks(())  # ignore xticks
    plt.xticks(np.arange(5))
    plt.yticks([10, 20, 30, 50], ['Level1', 'Level2', 'Level3', 'Level5'])

    # plt.gca获取坐标轴信息，spines设置边框属性
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # 使用.spines设置边框：x轴；使用.set_position设置边框位置：y=0的位置；（位置所有属性：outward，axes，data）
    # 使用.spines设置边框：y轴；使用.set_position设置边框位置：x=0的位置；（位置所有属性：outward，axes，data）
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data',0))

    # 使用.xaxis.set_ticks_position设置x坐标刻度数字或名称的位置：bottom.（所有位置：top，bottom，both，default，none）
    # 使用.yaxis.set_ticks_position设置y坐标刻度数字或名称的位置：left.（所有位置：left，right，both，default，none）
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

    # 标注
    plt.scatter(10, 10, s=50, color='b')  # 标志点
    plt.plot([10, 10], [0, 10], 'k--', linewidth=2.5)  # 垂线

    # annotate参数xycoords='data' 是说基于数据的值来选位置
    # xytext=(+30, -30) 和 textcoords='offset points' 对于标注位置的描述 和 xy 偏差值, arrowprops是箭头类型设置
    plt.annotate(r'This is a mark', xy=(10, 10), xycoords='data', xytext=(+30, -30),
                 textcoords='offset points', fontsize=16,
                 arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
    plt.text(-3.7, 50, r'$This\ is\ the\ some\ text. \mu\ \sigma_i\ \alpha_t$',
             fontdict={'size': 16, 'color': 'r'})
    plt.show()


def dual_y_ax():
    x = np.arange(0, 10, 0.1)
    y1 = 0.05 * x ** 2
    y2 = -1 * y1

    # 获取figure默认的坐标系 ax1
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # 生成一个翻转的次坐标轴ax2
    # 在分别在主次坐标轴上绘图
    ax1.plot(x, y1, 'g-')  # green, solid line
    ax1.set_xlabel('X data')
    ax1.set_ylabel('Y1 data', color='g')
    ax2.plot(x, y2, 'b-')  # blue
    ax2.set_ylabel('Y2 data', color='b')

    plt.show()


def plt_scatter():
    # 随机散点图样例
    n = 1024    # data size
    X = np.random.normal(0, 1, n)  # 每一个点的X值
    Y = np.random.normal(0, 1, n)  # 每一个点的Y值
    T = np.arctan2(Y, X)  # for color value

    plt.scatter(X, Y, s=75, c=T, alpha=.5)

    plt.xlim(-1.5, 1.5)
    plt.xticks(())  # ignore xticks
    plt.ylim(-1.5, 1.5)
    plt.yticks(())  # ignore yticks

    plt.show()


def plt_col():
    # 柱形图样例
    n = 12
    X = np.arange(n)
    Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
    Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

    plt.bar(X, +Y1)
    plt.bar(X, -Y2)

    plt.xlim(-.5, n)
    plt.xticks(())
    plt.ylim(-1.25, 1.25)
    plt.yticks(())

    plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
    plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

    for x, y in zip(X, Y1):
        # ha: horizontal alignment
        # va: vertical alignment
        plt.text(x + 0.4, y + 0.05, '%.2f' % y, ha='center', va='bottom')

    for x, y in zip(X, Y2):
        # ha: horizontal alignment
        # va: vertical alignment
        plt.text(x + 0.4, -y - 0.05, '%.2f' % y, ha='center', va='top')

    plt.show()


def height_map():
        # 等高线图
    def f(x,y):
        # the height function
        return (1 - x / 2 + x**5 + y**3) * np.exp(-x**2 -y**2)

    n = 256
    # x, y 分别是在区间 [-3,3] 中均匀分布的256个值
    x = np.linspace(-3, 3, n)
    y = np.linspace(-3, 3, n)
    # meshgrid在二维平面中将每一个x和每一个y分别对应起来，编织成栅格
    X, Y = np.meshgrid(x, y)

    # 把颜色加进去，位置参数分别为：X, Y, f(X,Y)。透明度0.75，并将 f(X,Y) 的值对应到color map的暖色组中寻找对应颜色
    plt.contourf(X, Y, f(X, Y), 8, alpha=.75, cmap=plt.cm.hot)
    # 等高线绘制，位置参数为：X, Y, f(X,Y)。颜色选黑色，线条宽度选0.5。
    # 8代表等高线的密集程度，这里被分为10个部分。如果是0，则图像被一分为二。
    C = plt.contour(X, Y, f(X, Y), 8, colors='black', linewidth=.5)
    # 加入Label，inline控制是否将Label画在线里面，字体大小为10。并将坐标轴隐藏
    plt.clabel(C, inline=True, fontsize=10)
    plt.xticks(())
    plt.yticks(())

    plt.show()


def multi_plt():
    # 多合一显示
    plt.figure()
    # plt.subplot(2,2,1)表示将整个图像窗口分为2行2列, 当前位置为1
    plt.subplot(2, 2, 1)
    # 在第1个位置创建一个小图
    plt.plot([0, 1], [0, 1])
    # 表示将整个图像窗口分为2行2列, 当前位置为2
    plt.subplot(2, 2, 2)
    # 在第2个位置创建一个小图
    plt.plot([0, 1], [0, 2])
    plt.subplot(2, 2, 3)
    plt.plot([0, 1], [0, 5])
    plt.subplot(2, 2, 4)
    plt.plot([0, 1], [0, 7])
    plt.show()


# ==================================================================
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

if __name__ == "__main__":
    # ==================================================================
    # file = r'D:\Python\PycharmProjects\data_samples\csv_sample.csv'
    # x_va1 = r'PCC Average SINR(Normal/csi-MeasSubframeSet1)(dB)'
    # y_va1 = r'PCC MAC Throughput DL(kbit/s)'
    # my_csv = csv.CsvDatUtil(file).get_df()
    # plt.plot(my_csv[x_va1], my_csv[y_va1], 'o')  # 可用'bo'表示蓝色圆点 r g b y m c k （红，绿，蓝，黄，品红，青，黑）
    # plt.axis([0, 6, 0, 20])  # 坐标轴范围，格式[xmin, xmax, ymin, ymax]
    # plt.xlabel('SINR(dB)')
    # plt.ylabel('MAC Thrp(kbps')
    # plt.show()

    # ==================================================================
    plot_function()
    dual_y_ax()
    plt_scatter()
    plt_col()
    height_map()

    multi_plt()

    pass




