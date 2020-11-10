import pandas as pd #利用pandas写好的函数载入处理数据
import numpy as np
from pandas import DataFrame
import json


def get_e12rel_e2(rels, triples, output):
    '''
    这是一个获取 e12rel_e2.json 文件的函数

    :param rels: 所有的关系，是细致化的关系，以数组的形式存储， [rel1, rel2, rel3......]
    :param triples: 所有的三元组集合，以数组的形式存储， [[h, r, t], [h, r, t], [h, r, t]....]
    :output:输出的路径，在main函数中定义
    '''

    e12rel_e2 = {}

    for triple in triples:
        if triple[1] in rels:
            if triple[0] + triple[1] not in e12rel_e2.keys():
                e12rel_e2[triple[0] + triple[1]] = []
                e12rel_e2[triple[0] + triple[1]].append(triple[2])
            else:
                e12rel_e2[triple[0] + triple[1]].append(triple[2])


            if triple[2] + triple[1] not in e12rel_e2.keys():
                e12rel_e2[triple[2] + triple[1]] = []
                e12rel_e2[triple[2] + triple[1]].append(triple[0])
            else:
                e12rel_e2[triple[2] + triple[1]].append(triple[0])

        

    #wirte into the file in json format
    with open(output, 'w') as b:
        json.dump(e12rel_e2, b)

    print("—— e1rel_e2.json 文件加载完成——")
    


