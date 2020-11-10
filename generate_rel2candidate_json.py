import pandas as pd #利用pandas写好的函数载入处理数据
import numpy as np
from pandas import DataFrame
import json

def get_rel2candidate_json(rels, triples, output):
    rel2candidate = {}
    for _ in rels:
        rel2candidate[_] = [] #到这里就创建了所有关系的空辞典


    for triple in triples:
        if triple[1] in rels:
            rel2candidate[triple[1]].append(triple[0])
            rel2candidate[triple[1]].append(triple[2])

    #对每个关系下的节点进行去重
    for k in rel2candidate.keys():
        temp = list(set(rel2candidate[k]))
        rel2candidate[k] = temp
    
    #wirte into the file in json format
    with open(output, 'w') as b:
        json.dump(rel2candidate, b)

    print("—— rel2candidates.json 文件加载完成——")
    


