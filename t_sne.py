import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import json


#从数据文件中载入数据
data_emb = np.load('./HW/embedding/transR-3000.npy')
with open('./HW/ent2ids', 'r', encoding='utf-8') as f:
    data_dict = json.load(f)

#根据顶点的属性赋予label

#首先对字典进行排序
data_dict_tuple = []
for i in data_dict.items():
    data_dict_tuple.append(i)

#根据序号进行排序
data_dict_tuple_sorted = sorted(data_dict_tuple, key= lambda x : x[1])
# print(len(data_dict.keys()))
#根据名字创建标签
label = []
count_0,count_1, count_2,count_3 = 0,0,0,0
for j in data_dict_tuple_sorted:
    if 'Compound' in j[0]:
        label.append(0)
        count_0 += 1
    elif 'Disease' in j[0]:
        label.append(1)
        count_1 += 1

    elif 'Gene' in j[0]:
        label.append(2)
        count_2 += 1

    elif 'Anatomy' in j[0]:
        label.append(3)
        count_3 += 1
print('最后label 的统计结果：Compound {}  DIsease {} Gene {} Anatomy {} sum {}'.format(count_0, count_1, count_2, count_3, (count_0 + count_1 + count_2 + count_3)))


#进行画点




############
#对数据进行预处理
def plot_embedding(data, label, title):
    """
    :param data:数据集
    :param label:样本标签
    :param title:图像标题
    :return:图像
    """
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)		# 对数据进行归一化处理
    fig = plt.figure()		# 创建图形实例
    ax = plt.subplot(111)		# 创建子图
    # 遍历所有样本
    for i in range(data.shape[0]):
        # 在图中为每个数据点画出标签
        plt.text(data[i, 0], data[i, 1], str(label[i]), color=plt.cm.Set1(label[i] / 1),
                 fontdict={'weight': 'bold', 'size': 7})
    plt.xticks()		# 指定坐标的刻度
    plt.yticks()
    plt.title(title, fontsize=14)
    plt.savefig('./figure_prc.pdf', dpi=1200, format='pdf')

    # 返回值
    return fig
#准备数据
# data = data_drug + data_protein
# label = label_drug + label_pro

print('Starting compute t-SNE Embedding...')
#设置好参数
ts = TSNE(n_components=2, init='pca', random_state=0)
# t-SNE降维
reslut = ts.fit_transform(data_emb)
print('下面开始画图')
# 调用函数，绘制图像
fig = plot_embedding(reslut, label, 't-SNE Embedding of digits')
# 显示图像

plt.show()