import numpy as np
import matplotlib.pyplot as plt
import sklearn.decomposition as dp
from sklearn.datasets import load_iris


def iris_case():
    # 加载鸢尾花数据集
    x, y = load_iris(return_X_y=True)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)

    # 创建 PCA 对象，设置主成分数为 2
    pca = dp.PCA(n_components=2)
    # 对数据进行 PCA 降维
    reduced_data = pca.fit_transform(x)

    # ========== 打印分析结果 ==========
    print("=" * 50)
    print("PCA 降维结果分析")
    print("=" * 50)

    # 1. 各主成分的方差解释率
    print(f"\n📊 各主成分方差解释率 (Explained Variance Ratio):")
    for i, ratio in enumerate(pca.explained_variance_ratio_):
        print(f"   主成分 {i+1}: {ratio:.4f} ({ratio*100:.2f}%)")
    print(f"   累计方差解释率: {pca.explained_variance_ratio_.sum():.4f} ({pca.explained_variance_ratio_.sum()*100:.2f}%)")

    # 2. 各主成分的特征向量（载荷）
    print(f"\n📐 各主成分的特征向量 (Components / Loadings):")
    for i, comp in enumerate(pca.components_):
        print(f"   主成分 {i+1}: {np.round(comp, 4)}")

    # 3. 降维后的数据（前10行）
    print(f"\n📝 降维后数据 (前10行):")
    print(f"   {'序号':>4}  {'PC1':>12}  {'PC2':>12}  {'标签':>6}")
    for i in range(min(10, len(reduced_data))):
        print(f"   {i+1:>4}  {reduced_data[i][0]:>12.4f}  {reduced_data[i][1]:>12.4f}  {y[i]:>6}")

    # 4. 原始数据形状 vs 降维后形状
    print(f"\n📐 数据形状:")
    print(f"   原始数据: {x.shape}")
    print(f"   降维后:   {reduced_data.shape}")

    # ========== 可视化 ==========
    red_x, red_y = [], []
    blue_x, blue_y = [], []
    green_x, green_y = [], []

    # 根据标签将数据点分为三类
    for i in range(len(reduced_data)):
        if y[i] == 0:
            red_x.append(reduced_data[i][0])
            red_y.append(reduced_data[i][1])
        elif y[i] == 1:
            blue_x.append(reduced_data[i][0])
            blue_y.append(reduced_data[i][1])
        else:
            green_x.append(reduced_data[i][0])
            green_y.append(reduced_data[i][1])

    # 绘制散点图
    plt.scatter(red_x, red_y, color='red', label='Setosa')
    plt.scatter(blue_x, blue_y, color='blue', label='Versicolor')
    plt.scatter(green_x, green_y, color='green', label='Virginica')

    # 添加图例和标题
    plt.legend()
    plt.title('PCA of Iris Dataset')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')

    # 显示图形
    plt.show()


if __name__ == '__main__':
    iris_case()