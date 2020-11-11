


def map_task(task, entities_dic, relation_dic):
    train = []
    for rel in task.keys():
        rel_idx = relation_dic.index(rel)
        for _ in task[rel]:
            temp = [entities_dic.index(_[0]), rel_idx, entities_dic.index(_[2])]
            train.append(temp)
    return train


def generate_three_tasks(train_task, dev_task, test_task, entities_dic, relation_dic):
    '''
    这是一个把我现有的数据生成方便进行embedding数据的函数
    :task: 是一个字典:{"key":[[h,r,t], h,r,t]], "key": [[h,r,t],[h,r,t]]}
    :entities_dic:一个列表，序号就是对应字典中的标号
    :relation_dic:一个列表，序号就是对应字典中的标号
    '''
    train = map_task(train_task, entities_dic, relation_dic)
    dev = map_task(dev_task, entities_dic, relation_dic)
    test = map_task(test_task, entities_dic, relation_dic)

    #这里输出的train，dev和test的格式：[[1,2,3], [2,3,4]....]
    return train, dev, test

#这个函数是用来把train/dev/test数据写到ForEmb文件夹中的    
def wirte_tasks(output_train_Emb, train):
    with open(output_train_Emb, 'w', encoding='utf-8') as output:
        for row in train:
            rowtext = '{}\t{}\t{}'.format(row[0], row[1], row[2])
            output.write(rowtext)
            output.write('\n')
    print('——task数据完成 +1 ——')

#这个函数是用来把关系写成一个词典的
def write_rel(output_relation_Emb, rels):
    with open(output_relation_Emb, 'w', encoding='utf-8') as rel_emb:
        for idx, each_rel in enumerate(rels):
            rowtext = '{}\t{}'.format(idx, each_rel)
            rel_emb.write(rowtext)
            rel_emb.write('\n')
    print('——relation字典完成——')
    
    
#我输出的是一个字典，输出的第一列是数字，第二列名称,中间用Tab链接
def write_ents(output_Embed, ent2ids_list):
    with open(output_Embed, 'w', encoding='utf-8') as emb:
        for idx_ents, row in enumerate(ent2ids_list):
            rowtext = '{}\t{}'.format(idx_ents, row)
            emb.write(rowtext)
            emb.write('\n')
    print('——entities字典完成——')