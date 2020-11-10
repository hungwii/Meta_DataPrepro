import pandas as pd
import numpy as np
#TODO:这个生成embedding的代码需要重新改过
def get_ent2vec(ent, embedding_vec, embedding_dic):
    #读取tsv文件，获取ent中所有节点的数字，把这数字保存为列表的形式
    #embedding——vec文件的数据格式就是一行行的向量，按照字典的顺序排列

    all_entities = []
    with open(embedding_dic, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.strip('\n').split('\t')[0]
            all_entities.append(temp)

    # print(len(all_entities))
    # print(all_entities[0])
    locs = []
    for _ in ent:
        locs.append(all_entities.index(_))
    print('找数字结束')

    #在embedding文件中找到对应的向量，一行一行添加下去
    all_vec = np.load(embedding_vec)
    dimension = all_vec[0].shape[0]
    ent2vec = np.zeros(shape=(len(locs), dimension))

    for i, loc in enumerate(locs):
        ent2vec[i] = all_vec[loc]
    #输出文件为npy格式
    np.save('./HW/ent2vec.npy', ent2vec)
    print('--- ent2vec.npy 文件完成---')