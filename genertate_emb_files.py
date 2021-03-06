import copy
from check import check_triples


def get_ents(rel_list):
    ents = []
    for triple in rel_list:
        ents.append(triple[0])
        ents.append(triple[2])
    ents_set = list(set(ents))
    ents_num = int(len(rel_list) * 0.9)
    return  ents_set, ents_num

def map_task(task, entities_dic, relation_dic):
    print('----下面开始一个数据集的映射')
    train = []
    count = 0
    for rel in task.keys():
        rel_idx = relation_dic.index(rel)
        for _ in task[rel]:
            temp = [entities_dic.index(_[0]), rel_idx, entities_dic.index(_[2])]
            train.append(temp)
        count += 1
        print('--------第{}个关系{}完成'.format(count, rel))
    return train

#TODO：修改这里的函数，最后只输出train和valid
def generate_three_tasks(all_tasks, all_keys, entities_dic, relation_dic):
    '''
    这是一个把我现有的数据生成方便进行embedding数据的函数,按照9:1进行划分
    :all_tasks: 是一个字典:{"key":[[h,r,t], [h,r,t]], "key": [[h,r,t],[h,r,t]]}
    :all_keys: 是一个列表，包含了all_tasks中所有的key。这个传进来主要是为了避免再算一次，减少时间
    :entities_dic:一个列表，序号就是对应字典中的标号
    :relation_dic:一个列表，序号就是对应字典中的标号
    '''
    #TODO:这里做错了，我是把所有数据都拿来分成train和dev了。应该先去除掉test
    #TODO:分割之前先检查一个数据量
    # #首先检查数据的格式
    print('输入中key的长度为', len(all_keys), len(list(all_tasks.keys())))
    check_triples(all_tasks, 'train_dev的三元组个数和边的个数')
    input('暂停一下检查数据的格式')
    train_forEmb, dev_forEmb, rel_ents_set, rel_ents_num = {}, copy.deepcopy(all_tasks), {}, {}
    for i in all_keys:
        rel_ents_set[i], rel_ents_num[i] = get_ents(all_tasks[i])
        train_forEmb[i] = []
    
    # for uu in all_keys:
    #     print(rel_ents_num[uu], len(all_tasks[uu]))
    
    # input('hello检查')
    #这个就是分割数据代码的主体
    times = 0 #记录循环的次数
    train_sum = 0
    dev_sum = 0
    for rel in all_keys:
        count, idx = 0, 0
        cur_ents_set = rel_ents_set[rel]  #获取到当前关系下的顶点集合

        #下面开始分割数据
        while count < rel_ents_num[rel] and idx < len(all_tasks[rel]): 
            head, tail= all_tasks[rel][idx][0], all_tasks[rel][idx][2]

            if  head in cur_ents_set or tail in cur_ents_set:#TODO：最后结果不行的话逻辑再改成and

                #一个添加，一个按值删除
                train_forEmb[rel].append(all_tasks[rel][idx])
                dev_forEmb[rel].remove(all_tasks[rel][idx]) #删除后，最后剩下的就是我要的dev_forEmb
                # print('删除后检查，{} {}'.format(len(train_forEmb[rel]), len(dev_forEmb[rel])))
                count += 1

                #删除查找表中的值
                if head in cur_ents_set:
                    cur_ents_set.remove(head)
                if tail in cur_ents_set:
                    cur_ents_set.remove(tail)
            
            #不管有没有找到，idx都加一，循环继续。
            idx += 1
        
        #while循环结束之后，要补充train中不够的数量
        while count < rel_ents_num[rel]:
            train_forEmb[rel].append(dev_forEmb[rel][0])
            dev_forEmb[rel].remove(dev_forEmb[rel][0])
            count += 1
        
        print('整个关系删除后检查，train{}, dev{}, 删除前总和{} 删除后总和 {}'.format(len(train_forEmb[rel]), len(dev_forEmb[rel]), len(all_tasks[rel]), len(train_forEmb[rel])+len(dev_forEmb[rel])))
        train_sum += len(train_forEmb[rel])
        dev_sum += len(dev_forEmb[rel])
            
        times += 1 #计数器+1
        print('---第{}次循环--{}---'.format(times, rel))
    
    
    # #检查分割的数据的格式：1、首先保证数量是正确的
    # print('train中关系的数量(91)',len(train_forEmb.keys()))
    # print('dev中关系的数量(91)', len(dev_forEmb.keys()))
    # input('暂停一下')
    
    # for t, _ in enumerate(all_keys):
    #     print('--{}--{}--'.format(len(train_forEmb[_]), len(dev_forEmb[_])))
    #     if t % 10 == 0 and t != 0:
    #         input('暂停检查一下数量')
    
    print('进行映射前的数据检查')
    print('训练集中三元组的数量：', train_sum)
    print('测试集中三元组的数量', dev_sum)
    print('训练加测试中三元组数量的总和：', train_sum + dev_sum)
    print('映射前检查')
    print('开始字典映射')
    #把字典映射
    train = map_task(train_forEmb, entities_dic, relation_dic)
    dev = map_task(dev_forEmb, entities_dic, relation_dic)
    print('映射完成')

    #这里输出的train，dev和test的格式：[[1,2,3], [2,3,4]....]
    return train, dev

#这个函数是用来把train/dev/test数据写到ForEmb文件夹中的    
def wirte_tasks(output_train_Emb, train):
    print('--开始写文件')
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