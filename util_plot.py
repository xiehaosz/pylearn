import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FuncFormatter, MultipleLocator, FormatStrFormatter  # 坐标轴设置

"""
Dateframe和Array的相互转换
    np_array = df.values
    df = pd.DataFrame(np_array, index=[], columns=[])

matplotlib.pyplot
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html

显示中文/特殊符号和转义字符
    1. u'\u2103'是摄氏度符号，前面的u代表unicode，引号中是该符号对应的unicode编码
    2. 显示中文: plt.xlabel((u'中文标题', fontproperties='SimHei')
    3. 显示公式: plt.xlabel('Rice('+r'$\mu\mathrm{mol}$'+' '+'$ \mathrm{m}^{-2} \mathrm{s}^{-1}$'+')')
    4. 文本中的空格需要转义符 'hello\ world'

字体的设置：
    https://blog.csdn.net/helunqu2017/article/details/78659490
    fontsize=12,  ['xx-small', 'x-small', 'small', 'medium', 'large','x-large', 'xx-large']
    fontweight='bold',  ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
    fontstyle设置字体类型，可选参数[ 'normal' | 'italic' | 'oblique' ]，italic斜体，oblique倾斜
    verticalalignment设置水平对齐方式 ，可选参数 ： 'center' , 'top' , 'bottom' ,'baseline' 
    horizontalalignment设置垂直对齐方式，可选参数：left,right,center
    rotation(旋转角度)可选参数为:vertical,horizontal 也可以为数字
    alpha透明度，参数值0至1之间
    backgroundcolor标题背景颜色
    bbox给标题增加外框 ，常用参数如下：
        boxstyle方框外形
        facecolor(简写fc)背景颜色
        edgecolor(简写ec)边框线条颜色
        edgewidth边框线条大小

线条和点的样式设置: 
    linestyle='--' 或 linefmt='--'
    参考1: https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    参考2: https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
    
    color='red'
    参考1: https://matplotlib.org/stable/tutorials/colors/colors.html
    参考2: 颜色代码表 https://www.jianshu.com/p/f674e71b429c
    参考3: 颜色色系 https://zhuanlan.zhihu.com/p/65220518
    
    marker='|' 或 markerfmt='|'
    参考1: https://matplotlib.org/stable/api/markers_api.html
    
    综合参考: https://www.cnblogs.com/darkknightzh/p/6117528.html
"""


def foo_plt_save_graphs(title_, path_=None):
    if path_ is not None:
        plt.savefig(os.path.join(path_, title_+'.png'), dpi=120)
    else:
        if not os.path.exists('output_graphs'):
            os.mkdirs('output_graphs')
            plt.savefig(os.path.join('output_graphs', title_+'.png'), dpi=120)


def foo_plt_basic_setting(title_=None, xlabel_=None, ylabel_=None,
                xlim_=None, ylim_=None,
                is_legend=True, is_grid=True):
    if title_ is not None:
        plt.title(title_)
        # plt.title(_title, loc='left', verticalalignment='bottom', fontsize=12, fontweight='bold', color='blue',
        #           rotation=3, bbox=dict(facecolor='g', edgecolor='blue', alpha=0.5))
    if xlabel_ is not None:
        plt.xlabel(xlabel_)
        # plt.xlabel(_xlabel, fontsize=8, fontproperties='SimHei')
    if ylabel_ is not None:
        plt.ylabel(ylabel_)
    if xlim_ is not None:
        plt.xlim(xlim_)  # 元组(min, max)
    if ylim_ is not None:
        plt.ylim(ylim_)  # 元组(min, max)
    if is_legend is not None:
        plt.legend(prop={'size': 8})
        # plt.legend(loc=0, prop={'size': 10, 'weight': 'normal', 'family': 'Times New Roman'})
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
    if is_grid:
        # plt.grid()
        plt.grid(which='major', axis='both', linestyle='-.')  # ['major','minor','both'] ['x','y','both']
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.html


def foo_plt_advanced_setting():
    # 添加文本注释, xy是注释点坐标, xytext是文本坐标, 可以箭头(文本指向注释点)
    plt.annotate('Annotate', xy=(8, 5), xytext=(5, 40), arrowprops=dict(facecolor='red', shrink=0))

    # 设置画布背景色
    plt.gcf().set_facecolor('#CCFFFF')

    # # 设置轴值范围[xmin,xmax,ymin,ymax], 等效于同时设置plt.xlim + ylim
    # plt.axis([0, 10, 0, 100])
    #
    # # 设置轴标签, 第一个数组参数是值，第二个数组参数文本显示(可选)
    # plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # plt.yticks([0, 20, 60, 80, 100],
    #            [r'really\ bad', r'$bad$', r'$normal$', r'$good$', r'$readly\ good$'])


