def check_ents(task, tiltle):
    ents = []
    for rel in task:
        for triple in task[rel]:
            ents.append(triple[0])
            ents.append(triple[2])
    
    print(tiltle, len(set(ents)))
    input('--暂停一下--')
