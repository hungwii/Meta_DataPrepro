#-*- coding: UTF-8 -*-

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from extract import single_column
import os

'''
这个主函数是从我生蚝好的多个文件中提取出样本画AUC
'''

#-------------------------参数设置---------------------------
file_class = '../MetaR/test_result/TransR3000_30shot_test/' #数据所在的文件夹路径
file_num = 6 #这个数量是我test文件的数量，相当于要预测的任务的数量
filepath_output = './test_result_graphs/TransR3000_30shot/'
proportion = 4 #采样比例
#-----------------------------------------------------------
#创建文件夹
folder = os.path.exists(filepath_output)
if not folder:
    os.makedirs(filepath_output)

def normalization(socres_list):
    #min-max标准化
    max_num = max(socres_list)
    min_num = min(socres_list)
    rst = []
    for score in socres_list:
        rst.append((score - min_num)/(max_num-min_num))
    return rst

def draw_one(filepath,output_path,score_col=3, label_col=4):

    result_score = single_column(filepath, col_num=score_col)
    result_label = single_column(filepath,col_num=label_col)

    all_score = list(map(float, result_score))
    all_label = list(map(int, result_label)) 

    #进行归一化
    all_score = normalization(all_score)

    long_ = sum(all_label)
    zipped = zip(all_score, all_label)

    # 先按 x[1] 进行排序，若 x[1] 相同，再按照 x[0] 排序
    combine_zip = sorted(zipped, key=lambda x : (x[1], x[0]),reverse=True)
    combine = zip(*combine_zip)
    all_score_new, all_label_new = [list(x) for x in combine]
    
    score = all_score_new[:proportion*long_]
    label = all_label_new[:proportion*long_]
    
    with open(output_path, 'w', encoding='utf-8') as output:
        for row in range(len(score)):
            rowtext = '{} {}'.format(score[row], label[row])
            output.write(rowtext)
            output.write('\n')
    
    # input('stop')
    return score, label

filepath_0 = file_class + 'new_result_0.txt'
filepath_1 = file_class + 'new_result_1.txt'
filepath_2 = file_class + 'new_result_2.txt'
filepath_3 = file_class + 'new_result_3.txt'
filepath_4 = file_class + 'new_result_4.txt'
filepath_5 = file_class + 'new_result_5.txt'

#使用自己写的函数提取出必要的数据
score_0, label_0 = draw_one(filepath_0, output_path=filepath_output + 'ANTIBODY.txt')
score_1, label_1 = draw_one(filepath_1, output_path=filepath_output + 'BINDER.txt')
score_2, label_2 = draw_one(filepath_2, output_path=filepath_output + 'MODULATOR.txt')
score_3, label_3 = draw_one(filepath_3,score_col=4, label_col=5, output_path=filepath_output + 'PARTIAL_AGONIST.txt')
score_4, label_4 = draw_one(filepath_4,score_col=4, label_col=5, output_path=filepath_output + 'DIRECT_INTERACTION.txt')
score_5, label_5 = draw_one(filepath_5,score_col=4, label_col=5, output_path=filepath_output + 'PHYSICAL_ASSOCIATION.txt')

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

#控制台输出auc分数
print('ANTIBODY:\t{}\nBINDER:\t{}\nMODULATOR:\t{}\nPARTIAL AGONIST:\t{}\nDIRECT INTERACTION:\t{}\nPHYSICAL ASSOCIATION:\t{}'.format(roc_auc_0,roc_auc_1,roc_auc_2,roc_auc_3,roc_auc_4,roc_auc_5))
input('stop')

# 画ROC图
plt.figure()
lw = 2
plt.figure(figsize=(10, 8))

#下面开始绘制多条线
plt.plot(fpr_0, tpr_0, color='red',lw=lw, label='ANTIBODY = %0.3f' % roc_auc_0)
plt.plot(fpr_1, tpr_1, color='green',lw=lw, label='BINDER = %0.3f' % roc_auc_1)
plt.plot(fpr_2, tpr_2, color='darkorange',lw=lw, label='MODULATOR = %0.3f' % roc_auc_2)
plt.plot(fpr_3, tpr_3, color='purple',lw=lw, label='PARTIAL AGONIST = %0.3f' % roc_auc_3)
plt.plot(fpr_4, tpr_4, color='blue',lw=lw, label='DIRECT INTERACTION = %0.3f' % roc_auc_4)
plt.plot(fpr_5, tpr_5, color='black',lw=lw, label='PHYSICAL ASSOCIATION = %0.3f' % roc_auc_5)

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# plt.title('Roc Curve')
plt.legend(loc="lower right")
plt.savefig(filepath_output + 'figure.pdf', dpi=1200, format='pdf')
plt.show()

print('end')