def foo_axes_advanced_setting():
    """ 图表区的详细设置, 图表(axes)的设置会覆盖绘图板(plt)的设置 """
    ax = plt.gca()  # Get Current Axes'

    # 设置图表区域边框颜色(无色为'none')
    ax.spines['top'].set_color('red')
    ax.spines['bottom'].set_color('blue')
    ax.spines['left'].set_color('green')
    ax.spines['right'].set_color('yellow')

    # 设置图表区域边框位置
    ax.spines['bottom'].set_position(('data', 10))
    ax.spines['left'].set_position(('data', 2))

    # # 获取坐标轴标签的信息: 标签/对应值/格式
    # ax.xaxis.get_major_ticks()
    # ax.xaxis.get_minor_ticks()
    # ax.xaxis.get_major_locator()
    # ax.xaxis.get_minor_locator()
    # ax.xaxis.get_major_formatter()
    # ax.xaxis.get_minor_formatter()

    # 设置坐标轴标签位置
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('right')

    # 设置坐标轴标签和样式
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e'])
    ax.set_xlim(0, 11)
    ax.set_xlabel('X axis', {'family': 'Times New Roman', 'weight': 'normal', 'size': 20, })

    # 设置坐标轴线样式
    ax.axhline(0, color="k", clip_on=False)

    # 设置图例
    ax.legend()

    # 设置主/次轴标签(设置后才有主/次网格线)
    ax.xaxis.set_major_locator(MultipleLocator(2))  # plt.MultipleLocator相同
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.grid(which='minor', axis='x', color='orangered', linestyle=':', linewidth=0.75)

    ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
    ax.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

    # 设置刻度标签的文本格式
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    # 使用用户函数来定义刻度格式
    # 首先要定义一个格式函数, 需要两个参数:标签内容值和位置, 返回对应位置的格式化后的字符串
    def _foo_tick(x, pos):
        # x:  tick value - ie. what you currently see in yticks
        # pos: a position - ie. the index of the tick (from 0 to 9 in this example)
        if not x % 1.0:
            return ''
        return '%.2f' % x
    # FuncFormatter将格式函数转换为formatter对象
    ax.xaxis.set_minor_formatter(FuncFormatter(_foo_tick))

    # 设置坐标轴标签格式
    ax.tick_params('x', which='minor', length=5, width=1.0, labelsize=5, labelcolor='0.25')

    # # 删除坐标轴的标签刻度
    # ax.yaxis.set_major_locator(plt.NullLocator())
    # ax.xaxis.set_major_formatter(plt.NullFormatter())


def foo_plt_plot(label_, *args):
    """
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot
    :param label_: 数据标签
    :param args: x值, y值
    :return: none
    """
    # if len(args) == 1:
    #     plt.plot(*zip(*enumerate(args[0])), label='%s [Mean:%.2f]' % (label_, np.mean(args[0])))
    # elif len(args) > 1:
    #     plt.plot(args[0], args[1], label='%s [Mean:%.2f]' % (label_, np.mean(args[1])))

    # 更多参数样例:
    plt.plot(args[0], args[1], marker='o', markersize=2, linewidth=2)
    # plot可以用数组绘制并返回线条组: linesList=plt.plot(x1, y1, x2, y2, x3, y3..)
    # 用plt.setp方法可以同时设置多个线条的属性, plt.setp(linesList, color='r')


def foo_plt_scatter(label_, arr_x, arr_y):
    """
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html#matplotlib.pyplot.scatter
    :param label_: 数据标签
    :param arr_x: x值
    :param arr_y: y值
    :return: None
    """
    plt.scatter(arr_x, arr_y, label='%s [Mean:%.2f]' % (label_, np.mean(arr_y)))
    # 更多参数样例:
    # plt.scatter(arr_x, arr_y, s=10, color='blue', marker='*', alpha=0.5, linewidths=2, edgecolors='red')

    # # 扩展: 定义一个长度和数据一致的颜色数组为每一个点染色
    # _colours = ['Crimson', 'Blue', 'Fuchsia', 'Tomato', 'Indigo', 'Turquoise', 'Brown', 'Wheat']
    # plt.scatter(_arr_x, _arr_x, color=_colours)


def foo_plt_stem(label_, arr_x, arr_y):
    """
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.stem.html
    :param label_: 数据标签
    :param arr_x: x值
    :param arr_y: y值
    :return: None
    """
    _markerline, _stemlines, _baseline = plt.stem(arr_x, arr_y, label=label_)
    # 更多参数样例:
    # plt.stem(arr_x, arr_y, label=_label, linefmt='--', markerfmt='d', basefmt='C13-', bottom=10)

    # # 单独或批量设置棉棒末端, 棉棒连线和基线的属性
    # plt.setp(_markerline, color='k')  # 将棉棒末端设置为黑色


