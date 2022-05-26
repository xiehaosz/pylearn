from sklearn import datasets
from sklearn import cluster as cl
import matplotlib.pyplot as plt
import numpy as np


def demo_cluster(option):
    # python实现聚类算法: https://blog.csdn.net/xc_zhou/article/details/88316299
    # X, y = datasets.make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0,
    #                                     n_clusters_per_class=1, random_state=4)
    X, y = datasets.make_blobs(n_samples=1000, n_features=2, centers=3)
    # for class_value in range(2):
    #     row_ix = np.where(y == class_value)
    #     plt.scatter(X[row_ix, 0], X[row_ix, 1], s=10)
    # plt.show()

    if option == 1:
        # 亲和力传播聚类
        model = cl.AffinityPropagation(damping=0.9)
        model.fit(X)
        yhat = model.predict(X)
    if option == 2:
        # 聚合聚类涉及合并示例，直到达到所需的群集数量为止
        model = cl.AgglomerativeClustering(n_clusters=2)
        yhat = model.fit_predict(X)
    if option == 3:
        # BIRCH 聚类（ BIRCH 是平衡迭代减少的缩写，聚类使用层次结构)包括构造一个树状结构，从中提取聚类质心
        model = cl.AgglomerativeClustering(n_clusters=2)
        yhat = model.fit_predict(X)
    if option == 4:
        # DBSCAN 聚类（其中 DBSCAN 是基于密度的空间聚类的噪声应用程序）涉及在域中寻找高密度区域，并将其周围的特征空间区域扩展为群集
        # 标签为-1的类是离散点
        model = cl.DBSCAN(eps=3, min_samples=10)
        yhat = model.fit_predict(X)
    if option == 5:
        # K-均值聚类可以是最常见的聚类算法，并涉及向群集分配示例，以尽量减少每个群集内的方差
        model = cl.KMeans(n_clusters=2)
        model.fit(X)
        yhat = model.fit_predict(X)
    if option == 6:
        # Mini-Batch K-均值是 K-均值的修改版本，它使用小批量的样本对群集质心进行更新使大数据集的更新速度更快
        model = cl.MiniBatchKMeans(n_clusters=2)
        model.fit(X)
        yhat = model.fit_predict(X)
    if option == 7:
        # 均值漂移聚类涉及到根据特征空间中的实例密度来寻找和调整质心
        # Mean-shift 算法的核心思想就是不断的寻找新的圆心坐标，直到密度最大的区域
        model = cl.MeanShift(bandwidth=2)
        yhat = model.fit_predict(X)
    if option == 8:
        # OPTICS 聚类（ OPTICS 短于订购点数以标识聚类结构）是上述 DBSCAN 的修改版本。
        model = cl.OPTICS(eps=0.8, min_samples=10)
        yhat = model.fit_predict(X)
    if option == 9:
        # 光谱聚类是一类通用的聚类方法，取自线性线性代数
        model = cl.SpectralClustering(n_clusters=2)
        yhat = model.fit_predict(X)
    if option == 10:
        # 高斯混合模型总结了一个多变量概率密度函数，顾名思义就是混合了高斯概率分布
        from sklearn.mixture import GaussianMixture
        model = GaussianMixture(n_components=3)
        model.fit(X)
        yhat = model.fit_predict(X)

    clusters = np.unique(yhat)
    print(clusters)
    for cluster in clusters:
        row_ix = np.where(yhat == cluster)
        plt.scatter(X[row_ix, 0], X[row_ix, 1], s=12)
    plt.show()


if __name__ == '__main__':
    demo_cluster(7)
