# -*- coding: utf-8 -*-
import pandas as pd #利用pandas写好的函数载入处理数据
import numpy as np
from pandas import DataFrame
import json
from generate_e12rel_e2_json import get_e12rel_e2
from generate_ent2ids import get_ent2ids
from generate_rel2candidate_json import get_rel2candidate_json
from generate_ent2vec import get_ent2vec
from seperate_task import seperate_task
from genertate_emb_files import generate_three_tasks, wirte_tasks, write_rel, write_ents



#--------------------------参数设置----------------------------

#the relation I want to extract in the drkg
rel_we_need = ['Compound:Gene', 'Compound:Disease', 'Disease:Gene', 'Gene:Gene', \
    'Compound:Compound', 'Anatomy:Gene', 'Anatomy:Disease']


#下面是分割数据集的参数
#论文中的设置大概是7:2:1,我自己共有97种关系
train_rel_num = 81
dev_rel_num = 10
test_rel_num = 6 #这里的6个关系对应下面的rel_i_want

rel_i_want = ['DGIDB::ANTIBODY::Gene:Compound','DGIDB::BINDER::Gene:Compound', 'DGIDB::MODULATOR::Gene:Compound',\
            'DGIDB::PARTIAL AGONIST::Gene:Compound', 'INTACT::DIRECT INTERACTION::Compound:Gene',\
            'INTACT::PHYSICAL ASSOCIATION::Compound:Gene']


#the file path of the data
filepath_triple = './drkg_source_data/drkg.tsv' # 包含所有的三元组，非数字，纯名字
filepath_relation = './drkg_source_data/relation_glossary.tsv'  #包含了关系名字对应的节点类别，方便我们根据rel_we_want提取出想要的关系
filepath_ent_dic = './drkg_source_data/entities.tsv' # 这个是包含所有顶点的字典


#the output filepath for MetaR model
output_all_tasks = './HW/tasks.json'
output_ent2ids = './HW/ent2ids'
output_e1rel_e2 = './HW/e1rel_e2.json'
output_rel2candidates = './HW/rel2candidates.json'

#the output filepath for Embed（这里是输出生成embedding的文件）
output_ent2ids_Emb = './HW/ForEmb/entities.txt'
output_relation_Emb = './HW/ForEmb/relations.txt'
output_train_Emb = './HW/ForEmb/train.txt'
output_dev_Emb = './HW/ForEmb/valid.txt'
output_test_Emb = './HW/ForEmb/test.txt'

#the output filepath for Me(这里是输出一些方便我自己看的数据)
output_ent_nums_of_all_rels = './HW/ForMe/ent_nums_of_all_rels'


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

for k in all_type_dic.keys():
    print(k)
    print(all_type_dic[k])
    print(len(all_type_dic[k]))
    print('--------------')

#create a task dictionary to classify all triples we need
tasks = {}
for _ in rels:
    tasks[_] = [] #到这里就创建了所有关系的空辞典

#下面就是往key对应的value里面放元祖
for triple in triples:
    if triple[1] in rels:
        tasks[triple[1]].append(triple)

#打印/输出文件：每一种小任务下的三元组的数量
# for _ in all_type_dic.keys():
#     print(str(_) + ':')
#     for r in all_type_dic[_]:
#         print('---' + r + '=' + str(len(tasks[r])))

print('——开始写入ent_nums_of_all_rels.txt文件——')
#输出我自己需要的文件，方便以后进行数据查看
with open(output_ent_nums_of_all_rels, 'w', encoding='utf-8') as output:
    for _ in all_type_dic.keys():
        for r in all_type_dic[_]:
            rowtext = '{}\t{}'.format(r, len(tasks[r]))
            output.write(rowtext)
            output.write('\n')
print('——ent_nums_of_all_rels.txt 文件加载完成——')

#wirte into the file in json format
with open(output_all_tasks, 'w') as a:
    json.dump(tasks, a)
print("——task.json文件加载完成——")



#-------call the function to genrate the file that MetaR model need---------

train_task, dev_task, test_task = seperate_task(output_all_tasks, train_rel_num, dev_rel_num, test_rel_num, rel_i_want)

get_e12rel_e2(rels, triples, output_e1rel_e2)

get_rel2candidate_json(rels, triples, output_rel2candidates)

ents = get_ent2ids(rels, triples, output_ent2ids, output_ent2ids_Emb)



#现在拿到了所有需要的数据，调用函数进行映射成数字关系
train, dev, test = generate_three_tasks(train_task, dev_task, test_task, ents, rels)

#---------输出embedding需要的5个文件--------------
wirte_tasks(output_train_Emb, train)
wirte_tasks(output_dev_Emb, dev)
wirte_tasks(output_test_Emb, test)
write_rel(output_relation_Emb,rels)
write_ents(output_ent2ids_Emb, ents)

print('所有步骤执行完毕，下面可以发送文件过去进行embedding的计算')




        



    