def foo_plt_bar(label_, arr_bars, arr_tag=None, bottom_=0, width_=0.75, overlap=False):
    """
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
    pyplot的柱状图是绘制相对基准值(bottom, 默认为0)的偏离度(height)
    本函数为绝对柱形图,大于基准值柱形向上,小于基准值柱形向下
    :param label_: 数据标签
    :param arr_bars: 嵌套列表,第一层为数据组,第二层为数据值系列
    :param arr_tag: x轴标签
    :param bottom_: 基准值
    :param width_: 柱形总宽度(多组数据均分)
    :return: None
    """
    def tick_shift(x, pos, bottom):
        return '%.0f' % (x + bottom)

    _num = len(arr_bars)
    if overlap:
        _width, _shift = width_, width_/_num
    else:
        _width, _shift = width_/_num, width_/_num

    for _i in range(_num):
        _bars = np.asarray(arr_bars[_i]) - bottom_
        arr_x = np.asarray(range(len(_bars))) + _i * _shift
        plt.bar(arr_x, _bars, label=label_, width=_width)
        # 更多参数样例:
        # plt.bar(arr_x, arr_y, alpha=0.9, width=0.35, facecolor='lightskyblue', edgecolor='white', lw=1)

    formatter = FuncFormatter(lambda x, pos: tick_shift(x, pos, bottom_))
    ax = plt.gca()
    ax.yaxis.set_major_formatter(formatter)

    if arr_tag is not None:
        plt.xticks(range(len(arr_tag)), arr_tag)


def gen_sample_data_array(n=100):
    from random import randint
    _arr_x = np.linspace(2, 10, n)
    _arr_y = _arr_x ** 4 * randint(1, 5) * randint(-1, 1) + \
             _arr_x ** 3 * randint(1, 8) * randint(-1, 1) + \
             _arr_x ** 2 * randint(1, 10) * randint(-1, 1) + \
             _arr_x * randint(1, 15) * randint(-1, 1)
    _arr_d = np.random.randint(-500, 500, n)
    return _arr_x, _arr_y + _arr_d


