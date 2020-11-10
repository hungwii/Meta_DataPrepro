train_all_ents = [1,2,3, 5]
dev_all_ents = [2,3,4]
test_all_ents = [1,2,3,4]
print("train U dev - test:",len(list(set(train_all_ents) | set(dev_all_ents) - set(test_all_ents))))

count = len(list(set(test_all_ents) - (set(train_all_ents) | set(dev_all_ents))))
print(count, list(set(test_all_ents) - (set(train_all_ents) | set(dev_all_ents))))

     