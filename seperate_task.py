import random
import json
from check import check_ents


def get_all_ent(the_task):
    result = []
    for _key in the_task.keys():
        for _triple in the_task[_key]:
            result.append(_triple[0])
            result.append(_triple[2])
    return list(set(result))


def seperate_task(filepath_all_tasks, train_rel_num, dev_rel_num, test_rel_num, rel_i_want):

    with open(filepath_all_tasks, 'r', encoding='utf-8') as f:
        all_tasks = json.load(f)
        all_keys = list(all_tasks.keys())


    #删除我最后要用来预测的关系，放在predict{}里面
    predict = {}
    for _ in all_keys:
        if _ in rel_i_want:
            predict[_] = all_tasks[_]
            del all_tasks[_]
            print(_)

    #更新all_keys
    all_keys = list(all_tasks.keys()) #这里all_keys的长度应该和train，dev的总和相等
    print('len(all_keys):',len(all_keys))

    train_rel = random.sample(all_keys, train_rel_num)
    dev_rel = list(set(all_keys) - set(train_rel))
    print('len(train_rel), len()dev_rel', len(train_rel), len(dev_rel))

    train_tasks = {}
    for t_ in train_rel:
        # train_tasks[t_] = []
        train_tasks[t_] = all_tasks[t_]

    dev_tasks = {}
    for d_ in dev_rel:
        # dev_tasks[d_] = []
        dev_tasks[d_] = all_tasks[d_]

    test_tasks = predict

    #下面检查train、dev的所有顶点有没有包含test的所有顶点
    train_all_ents = get_all_ent(train_tasks)
    dev_all_ents = get_all_ent(dev_tasks)
    test_all_ents = get_all_ent(test_tasks)

    #把在test中但是不在train 和 dev 中的顶点输出出来，方便之后进行处理
    raw_entities = list(set(test_all_ents) - (set(train_all_ents) | set(dev_all_ents)))
    count = len(raw_entities)
    if count != 0:
        with open('./HW/ForMe/entities_inTest_notInTrainAndDev.txt', 'w', encoding='utf-8') as output:
            for row in raw_entities:
                rowtext = '{}'.format(row)
                output.write(rowtext)
                output.write('\n')
    print('--输出entities_inTest_notInTrainAndDev.txt完成--')

    #检查数据的形式
    print('抽取的关系的数量：', len(rel_i_want) )
    print('抽取关系之后，剩下的关系的数量(应该为91)：', len(all_keys))

    print('train_task:', type(train_tasks), len(train_tasks))
    print('dev_task:', type(dev_tasks), len(dev_tasks))
    print('test_task:', type(test_tasks), len(test_tasks))

    input('这里暂停一下')

    with open('./HW/train_tasks.json', 'w', encoding='utf-8') as a:
        json.dump(train_tasks, a)
    print('train_tasks is finish')

    with open('./HW/test_tasks.json', 'w', encoding='utf-8') as b:
        json.dump(test_tasks, b)
    print('test_tasks is finish')

    with open('./HW/dev_tasks.json', 'w', encoding='utf-8') as c:
        json.dump(dev_tasks, c)
    print('dev_tasks is finish')

    print("——train.json, dev.json, test.json 文件加载完成——")

    return train_tasks, dev_tasks, test_tasks

