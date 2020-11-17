def check_ents(task, tiltle):
    '''
    这个函数是用来检查一个任务中有多少种顶点的。注意是多少种，用到了set
    '''
    ents = []
    for rel in task:
        for triple in task[rel]:
            ents.append(triple[0])
            ents.append(triple[2])
    
    print(tiltle, len(set(ents)))
    input('--暂停一下--')

def check_triples(task, title):
    '''
    这个函数用来检查一个任务种有多少个三元组的
    '''
    triple_nums = 0
    rel_nums = 0
    for rel in task:
        triple_nums += len(task[rel])
        rel_nums += 1
    print(title, 'rel的数量：{} triple的数量{}'.format(rel_nums, triple_nums))
