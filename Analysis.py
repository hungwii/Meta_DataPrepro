#-*- coding: UTF-8 -*-

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from extract import single_column

'''
这个主函数是从我生蚝好的多个文件中提取出样本画AUC
'''

#-------------------------参数设置---------------------------
file_class = '../MetaR/test_result/TransR3000_30shot_test/' #数据所在的文件夹路径
file_num = 6 #这个数量是我test文件的数量，相当于要预测的任务的数量
filepath_output = './test_result_graph/TransR3000_30shot.pdf'
#-----------------------------------------------------------
def draw_one(filepath,score_col=3, label_col=4):
    #TODO:不知道负数的分数有没有什么影响，可以先做做看,可以用一个sigmoid
    #TODO：计算auc要把所有的1给单独抽出来。不可以像现在这样取top

    result_0_score = single_column(filepath, col_num=score_col)
    result_0_label = single_column(filepath,col_num=label_col)

    all_score_0 = list(map(float, result_0_score))
    all_label_0 = list(map(int, result_0_label))
    long_0 = sum(all_label_0)
    zipped = zip(all_score_0, all_label_0)
    # sort_zipped = sorted(zipped,key=lambda x:(x[1],x[0]))
# 先按 x[1] 进行排序，若 x[1] 相同，再按照 x[0] 排序
    combine_zip = sorted(zipped, key=lambda x : (x[1], x[0]),reverse=True)
    combine = zip(*combine_zip)
    all_score_0_new, all_label_0_new = [list(x) for x in combine]
    
    score_0 = all_score_0_new[:3*long_0]
    label_0 = all_label_0_new[:3*long_0]
    
    print(score_0[:10])
    print(label_0[:10])
    input('stop')
    return score_0, label_0

filepath_0 = file_class + 'new_result_0.txt'
filepath_1 = file_class + 'new_result_1.txt'
filepath_2 = file_class + 'new_result_2.txt'
filepath_3 = file_class + 'new_result_3.txt'
filepath_4 = file_class + 'new_result_4.txt'
filepath_5 = file_class + 'new_result_5.txt'


#使用自己写的函数提取出必要的数据
score_0, label_0 = draw_one(filepath_0)
score_1, label_1 = draw_one(filepath_1)
score_2, label_2 = draw_one(filepath_2)
score_3, label_3 = draw_one(filepath_3,score_col=4, label_col=5)
score_4, label_4 = draw_one(filepath_4,score_col=4, label_col=5)
score_5, label_5 = draw_one(filepath_5,score_col=4, label_col=5)
#调包计算画图必要的数据
fpr_0, tpr_0, threshold_0 = roc_curve(label_0, score_0)
fpr_1, tpr_1, threshold_1 = roc_curve(label_1, score_1)
fpr_2, tpr_2, threshold_2 = roc_curve(label_2, score_2)
fpr_3, tpr_3, threshold_3 = roc_curve(label_3, score_3)
fpr_4, tpr_4, threshold_4 = roc_curve(label_4, score_4)
fpr_5, tpr_5, threshold_5 = roc_curve(label_5, score_5)

#计算auc
roc_auc_0 = auc(fpr_0, tpr_0)
roc_auc_1 = auc(fpr_1, tpr_1)
roc_auc_2 = auc(fpr_2, tpr_2)
roc_auc_3 = auc(fpr_3, tpr_3)
roc_auc_4 = auc(fpr_4, tpr_4)
roc_auc_5 = auc(fpr_5, tpr_5)


print('0:{}, 1:{}, 2:{},3:{},4:{},5:{}'.format(roc_auc_0,roc_auc_1,roc_auc_2,roc_auc_3,roc_auc_4,roc_auc_5))
input('stop')

# 画ROC图
plt.figure()
lw = 2
plt.figure(figsize=(10, 8))

#下面开始绘制4条线
plt.plot(fpr_0, tpr_0, color='red',lw=lw, label='0 = %0.3f' % roc_auc_0)
plt.plot(fpr_1, tpr_1, color='green',lw=lw, label='1 = %0.3f' % roc_auc_1)
plt.plot(fpr_2, tpr_2, color='darkorange',lw=lw, label='2 = %0.3f' % roc_auc_2)
plt.plot(fpr_3, tpr_3, color='purple',lw=lw, label='3 = %0.3f' % roc_auc_3)
plt.plot(fpr_4, tpr_4, color='blue',lw=lw, label='4 = %0.3f' % roc_auc_4)
plt.plot(fpr_5, tpr_5, color='black',lw=lw, label='5 = %0.3f' % roc_auc_5)

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# plt.title('Roc Curve')
plt.legend(loc="lower right")
plt.savefig(filepath_output, dpi=1200, format='pdf')
plt.show()

print('end')