if __name__ == "__main__":
    """ matplotlib.pyplot绘图 """
    # 新建绘图画板, 默认会生成一个axes(画布/绘图区)，一个画板上可以有多个画布
    # plt.figure()

    # for i in range(3):
    #     x_values, y_values = gen_sample_data_array()
    #     # 添加散点平滑线
    #     foo_plt_plot('sample-%d' % i, x_values, y_values)
    #
    # x_values, y_values = gen_sample_data_array()
    # # 添加散点图
    # foo_plt_scatter('sample-scatter', x_values, y_values)
    #
    # x_values, y_values = gen_sample_data_array(10)
    # # 添加棉棒图
    # foo_plt_stem('sample-stem', x_values, y_values)
    #
    # arr_bars = []
    # for i in range(2):
    #     x_values, y_values = gen_sample_data_array(10)
    #     arr_bars.append(y_values)
    # # # 添加柱形图图
    # foo_plt_bar('sample-bar', arr_bars, bottom_=-2, arr_tag=['a','b','c','c','e','f','g'], width_=0.7)

    # # 设置图表基础格式,如标题/轴标题/网格/轴值域等
    # foo_plt_basic_setting(title_='This_is_a_sample', xlabel_='x value(dB)', ylabel_='y value(Mbit/s)',
    #                       xlim_=None, ylim_=None)
    #
    # foo_plt_advanced_setting()
    # foo_axes_advanced_setting()

    """ seanborn绘图 """
    arr = []
    for i in range(3):
        x_values, y_values = gen_sample_data_array(30)
        arr.append(np.transpose(np.vstack((x_values, y_values, np.ones_like(x_values) * i, np.ones_like(x_values) * i,
                                           np.random.randint(1, 5, size=30)))))

    # 使用dataframe格式作为seaborn数据源更便捷
    df = pd.DataFrame(np.concatenate(arr), columns=['x', 'y', 'hue', 'style', 'size'])

    ''' seanborn散点图scatterplot/线图lineplot/关系图relplot: 一般散点图 '''
    # # relplot是scatterplot和lineplot的集合, 通过参数指定类型kind='line'
    # # 常用参数:
    # # hue, style, size分组
    # # 颜色palette=['b', 'r']
    # # 分别画子图col='time',row='sex'
    # ax = sns.scatterplot(x='x', y='y', hue='hue', data=df)
    # # ax = sns.lineplot(x='x', y='y', markers=True, dashes=False, data=df)

    ''' seanborn直方图distplot: 变量的分布规律 '''
    # # 常用参数:
    # # kde=False, 不显示密度曲线
    # # ax=axes[0], 指定画布
    # # rug=True, 显示边际毛毯
    # # hist_kws, kde_kws, rug_kws, 详细的格式设置
    #
    # # 创建1行2列画布方便对比
    # fig, axes = plt.subplots(1, 2)
    #
    # hue = df['hue'].dropna()  # distplot不能处理缺失数据, 需要去除缺失值(可选)
    # sns.distplot(hue, rug=True, ax=axes[0])
    # sns.distplot(df['size'], kde=False, ax=axes[1], hist_kws={'color': 'green', 'label': 'hist'})

    ''' seanborn条形图barplot: 数值变量的集中趋势和置信区间 '''
    # # 常用参数:
    # # estimator=median/max, 统计方法
    # # order/hue_order, 标题数组, 可以控制条形图的顺序
    # # orient=v/h 绘图方向
    # # errcolor, errwidth 误差线的格式
    #
    # sns.barplot(x='style', y='y', hue='size', data=df)
    # # ax = plt.gca()
    # # ax.axhline(0, color="k", clip_on=False)
    #
    # # countplot即简化版的barplot, 只有计数的柱形
    # # sns.countplot(x='style', hue='size', data=df)
    # # sns.countplot(y='style', hue='size', data=df)

    ''' seanborn分布密度散点图 stripplot/swarmplot: 观察数据分布 '''
    # # stripplot是随机抖动展开, swarmplot则是不重复展开,适用于小数据量
    # # 常用参数:
    # # jitter=1, 调整抖动范围
    # fig, axes = plt.subplots(1, 2)
    # sns.stripplot(x='size', y='y', hue='style', data=df, ax=axes[0])
    # sns.swarmplot(x='size', y='y', hue='style', data=df, ax=axes[1])

    ''' seanborn箱线图 stripplot: 数据分散情况统计[异常值/极大极小值/中位数/上下四分位数] '''
    # # 可以叠加分布散点图:
    # sns.boxplot(x='style', y='size', data=df, linewidth=1)

    ''' seanborn小提琴图 violinplot: 箱线图和密度散点的结合 '''
    # # 常用参数:
    # # 当hue分组为2时，可以通过设置split参数左右显示
    # # inner='stick'/None, 内部图形
    # # 可以叠加分布散点图
    # sns.violinplot(x='style', y='size', data=df, linewidth=1, inner='stick')

    ''' seanborn 线性回归图replot/ 回归模型图lmplot: 即散点图+趋势线, 分析变量关联关系 '''
    # # 常用参数:
    # # 颜色分组hue, 样式分组style, 大小分组size
    # # 用col代替hue, 会分开作图
    # # color, marker可以是数组对应多个分组
    # # ci=None, 置信区间(拟合线的阴影)
    # # order 多项式拟合阶数
    # # lowess=True 局部加权回归散点平滑法(locally weighted scatterplot smoothing，LOWESS)，是一种非参数回归拟合的方式，
    # # 其主要思想是选取一定比例的局部数据，拟合多项式回归曲线，以便观察到数据的局部规律和趋势。适用非线性关系。

    # sns.regplot(x='x', y='y', data=df, hue='hue', style='style', size='size')
    sns.lmplot(x='x', y='y', data=df, hue='hue', lowess=True)
    # # sns.lmplot(x='x', y='y', data=df)

    ''' seanborn复合图表联合分布图jointplot, 中央图+维度分布'''
    # # 常用参数:
    # # kind : { “scatter” | “reg” | “resid” | “kde” | “hex” }。默认散点图；
    # # stat_func：用于计算统计量关系的函数；
    # # ratio：中心图与侧边图的比例，越大、中心图占比越大；
    # # dropna：去除缺失值；
    # # height：图的尺度大小（正方形）；
    # # space：中心图与侧边图的间隔大小；
    # # xlim，ylim：x，y的范围
    # sns.jointplot(x='x', y='y', kind='kde', data=df)

    ''' seanborn热力图heatmap '''
    # ax = sns.heatmap(data=df[['x', 'y']], annot=True, annot_kws={'size': 9, 'weight': 'bold', 'color': 'w'}, fmt='.2f')

    # seanborn定义主题风格 [ticks, dark, white, darkgrid, whitegrid]
    sns.set(style='darkgrid')
    sns.set_style('darkgrid')
    # axes_styles

    # 字体大小sns.set_context [paper, notebook, talk, poster]
    sns.plotting_context("notebook")

    plt.show()
