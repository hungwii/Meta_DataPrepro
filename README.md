# Meta_DataPrepro
这个文件夹下的代码主要完成两个工作：
1. 使用原始的drkg_source_data文件夹下的数据，生成MetaR需要的数据，以及embedding需要的文件
2. 对于模型跑出来的test结果进行画图分析

## 数据预处理

只需要调用```main.py```就可以了。参数也是在这个文件里面设置

## 结果分析

需要分别调用```Analysis_auc.py```和```Analysis_pr.py```

T-SNE可视化分析，调用```t_sne_all.py``` 或```t_sne_partial```