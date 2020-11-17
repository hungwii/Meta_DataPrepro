import pandas as pd #利用pandas写好的函数载入处理数据
import numpy as np
from pandas import DataFrame
import json
import random

def get_ent2ids(rels, triples, output, output_Embed):
    ent = []
    print('总共有' + str(len(triples)) + '个triple')
    count = 0
    input('停一下啊')

    for triple in triples:
        count += 1
        if count % 10000 == 4261:
            print(count)
        if triple[1] in rels:
            if triple[0] not in ent:
                ent.append(triple[0])
            if triple[2] not in ent:
                ent.append(triple[2])
    print('ent的长度为' + str(len(ent)))
    
    num = [i for i in range(len(ent))]
    print('num的长度为：' + str(len(num)))
    random.shuffle(ent)

    ent2ids_dic = dict(zip(ent, num))

    #wirte into the file in json format
    with open(output, 'w') as c:
        json.dump(ent2ids_dic, c)

    print("——ent2id文件加载完成——")
    return ent
    


