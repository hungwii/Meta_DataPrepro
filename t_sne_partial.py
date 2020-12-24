
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd #利用pandas写好的函数载入处理数据
import numpy as np
from pandas import DataFrame
import json

#这个文件调用后，可以用来画小关系的tsne

#--------------------------参数设置----------------------------
#the relation I want to extract in the drkg
rel_we_need = ['Compound:Gene', 'Compound:Disease', 'Disease:Gene', 'Gene:Gene', \
    'Compound:Compound', 'Anatomy:Gene', 'Anatomy:Disease']

rel_i_want = ['DGIDB::ANTIBODY::Gene:Compound','DGIDB::BINDER::Gene:Compound', 'DGIDB::MODULATOR::Gene:Compound',\
            'DGIDB::PARTIAL AGONIST::Gene:Compound', 'INTACT::DIRECT INTERACTION::Compound:Gene',\
            'INTACT::PHYSICAL ASSOCIATION::Compound:Gene']

rel_i_want_draw = 'INTACT::PHYSICAL ASSOCIATION::Compound:Gene' #这个就是我想要画图的关系

#the file path of the data
filepath_triple = './drkg_source_data/drkg.tsv' # 包含所有的三元组，非数字，纯名字
filepath_relation = './drkg_source_data/relation_glossary.tsv'  #包含了关系名字对应的节点类别，方便我们根据rel_we_want提取出想要的关系
filepath_ent_dic = './ent2ids.json' # 这个是包含所有顶点的字典
filepath_ent_emb = './HW/ent2vec.npy'
#------------------------------------------------------------

#extract the relation we need 
data = pd.read_csv(filepath_relation, delimiter='\t')
relations = data.values.tolist()

#extrat the triple we need
data2 = pd.read_csv(filepath_triple, delimiter='\t', header=None)
triples = data2.values.tolist()

# 输出我们需要的大类别下的小类别，方便数据检查，all_type_dic是一个字典。key是大类名，value是小类名组成的数组
all_type_dic = {}
for _ in rel_we_need:
    all_type_dic[_] = []

rels = []
for relation in relations:
    if relation[2] in rel_we_need:
        rels.append(relation[0]) #这里我就得到了所有我需要的关系，是细致化的关系，以数组的形式存储rel 
        all_type_dic[relation[2]].append(relation[0])

# for k in all_type_dic.keys():
#     print(k)
#     print(all_type_dic[k])
#     print(len(all_type_dic[k]))
#     print('--------------')

#create a task dictionary to classify all triples we need
tasks = {}
for _ in rels:
    tasks[_] = [] #到这里就创建了所有关系的空辞典

#下面就是往key对应的value里面放元祖
for triple in triples:
    if triple[1] in rels:
        tasks[triple[1]].append(triple)

#提取出我想画的关系的所有三元组
task_i_want_draw = tasks[rel_i_want_draw]
print(len(task_i_want_draw))
print(task_i_want_draw[0])


#把我想要的关系中的药物和gene分开
drug_i_want_draw = []
gene_i_want_draw = []
for i in task_i_want_draw:
    drug_i_want_draw.append(i[2])
    gene_i_want_draw.append(i[0])

#去重
drug_i_want_draw = list(set(drug_i_want_draw))
gene_i_want_draw = list(set(gene_i_want_draw))
#根据名字，在词典中找到序号，并转换成对应的embdding.(注意这里的词典可能已经不是最开始drkg中的embedding了)
drug_index = []
gene_index = []

with open(filepath_ent_dic, 'r', encoding='utf-8') as f:
    ents_dic = json.load(f)

for _drug in drug_i_want_draw:
    drug_index.append(ents_dic[_drug])

for _gene in gene_i_want_draw:
    gene_index.append(ents_dic[_gene])

#检查数据格式
print(len(drug_index), len(gene_index))
print(len(drug_i_want_draw), len(gene_i_want_draw))

#根据序号去找embdding
data = np.load(filepath_ent_emb)

drug_emb = []
gene_emb = []

for u in drug_index:
    drug_emb.append(data[u])
for v in gene_index:
    gene_emb.append(data[v])

print(len(drug_emb), len(gene_emb))

#下面进行拼接
drug_true = [1 for i in range(len(drug_emb))]
gene_true = [0 for j in range(len(gene_emb))]
emb = drug_emb + gene_emb
true = drug_true + gene_true

#下面进行tsne
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
    # ax = plt.subplot(111)		# 创建子图

    #遍历所有样本画图
    for i in range(data.shape[0]):
        # 在图中为每个数据点画出标签
        plt.text(data[i, 0], data[i, 1], str(label[i]), color=plt.cm.Set1(label[i] + 2),fontdict={'weight': 'bold', 'size': 7})
    plt.xticks()		# 指定坐标的刻度
    plt.yticks()
    plt.title(title, fontsize=14)
    plt.savefig('./figure_tsne.pdf', dpi=1200, format='pdf')

    # 返回值
    return fig
print('Starting compute t-SNE Embedding...')
#设置好参数
ts = TSNE(n_components=2, init='pca', random_state=0, perplexity=50)
# t-SNE降维
reslut = ts.fit_transform(emb)
print('下面开始画图')
# 调用函数，绘制图像
fig = plot_embedding(reslut, true, 't-SNE Embedding of digits')
# 显示图像
plt.show()




